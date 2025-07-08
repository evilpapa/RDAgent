from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from rdagent.core.evaluation import EvaluableObj
from rdagent.core.knowledge_base import KnowledgeBase

if TYPE_CHECKING:
    from rdagent.core.evaluation import Feedback
    from rdagent.core.scenario import Scenario


class Knowledge:
    """
    知识的占位符基类。
    Represents a piece of knowledge. This is a placeholder base class.
    """
    pass


class QueriedKnowledge:
    """
    查询到的知识的占位符基类。
    Represents knowledge retrieved from a query. This is a placeholder base class.
    """
    pass


class EvolvingKnowledgeBase(KnowledgeBase):
    """
    可进化的知识库抽象基类。
    Abstract base class for a knowledge base that can be queried during evolution.
    它继承自通用的知识库基类 `KnowledgeBase`。
    """
    @abstractmethod
    def query(
        self,
        # TODO: 这里的参数可以更具体化，例如接收 EvolvableSubjects 或 evolving_trace
        # The parameters here could be more specific, e.g., accepting EvolvableSubjects or evolving_trace
    ) -> QueriedKnowledge | None:
        """
        从知识库中查询相关知识。
        Queries the knowledge base for relevant information.

        :return: 查询到的知识对象，如果未找到则为 None。
                 The queried knowledge object, or None if not found.
        """
        raise NotImplementedError


class EvolvableSubjects(EvaluableObj):
    """
    可进化主题/对象。这是在进化过程中被迭代改进的目标对象。
    The target object to be evolved. This is the central piece that an agent iteratively improves.
    它继承自 `EvaluableObj`，意味着它可以被评估（例如，评估代码的正确性、模型的性能等）。
    It inherits from `EvaluableObj`, meaning it can be evaluated (e.g., for code correctness, model performance).
    """

    def clone(self) -> EvolvableSubjects:
        """
        创建当前可进化对象的深拷贝。
        Creates a deep copy of the current evolvable object.
        这对于在进化过程中保存状态或探索不同分支非常重要。
        This is important for preserving state or exploring different branches during evolution.

        :return: 当前对象的深拷贝实例。
                 A deep copy instance of the current object.
        """
        return copy.deepcopy(self)


@dataclass
class EvoStep:
    """
    代表进化过程中的一个具体步骤或迭代。
    Represents a specific step or iteration in the evolution process.

    在一个进化步骤中，基于：
    - 先前的进化轨迹 (`previous trace`，隐式包含在调用策略时的 `evolving_trace` 中)
    - 新检索到的 RAG 知识 (`QueriedKnowledge`)

    `EvolvableSubjects` 会被进化（转换）成一个新的状态。
    (可选地) 在评估之后，我们会得到关于这个新状态的反馈 (`feedback`)。
    """

    evolvable_subjects: EvolvableSubjects
    """当前进化步骤完成后，得到的可进化对象。The state of the evolvable object after this evolution step."""

    queried_knowledge: QueriedKnowledge | None = None
    """(可选) 在此步骤中从知识库查询到的，用于辅助进化的知识。
    (Optional) The knowledge queried from the knowledge base in this step, used to aid evolution."""

    feedback: Feedback | None = None
    """(可选) 对当前 `evolvable_subjects` 进行评估后得到的反馈信息。
    (Optional) The feedback obtained after evaluating the current `evolvable_subjects`."""


