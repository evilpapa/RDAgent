from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
# TYPE_CHECKING 用于类型提示，避免循环导入
# Any 用于泛型类型，Generic 用于创建泛型类，TypeVar 用于声明类型变量
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from tqdm import tqdm # 用于显示进度条

if TYPE_CHECKING:
    # 仅在类型检查时导入，避免运行时循环依赖
    # EvolvableSubjects 定义在 evolving_framework.py 中
    from rdagent.core.evolving_framework import EvolvableSubjects, QueriedKnowledge, RAGStrategy


# 从 evaluation 模块导入评估相关的基类和反馈类
from rdagent.core.evaluation import EvaluableObj, Evaluator, Feedback
# 从 evolving_framework 模块导入进化策略和进化步骤数据类
from rdagent.core.evolving_framework import EvolvingStrategy, EvoStep
# 导入日志记录器
from rdagent.log import rdagent_logger as logger

# 定义一个类型变量 ASpecificEvaluator，它必须是 Evaluator 的子类
# This defines a type variable ASpecificEvaluator, which must be a subclass of Evaluator.
ASpecificEvaluator = TypeVar("ASpecificEvaluator", bound=Evaluator)


class EvoAgent(ABC, Generic[ASpecificEvaluator]):
    """
    进化智能体 (Evolving Agent) 的抽象基类。
    Abstract base class for an Evolving Agent.

    它是一个泛型类，参数化了特定的评估器类型 `ASpecificEvaluator`。
    It's a generic class parameterized by a specific evaluator type `ASpecificEvaluator`.
    负责驱动 `EvolvableSubjects` 在多个步骤中进行进化。
    Responsible for driving the evolution of `EvolvableSubjects` over multiple steps.
    """

    def __init__(self, max_loop: int, evolving_strategy: EvolvingStrategy) -> None:
        """
        初始化进化智能体。
        Initializes the Evolving Agent.

        :param max_loop: 最大进化循环次数。
                         Maximum number of evolution loops.
        :param evolving_strategy: 该智能体采用的进化策略实例。
                                  The evolving strategy instance used by this agent.
        """
        self.max_loop = max_loop
        self.evolving_strategy = evolving_strategy

    @abstractmethod
    def multistep_evolve(
        self,
        evo: EvolvableSubjects,
        eva: ASpecificEvaluator | Feedback,
    ) -> Generator[EvolvableSubjects, None, None]:
        """
        执行多步进化过程。
        Performs a multi-step evolution process.

        这是一个生成器 (generator)，在每个进化步骤完成后，它会 `yield` 当前的 `EvolvableSubjects`。
        This is a generator that yields the current `EvolvableSubjects` after each evolution step.
        这样做的好处是调用者可以方便地控制流程、记录日志或进行中间检查。
        This allows the caller to easily control the process, log information, or perform intermediate checks.

        :param evo: 初始的可进化对象。
                    The initial evolvable object.
        :param eva: 用于评估进化结果的评估器实例，或者一个直接的反馈对象。
                    The evaluator instance used to assess the evolution results, or a direct Feedback object.
        :return: 一个生成器，每次产出进化后的 `EvolvableSubjects`。
                 A generator that yields the evolved `EvolvableSubjects` at each step.
        """
        # 子类需要实现这个方法
        # Subclasses must implement this method.
        raise NotImplementedError


class RAGEvaluator(Evaluator):
    """
    支持 RAG (Retrieval Augmented Generation) 的评估器抽象基类。
    Abstract base class for an evaluator that supports RAG (Retrieval Augmented Generation).

    它扩展了标准的 `Evaluator`，允许在评估时考虑从知识库中查询到的知识。
    It extends the standard `Evaluator` to allow consideration of knowledge queried
    from a knowledge base during evaluation.
    """

    @abstractmethod
    def evaluate(
        self,
        eo: EvaluableObj, # eo: 可评估对象 (Evaluable Object)
        queried_knowledge: QueriedKnowledge | None = None, # 允许传入查询到的知识
    ) -> Feedback:
        """
        评估一个可评估对象。
        Evaluates an evaluable object.

        :param eo: 需要被评估的对象。
                   The object to be evaluated.
        :param queried_knowledge: (可选) 在评估时可以参考的、从知识库查询到的知识。
                                  (Optional) Knowledge queried from a knowledge base that can be referenced during evaluation.
        :return: 评估后产生的反馈信息。
                 The feedback produced after evaluation.
        """
        raise NotImplementedError


