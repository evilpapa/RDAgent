# TODO: 如果将轨迹(traces)传递给实例，则移除 `self.scen`。
# This is a note for future refactoring: if traces are passed into instances, `self.scen` might be redundant.

from __future__ import annotations # 确保类型提示中的向前引用有效

import asyncio # 用于异步编程
from abc import ABC, abstractmethod # 导入抽象基类和抽象方法
from typing import TYPE_CHECKING, Generic, TypeVar # 导入类型提示相关的工具

from rdagent.core.conf import RD_AGENT_SETTINGS # 导入框架的配置设置
from rdagent.core.evaluation import Feedback # 从评估模块导入 Feedback 基类
from rdagent.core.experiment import ASpecificExp, Experiment # 从实验模块导入 Experiment 基类和特定实验类型变量
from rdagent.core.knowledge_base import KnowledgeBase # 导入知识库基类
from rdagent.core.scenario import Scenario # 导入场景基类

if TYPE_CHECKING: # 仅在类型检查时执行，避免循环导入
    from rdagent.utils.workflow.loop import LoopBase # 从工作流循环模块导入 LoopBase


class Hypothesis:
    """
    代表一个假设或想法 (Hypothesis / Idea)。
    Represents a hypothesis or an idea.

    TODO: 我们可以为它找到一个更好的名字。
          We may have a better name for it.
    候选名称 (Name Candidates):
    - Belief (信念)
    """

    def __init__(
        self,
        hypothesis: str, # 假设的核心内容
        reason: str, # 提出该假设的详细理由
        concise_reason: str, # 简洁的理由
        concise_observation: str, # 简洁的观察结果
        concise_justification: str, # 简洁的论证/辩护
        concise_knowledge: str, # 相关的简洁知识
    ) -> None:
        self.hypothesis: str = hypothesis
        self.reason: str = reason
        self.concise_reason: str = concise_reason
        self.concise_observation: str = concise_observation
        self.concise_justification: str = concise_justification
        self.concise_knowledge: str = concise_knowledge

    def __str__(self) -> str:
        """返回假设及其理由的字符串表示。"""
        return f"""Hypothesis: {self.hypothesis}
Reason: {self.reason}"""

    # 备忘：来源可能是数据分析结果或模型分析结果等
    # source: data_ana | model_nan = None


# 流程示意：原始信息(仓库路径/数据/反馈) => 视图/摘要 => 生成的假设
# Origin(path of repo/data/feedback) => view/summarization => generated Hypothesis


class ExperimentFeedback(Feedback):
    """
    实验反馈类，继承自通用的 Feedback。
    Class for experiment feedback, inheriting from the generic Feedback.
    专门用于封装实验执行后的结果和决策。
    Specialized for encapsulating results and decisions after experiment execution.
    """
    def __init__(
        self,
        reason: str, # 对于决策的解释或原因
        *,
        code_change_summary: str | None = None, # (可选) 代码变更的摘要
        decision: bool, # 实验是否成功或被采纳的布尔决策
        exception: Exception | None = None, # (可选) 实验过程中发生的异常
    ) -> None:
        self.decision = decision # True 表示采纳/成功, False 表示不采纳/失败
                                 # True means accepted/successful, False means not accepted/failed.
        self.reason = reason
        # 如果 exception 不为 None，意味着由于异常导致未能成功生成可运行的实验。
        # 但可运行的结果也并不总是好的。
        # Exception is not None means failing to generate runnable experiments due to exception.
        # Runnable results are not always good.
        self.exception: Exception | None = (
            exception  # 如果实验引发异常，该异常将被整合到反馈中
                       # if the experiment raises an exception, it will be integrated into part of the feedback.
        )
        self.code_change_summary = code_change_summary

    def __bool__(self) -> bool:
        """定义实验反馈在布尔上下文中的值，直接反映 `decision`。"""
        return self.decision

    def __str__(self) -> str:
        """返回实验反馈的字符串表示。"""
        res = f"Decision: {self.decision}\nReason: {self.reason}"
        if self.code_change_summary is not None:
            res += "\nCode Change Summary: " + self.code_change_summary
        return res

    @classmethod
    def from_exception(cls, e: Exception) -> ExperimentFeedback:
        """
        一个便捷的类方法，用于从一个异常对象创建 ExperimentFeedback 实例。
        A convenient class method to create an ExperimentFeedback instance from an exception object.
        通常表示实验失败。
        Usually indicates experiment failure.
        """
        return cls(decision=False, reason=f"The experiment fails due to {e!s}", exception=e)


