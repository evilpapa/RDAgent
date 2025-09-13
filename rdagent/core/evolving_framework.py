from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from rdagent.core.evaluation import EvaluableObj
from rdagent.core.knowledge_base import KnowledgeBase

if TYPE_CHECKING:
    from rdagent.core.evaluation import Feedback
    from rdagent.core.scenario import Scenario


class Knowledge:
    pass


class QueriedKnowledge:
    pass


class EvolvingKnowledgeBase(KnowledgeBase):
    @abstractmethod
    def query(
        self,
    ) -> QueriedKnowledge | None:
        raise NotImplementedError


class EvolvableSubjects(EvaluableObj):
    """要演进的目标对象"""

    def clone(self) -> EvolvableSubjects:
        return copy.deepcopy(self)


ASpecificEvolvableSubjects = TypeVar("ASpecificEvolvableSubjects", bound=EvolvableSubjects)


@dataclass
class EvoStep(Generic[ASpecificEvolvableSubjects]):
    """在特定步骤中，
    基于
    - 先前的跟踪
    - 新的 RAG 知识 `QueriedKnowledge`

    EvolvableSubjects 将演进为一个新的 `EvolvableSubjects`。

    （可选）评估后，我们得到反馈 `feedback`。
    """

    evolvable_subjects: ASpecificEvolvableSubjects

    queried_knowledge: QueriedKnowledge | None = None
    feedback: Feedback | None = None


class EvolvingStrategy(ABC, Generic[ASpecificEvolvableSubjects]):
    def __init__(self, scen: Scenario) -> None:
        self.scen = scen

    @abstractmethod
    def evolve(
        self,
        *evo: ASpecificEvolvableSubjects,
        evolving_trace: list[EvoStep[ASpecificEvolvableSubjects]] | None = None,
        queried_knowledge: QueriedKnowledge | None = None,
        **kwargs: Any,
    ) -> ASpecificEvolvableSubjects:
        """演进跟踪是按时间排序的（可演进主题，反馈）列表。

        该参数对演进很重要的原因。
        - evolving_trace：历史反馈很重要。
        - queried_knowledge：查询到的知识
        """


class RAGStrategy(ABC, Generic[ASpecificEvolvableSubjects]):
    """检索增强生成策略"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.knowledgebase: EvolvingKnowledgeBase = self.load_or_init_knowledge_base(*args, **kwargs)

    @abstractmethod
    def load_or_init_knowledge_base(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> EvolvingKnowledgeBase:
        pass

    @abstractmethod
    def query(
        self,
        evo: ASpecificEvolvableSubjects,
        evolving_trace: list[EvoStep],
        **kwargs: Any,
    ) -> QueriedKnowledge | None:
        pass

    @abstractmethod
    def generate_knowledge(
        self,
        evolving_trace: list[EvoStep[ASpecificEvolvableSubjects]],
        *,
        return_knowledge: bool = False,
        **kwargs: Any,
    ) -> Knowledge | None:
        """基于演进跟踪生成新知识。
        - 鼓励在生成新知识之前查询相关知识。

        RAGStrategy 应自行维护新知识。
        """

    @abstractmethod
    def dump_knowledge_base(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def load_dumped_knowledge_base(self, *args: Any, **kwargs: Any) -> None:
        """这是为了加载转储的知识库。
        它主要用于并行编码，其中多个编码器共享同一个知识库。
        然后，智能体在更新知识库之前应从其他地方加载知识库。
        """
