from __future__ import annotations # 确保类型提示中的向前引用有效

import os # 用于操作系统相关功能，如符号链接
import platform # 用于获取操作系统信息
import re # 用于正则表达式操作
import shutil # 用于高级文件操作，如删除目录树
import typing # 主要用于 TYPE_CHECKING
import uuid # 用于生成唯一ID
from abc import ABC, abstractmethod # 导入抽象基类和抽象方法
from collections.abc import Sequence # 用于类型提示序列
from copy import deepcopy # 用于深拷贝对象
from dataclasses import dataclass # 用于创建数据类
from pathlib import Path # 用于面向对象的文件系统路径操作
from typing import TYPE_CHECKING, Any, Generic, TypeVar # 类型提示工具

from rdagent.core.conf import RD_AGENT_SETTINGS # 导入框架配置
from rdagent.core.evaluation import Feedback # 从评估模块导入 Feedback 基类
from rdagent.utils import filter_redundant_text # 从工具模块导入文本过滤函数

if TYPE_CHECKING: # 仅在类型检查时执行，避免循环导入
    from rdagent.utils.env import EnvResult # 从环境模块导入 EnvResult

from rdagent.utils.fmt import shrink_text # 从格式化工具导入文本缩减函数

if typing.TYPE_CHECKING: # 再次使用 TYPE_CHECKING 块，通常合并更佳
    from rdagent.core.proposal import Hypothesis # 从提议模块导入 Hypothesis 类
    from rdagent.utils.env import Env # 从环境模块导入 Env 类

"""
此文件包含 RD-Agent 中用于组织任务的所有相关类。
This file contains all the classes about organizing tasks in RD-Agent.
"""


class AbsTask(ABC):
    """
    任务 (Task) 的抽象基类。
    Abstract base class for a Task.
    """
    def __init__(self, name: str, version: int = 1) -> None:
        """
        初始化任务。
        Initializes the task.

        :param name: 任务的名称。
        :param version: 任务的版本，默认为 1。
                        因为 qlib 任务执行和 kaggle 任务执行不同，我们需要区分它们。
                        TODO: 未来可能会统一它们。
                        The version of the task, default is 1.
                        Because qlib tasks execution and kaggle tasks execution are different, we need to distinguish them.
                        TODO: We may align them in the future.
        """
        self.version = version
        self.name = name

    @abstractmethod
    def get_task_information(self) -> str:
        """
        获取任务信息的字符串表示，用于构建唯一键。
        Get the task information string to build a unique key.
        子类必须实现此方法。
        Subclasses must implement this method.

        :return: 任务信息的字符串。
                 A string of task information.
        """
        raise NotImplementedError


class Task(AbsTask):
    """
    具体的任务 (Task) 类。
    Concrete Task class.
    继承自 AbsTask，并添加了描述属性。
    Inherits from AbsTask and adds a description attribute.
    """
    def __init__(self, name: str, version: int = 1, description: str = "") -> None:
        """
        初始化具体任务。
        Initializes a concrete task.

        :param name: 任务名称。
        :param version: 任务版本。
        :param description: 任务的详细描述。
        """
        super().__init__(name, version)
        self.description = description

    def get_task_information(self) -> str:
        """返回任务名称和描述的组合字符串。"""
        return f"Task Name: {self.name}\nDescription: {self.description}"

    def __repr__(self) -> str:
        """返回任务对象的易读字符串表示，主要用于调试。"""
        return f"<{self.__class__.__name__} {self.name}>"


# 类型变量，表示 Task 的任何子类
ASpecificTask = TypeVar("ASpecificTask", bound=Task)
# 类型变量，表示 Feedback 的任何子类
ASpecificFeedback = TypeVar("ASpecificFeedback", bound=Feedback)


@dataclass
class RunningInfo:
    """
    数据类，用于存储实验或任务的运行信息。
    Data class for storing running information of an experiment or task.
    """
    result: object = None  # 实验的结果，可以是不同场景下的不同类型。
                           # The result of the experiment, can be different types in different scenarios.
    running_time: float | None = None # 运行时间（秒）。
                                      # Running time (seconds).