class HypothesisFeedback(ExperimentFeedback):
    """
    假设反馈类，继承自 ExperimentFeedback。
    Class for hypothesis feedback, inheriting from ExperimentFeedback.
    用于更复杂的场景，其中反馈不仅包含实验结果，还包含对假设本身的评估和新假设的提出。
    Used for more complex scenarios where feedback includes not only experiment results
    but also evaluation of the hypothesis itself and proposal of new hypotheses.
    """
    def __init__(
        self,
        observations: str, # 基于实验结果的观察
        hypothesis_evaluation: str, # 对当前假设的评估
        new_hypothesis: str, # 基于当前结果提出的新假设或改进方向
        reason: str, # 做出此反馈的原因（继承自父类）
        *,
        code_change_summary: str | None = None, # (可选) 代码变更摘要
        decision: bool, # 关于当前假设或实验路径的决策
    ) -> None:
        super().__init__(reason, decision=decision, code_change_summary=code_change_summary)
        self.observations = observations
        self.hypothesis_evaluation = hypothesis_evaluation
        self.new_hypothesis = new_hypothesis

    def __str__(self) -> str:
        """返回假设反馈的字符串表示，包含父类信息和自身特有信息。"""
        return f"""{super().__str__()}
Observations: {self.observations}
Hypothesis Evaluation: {self.hypothesis_evaluation}
New Hypothesis: {self.new_hypothesis}"""


# 定义类型变量，用于泛型类 Trace
ASpecificScen = TypeVar("ASpecificScen", bound=Scenario) # 特定场景类型
ASpecificKB = TypeVar("ASpecificKB", bound=KnowledgeBase) # 特定知识库类型


