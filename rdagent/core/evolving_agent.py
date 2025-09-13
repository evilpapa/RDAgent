from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import nullcontext
from typing import Any, Generic, TypeVar

from filelock import FileLock
from tqdm import tqdm

from rdagent.core.evaluation import EvaluableObj, Evaluator, Feedback
from rdagent.core.evolving_framework import EvolvableSubjects, EvolvingStrategy, EvoStep
from rdagent.log import rdagent_logger as logger

ASpecificEvaluator = TypeVar("ASpecificEvaluator", bound=Evaluator)
ASpecificEvolvableSubjects = TypeVar("ASpecificEvolvableSubjects", bound=EvolvableSubjects)


class EvoAgent(ABC, Generic[ASpecificEvaluator, ASpecificEvolvableSubjects]):

    def __init__(self, max_loop: int, evolving_strategy: EvolvingStrategy) -> None:
        self.max_loop = max_loop
        self.evolving_strategy = evolving_strategy

    @abstractmethod
    def multistep_evolve(
        self,
        evo: ASpecificEvolvableSubjects,
        eva: ASpecificEvaluator | Feedback,
    ) -> Generator[ASpecificEvolvableSubjects, None, None]:
        """
        为调用者生成 EvolvableSubjects，以便于过程控制和日志记录。
        """


class RAGEvaluator(Evaluator):

    @abstractmethod
    def evaluate(
        self,
        eo: EvaluableObj,
        queried_knowledge: object = None,
    ) -> Feedback:
        raise NotImplementedError


class RAGEvoAgent(EvoAgent[RAGEvaluator, ASpecificEvolvableSubjects], Generic[ASpecificEvolvableSubjects]):

    def __init__(
        self,
        max_loop: int,
        evolving_strategy: EvolvingStrategy,
        rag: Any,
        *,
        with_knowledge: bool = False,
        with_feedback: bool = True,
        knowledge_self_gen: bool = False,
        enable_filelock: bool = False,
        filelock_path: str | None = None,
    ) -> None:
        super().__init__(max_loop, evolving_strategy)
        self.rag = rag
        self.evolving_trace: list[EvoStep[ASpecificEvolvableSubjects]] = []
        self.with_knowledge = with_knowledge
        self.with_feedback = with_feedback
        self.knowledge_self_gen = knowledge_self_gen
        self.enable_filelock = enable_filelock
        self.filelock_path = filelock_path

    def multistep_evolve(
        self,
        evo: ASpecificEvolvableSubjects,
        eva: RAGEvaluator | Feedback,
    ) -> Generator[ASpecificEvolvableSubjects, None, None]:
        for evo_loop_id in tqdm(range(self.max_loop), "Implementing"):
            with logger.tag(f"evo_loop_{evo_loop_id}"):
                # 1. RAG
                queried_knowledge = None
                if self.with_knowledge and self.rag is not None:
                    # TODO: 在此处放置演进跟踪实际上不起作用
                    queried_knowledge = self.rag.query(evo, self.evolving_trace)

                # 2. 演进
                evo = self.evolving_strategy.evolve(
                    evo=evo,
                    evolving_trace=self.evolving_trace,
                    queried_knowledge=queried_knowledge,
                )

                # 3. 打包演进结果
                es = EvoStep[ASpecificEvolvableSubjects](evo, queried_knowledge)

                # 4. 评估
                if self.with_feedback:
                    es.feedback = (
                        eva if isinstance(eva, Feedback) else eva.evaluate(evo, queried_knowledge=queried_knowledge)
                    )
                    logger.log_object(es.feedback, tag="evolving feedback")

                # 5. 更新跟踪
                self.evolving_trace.append(es)

                # 6. 知识自演进
                if self.knowledge_self_gen and self.rag is not None:
                    with FileLock(self.filelock_path) if self.enable_filelock else nullcontext():  # type: ignore[arg-type]
                        self.rag.load_dumped_knowledge_base()
                        self.rag.generate_knowledge(self.evolving_trace)
                        self.rag.dump_knowledge_base()

                yield evo  # 将控制权交给调用者以进行过程控制和日志记录。

                # 7. 检查是否所有任务都已完成
                if self.with_feedback and es.feedback is not None and es.feedback.finished():
                    logger.info("All tasks in evolving subject have been completed.")
                    break
