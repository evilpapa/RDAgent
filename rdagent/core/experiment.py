from __future__ import annotations

import io
import os
import platform
import re
import shutil
import typing
import uuid
import zipfile
from abc import ABC, abstractmethod
from collections.abc import Sequence
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from rdagent.core.conf import RD_AGENT_SETTINGS
from rdagent.core.evaluation import Feedback

if TYPE_CHECKING:
    from rdagent.utils.env import EnvResult


if typing.TYPE_CHECKING:
    from rdagent.core.proposal import Hypothesis
    from rdagent.utils.env import Env

"""
该文件包含有关在 RD-Agent 中组织任务的所有类。
"""


class AbsTask(ABC):
    def __init__(self, name: str, version: int = 1) -> None:
        """
        任务的版本，默认为 1
        因为 qlib 任务执行和 kaggle 任务执行不同，我们需要区分它们。
        TODO: 我们将来可能会对齐它们。
        """
        self.version = version
        self.name = name

    @abstractmethod
    def get_task_information(self) -> str:
        """
        获取任务信息字符串以构建唯一密钥
        """


class Task(AbsTask):
    def __init__(self, name: str, version: int = 1, description: str = "") -> None:
        super().__init__(name, version)
        self.description = description

    def get_task_information(self) -> str:
        return f"任务名称: {self.name}\n描述: {self.description}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"


ASpecificTask = TypeVar("ASpecificTask", bound=Task)
ASpecificFeedback = TypeVar("ASpecificFeedback", bound=Feedback)


@dataclass
class RunningInfo:
    result: object = None  # 实验结果，在不同场景中可以是不同类型。
    running_time: float | None = None


class Workspace(ABC, Generic[ASpecificTask, ASpecificFeedback]):
    """
    工作区是存储任务实现的地方。它随着开发人员实现任务而演变。
    要获取工作区的快照，请确保调用 `copy` 来获取工作区的副本。
    """

    def __init__(self, target_task: ASpecificTask | None = None) -> None:
        self.target_task: ASpecificTask | None = target_task
        self.feedback: ASpecificFeedback | None = None
        self.running_info: RunningInfo = RunningInfo()

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> object | None:
        error_message = "execute 方法未实现。"
        raise NotImplementedError(error_message)

    @abstractmethod
    def copy(self) -> Workspace:
        error_message = "copy 方法未实现。"
        raise NotImplementedError(error_message)

    @property
    @abstractmethod
    def all_codes(self) -> str:
        """
        将工作区中的所有代码文件作为单个字符串获取。
        """

    # 当工作区是可变的原地时，提供创建检查点和恢复的支持。
    @abstractmethod
    def create_ws_ckp(self) -> None:
        """
        创建工作区的内存中检查点，以便以后可以恢复。
        """

    @abstractmethod
    def recover_ws_ckp(self) -> None:
        """
        从 :py:meth:`create_ws_ckp` 创建的检查点恢复工作区。
        """


ASpecificWS = TypeVar("ASpecificWS", bound=Workspace)


class WsLoader(ABC, Generic[ASpecificTask, ASpecificWS]):
    @abstractmethod
    def load(self, task: ASpecificTask) -> ASpecificWS:
        error_message = "load 方法未实现。"
        raise NotImplementedError(error_message)


