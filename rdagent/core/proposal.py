# TODO: 如果将跟踪传递到实例中，则删除 `self.scen`。

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from rdagent.core.conf import RD_AGENT_SETTINGS
from rdagent.core.evaluation import Feedback
from rdagent.core.experiment import (
    ASpecificExp,
    ASpecificPlan,
    Experiment,
    ExperimentPlan,
)
from rdagent.core.knowledge_base import KnowledgeBase
from rdagent.core.scenario import Scenario

if TYPE_CHECKING:
    from rdagent.utils.workflow.loop import LoopBase


class Hypothesis:
    """
    TODO: 我们可能会有更好的名字。

    候选名称：
    - 信念
    """

    def __init__(
        self,
        hypothesis: str,
        reason: str,
        concise_reason: str,
        concise_observation: str,
        concise_justification: str,
        concise_knowledge: str,
    ) -> None:
        self.hypothesis: str = hypothesis
        self.reason: str = reason
        self.concise_reason: str = concise_reason
        self.concise_observation: str = concise_observation
        self.concise_justification: str = concise_justification
        self.concise_knowledge: str = concise_knowledge

    def __str__(self) -> str:
        return f"""假设: {self.hypothesis}
原因: {self.reason}"""

    # 来源：data_ana | model_nan = None


# 来源(仓库/数据/反馈的路径) => 视图/摘要 => 生成的假设


class ExperimentFeedback(Feedback):
    def __init__(
        self,
        reason: str,
        *,
        code_change_summary: str | None = None,
        decision: bool,
        eda_improvement: str | None = None,
        exception: Exception | None = None,
    ) -> None:
        self.decision = decision
        self.eda_improvement = eda_improvement
        self.reason = reason
        # 异常不为 None 意味着由于异常而无法生成可运行的实验。
        # 可运行的结果并不总是好的。
        self.exception: Exception | None = (
            exception  # 如果实验引发异常，它将被集成到反馈的一部分。
        )
        self.code_change_summary = code_change_summary

    def __bool__(self) -> bool:
        return self.decision

    def __str__(self) -> str:
        res = f"决定: {self.decision}\n原因: {self.reason}"
        code_change_summary = getattr(self, "code_change_summary", None)
        if code_change_summary is not None:
            res += "\n代码更改摘要: " + code_change_summary
        return res

    @classmethod
    def from_exception(cls, e: Exception) -> ExperimentFeedback:
        """
        一个从异常创建反馈的便捷方法。
        """
        return cls(decision=False, reason=f"实验由于 {e!s} 而失败", exception=e)


class HypothesisFeedback(ExperimentFeedback):
    def __init__(
        self,
        observations: str,
        hypothesis_evaluation: str,
        new_hypothesis: str,
        reason: str,
        *,
        code_change_summary: str | None = None,
        decision: bool,
        eda_improvement: str | None = None,
        acceptable: bool | None = None,
    ) -> None:
        super().__init__(
            reason,
            decision=decision,
            code_change_summary=code_change_summary,
            eda_improvement=eda_improvement,
        )
        self.observations = observations
        self.hypothesis_evaluation = hypothesis_evaluation
        self.new_hypothesis = new_hypothesis
        self.acceptable = acceptable

    def __str__(self) -> str:
        return f"""{super().__str__()}
观察: {self.observations}
假设评估: {self.hypothesis_evaluation}
新假设: {self.new_hypothesis}"""


ASpecificScen = TypeVar("ASpecificScen", bound=Scenario)
ASpecificKB = TypeVar("ASpecificKB", bound=KnowledgeBase)