class EvolvingStrategy(ABC):
    """
    进化策略的抽象基类。
    Abstract base class for an evolving strategy.
    它定义了如何将一个或多个 `EvolvableSubjects` 进化到下一个状态的逻辑。
    It defines the logic for how to evolve one or more `EvolvableSubjects` to their next state.
    """
    def __init__(self, scen: Scenario) -> None:
        """
        初始化进化策略。
        Initializes the evolving strategy.

        :param scen: 当前智能体运行的场景对象。
                     The scenario object in which the agent is currently operating.
        """
        self.scen = scen

    @abstractmethod
    def evolve(
        self,
        *evo: EvolvableSubjects, # 通常是一个 EvolvableSubjects 实例
                                 # Typically a single EvolvableSubjects instance
        evolving_trace: list[EvoStep] | None = None,
        queried_knowledge: QueriedKnowledge | None = None,
        **kwargs: Any,
    ) -> EvolvableSubjects:
        """
        执行一次进化操作。
        Performs one evolution step.

        进化轨迹 (`evolving_trace`) 是一个按照时间顺序排列的 `EvoStep` 列表。
        The evolving trace is a list of `EvoStep` objects ordered chronologically.

        为什么这些参数对于进化很重要：
        - `evolving_trace`: 历史反馈对于指导后续进化至关重要。
                           Historical feedback is crucial for guiding subsequent evolution.
        - `queried_knowledge`: 从知识库查询到的知识可以为进化提供新的信息或方向。
                               Queried knowledge from a knowledge base can provide new information or direction for evolution.

        :param evo: 当前的一个或多个可进化对象。
                    The current evolvable subject(s).
        :param evolving_trace: (可选) 历史进化步骤的列表。
                               (Optional) List of historical evolution steps.
        :param queried_knowledge: (可选) 当前查询到的知识。
                                  (Optional) Currently queried knowledge.
        :param kwargs: 其他特定策略可能需要的参数。
                       Other parameters that might be needed by specific strategies.
        :return: 经过一次进化操作后新的可进化对象。
                 The new evolvable object after one evolution step.
        """
        raise NotImplementedError


class RAGStrategy(ABC):
    """
    检索增强生成 (Retrieval Augmentation Generation, RAG) 策略的抽象基类。
    Abstract base class for a Retrieval Augmentation Generation (RAG) strategy.
    定义了如何与知识库交互以进行知识的检索和生成。
    Defines how to interact with a knowledge base for knowledge retrieval and generation.
    """

    def __init__(self, knowledgebase: EvolvingKnowledgeBase) -> None:
        """
        初始化 RAG 策略。
        Initializes the RAG strategy.

        :param knowledgebase: 一个实现了 `EvolvingKnowledgeBase` 接口的知识库实例。
                              An instance of a knowledge base that implements the `EvolvingKnowledgeBase` interface.
        """
        self.knowledgebase: EvolvingKnowledgeBase = knowledgebase

    @abstractmethod
    def query(
        self,
        evo: EvolvableSubjects,
        evolving_trace: list[EvoStep],
        **kwargs: Any,
    ) -> QueriedKnowledge | None:
        """
        根据当前进化状态和历史轨迹，从知识库中查询相关知识。
        Queries relevant knowledge from the knowledge base based on the current evolution state and historical trace.

        :param evo: 当前的可进化对象。
                    The current evolvable object.
        :param evolving_trace: 历史进化步骤的列表。
                               List of historical evolution steps.
        :param kwargs: 其他特定查询可能需要的参数。
                       Other parameters that might be needed for specific queries.
        :return: 查询到的知识对象，如果未找到或不适用则为 None。
                 The queried knowledge object, or None if not found or not applicable.
        """
        pass

    @abstractmethod
    def generate_knowledge(
        self,
        evolving_trace: list[EvoStep],
        *,
        return_knowledge: bool = False, # 指示是否应返回生成的知识对象
                                         # Indicates whether the generated knowledge object should be returned
        **kwargs: Any,
    ) -> Knowledge | None:
        """
        基于进化轨迹生成新的知识。
        Generates new knowledge based on the evolving trace.

        鼓励在生成新知识之前先查询相关知识。
        It is encouraged to query related knowledge before generating new knowledge.

        RAGStrategy 应自行维护新知识（例如，将其存入知识库）。
        The RAGStrategy should maintain the new knowledge all by itself (e.g., by storing it in the knowledge base).

        :param evolving_trace: 历史进化步骤的列表。
                               List of historical evolution steps.
        :param return_knowledge: 如果为 True，则返回生成的知识对象。
                                 If True, returns the generated knowledge object.
        :param kwargs: 其他特定知识生成可能需要的参数。
                       Other parameters that might be needed for specific knowledge generation.
        :return: 如果 `return_knowledge` 为 True，则返回生成的知识对象，否则通常为 None。
                 If `return_knowledge` is True, returns the generated knowledge object, otherwise typically None.
        """
        pass