class FBWorkspace(Workspace):
    """
    基于文件的任务工作区

    实现的任务将是一个包含相关元素的文件夹。
    - 数据
    - 代码工作区
    - 输出
        - 执行后，它将生成最终输出作为文件。

    运行 FBWorkspace 管道的典型方法是：
    （我们没有将其添加为方法，因为我们可能会根据我们的要求将参数传递到
    `prepare` 或 `execute` 中。）

    .. code-block:: python

        def run_pipeline(self, **files: str):
            self.prepare()
            self.inject_files(**files)
            self.execute()

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.file_dict: dict[str, Any] = (
            {}
        )  # 注入到文件夹中的代码，将它们存储在变量中以重现以前的结果
        self.workspace_path: Path = RD_AGENT_SETTINGS.workspace_path / uuid.uuid4().hex
        self.ws_ckp: bytes | None = None  # 由 ``create_ws_ckp`` 创建的内存中检查点数据。
        self.change_summary: str | None = None  # 与先前版本工作区的更改

    @staticmethod
    def _format_code_dict(code_dict: dict[str, str]) -> str:
        """
        帮助函数，用于将代码字典格式化为字符串。
        """
        code_string = ""
        for file_name in sorted(code_dict.keys()):
            code_string += f"\n文件路径: {file_name}\n```\n{code_dict[file_name]}\n```"
        return code_string

    @property
    def all_codes(self) -> str:
        """
        将工作区中的所有代码文件作为单个字符串获取，不包括测试文件。
        """
        filtered_dict = {k: v for k, v in self.file_dict.items() if k.endswith(".py") and "test" not in k}
        return self._format_code_dict(filtered_dict)

    def get_codes(self, pattern: str) -> str:
        """
        将与特定模式匹配的代码文件作为单个字符串获取，不包括测试文件。
        """
        filtered_dict = {
            k: v for k, v in self.file_dict.items() if re.search(pattern, k) and k.endswith(".py") and "test" not in k
        }
        return self._format_code_dict(filtered_dict)

    def prepare(self) -> None:
        """
        准备工作区，但不包括注入的代码
        - 数据
        - 文档
            `*args, **kwargs` 的典型用法：
                不同的方法共享相同的数据。数据通过参数传递。
        """
        self.workspace_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def link_all_files_in_folder_to_workspace(data_path: Path, workspace_path: Path) -> None:
        data_path = Path(data_path).absolute()  # 以防在我们更改 cwd 时相对路径将无效。
        workspace_path = Path(workspace_path)
        for data_file_path in data_path.iterdir():
            workspace_data_file_path = workspace_path / data_file_path.name
            if workspace_data_file_path.exists():
                workspace_data_file_path.unlink()
            if platform.system() in ("Linux", "Darwin"):
                workspace_data_file_path.symlink_to(data_file_path)
            if platform.system() == "Windows":
                os.link(data_file_path, workspace_data_file_path)

    DEL_KEY = "__DEL__"

    def inject_files(self, **files: str) -> None:
        """
        将代码注入文件夹。
        {
            <文件名1>: <code>,  // 表示将 <code> 写入 <文件名>
                          （创建新文件或替换现有文件）
            <文件名2>: "__DEL__"  // 表示删除文件名2。当我们想将文件替换为新文件时，
                          我们通常使用它
        }
        """
        self.prepare()
        for k, v in files.items():
            target_file_path = self.workspace_path / k  # 在使用它之前定义 target_file_path
            if v == self.DEL_KEY:  # 使用 self.DEL_KEY 访问类变量
                if target_file_path.exists():
                    target_file_path.unlink()  # 如果文件存在，则取消链接
                self.file_dict.pop(k, None)  # 安全地从 file_dict 中删除键
            else:
                self.file_dict[k] = v
                target_file_path.parent.mkdir(parents=True, exist_ok=True)
                target_file_path.write_text(v)

    def get_files(self) -> list[Path]:
        """
        获取环境描述。

        为了一般性，我们只返回一个文件名列表。
        如何总结环境是开发人员的责任。
        """
        return list(self.workspace_path.iterdir())

    def inject_code_from_folder(self, folder_path: Path) -> None:
        """
        从文件夹加载工作区
        """
        for file_path in folder_path.rglob("*"):
            if file_path.suffix in (".py", ".yaml", ".md"):
                relative_path = file_path.relative_to(folder_path)
                self.inject_files(**{str(relative_path): file_path.read_text()})

    def inject_code_from_file_dict(self, workspace: FBWorkspace) -> None:
        """
        从 file_dict 加载工作区
        """
        for name, code in workspace.file_dict.items():
            self.inject_files(**{name: code})

    def copy(self) -> FBWorkspace:
        """
        从原始工作区复制工作区
        """
        return deepcopy(self)

    def clear(self) -> None:
        """
        清除工作区
        """
        shutil.rmtree(self.workspace_path, ignore_errors=True)
        self.file_dict = {}

    def before_execute(self) -> None:
        """
        在执行代码之前，我们需要准备工作区并将代码注入工作区。
        """
        self.prepare()
        self.inject_files(**self.file_dict)

    def execute(self, env: Env, entry: str) -> str:
        """
        在每次执行之前，请确保准备和注入代码。
        """
        result = self.run(env, entry)
        return result.get_truncated_stdout()  # 注意：截断只是为了与旧代码对齐。

    def run(self, env: Env, entry: str) -> EnvResult:
        """
        在环境中执行代码并返回一个 EnvResult 对象（stdout、exit_code、running_time）。

        在每次执行之前，请确保准备和注入代码。
        """
        self.prepare()
        self.inject_files(**self.file_dict)
        return env.run(entry, str(self.workspace_path), env={"PYTHONPATH": "./"})

    def create_ws_ckp(self) -> None:
        """
        将 ``workspace_path`` 的内容压缩并将其存档保留在
        ``self.ws_ckp`` 上，以便以后通过 :py:meth:`recover_ws_ckp` 进行恢复。
        """
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in self.workspace_path.rglob("*"):
                # 仅包括高达 100 KB 的常规文件，以便检查点
                # 保持轻量级。较大的文件（例如数据集）
                # 预计将单独重新创建或挂载。
                if file_path.is_symlink():
                    # 在存档中保留符号链接
                    zi = zipfile.ZipInfo(str(file_path.relative_to(self.workspace_path)))
                    zi.create_system = 3  # 表示 Unix
                    zi.external_attr = 0o120777 << 16  # 符号链接文件类型 + 0777 权限
                    zf.writestr(zi, str(file_path.readlink()))
                elif file_path.is_file():
                    size_limit = RD_AGENT_SETTINGS.workspace_ckp_size_limit
                    if (
                        RD_AGENT_SETTINGS.workspace_ckp_white_list_names is not None
                        and file_path.name in RD_AGENT_SETTINGS.workspace_ckp_white_list_names
                    ) or (size_limit <= 0 or file_path.stat().st_size <= size_limit):
                        zf.write(file_path, file_path.relative_to(self.workspace_path))
        self.ws_ckp = buf.getvalue()

    def recover_ws_ckp(self) -> None:
        """
        从由 :py:meth:`create_ws_ckp` 创建的内存中检查点恢复工作区目录。
        """
        if self.ws_ckp is None:
            msg = "工作区检查点不存在。请先调用 `create_ws_ckp`。"
            raise RuntimeError(msg)
        shutil.rmtree(self.workspace_path, ignore_errors=True)
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        buf = io.BytesIO(self.ws_ckp)
        with zipfile.ZipFile(buf, "r") as zf:
            for info in zf.infolist():
                dest_path = self.workspace_path / info.filename
                # 文件类型位（高 4 位）位于 external_attr 的高 16 位中
                mode = (info.external_attr >> 16) & 0o170000
                symlink_mode = 0o120000  # Unix 中符号链接文件类型的常量
                if mode == symlink_mode:  # 符号链接
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    link_target = zf.read(info).decode()
                    dest_path.symlink_to(link_target)
                elif info.is_dir():
                    dest_path.mkdir(parents=True, exist_ok=True)
                else:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    with dest_path.open("wb") as f:
                        f.write(zf.read(info))
        # 注意：非常重要，以减小对象的大小
        self.ws_ckp = None

    def __str__(self) -> str:
        return f"Workspace[{self.workspace_path=}" + (
            "]" if self.target_task is None else f",{self.target_task.name=}]"
        )


ASpecificWSForExperiment = TypeVar("ASpecificWSForExperiment", bound=Workspace)
ASpecificWSForSubTasks = TypeVar("ASpecificWSForSubTasks", bound=Workspace)


class ExperimentPlan(dict[str, Any]):
    """
    实验计划，这是一个包含每个阶段计划的字典。
    """


class Experiment(
    ABC,
    Generic[ASpecificTask, ASpecificWSForExperiment, ASpecificWSForSubTasks],
):
    """
    实验是开发人员生成任务后的一系列任务和任务的实现。
    """

    def __init__(
        self,
        sub_tasks: Sequence[ASpecificTask],
        based_experiments: Sequence[ASpecificWSForExperiment] = [],
        hypothesis: Hypothesis | None = None,
    ) -> None:
        self.hypothesis: Hypothesis | None = hypothesis  # 实验可选择由假设生成
        self.sub_tasks: Sequence[ASpecificTask] = sub_tasks
        # None 表示
        # - 实现前的初始化占位符
        # - 开发人员主动跳过任务；
        self.sub_workspace_list: list[ASpecificWSForSubTasks | None] = [None] * len(self.sub_tasks)
        # TODO:
        # 它将在历史记录中的运行器中使用
        # 如果我们实现了整个工作流程，我们就不必使用它，然后我们将其删除。
        self.based_experiments: Sequence[ASpecificWSForExperiment] = based_experiments

        self.experiment_workspace: ASpecificWSForExperiment | None = None

        # 实验可能由不同的开发人员开发。
        # 上一个反馈用于将信息传播给下一个开发人员。
        # 生命周期：
        # - 开发人员为下一个组件分配反馈；
        # - 工作流控制清除反馈。
        self.prop_dev_feedback: Feedback | None = None

        # TODO: (xiao) 我认为这太具体了；我们应该把它移到
        # 注意：假设
        # - 只有运行器会分配此变量
        # - 当我们进入下一个新循环时，我们将始终创建一个新的实验，而无需复制以前的结果。
        self.running_info = RunningInfo()
        self.sub_results: dict[str, float] = (
            {}
        )  # TODO: 在 Kaggle 中，现在子结果都保存在 self.result 中，将来会删除它。

        # 用于并行多跟踪支持
        self.local_selection: tuple[int, ...] | None = None
        self.plan: ExperimentPlan | None = (
            None  # 用于存储此实验的规划信息，应在 exp_gen.gen 内部生成
        )

    @property
    def result(self) -> object:
        return self.running_info.result

    @result.setter
    def result(self, value: object) -> None:
        self.running_info.result = value

    # 当工作区是可变的原地时，提供创建检查点和恢复的支持。
    def create_ws_ckp(self) -> None:
        if self.experiment_workspace is not None:
            self.experiment_workspace.create_ws_ckp()
        for ws in self.sub_workspace_list:
            if ws is not None:
                ws.create_ws_ckp()

    def recover_ws_ckp(self) -> None:
        if self.experiment_workspace is not None:
            self.experiment_workspace.recover_ws_ckp()
        for ws in self.sub_workspace_list:
            if ws is not None:
                try:
                    ws.recover_ws_ckp()
                except RuntimeError:
                    # FBWorkspace 在 experiment_workspace 和 sub_workspace_list 之间共享，
                    # 因此如果一个工作区被恢复两次，recover_ws_ckp 将引发 RuntimeError。
                    print("由于一个工作区被恢复两次，recover_ws_ckp 失败。")


ASpecificExp = TypeVar("ASpecificExp", bound=Experiment)
ASpecificPlan = TypeVar("ASpecificPlan", bound=ExperimentPlan)

TaskOrExperiment = TypeVar("TaskOrExperiment", Task, Experiment)


class Loader(ABC, Generic[TaskOrExperiment]):
    @abstractmethod
    def load(self, *args: Any, **kwargs: Any) -> TaskOrExperiment:
        err_msg = "load 方法未实现。"
        raise NotImplementedError(err_msg)