class Workspace(ABC, Generic[ASpecificTask, ASpecificFeedback]):
    """
    工作空间 (Workspace) 的抽象基类。
    Abstract base class for a Workspace.

    工作空间是存储任务实现的地方。它会随着开发者实现任务而演进。
    A workspace is a place to store the task implementation. It evolves as the developer implements the task.
    要获取工作空间的快照，请确保调用 `copy` 方法以获取副本。
    To get a snapshot of the workspace, make sure to call `copy` to get a copy of the workspace.

    泛型参数:
    - ASpecificTask: 此工作空间关联的任务类型。
    - ASpecificFeedback: 与此工作空间关联的反馈类型。
    """

    def __init__(self, target_task: ASpecificTask | None = None) -> None:
        """
        初始化工作空间。
        Initializes the workspace.

        :param target_task: (可选) 此工作空间的目标任务。
        """
        self.target_task: ASpecificTask | None = target_task # 关联的目标任务
        self.feedback: ASpecificFeedback | None = None # 对此工作空间的反馈
        self.running_info: RunningInfo = RunningInfo() # 运行信息

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> object | None:
        """
        执行工作空间中的任务或代码。
        Executes the task or code in the workspace.
        子类必须实现此方法。
        Subclasses must implement this method.
        """
        error_message = "execute method is not implemented."
        raise NotImplementedError(error_message)

    @abstractmethod
    def copy(self) -> Workspace: # type: ignore[type-var] # mypy 对于返回自身类型的处理问题
        """
        创建当前工作空间的副本。
        Creates a copy of the current workspace.
        通常应实现为深拷贝。
        Typically should be implemented as a deep copy.
        子类必须实现此方法。
        Subclasses must implement this method.
        """
        error_message = "copy method is not implemented."
        raise NotImplementedError(error_message)

    @property
    @abstractmethod
    def all_codes(self) -> str:
        """
        获取工作空间中所有代码文件的字符串表示。
        Get all the code files in the workspace as a single string.
        子类必须实现此属性。
        Subclasses must implement this property.
        """
        raise NotImplementedError


# 类型变量，表示 Workspace 的任何子类
ASpecificWS = TypeVar("ASpecificWS", bound=Workspace)


class WsLoader(ABC, Generic[ASpecificTask, ASpecificWS]):
    """
    工作空间加载器 (Workspace Loader) 的抽象基类。
    Abstract base class for a Workspace Loader.
    负责根据任务加载或创建相应的工作空间。
    Responsible for loading or creating a workspace based on a task.
    """
    @abstractmethod
    def load(self, task: ASpecificTask) -> ASpecificWS:
        """
        根据给定的任务加载或创建工作空间。
        Loads or creates a workspace based on the given task.
        子类必须实现此方法。
        Subclasses must implement this method.
        """
        error_message = "load method is not implemented."
        raise NotImplementedError(error_message)