class Trace(Generic[ASpecificScen, ASpecificKB]):
    """
    轨迹 (Trace) 类，用于记录和管理整个研发过程的历史和上下文。
    Trace class, used to record and manage the history and context of the entire R&D process.
    它是一个泛型类，可以针对特定的场景和知识库类型进行参数化。
    It is a generic class that can be parameterized for specific scenario and knowledge base types.
    """
    NodeType = tuple[Experiment, ExperimentFeedback]  # 定义 NodeType 为 (实验, 实验反馈) 的元组类型
                                                      # Define NodeType as a tuple type of (Experiment, ExperimentFeedback)
    NEW_ROOT: tuple = () # 表示一个新的、无父节点的根轨迹的常量
                         # Constant representing a new root trace with no parent

    def __init__(self, scen: ASpecificScen, knowledge_base: ASpecificKB | None = None) -> None:
        """
        初始化轨迹。
        Initializes the trace.

        :param scen: 当前的场景实例。
        :param knowledge_base: (可选) 关联的知识库实例。
        """
        self.scen: ASpecificScen = scen
        self.hist: list[Trace.NodeType] = ( # 历史记录列表，存储 (实验, 实验反馈) 对，按时间组织
            []
        )  # List of tuples containing experiments and their feedback, organized over time.
        self.dag_parent: list[tuple[int, ...]] = []  # 列表，存储 DAG 结构中父节点的索引。
                                                     # List of tuples representing parent indices in the DAG structure.
                                                     # () 代表无父节点；(1,) 代表一个父节点；(1, 2) 代表两个父节点。
        # (,) represents no parent; (1,) presents one parent; (1, 2) represents two parents.

        # TODO: self.hist 现在是二元组，从中移除 hypothesis，稍后修改旧代码以适应此更改。
        # self.hist is a 2-tuple now, remove hypothesis from it, change old code for this later.
        self.knowledge_base: ASpecificKB | None = knowledge_base
        self.current_selection: tuple[int, ...] = (-1,) # 当前在轨迹中选择的节点（实验）的索引，默认为最新的(-1)
                                                       # Index of the currently selected node (experiment) in the trace, defaults to the latest (-1).

    def get_sota_hypothesis_and_experiment(self) -> tuple[Hypothesis | None, Experiment | None]:
        """
        访问最新的、被认为是成功的实验结果及其对应的假设。
        Access the latest experiment result deemed successful, its sub-task, and the corresponding hypothesis.
        SOTA: State-of-the-Art (当前最佳)
        """
        # TODO: 返回值与签名不完全一致 (签名中没有 sub-task)。需要检查 Experiment 是否包含 hypothesis。
        # The return value does not align with the signature (no sub-task in signature). Need to check if Experiment contains hypothesis.
        # 假设 Experiment 对象有一个 hypothesis 属性。
        # Assuming the Experiment object has a hypothesis attribute.
        for experiment, feedback in self.hist[::-1]: # 从后向前遍历历史记录
            if feedback.decision: # 如果反馈决策是成功的
                # 假设 experiment 对象有一个 'hypothesis' 属性
                # Assuming the experiment object has a 'hypothesis' attribute
                return getattr(experiment, 'hypothesis', None), experiment
        return None, None

    def is_selection_new_tree(self, selection: tuple[int, ...] | None = None) -> bool:
        """
        检查当前选择是否代表开始一个新的进化树/分支。
        Check if the current selection represents the start of a new evolution tree/branch.
        - 当 `dag_parent` 为空时，`selection` 可能是 `(-1,)`。
          `selection` may be `(-1,)` when `dag_parent` is empty.
        """
        if selection is None:
            selection = self.get_current_selection()

        return selection == self.NEW_ROOT or len(self.dag_parent) == 0

    def get_current_selection(self) -> tuple[int, ...]:
        """获取当前选择的节点索引。"""
        return self.current_selection

    def set_current_selection(self, selection: tuple[int, ...]) -> None:
        """设置当前选择的节点索引。"""
        self.current_selection = selection

    def get_parent_exps(
        self,
        selection: tuple[int, ...] | None = None,
    ) -> list[Trace.NodeType]:
        """
        收集给定选择节点的所有祖先节点（实验和反馈对）。
        Collect all ancestors of the given selection.
        返回的列表顺序为 [根节点 -> ... -> 父节点 -> 当前节点的前一个节点]。
        The return list follows the order of [root->...->parent->node_before_current_node].
        注意：这里返回的是祖先链，不包括当前选择的节点本身。
        Note: This returns the ancestor chain, not including the selected node itself.
        """
        if selection is None:
            selection = self.get_current_selection()

        if self.is_selection_new_tree(selection) or not selection: # 如果是新树或选择为空
            return []

        # get_parents 返回的是索引列表，这里根据索引从 hist 中取出对应的实验和反馈
        # get_parents returns a list of indices, here we retrieve the corresponding experiments and feedback from hist
        return [self.hist[i] for i in self.get_parents(selection[0])]

    def exp2idx(self, exp: Experiment | list[Experiment]) -> int | list[int] | None:
        """
        将一个或多个实验对象转换为其在 `hist` 列表中的索引。
        Converts one or more experiment objects to their indices in the `hist` list.
        """
        if isinstance(exp, list):
            exps_list: list[Experiment] = exp
            # 为了保持顺序，先构建一个从实验对象到索引的映射
            # To maintain order, first build a mapping from experiment object to index
            exp_to_index: dict[Experiment, int] = {_exp: i for i, (_exp, _) in enumerate(self.hist)}
            try:
                return [exp_to_index[_e] for _e in exps_list]
            except KeyError: # 如果有实验不在 hist 中
                return None
        # 单个实验对象
        single_exp: Experiment = exp
        for i, (_exp_hist, _) in enumerate(self.hist):
            if _exp_hist == single_exp:
                return i
        return None # 未找到

    def idx2exp(self, idx: int | list[int]) -> Experiment | list[Experiment] | None:
        """
        将一个或多个索引转换为 `hist` 列表中对应的实验对象。
        Converts one or more indices to the corresponding experiment objects in the `hist` list.
        """
        try:
            if isinstance(idx, list):
                idxs_list: list[int] = idx
                return [self.hist[_i][0] for _i in idxs_list]
            # 单个索引
            single_idx: int = idx
            return self.hist[single_idx][0]
        except IndexError: # 如果索引越界
            return None


    def is_parent(self, parent_idx: int, child_idx: int) -> bool:
        """
        检查 `parent_idx` 是否是 `child_idx` 的祖先节点。
        Checks if `parent_idx` is an ancestor of `child_idx`.
        """
        ancestors = self.get_parents(child_idx)
        return parent_idx in ancestors

    def get_parents(self, child_idx: int) -> list[int]:
        """
        获取指定子节点的所有祖先节点的索引列表，按从根到直接父节点的顺序排列。
        Gets the list of indices of all ancestor nodes of the specified child node,
        ordered from the root to the direct parent.
        """
        if child_idx < 0 or child_idx >= len(self.dag_parent): # 基本的边界检查
            return []
        if self.is_selection_new_tree((child_idx,)): # 如果是新树的根节点
            return []

        ancestors: list[int] = []
        curr = child_idx
        visited_indices = set() # 防止循环（理论上不应发生，但作为保护）

        while curr not in visited_indices:
            visited_indices.add(curr)
            ancestors.insert(0, curr) # 插入到列表头部以保持顺序
            if curr >= len(self.dag_parent): # curr 索引超出了 dag_parent 的范围
                 break
            parent_tuple = self.dag_parent[curr]
            if not parent_tuple: # 没有父节点了，到达根节点
                break
            # 假设通常只有一个父节点，取第一个
            # Assuming typically only one parent, take the first one.
            # 如果 parent_tuple[0] == curr，说明是自指，也应停止
            # If parent_tuple[0] == curr, it's a self-reference, should also stop.
            if parent_tuple[0] == curr: # 避免无限循环
                break
            curr = parent_tuple[0]
            if curr < 0 : #父节点索引无效
                break

        # 如果 ancestors 只包含 child_idx 本身，且它不是根节点（有parent信息但parent_tuple为空），
        # 这意味着它是一个孤立的节点或者其父节点信息不完整。
        # 通常，根节点的 parent_tuple 为空。
        # 此处返回的祖先列表不应包含 child_idx 自身，除非它是唯一的根。
        # 但按原代码逻辑，是包含自身的，然后向上追溯。
        # 如果要返回纯粹的父节点列表，需要在末尾移除child_idx。
        # 让我们保持原代码逻辑，返回包含自身到根的路径。
        return ancestors