class Trace(Generic[ASpecificScen, ASpecificKB]):
    NodeType = tuple[Experiment, ExperimentFeedback]  # 将 NodeType 定义为表示元组的新类型
    NEW_ROOT: tuple = ()

    def __init__(self, scen: ASpecificScen, knowledge_base: ASpecificKB | None = None) -> None:
        self.scen: ASpecificScen = scen

        # 开始：图结构 -------------------------
        self.hist: list[Trace.NodeType] = (
            []
        )  # 包含实验及其反馈的元组列表，按时间组织。
        self.dag_parent: list[tuple[int, ...]] = []  # 表示 DAG 结构中父索引的元组列表。
        # 定义：
        # - (,) 表示没有父节点（一棵树中的根节点）；
        # - (1,) 表示一个父节点；
        # - (1, 2) 表示两个父节点（尚未实现多个父节点）。
        # 父关系的语法糖：
        # - 仅用于选择：
        #    - (-1,) 表示选择最后一个记录节点作为父节点。

        # 注意：hist 和 dag_parent 的序列是按记录实验的顺序组织的。
        # 因此，它可能与 loop_id 的顺序不同。
        # 因此，我们需要一个额外的映射来将入队 id 映射回循环 id。
        self.idx2loop_id: dict[int, int] = {}

        # 设计讨论：
        # - 如果我们统一 loop_id 和入队 id，我们将减少识别负担。
        # - 如果我们为循环和入队使用不同的 id，我们就不必处理占位符逻辑。
        # 结束：图结构 -------------------------

        # TODO: self.hist 现在是 2 元组，从中删除假设，稍后为此更改旧代码。
        self.knowledge_base: ASpecificKB | None = knowledge_base
        self.current_selection: tuple[int, ...] = (-1,)

    def get_sota_hypothesis_and_experiment(self) -> tuple[Hypothesis | None, Experiment | None]:
        """访问上一个实验结果、子任务和相应的假设。"""
        # TODO: 返回值与签名不符。
        for experiment, feedback in self.hist[::-1]:
            if feedback.decision:
                return experiment.hypothesis, experiment

        return None, None

    def is_selection_new_tree(self, selection: tuple[int, ...] | None = None) -> bool:
        """
        检查当前跟踪是否为新树。
        - 当 dag_parent 为空时，选择可能是 (-1,)。
        """
        if selection is None:
            selection = self.get_current_selection()

        return selection == self.NEW_ROOT or len(self.dag_parent) == 0

    def get_current_selection(self) -> tuple[int, ...]:
        return self.current_selection

    def set_current_selection(self, selection: tuple[int, ...]) -> None:
        self.current_selection = selection

    def get_parent_exps(
        self,
        selection: tuple[int, ...] | None = None,
    ) -> list[Trace.NodeType]:
        """
        收集给定选择的所有祖先。
        返回列表遵循 [root->...->parent->current_node] 的顺序。
        """
        if selection is None:
            selection = self.get_current_selection()

        if self.is_selection_new_tree(selection):
            return []

        return [self.hist[i] for i in self.get_parents(selection[0])]

    def exp2idx(self, exp: Experiment | list[Experiment]) -> int | list[int] | None:
        if isinstance(exp, list):
            exps: list[Experiment] = exp

            # 保持顺序
            exp_to_index: dict[Experiment, int] = {_exp: i for i, (_exp, _) in enumerate(self.hist)}
            return [exp_to_index[_exp] for _exp in exps]
        for i, (_exp, _) in enumerate(self.hist):
            if _exp == exp:
                return i
        return None

    def idx2exp(self, idx: int | list[int]) -> Experiment | list[Experiment]:
        if isinstance(idx, list):
            idxs: list[int] = idx
            return [self.hist[_idx][0] for _idx in idxs]
        return self.hist[idx][0]

    def is_parent(self, parent_idx: int, child_idx: int) -> bool:
        ancestors = self.get_parents(child_idx)
        return parent_idx in ancestors

    def get_parents(self, child_idx: int) -> list[int]:
        if self.is_selection_new_tree((child_idx,)):
            return []

        ancestors: list[int] = []
        curr = child_idx
        while True:
            ancestors.insert(0, curr)
            parent_tuple = self.dag_parent[curr]
            if not parent_tuple or parent_tuple[0] == curr:
                break
            curr = parent_tuple[0]

        return ancestors