class RAGEvoAgent(EvoAgent[RAGEvaluator]):
    """
    支持 RAG (Retrieval Augmented Generation) 的进化智能体。
    An Evolving Agent that supports RAG (Retrieval Augmented Generation).

    它继承自 `EvoAgent`，并专门使用 `RAGEvaluator` 进行评估。
    It inherits from `EvoAgent` and specifically uses a `RAGEvaluator` for evaluation.
    该智能体在进化循环中集成了知识的检索（query）和（可选的）生成（generate_knowledge）。
    This agent integrates knowledge retrieval (query) and (optional) generation (generate_knowledge)
    within its evolution loop.
    """

    def __init__(
        self,
        max_loop: int,
        evolving_strategy: EvolvingStrategy,
        rag: RAGStrategy | None, # RAG 策略实例，用于知识的查询与生成
                                 # RAG strategy instance for knowledge query and generation
        *,
        with_knowledge: bool = False, # 是否在进化过程中使用知识库 (通过 RAG query)
                                      # Whether to use the knowledge base (via RAG query) during evolution
        with_feedback: bool = True,   # 是否在进化后进行评估并使用反馈
                                      # Whether to evaluate and use feedback after evolution
        knowledge_self_gen: bool = False, # 知识库是否进行自我生成/更新新知识
                                         # Whether the knowledge base should self-generate/update new knowledge
    ) -> None:
        """
        初始化 RAG 进化智能体。
        Initializes the RAG Evolving Agent.

        :param max_loop: 最大进化循环次数。
        :param evolving_strategy: 采用的进化策略。
        :param rag: RAG 策略实例。如果为 None，则与知识相关的步骤将被跳过。
        :param with_knowledge: 如果为 True，则在进化步骤中会尝试从 RAG 策略查询知识。
        :param with_feedback: 如果为 True，则在进化步骤后会进行评估并记录反馈。
        :param knowledge_self_gen: 如果为 True，则在每次进化循环开始时，会尝试让 RAG 策略生成新知识。
        """
        super().__init__(max_loop, evolving_strategy)
        self.rag: RAGStrategy | None = rag # RAG 策略实例
        self.evolving_trace: list[EvoStep] = [] # 存储进化历史轨迹的列表
                                                # List to store the history of evolution steps
        self.with_knowledge = with_knowledge
        self.with_feedback = with_feedback
        self.knowledge_self_gen = knowledge_self_gen

    def multistep_evolve(
        self,
        evo: EvolvableSubjects, # 初始的可进化对象
        eva: RAGEvaluator | Feedback, # RAG 评估器或直接的反馈
    ) -> Generator[EvolvableSubjects, None, None]:
        """
        执行 RAG 增强的多步进化过程。
        Performs a RAG-enhanced multi-step evolution process.

        循环执行以下步骤直到达到 `max_loop` 或满足终止条件：
        1. (可选) 知识自进化: 如果 `knowledge_self_gen` 为 True 且 RAG 策略存在，调用 `rag.generate_knowledge()`。
        2. (可选) RAG 查询: 如果 `with_knowledge` 为 True 且 RAG 策略存在，调用 `rag.query()` 获取相关知识。
        3. 进化: 调用 `evolving_strategy.evolve()` 应用进化策略。
        4. 打包进化结果: 创建 `EvoStep` 对象记录当前步骤的信息。
        5. (可选) 评估: 如果 `with_feedback` 为 True，使用评估器 `eva` 对进化结果进行评估。
        6. 更新轨迹: 将当前 `EvoStep` 添加到 `evolving_trace`。
        7. 产出结果: `yield` 当前进化后的 `EvolvableSubjects`。
        8. 检查完成条件: 如果有反馈且反馈表明所有任务已完成，则提前终止循环。

        :param evo: 初始的可进化对象。
        :param eva: `RAGEvaluator` 实例或 `Feedback` 对象。
        :return: 一个生成器，每次产出进化后的 `EvolvableSubjects`。
        """
        # 使用 tqdm 创建一个进度条，显示当前正在执行的循环名称为 "Implementing"
        # Creates a progress bar using tqdm, displaying the current loop name as "Implementing"
        for evo_loop_id in tqdm(range(self.max_loop), "Implementing"):
            # 使用 logger.tag 为当前进化循环创建一个日志上下文，方便追踪日志
            # Uses logger.tag to create a logging context for the current evolution loop for easier log tracking
            with logger.tag(f"evo_loop_{evo_loop_id}"):
                queried_knowledge: QueriedKnowledge | None = None # 初始化查询到的知识为 None

                # 1. 知识自进化 (Knowledge self-evolving)
                # 如果配置了知识自生成，并且 RAG 策略实例存在
                if self.knowledge_self_gen and self.rag is not None:
                    # 调用 RAG 策略的 generate_knowledge 方法，传入当前的进化轨迹
                    # 让知识库有机会基于历史经验学习和生成新知识
                    self.rag.generate_knowledge(self.evolving_trace)

                # 2. RAG 查询 (RAG Query)
                # 如果配置了使用知识，并且 RAG 策略实例存在
                if self.with_knowledge and self.rag is not None:
                    # 调用 RAG 策略的 query 方法，传入当前的可进化对象和进化轨迹
                    # TODO: 注释中提到 "Putting the evolving trace in here doesn't actually work"
                    # 这可能是一个需要注意或修复的点，即进化轨迹是否能被 query 方法有效利用
                    # This might be a point to note or fix, i.e., whether the evolving trace
                    # can be effectively utilized by the query method.
                    queried_knowledge = self.rag.query(evo, self.evolving_trace)
                    if queried_knowledge:
                        logger.log_object(queried_knowledge, tag="queried_knowledge")


                # 3. 进化 (Evolve)
                # 调用进化策略的 evolve 方法，传入：
                # - evo: 当前的可进化对象
                # - evolving_trace: 历史进化轨迹
                # - queried_knowledge: 从 RAG 查询到的知识
                # 返回经过一次进化操作后的新的可进化对象
                evo = self.evolving_strategy.evolve(
                    evo=evo, # pyright: ignore[reportArgumentType] # 忽略 evolve 方法的类型检查 (evo 参数)
                    evolving_trace=self.evolving_trace,
                    queried_knowledge=queried_knowledge,
                )

                # 4. 打包进化结果 (Pack evolve results)
                # 创建一个 EvoStep 数据对象，记录当前步骤的进化结果和使用的知识
                es = EvoStep(evolvable_subjects=evo, queried_knowledge=queried_knowledge)

                # 5. 评估 (Evaluation)
                # 如果配置了使用反馈
                if self.with_feedback:
                    # 如果传入的 eva 本身就是 Feedback 对象，则直接使用
                    # 否则，调用 eva (RAGEvaluator) 的 evaluate 方法进行评估
                    # 评估时传入当前进化后的对象 evo 和查询到的知识 queried_knowledge
                    es.feedback = (
                        eva if isinstance(eva, Feedback) else eva.evaluate(eo=evo, queried_knowledge=queried_knowledge)
                    )
                    # 记录反馈信息到日志
                    logger.log_object(es.feedback, tag="evolving_feedback") # 更正了原版日志标签

                # 6. 更新轨迹 (Update trace)
                # 将当前进化步骤的信息 (EvoStep) 添加到进化轨迹列表中
                self.evolving_trace.append(es)

                # yield 当前进化后的可进化对象 evo
                # 这允许调用者在每一步进化后获取控制权，例如用于保存、日志或其他处理
                yield evo  # yield the control to caller for process control and logging.

                # 7. 检查是否所有任务都已完成 (Check if all tasks are completed)
                # 如果配置了使用反馈，并且当前步骤有反馈信息，并且反馈表明任务已完成
                if self.with_feedback and es.feedback is not None and es.feedback.finished():
                    logger.info("All tasks in evolving subject have been completed.")
                    break # 结束进化循环