class CheckpointSelector(ABC):
    """
    检查点选择器抽象基类。
    Abstract base class for a Checkpoint Selector.
    用于从轨迹中选择一个“检查点”（即一个历史实验节点）作为新一轮研发的起点。
    Used to select a "checkpoint" (i.e., a historical experiment node) from the trace
    as the starting point for a new round of R&D.
    """

    @abstractmethod
    def get_selection(self, trace: Trace) -> tuple[int, ...] | None:
        """
        选择一个检查点。
        Selects a checkpoint.

        `checkpoint_idx` (隐式地通过返回值表达) 代表我们想要创建新节点的地方。
        The return value should be the index/indices of the target node(s) (the parent(s) of the new generating node).
        返回元组的含义：
        - `(-1, )`: 代表从轨迹中的最新试验开始 (默认值)。
                     Represents starting from the latest trial in the trace (default value).
        - `(idx, )`: 代表从轨迹中索引为 `idx` 的试验开始。
                     Represents starting from the trial at index `idx` in the trace.
        - `None`: 代表从头开始 (开始一个新的轨迹)。
                  Represents starting from scratch (start a new trace).
        - 更高级的选择策略可能在 `select.py` 中实现。
          More advanced selection strategies might be implemented in `select.py`.

        :param trace: 当前的轨迹对象。
        :return: 一个包含选定父节点索引的元组，或 None。
                 A tuple containing the indices of selected parent nodes, or None.
        """
        raise NotImplementedError