class FBWorkspace(Workspace[ASpecificTask, ASpecificFeedback]): # 明确泛型参数
    """
    基于文件系统的工作空间 (File-based Workspace)。
    File-based task workspace.

    已实现的任务将表现为一个包含相关元素的文件夹，例如：
    The implemented task will be a folder which contains related elements, such as:
    - 数据 (Data)
    - 代码工作区 (Code Workspace)
    - 输出 (Output)
        - 执行后，它将生成最终输出作为文件。
          After execution, it will generate the final output as a file.

    运行 FBWorkspace 流水线的典型方式如下：
    A typical way to run the pipeline of FBWorkspace will be:
    (我们没有将其添加为方法，因为我们可能需要根据需求向 `prepare` 或 `execute` 传递参数。)
    (We didn't add it as a method due to the fact that we may pass arguments into
    `prepare` or `execute` based on our requirements.)

    .. code-block:: python

        def run_pipeline(self, **files: str):
            self.prepare() # 准备工作区
            self.inject_files(**files) # 注入文件
            self.execute() # 执行
    """

    DEL_KEY = "__DEL__" # 特殊键，用于指示 inject_files 删除文件
                        # Special key used in inject_files to indicate file deletion.

    def __init__(self, target_task: ASpecificTask | None = None, **kwargs: Any) -> None: # 添加 target_task 以匹配父类
        super().__init__(target_task=target_task, **kwargs) # 正确调用父类构造器
        self.file_dict: dict[str, str] = ( # 文件字典，键为相对路径，值为文件内容（字符串）
                                            # File dictionary, keys are relative paths, values are file contents (string).
            {}
        )  # 注入到文件夹中的代码，将其存储在变量中以便重现先前结果
           # The code injected into the folder, store them in the variable to reproduce the former result
        self.workspace_path: Path = RD_AGENT_SETTINGS.workspace_path / uuid.uuid4().hex # 生成唯一的工作区路径
                                                                                        # Generate a unique workspace path

    @staticmethod
    def _format_code_dict(code_dict: dict[str, str]) -> str:
        """
        辅助函数，用于将代码字典格式化为字符串。
        Helper function to format the code dictionary into a string.
        """
        code_string = ""
        for file_name in sorted(code_dict.keys()): # 按文件名排序以保证一致性
            code_string += f"\nFile Path: {file_name}\n```\n{code_dict[file_name]}\n```"
        return code_string

    @property
    def all_codes(self) -> str:
        """
        获取工作空间中所有 Python 代码文件（不包括测试文件）的内容，并将其格式化为单个字符串。
        Get all the Python code files in the workspace as a single string, excluding test files.
        """
        # 过滤出 .py 文件，并且文件名中不含 "test"
        filtered_dict = {
            k: v for k, v in self.file_dict.items() if isinstance(v, str) and k.endswith(".py") and "test" not in k
        }
        return self._format_code_dict(filtered_dict)

    def get_codes(self, pattern: str) -> str:
        """
        获取匹配特定正则表达式 `pattern` 的 Python 代码文件（不包括测试文件）的内容。
        Get code files matching a specific pattern as a single string, excluding test files.
        """
        filtered_dict = {
            k: v for k, v in self.file_dict.items()
            if isinstance(v, str) and re.search(pattern, k) and k.endswith(".py") and "test" not in k
        }
        return self._format_code_dict(filtered_dict)

    def prepare(self) -> None:
        """
        准备工作空间（主要是创建工作区目录），但不包括注入代码。
        Prepare the workspace except for the injected code.
        这可能还包括准备：
        - 数据 (Data)
        - 文档 (Documentation)
            `*args, **kwargs` 的典型用法：
                不同方法共享相同数据，数据通过参数传递。
                Typical usage of `*args, **kwargs`:
                Different methods share the same data. The data are passed by the arguments.
        """
        self.workspace_path.mkdir(parents=True, exist_ok=True) # 创建目录，如果父目录不存在也一并创建

    @staticmethod
    def link_all_files_in_folder_to_workspace(data_path: Path, workspace_path: Path) -> None:
        """
        将指定数据文件夹 `data_path` 中的所有文件链接到工作空间路径 `workspace_path` 下。
        Links all files in the specified data folder `data_path` to the workspace path `workspace_path`.
        在 Linux 上使用符号链接，在 Windows 上使用硬链接。
        Uses symbolic links on Linux and hard links on Windows.
        """
        data_path = Path(data_path).absolute()  # 处理相对路径，以防当前工作目录更改导致路径失效
                                                # Handle relative paths in case the current working directory changes.
        workspace_path = Path(workspace_path)
        for data_file_path in data_path.iterdir(): # 遍历数据文件夹中的每个项目
            workspace_data_file_path = workspace_path / data_file_path.name # 构造在工作区中的对应路径
            if workspace_data_file_path.exists(): # 如果目标路径已存在，则先删除
                workspace_data_file_path.unlink()
            # 根据操作系统类型选择链接方式
            if platform.system() == "Linux":
                os.symlink(data_file_path, workspace_data_file_path) # 创建符号链接
            elif platform.system() == "Windows": # 注意: Windows 的 os.link 创建的是硬链接
                os.link(data_file_path, workspace_data_file_path)    # 创建硬链接
            # 对于其他操作系统，此代码没有处理，可能需要添加 shutil.copy
            # For other OS, this code doesn't handle it, might need to add shutil.copy

    def inject_files(self, **files: str) -> None:
        """
        将文件内容注入到工作空间文件夹中。
        Injects file content into the workspace folder.

        `files` 参数是一个字典，其中：
        - 键 (key) 是文件名（相对路径）。
        - 值 (value) 是要写入的文件内容（字符串）。
          如果值为 `FBWorkspace.DEL_KEY` (即 "__DEL__")，则表示删除对应的文件。
        The `files` parameter is a dictionary where:
        - key is the filename (relative path).
        - value is the file content to write (string).
          If the value is `FBWorkspace.DEL_KEY` (i.e., "__DEL__"), it indicates removal of the corresponding file.

        示例 (Example):
        {
            "script.py": "print('Hello')",  // 表示将 "print('Hello')" 写入到 script.py
                                          // (创建新文件或替换现有文件)
                                          // Indicates writing "print('Hello')" into script.py
                                          // (create new file or replace existing file)
            "old_config.txt": "__DEL__"   // 表示删除 old_config.txt 文件。
                                          // 当我们想用新文件替换旧文件时，通常使用此方法。
                                          // Indicates removing file old_config.txt.
                                          // When we want to replace a file with a new one, we usually use this.
        }
        """
        self.prepare() # 确保工作区目录已创建
        for k, v in files.items():
            target_file_path = self.workspace_path / k  # 构造目标文件的完整路径
            if v == self.DEL_KEY:  # 检查是否为删除标记
                if target_file_path.exists():
                    target_file_path.unlink()  # 如果文件存在，则删除
                self.file_dict.pop(k, None)  # 从内部文件字典中安全移除该键
            else:
                self.file_dict[k] = v # 更新内部文件字典
                target_file_path.parent.mkdir(parents=True, exist_ok=True) # 确保目标文件的父目录存在
                target_file_path.write_text(v) # 将内容写入文件

    def get_files(self) -> list[Path]:
        """
        获取工作空间目录中所有文件和目录的路径列表。
        Get the list of paths for all files and directories in the workspace.

        为了通用性，我们只返回文件名列表。
        To be general, we only return a list of filenames (actually Path objects).
        如何总结环境是开发者（Developer）的责任。
        How to summarize the environment is the responsibility of the Developer.
        """
        if self.workspace_path.exists():
            return list(self.workspace_path.iterdir())
        return []

    def inject_code_from_folder(self, folder_path: Path) -> None:
        """
        从指定的外部文件夹加载代码（.py, .yaml, .md 文件）到当前工作空间。
        Loads code (.py, .yaml, .md files) from the specified external folder into the current workspace.
        """
        for file_path in folder_path.rglob("*"): #递归遍历文件夹中的所有文件和子文件夹
            if file_path.is_file() and file_path.suffix in (".py", ".yaml", ".md"): # 只处理特定后缀的文件
                relative_path = str(file_path.relative_to(folder_path)) # 获取相对于源文件夹的路径
                self.inject_files(**{relative_path: file_path.read_text()}) # 注入文件

    def inject_code_from_file_dict(self, workspace: FBWorkspace) -> None:
        """
        从另一个 `FBWorkspace` 实例的 `file_dict` 加载代码到当前工作空间。
        Loads code from the `file_dict` of another `FBWorkspace` instance into the current workspace.
        """
        self.inject_files(**workspace.file_dict) # 直接使用另一个工作空间的文件字典注入

    def copy(self) -> FBWorkspace:
        """
        创建当前 `FBWorkspace` 实例的深拷贝。
        Creates a deep copy of the current `FBWorkspace` instance.
        这对于保存工作空间快照或进行分支探索非常重要。
        This is important for saving workspace snapshots or exploring branches.
        """
        # 注意：deepcopy 可能不会正确处理 Path 对象或需要自定义复制逻辑。
        # 对于 FBWorkspace，主要状态是 self.file_dict 和 self.target_task (如果相关)。
        # workspace_path 应该是新的。
        # A simple deepcopy might be too naive if Path objects or other complex states are involved.
        # For FBWorkspace, the main state is self.file_dict and self.target_task.
        # The workspace_path should ideally be new for a true copy to avoid side effects.
        # The current deepcopy(self) will create a new FBWorkspace with a *new* unique workspace_path
        # due to how __init__ works if not careful.
        # A more controlled copy would be:
        new_ws = FBWorkspace(target_task=deepcopy(self.target_task) if self.target_task else None)
        new_ws.file_dict = deepcopy(self.file_dict)
        # new_ws.feedback and new_ws.running_info will be new instances.
        # If self.workspace_path needs to be copied (e.g. for re-execution), that's different.
        # But typically a copy means a new, independent workspace based on the state.
        # The original code `return deepcopy(self)` is kept for now.
        return deepcopy(self)

    def clear(self) -> None:
        """
        清空工作空间：删除磁盘上的工作区文件夹，并清空内部的 `file_dict`。
        Clears the workspace: removes the workspace folder from disk and clears the internal `file_dict`.
        """
        if self.workspace_path.exists():
            shutil.rmtree(self.workspace_path, ignore_errors=True) # 忽略错误以确保即使部分失败也能继续
        self.file_dict = {}

    def before_execute(self) -> None:
        """
        在执行代码之前，需要准备工作空间并将代码注入到工作空间。
        Before executing the code, we need to prepare the workspace and inject code into the workspace.
        """
        self.prepare()
        self.inject_files(**self.file_dict) # 使用当前 file_dict 的内容确保工作区文件最新

    def execute(self, env: Env, entry: str) -> str:
        """
        在指定环境中执行工作空间中的入口点，并返回标准输出。
        Executes the entry point in the workspace within the specified environment and returns stdout.
        在每次执行前，确保准备和注入代码。
        Before each execution, make sure to prepare and inject code.
        """
        # self.before_execute() # run 方法内部会调用 prepare 和 inject_files
        result: EnvResult = self.run(env, entry)
        return result.stdout

    def run(self, env: Env, entry: str) -> EnvResult:
        """
        在指定环境中执行代码，并返回一个 `EnvResult` 对象（包含标准输出、退出码、运行时间）。
        Executes the code in the environment and returns an `EnvResult` object (stdout, exit_code, running_time).

        在每次执行前，确保准备和注入代码。
        Before each execution, make sure to prepare and inject code.
        """
        self.before_execute() # 确保工作区是最新的
        # 在指定的工作区路径下运行入口命令，并设置 PYTHONPATH 环境变量为当前目录 ("./")
        # This allows relative imports within the workspace to function correctly.
        result: EnvResult = env.run(entry, str(self.workspace_path), env={"PYTHONPATH": "./"})

        # 对标准输出进行过滤和缩减，以便于阅读和存储
        # Filter and shrink the stdout for better readability and storage.
        result.stdout = shrink_text(
            filter_redundant_text(result.stdout), # 首先过滤掉冗余文本
            context_lines=RD_AGENT_SETTINGS.stdout_context_len, # 保留的上下文行数
            line_len=RD_AGENT_SETTINGS.stdout_line_len, # 每行的最大长度
        )
        self.running_info.running_time = result.running_time # 保存运行时间
        # 结果也可能需要保存到 self.running_info.result，取决于 env.run 的具体约定
        # The result itself might also need to be saved to self.running_info.result,
        # depending on the contract of env.run.
        return result

    def __str__(self) -> str:
        """返回工作空间的字符串表示，包含路径和关联的任务名（如果存在）。"""
        task_name_str = f",{self.target_task.name=}" if self.target_task else ""
        return f"Workspace[{self.workspace_path=}{task_name_str}]"