class CheckpointSelector:
    """
    在跟踪中，我们可以从任何检查点开始（我们将其表示为变量 `from_checkpoint_idx`）
    """

    @abstractmethod
    def get_selection(self, trace: Trace) -> tuple[int, ...] | None:
        """
        checkpoint_idx 表示我们要创建新节点的位置。
        返回值应该是目标节点的索引（新生成节点的父节点）。
        - `(-1, )` 表示从跟踪中的最新试验开始 - 默认值

          - 注意：我们不鼓励使用此选项；当有多个跟踪时，它会令人困惑。

        - `(idx, )` 表示从跟踪中的第 `idx` 次试验开始。
        - `None` 表示从头开始（开始一个新的跟踪）


        - `select.py` 中更高级的选择策略
        """


class SOTAexpSelector:
    """
    从跟踪中选择 SOTA 实验以提交
    """

    @abstractmethod
    def get_sota_exp_to_submit(self, trace: Trace) -> Experiment | None:
        """
        从跟踪中选择 SOTA 实验以提交
        """


class ExpPlanner(ABC, Generic[ASpecificPlan]):
    """
    一个用于规划实验的抽象类。
    规划器应根据跟踪为实验生成一个计划。
    """

    def __init__(self, scen: Scenario) -> None:
        self.scen = scen

    @abstractmethod
    def plan(self, trace: Trace) -> ASpecificPlan:
        """
        根据跟踪为实验生成一个计划。
        该计划应该是一个包含每个阶段计划的字典。
        """


class ExpGen(ABC):

    def __init__(self, scen: Scenario) -> None:
        self.scen = scen

    @abstractmethod
    def gen(self, trace: Trace, plan: ExperimentPlan | None = None) -> Experiment:
        """
        根据跟踪生成实验。
        规划是 gen 的一部分，但由于我们可能支持多阶段规划，
        我们需要将计划作为可选参数传递。

        `ExpGen().gen()` 的作用类似于

        .. code-block:: python

            # ExpGen().gen() ==
            Hypothesis2Experiment().convert(
                HypothesisGen().gen(trace)
            )
        """

    async def async_gen(self, trace: Trace, loop: LoopBase) -> Experiment:
        """
        生成实验并决定是否停止生成并放弃对其他例程的控制。
        """
        # 我们在这里给出一个默认实现。
        # 提案被设置为尽力在最大并行级别生成实验。
        while True:
            if loop.get_unfinished_loop_cnt(loop.loop_idx) < RD_AGENT_SETTINGS.get_max_parallel():
                return self.gen(trace)
            await asyncio.sleep(1)


class HypothesisGen(ABC):

    def __init__(self, scen: Scenario) -> None:
        self.scen = scen

    @abstractmethod
    def gen(
        self,
        trace: Trace,
        plan: ExperimentPlan | None = None,
    ) -> Hypothesis:
        # def gen(self, scenario_desc: str, ) -> Hypothesis:
        """
        变量 `scenario_desc` 的动机：
            - 模拟数据科学家正在观察场景。

        scenario_desc 可能包括：
            - 数据观察：
                - 原始或衍生
            - 任务信息：
        """


class Hypothesis2Experiment(ABC, Generic[ASpecificExp]):
    """
    [抽象描述 => 具体描述] => 代码实现卡
    """

    @abstractmethod
    def convert(self, hypothesis: Hypothesis, trace: Trace) -> ASpecificExp:
        """将想法提案与实施联系起来"""
        ...


# 布尔值、原因、置信度等。


class Experiment2Feedback(ABC):
    """ “从不同任务的 **已执行** 实现及其与先前性能的比较中生成的关于假设的反馈”"""

    def __init__(self, scen: Scenario) -> None:
        self.scen = scen

    @abstractmethod
    def generate_feedback(self, exp: Experiment, trace: Trace) -> ExperimentFeedback:
        """
        `exp` 应该被执行，并且结果应该被包括在内，以及与
        先前结果的比较（由 LLM 完成）。
        例如：将包括 Qlib 的 `mlflow`。
        """
        error_message = "generate_feedback 方法未实现。"
        raise NotImplementedError(error_message)