class SOTAexpSelector(ABC):
    """
    SOTA (State-of-the-Art) 实验选择器抽象基类。
    Abstract base class for a SOTA (State-of-the-Art) Experiment Selector.
    用于从轨迹中选择最终的、最好的实验结果用于提交或部署。
    Used to select the final, best experiment result from the trace for submission or deployment.
    """

    @abstractmethod
    def get_sota_exp_to_submit(self, trace: Trace) -> Experiment | None:
        """
        从轨迹中选择 SOTA 实验进行提交。
        Selects the SOTA experiment from the trace to submit.

        :param trace: 当前的轨迹对象。
        :return: 被选为 SOTA 的实验对象，或 None。
                 The experiment object selected as SOTA, or None.
        """
        raise NotImplementedError


class ExpGen(ABC):
    """
    实验生成器 (Experiment Generator) 的抽象基类。
    Abstract base class for an Experiment Generator.
    负责根据当前轨迹生成新的实验。
    Responsible for generating new experiments based on the current trace.
    """

    def __init__(self, scen: Scenario) -> None:
        """
        初始化实验生成器。
        Initializes the Experiment Generator.

        :param scen: 当前的场景实例。
        """
        self.scen = scen # TODO: 如文件开头的注释，如果 trace 包含了足够的场景信息，这个 scen 可能可以移除。

    @abstractmethod
    def gen(self, trace: Trace) -> Experiment:
        """
        根据轨迹生成实验。
        Generates an experiment based on the trace.

        `ExpGen().gen()` 的作用类似于 (plays a role like):

        .. code-block:: python

            # ExpGen().gen() ==
            Hypothesis2Experiment().convert(
                HypothesisGen().gen(trace)
            )

        即，它可能内部封装了“假设生成”和“假设到实验转换”的步骤。
        That is, it might internally encapsulate the steps of "hypothesis generation"
        and "hypothesis-to-experiment conversion".

        :param trace: 当前的轨迹对象。
        :return: 新生成的实验对象。
                 The newly generated experiment object.
        """
        raise NotImplementedError

    async def async_gen(self, trace: Trace, loop: LoopBase) -> Experiment:
        """
        异步生成实验，并决定是否暂停生成以将控制权交给其他协程。
        Asynchronously generates an experiment and decides whether to stop yielding generation
        and give up control to other coroutines.
        这主要用于控制并行任务的数量。
        This is primarily used to control the number of parallel tasks.
        """
        # 这里提供了一个默认实现。
        # A default implementation is provided here.
        # 目标是尽最大努力在最大并行度限制下生成实验。
        # The goal is to try its best to generate the experiment under the maximum parallelism limit.
        while True: # 无限循环，直到满足条件
            # 获取当前循环中未完成的任务数量，并与配置的最大并行数比较
            # Get the count of unfinished tasks in the current loop and compare with the configured max parallelism.
            if loop.get_unfinished_loop_cnt(loop.loop_idx) < RD_AGENT_SETTINGS.get_max_parallel():
                # 如果未完成任务数小于最大并行数，则调用同步的 gen 方法生成实验并返回
                # If the count of unfinished tasks is less than max parallelism, call the synchronous gen method.
                return self.gen(trace)
            await asyncio.sleep(1) # 否则，异步等待1秒后重试
                                   # Otherwise, asynchronously wait for 1 second and retry.