# 类型变量，分别表示实验级别和子任务级别特定的工作空间类型
ASpecificWSForExperiment = TypeVar("ASpecificWSForExperiment", bound=Workspace)
ASpecificWSForSubTasks = TypeVar("ASpecificWSForSubTasks", bound=Workspace)


class Experiment(
    ABC,
    Generic[ASpecificTask, ASpecificWSForExperiment, ASpecificWSForSubTasks],
):
    """
    实验 (Experiment) 的抽象基类。
    Abstract base class for an Experiment.

    实验是一系列任务以及由开发者生成（实现）的这些任务的组合。
    The experiment is a sequence of tasks and the implementations of these tasks after being generated by the Developer.
    它代表了一次完整的研发尝试。
    It represents a complete R&D attempt.

    泛型参数:
    - ASpecificTask: 实验中子任务的具体类型。
    - ASpecificWSForExperiment: 整个实验级别工作空间的具体类型。
    - ASpecificWSForSubTasks: 子任务级别工作空间的具体类型。
    """

    def __init__(
        self,
        sub_tasks: Sequence[ASpecificTask], # 构成此实验的子任务序列
        based_experiments: Sequence[ASpecificWSForExperiment] = [], # (可选) 当前实验所基于的先前实验的工作空间
        hypothesis: Hypothesis | None = None, # (可选) 生成此实验的原始假设
    ) -> None:
        self.hypothesis: Hypothesis | None = hypothesis  # 实验可以选择性地由一个假设生成
                                                        # Experiment is optionally generated by a hypothesis
        self.sub_tasks: Sequence[ASpecificTask] = sub_tasks # 子任务列表

        # `sub_workspace_list` 存储每个子任务对应的工作空间。
        # 初始化为与 `sub_tasks` 等长的 `None` 列表。
        # `None` 意味着：
        # - 实现前的初始化占位符。
        # - 开发者主动跳过了该任务。
        # `sub_workspace_list` stores the workspace corresponding to each sub_task.
        # Initialized as a list of `None` with the same length as `sub_tasks`.
        # `None` means:
        # - Initialization placeholder before implementation.
        # - The developer actively skipped the task.
        self.sub_workspace_list: list[ASpecificWSForSubTasks | None] = [None] * len(self.sub_tasks)

        # TODO: 这个属性将在历史记录中的运行器（runner）中使用。
        #       如果我们实现了完整的工作流，可能不再需要它，届时可以移除。
        # This attribute will be used in the runner in history.
        # If we implement the whole workflow, we don't have to use it, then we can remove it.
        self.based_experiments: Sequence[ASpecificWSForExperiment] = based_experiments

        self.experiment_workspace: ASpecificWSForExperiment | None = None # 整个实验级别的工作空间

        # 实验可能由不同的开发者（或开发阶段）处理。
        # `prop_dev_feedback` 用于将信息从一个开发者传递给下一个开发者或组件。
        # 生命周期 (Life cycle):
        # - 开发者为下一个组件分配反馈 (Developer assigns feedback for the next component)。
        # - 工作流控制器清除反馈 (Workflow control clears feedback)。
        # The experiment may be developed by different developers.
        # `prop_dev_feedback` is used to propagate info to the next developer.
        self.prop_dev_feedback: Feedback | None = None

        # TODO: (xiao) 我认为这个太具体了；我们应该将其移入更合适的地方。
        # NOTE: 假设 (Assumption)
        # - 只有运行器会分配这个变量。
        # - 当我们进入下一个新的循环时，总会创建一个新的 Experiment，而不会复制先前结果。
        # (xiao) I think this is too concrete; we should move it into a more appropriate place.
        # - Only the runner will assign this variable.
        # - We will always create a new Experiment without copying previous results when we go to the next new loop.
        self.running_info = RunningInfo() # 存储整个实验的运行信息

        # TODO: 在 Kaggle 场景中，目前所有子结果都保存在 self.result 中，未来移除此属性。
        # In Kaggle scenarios, currently all sub-results are saved in self.result, remove this in the future.
        self.sub_results: dict[str, float] = {} # 用于存储子任务的量化结果 (例如，按名称映射到浮点数值)
                                                 # Used to store quantitative results of sub-tasks.

        # 用于并行多轨迹支持，记录此实验在特定轨迹分支上的选择信息。
        # For parallel multi-trace support, records the selection information of this experiment on a specific trace branch.
        self.local_selection: tuple[int, ...] | None = None

    @property
    def result(self) -> object:
        """获取实验的整体结果。"""
        return self.running_info.result

    @result.setter
    def result(self, value: object) -> None:
        """设置实验的整体结果。"""
        self.running_info.result = value


# 类型变量，表示 Experiment 的任何子类
ASpecificExp = TypeVar("ASpecificExp", bound=Experiment)

# 类型变量，表示可以是 Task 或 Experiment
TaskOrExperiment = TypeVar("TaskOrExperiment", Task, Experiment)


class Loader(ABC, Generic[TaskOrExperiment]):
    """
    通用加载器 (Loader) 的抽象基类。
    Abstract base class for a generic Loader.
    可以用于加载任务 (Task) 或实验 (Experiment) 对象。
    Can be used to load Task or Experiment objects.
    """
    @abstractmethod
    def load(self, *args: Any, **kwargs: Any) -> TaskOrExperiment:
        """
        加载任务或实验。
        Loads a task or experiment.
        子类必须实现此方法。
        Subclasses must implement this method.
        """
        err_msg = "load method is not implemented."
        raise NotImplementedError(err_msg)