class HypothesisGen(ABC):
    """
    假设生成器 (Hypothesis Generator) 的抽象基类。
    Abstract base class for a Hypothesis Generator.
    负责根据当前轨迹生成新的假设。
    Responsible for generating new hypotheses based on the current trace.
    """

    def __init__(self, scen: Scenario) -> None:
        """
        初始化假设生成器。
        Initializes the Hypothesis Generator.

        :param scen: 当前的场景实例。
        """
        self.scen = scen # TODO: 同 ExpGen 中的 scen。

    @abstractmethod
    def gen(self, trace: Trace) -> Hypothesis:
        # 另一种可能的签名：def gen(self, scenario_desc: str, ) -> Hypothesis:
        # Another possible signature.
        """
        根据轨迹生成假设。
        Generates a hypothesis based on the trace.

        引入 `scenario_desc` 变量的动机 (Motivation of the variable `scenario_desc`):
            - 模拟数据科学家观察场景的过程。
              Mocking a data-scientist observing the scenario.

        `scenario_desc` 可能包含 (may include):
            - 数据观察 (data observation):
                - 原始数据或衍生数据 (Original or derivative)
            - 任务信息 (Task information):

        当前实现是直接使用 `trace` 对象，它内部可以访问到场景信息和历史。
        The current implementation uses the `trace` object directly, which internally
        has access to scenario information and history.

        :param trace: 当前的轨迹对象。
        :return: 新生成的假设对象。
                 The newly generated hypothesis object.
        """
        raise NotImplementedError


class Hypothesis2Experiment(ABC, Generic[ASpecificExp]):
    """
    假设到实验转换器 (Hypothesis to Experiment Converter) 的抽象基类。
    Abstract base class for a Hypothesis to Experiment Converter.
    负责将一个抽象的假设转换为一个具体的、可操作的实验对象。
    Responsible for converting an abstract hypothesis into a concrete, actionable experiment object.

    流程示意：[抽象描述 => 具体描述] => 代码实现卡片（比喻）
    Flow illustration: [Abstract description => concrete description] => Code implementation Card (metaphor)
    """

    @abstractmethod
    def convert(self, hypothesis: Hypothesis, trace: Trace) -> ASpecificExp:
        """
        将想法提议（假设）连接到具体实现（实验）。
        Connects the idea proposal (hypothesis) to implementation (experiment).

        :param hypothesis: 要转换的假设对象。
        :param trace: 当前的轨迹对象，提供上下文信息。
        :return: 转换后得到的特定类型的实验对象。
                 The specific type of experiment object obtained after conversion.
        """
        # `...` 在类型提示的上下文中通常表示省略号对象，这里可能只是占位符。
        # `...` in type hinting context usually refers to the Ellipsis object, here it might just be a placeholder.
        # 实际应为 raise NotImplementedError
        raise NotImplementedError


# 关于反馈内容的思考：布尔决策、原因、置信度等。
# Thoughts on feedback content: Boolean decision, Reason, Confidence, etc.


class Experiment2Feedback(ABC):
    """
    实验到反馈转换器 (Experiment to Feedback Converter) 的抽象基类。
    Abstract base class for an Experiment to Feedback Converter.

    负责根据已执行的实验（及其结果）生成结构化的反馈信息。
    Responsible for generating structured feedback information based on executed experiments (and their results).
    反馈内容是关于假设的，并且基于不同任务的**已执行**实现以及它们与先前性能的比较。
    "Generated feedbacks on the hypothesis from **Executed** Implementations of different tasks
    & their comparisons with previous performances"
    """

    def __init__(self, scen: Scenario) -> None:
        """
        初始化实验到反馈转换器。
        Initializes the Experiment to Feedback Converter.

        :param scen: 当前的场景实例。
        """
        self.scen = scen

    @abstractmethod
    def generate_feedback(self, exp: Experiment, trace: Trace) -> ExperimentFeedback:
        """
        生成实验反馈。
        Generates experiment feedback.

        传入的 `exp` 对象应该已经被执行，并且其结果（例如 Qlib 中的 mlflow 记录）应该包含在内。
        The `exp` object passed in should have been executed, and its results
        (e.g., mlflow records in Qlib) should be included.
        反馈还应包括与先前结果的比较（这部分可能由 LLM 完成）。
        The feedback should also include a comparison with previous results (this part might be done by an LLM).

        :param exp: 已执行并包含结果的实验对象。
        :param trace: 当前的轨迹对象，提供历史和上下文。
        :return: 生成的实验反馈对象。
                 The generated experiment feedback object.
        """
        error_message = "generate_feedback method is not implemented."
        raise NotImplementedError(error_message)
