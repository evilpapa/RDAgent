# 2. 核心模块解析 (`rdagent/core/`)

`rdagent/core/` 目录包含了 RD-Agent 框架最核心的类和机制，定义了智能体如何进化、如何与环境交互、如何利用知识以及如何被评估。理解这部分是掌握整个框架的关键。

## 2.1 主要文件与概念概览

通过对 `rdagent/core/` 目录下文件名的初步观察和部分核心代码的阅读，我们可以识别出以下关键组件和它们的作用：

*   **`evolving_framework.py`**:
    *   定义了进化的基本构建块和概念。
    *   `EvolvableSubjects`: 代表需要被迭代改进的目标（例如一个模型、一个因子、一段代码）。它是可评估的。
    *   `EvoStep`: 记录了进化过程中的一个完整步骤，包括进化后的对象、使用的知识和获得的反馈。
    *   `EvolvingStrategy`: 抽象了“如何进化”的策略。不同的策略可以实现不同的进化逻辑（例如，基于规则的、基于 LLM 的、基于遗传算法的等）。
    *   `RAGStrategy`: 抽象了“如何利用知识库进行检索增强生成”的策略，包括知识的查询和生成。
    *   `EvolvingKnowledgeBase`: 知识库的抽象，强调其在进化过程中的查询能力。

*   **`evolving_agent.py`**:
    *   定义了驱动进化过程的智能体。
    *   `EvoAgent`: 是进化智能体的基类，负责执行多步进化循环。
    *   `RAGEvoAgent`: 专为结合 RAG (Retrieval Augmented Generation) 的场景设计的进化智能体。它在进化过程中会与 `RAGStrategy` 交互，利用知识库辅助进化，并处理评估反馈。
    *   `RAGEvaluator`: 评估器的扩展，使其在评估时可以考虑从知识库中检索到的信息。

*   **`developer.py`**: (后续分析)
    *   预计与“Development”阶段相关，可能包含负责实现、编码、调试等具体开发任务的智能体或组件。

*   **`proposal.py`**: (后续分析)
    *   预计与“Research”阶段相关，可能定义了“提议”或“想法”的数据结构，以及生成这些提议的逻辑。

*   **`scenario.py`**: (后续分析)
    *   定义了智能体运行的具体场景或任务上下文，可能包括任务目标、可用数据、环境约束等。

*   **`knowledge_base.py`**: (后续分析)
    *   提供了知识库的基础抽象。`EvolvingKnowledgeBase` 是其在进化框架中的具体化。

*   **`evaluation.py`**: (后续分析)
    *   定义了评估体系，包括 `EvaluableObj` (可评估对象)、`Evaluator` (评估器) 和 `Feedback` (反馈)。

*   **`experiment.py`**: (后续分析)
    *   可能用于管理和记录实验的配置、过程和结果。

*   **`conf.py`, `exception.py`, `prompts.py`, `utils.py`**:
    *   这些是辅助性模块，分别处理配置、异常、Prompt 管理和通用工具函数。

## 2.2 评估体系 (`evaluation.py`) 详解

`evaluation.py` 文件定义了 RD-Agent 框架中用于评估可进化对象 (EvolvableSubjects) 的核心组件。评估的结果（反馈）是指导进化方向的关键。

### `Feedback`
```python
class Feedback:
    # ... (已省略具体实现细节)
    def finished(self) -> bool:
        return self.__bool__()

    def __bool__(self) -> bool:
        return True
```
- **中文解读**: “反馈”。此类用作评估结果的数据容器。
- **设计原则**: 更像一个数据类（dataclass），其构建过程主要在 `Evaluator` 中完成。
- **关键方法**:
    - `finished()`: 判断相关任务是否已经结束。一个值得注意的设计是，它认为“成功”和“跳过”都意味着任务结束。默认情况下，它调用 `__bool__()`。
    - `__bool__()`: 默认返回 `True`。这意味着一个基本的 `Feedback` 实例在布尔上下文中被视为“真”，可能暗示着默认的“完成”或“成功”状态。具体的成功、失败、得分、错误信息等详细反馈内容，预计由其子类或在实例中添加额外属性来承载。

### `EvaluableObj`
```python
class EvaluableObj:
    """
    A set of information that is evaluable. Following things can be included.
    - Task
    - Solution
    - Ground Truth
    """
```
- **中文解读**: “可评估对象”。这是一个基类或标记类，代表任何可以被评价的事物。
- **用途**: 在 RD-Agent 中，核心的 `EvolvableSubjects` 类就继承自 `EvaluableObj`。
- **包含内容**: 注释表明，一个可评估对象可能封装了任务描述 (Task)、智能体生成的解决方案 (Solution)，以及用于评价的基准真相或预期结果 (Ground Truth)。

### `Evaluator`
```python
class Evaluator(ABC):
    @abstractmethod
    def evaluate(
        self,
        eo: EvaluableObj,
    ) -> Feedback:
        raise NotImplementedError
```
- **中文解读**: “评估器”。这是一个抽象基类，定义了评估操作的接口。
- **核心方法 `evaluate()`**:
    - **输入**: `eo: EvaluableObj` - 一个可评估对象实例。
    - **输出**: `Feedback` - 对输入对象评估后产生的反馈信息。
- **设计原则**:
    - `Evaluator` 负责将原始信息（例如，代码执行的输出、模型在测试集上的指标）转化为结构化的 `Feedback` 对象。
    - 这个转化过程可能分为两步：
        1.  `Feedback` 对象自身可能包含解析某些原始信息（如stdout、文件内容）的逻辑。
        2.  `Evaluator` 的 `evaluate` 方法则负责进行更高级的分析和总结，生成最终的反馈内容。
- **子类化**: 具体的评估逻辑（例如，代码静态检查、单元测试执行、模型性能计算、与黄金标准对比等）将通过继承 `Evaluator` 并实现 `evaluate` 方法来定义。在 `evolving_agent.py` 中我们已经看到了 `RAGEvaluator` 作为其子类，增加了对 `queried_knowledge` 的处理。

## 2.3 知识库 (`knowledge_base.py`) 详解

`knowledge_base.py` 提供了一个简单的、支持持久化的通用知识库基类。

### `KnowledgeBase`
```python
class KnowledgeBase:
    def __init__(self, path: str | Path | None = None) -> None:
        # ...
    def load(self) -> None:
        # ...
    def dump(self) -> None:
        # ...
```
- **中文解读**: “知识库”。
- **功能**:
    - **持久化**: 能够将知识库的内容保存到磁盘文件，并在需要时重新加载。这是通过 `dill` 库（pickle 的一个更强大版本）实现的，它可以序列化更广泛的 Python 对象。
    - **存储机制**: 它直接将自身的 `__dict__` 属性（不包括 `path` 属性）进行序列化和反序列化。这意味着知识库中的“知识”是以其属性的形式存储的。
- **关键方法**:
    - `__init__(self, path: str | Path | None = None)`: 构造函数。可以传入一个文件路径 `path`，用于后续的加载和保存操作。如果提供了路径，会尝试立即调用 `load()`。
    - `load(self)`: 如果 `self.path` 已设置且文件存在，则从该文件加载数据并更新当前知识库实例的属性。它能智能处理加载的数据是字典还是另一个 `KnowledgeBase` 实例的 `__dict__` 的情况。
    - `dump(self)`: 如果 `self.path` 已设置，则将当前知识库实例的所有属性（除了 `path`）序列化并保存到 `self.path` 指定的文件。如果目录不存在，会尝试创建。
- **与进化框架的关联**:
    - 在 `evolving_framework.py` 中定义的 `EvolvingKnowledgeBase` 继承自此处的 `KnowledgeBase`。这使得进化过程中使用的知识库也具备了通用的加载和保存能力。
    - `EvolvingKnowledgeBase` 进一步添加了 `query` 等与进化逻辑更相关的抽象方法。

## 2.4 场景定义 (`scenario.py`) 详解

`scenario.py` 文件定义了 `Scenario` 类，它是 RD-Agent 中具体应用场景的抽象基类。每个特定的研发任务（如特定的Kaggle竞赛、某类金融策略的开发）都可以被定义为一个 `Scenario` 的子类。

### `Scenario`
```python
class Scenario(ABC):
    @property
    @abstractmethod
    def background(self) -> str:
        # ...

    def get_source_data_desc(self, task: Task | None = None) -> str:
        # ...

    @property
    @abstractmethod
    def rich_style_description(self) -> str:
        # ...

    @abstractmethod
    def get_scenario_all_desc(
        self,
        task: Task | None = None,
        filtered_tag: str | None = None,
        simple_background: bool | None = None,
    ) -> str:
        # ...

    @property
    def experiment_setting(self) -> str | None:
        # ...
```
- **中文解读**: “场景”。
- **核心作用**: 封装了一个特定研发问题的所有上下文信息，包括背景知识、数据源描述、实验配置等。这些信息对于指导智能体（尤其是基于LLM的智能体）理解任务、提出假设、设计实验至关重要。
- **设计原则**:
    - 类本身不应包含与具体实现方法相关的配置（例如RAG的参数），这些应由具体的智能体或组件处理。
    - 强调信息的描述性，为智能体提供丰富的上下文。
- **主要抽象属性和方法**:
    - `background` (属性): 提供场景的通用背景信息。子类必须实现。
    - `get_source_data_desc(self, task: Task | None = None) -> str` (方法): 返回源数据的描述。其巧妙之处在于它可以根据当前处理的具体 `Task` (来自 `experiment.py`) 来动态提供不同的数据描述。默认返回空字符串。
        - `source_data` (属性): `get_source_data_desc()` 的一个便捷包装。
    - `rich_style_description` (属性): 提供一个“富文本样式”的场景描述，可能用于生成更易读的报告或UI展示。子类必须实现。
    - `get_scenario_all_desc(...)` (方法): 一个核心方法，用于将场景的各种描述信息（背景、数据、实验设置等）整合在一起，生成一个全面的场景描述文本。它可以根据当前任务、过滤标签、是否简化背景等参数进行定制。这是LLM理解任务的主要输入之一。子类必须实现。
    - `experiment_setting` (属性): (可选) 提供实验配置的富文本描述。

## 2.5 提议与实验流程 (`proposal.py`) 详解

`proposal.py` 是 `rdagent/core` 中最为复杂和核心的文件之一。它定义了从“想法”（Hypothesis）的产生，到“实验”（Experiment）的设计与执行，再到结果“反馈”（Feedback）的整个闭环流程中的关键数据结构和抽象行为。

### `Hypothesis`
- **中文解读**: “假设”或“想法”。
- **结构**: 存储一项研究假设及其相关论证信息，如：
    - `hypothesis`: 假设的核心内容。
    - `reason`: 提出该假设的详细理由。
    - `concise_reason`, `concise_observation`, `concise_justification`, `concise_knowledge`: 对理由、观察、论证和相关知识的简洁表述，可能用于LLM的提示或摘要。

### `ExperimentFeedback` 和 `HypothesisFeedback`
- **`ExperimentFeedback(Feedback)`**: 继承自 `evaluation.Feedback`。
    - **用途**: 专门用于封装实验执行后的反馈。
    - **关键属性**:
        - `decision: bool`: 表示该实验是否被认为是“成功”或“值得采纳”的。这会影响 `__bool__` 的返回值。
        - `reason: str`: 做出该决策的原因。
        - `exception: Exception | None`: 如果实验过程中发生异常，则记录异常对象。
        - `code_change_summary: str | None`: 对实验中代码变更的总结。
    - **`from_exception(cls, e: Exception)`**: 一个方便的类方法，用于从捕获到的异常快速创建表示失败的 `ExperimentFeedback`。
- **`HypothesisFeedback(ExperimentFeedback)`**: 进一步扩展，用于包含对假设评估的反馈。
    - **额外属性**:
        - `observations: str`: 基于实验结果的观察。
        - `hypothesis_evaluation: str`: 对原假设的评估。
        - `new_hypothesis: str`: 基于当前观察和评估，提出的新假设或改进方向。

### `Trace`
```python
class Trace(Generic[ASpecificScen, ASpecificKB]):
    # NodeType = tuple[Experiment, ExperimentFeedback]
    # hist: list[Trace.NodeType]
    # dag_parent: list[tuple[int, ...]]
    # ...
```
- **中文解读**: “轨迹”或“历史记录”。
- **核心作用**: 这是RD-Agent中记录整个研发迭代过程的核心数据结构。它不仅仅是一个线性的列表，还能通过 `dag_parent` 维护实验之间的依赖关系（形成有向无环图DAG）。
- **泛型**: `ASpecificScen` (特定场景类型) 和 `ASpecificKB` (特定知识库类型)。
- **关键属性**:
    - `scen`: 当前的场景实例。
    - `knowledge_base`: 关联的知识库实例。
    - `hist`: 一个列表，存储了每个历史步骤的 `(Experiment, ExperimentFeedback)` 对。
    - `dag_parent`: 列表，其索引对应 `hist` 中的实验，值是一个元组，表示该实验的父实验在 `hist` 中的索引。这用于构建实验的依赖图或进化树。 `()` 表示没有父节点（新树的根）。
    - `current_selection`: 一个元组，表示当前在轨迹中选定的节点（实验）的索引，用于指导下一步操作的上下文。
- **主要方法**:
    - `get_sota_hypothesis_and_experiment()`: 从历史中找到当前被认为是最佳（State-of-the-Art, SOTA）的假设和对应实验。
    - `is_selection_new_tree()`: 判断当前选择是否代表开始一个新的进化分支/树。
    - `get_parent_exps()`: 获取当前选定节点的所有祖先实验节点，按从根到父的顺序。
    - `exp2idx()`, `idx2exp()`: 在实验对象和其在 `hist` 中的索引之间进行转换。
    - `is_parent()`, `get_parents()`: 用于查询和获取节点的父子关系。

### 核心流程抽象类
`proposal.py` 定义了构成“研究与开发”循环的几个关键步骤的抽象基类：

1.  **`HypothesisGen(ABC)`**: 假设生成器。
    - `gen(self, trace: Trace) -> Hypothesis`: **核心方法**。根据当前的 `trace`（包含历史实验、反馈、场景信息、知识库），生成一个新的 `Hypothesis` (想法)。这是“R”阶段的起点。

2.  **`Hypothesis2Experiment(ABC, Generic[ASpecificExp])`**: 假设到实验的转换器。
    - `convert(self, hypothesis: Hypothesis, trace: Trace) -> ASpecificExp`: **核心方法**。将一个抽象的 `Hypothesis` 对象，结合当前的 `trace`，转换为一个具体的、可操作的 `Experiment` 对象 (`ASpecificExp` 是 `core.experiment.Experiment` 的子类，代表特定类型的实验)。

3.  **`ExpGen(ABC)`**: 实验生成器（可选的封装）。
    - `gen(self, trace: Trace) -> Experiment`: 将上述1和2两个步骤封装起来，直接从 `trace` 生成 `Experiment`。
    - `async_gen`: 提供了异步生成实验的接口，用于控制并行度。

4.  **`Developer(ABC, Generic[ASpecificExp])`** (定义在 `developer.py`，但与此流程紧密相关): 开发者。
    - `develop(self, exp: ASpecificExp) -> ASpecificExp`: **核心方法**。接收一个 `Experiment` 对象，并对其进行“开发”——这可能包括生成代码、运行代码、执行测试、收集原始结果等。**重要**: 此方法应就地修改 `exp` 对象。

5.  **`Experiment2Feedback(ABC)`**: 实验到反馈的转换器。
    - `generate_feedback(self, exp: Experiment, trace: Trace) -> ExperimentFeedback`: **核心方法**。在一个 `Experiment` 被 `Developer` 处理（并通常已执行）后，此方法负责分析 `Experiment` 中的结果（例如，代码输出、性能指标、错误信息），并结合 `trace` 上下文，生成一个结构化的 `ExperimentFeedback` 对象。这是对“D”阶段结果的总结和评估。

### 决策与选择器
- **`CheckpointSelector(ABC)`**: 检查点选择器。
    - `get_selection(self, trace: Trace) -> tuple[int, ...] | None`: 从当前的 `trace` 中选择一个历史节点（实验）作为下一轮迭代的起点或父节点。返回的是该节点在 `hist` 中的索引元组。例如，`(-1,)` 可能表示从最新的实验开始，`None` 表示完全从头开始。
- **`SOTAexpSelector(ABC)`**: SOTA实验选择器。
    - `get_sota_exp_to_submit(self, trace: Trace) -> Experiment | None`: 从整个 `trace` 中挑选出最终被认为是最佳的（SOTA）实验，用于提交、报告或部署。

这个 `proposal.py` 文件通过这些类，清晰地勾勒出了一个从提出想法，到设计实验，到执行与评估，再到基于反馈产生新想法的完整研发闭环。`Trace` 对象是这个循环中承载所有历史和上下文的关键。

## 2.6 开发者 (`developer.py`) 详解

`developer.py` 文件定义了 `Developer` 类，它代表了RD-Agent中负责具体“开发”活动（对应R&D中的"D"）的组件或智能体。

### `Developer`
```python
class Developer(ABC, Generic[ASpecificExp]):
    def __init__(self, scen: Scenario) -> None:
        self.scen: Scenario = scen

    @abstractmethod
    def develop(self, exp: ASpecificExp) -> ASpecificExp: # TODO: remove return value
        # ...
```
- **中文解读**: “开发者”。
- **泛型**: `ASpecificExp`，表示此开发者处理特定类型的实验 (`core.experiment.Experiment` 的子类)。
- **初始化**: `__init__(self, scen: Scenario)`: 接收一个 `Scenario` 对象，表明开发活动是在特定场景上下文中进行的。
- **核心方法 `develop(self, exp: ASpecificExp) -> ASpecificExp`**:
    - **输入**: `exp: ASpecificExp` - 一个由“研究”阶段（例如 `Hypothesis2Experiment`）创建的 `Experiment` 对象。这个对象通常包含了要做什么实验的描述、目标、可能的代码片段或伪代码等。
    - **任务**: 此方法的核心职责是**实现或完善**这个实验。具体活动可能包括：
        - 根据实验描述生成完整的可执行代码。
        - 运行生成的代码。
        - 执行必要的测试。
        - 收集代码执行的输出、日志、性能指标、产生的错误等原始结果。
        - 将这些原始结果更新回传入的 `exp` 对象中。
    - **返回值与就地修改**:
        - **重要**: 当前方法签名包含返回值 `ASpecificExp`，但注释明确指出 `TODO: remove return value`。
        - **设计意图**: `Developer` 应该**就地修改 (in-place edit)** 传入的 `exp` 对象，而不是返回一个全新的实例。这样做是因为即使在开发过程中发生错误（例如代码无法编译或运行时崩溃），框架仍然希望能够访问到这个部分完成或失败的 `exp` 对象，以便从中提取有用的信息（如错误日志、部分生成的代码）用于后续的分析和反馈。
    - **反馈设置**: 如果开发者在开发过程中需要传递特定的信息给后续步骤（例如，关于代码质量的评论、遇到的特定问题），它应该在 `exp` 对象上设置一个 `ExperimentFeedback` 实例。

**与整体流程的关联**:

`Developer` 处在 "R&D" 循环的 "D" (Development) 阶段。它接收来自 "R" (Research/Proposal) 阶段产出的具体实验方案 (`Experiment` 对象)，负责将其付诸实践，并将实践的结果（成功、失败、数据、日志）记录回该 `Experiment` 对象中。随后，这个被“开发”过的 `Experiment` 对象会被传递给 `Experiment2Feedback` 组件，用于生成结构化的反馈，从而驱动下一轮的 "R" 阶段。

## 2.7 进化框架 (`evolving_framework.py`) 详解 (回顾)

在理解了 `Scenario`, `Proposal`, `Developer`, `Evaluation`, `KnowledgeBase` 之后，我们可以更清晰地回顾 `evolving_framework.py` 和 `evolving_agent.py` 的作用。

- `EvolvableSubjects`: 在很多场景下，一个 `Experiment` 对象（在 `Developer` 处理后，包含了代码和结果）就可以被视为一个 `EvolvableSubjects`。
- `EvolvingStrategy`: 它的 `evolve` 方法，实际上可能就封装了 `HypothesisGen` -> `Hypothesis2Experiment` -> (可选的 `ExpGen`) 的过程，或者更复杂的、利用LLM直接基于历史 `EvoStep` (其中包含 `Experiment` 和 `ExperimentFeedback`) 来生成下一个 `Experiment` (作为新的 `EvolvableSubjects`) 的逻辑。
- `EvoAgent` / `RAGEvoAgent`: 驱动整个迭代循环。
    - 在 `multistep_evolve` 中：
        - 调用 `evolving_strategy.evolve()` 得到新的 `evolvable_subjects` (例如，一个新的 `Experiment` 方案)。
        - **这里可以插入 `Developer` 的工作**: 在 `evolve` 之后、`evaluate` 之前，框架可以调用 `Developer.develop()` 来处理这个新的 `Experiment` 方案，将其实现并执行，结果填充回 `Experiment` 对象。
        - 然后，这个被 `develop` 过的 `Experiment` (现在是 `EvaluableObj`) 被传递给 `Evaluator.evaluate()` (或者在RAG场景下，`RAGEvaluator.evaluate()`，它可能对应于 `Experiment2Feedback.generate_feedback()`) 来产生 `Feedback`。
        - 这个 `Feedback` 和被 `develop` 过的 `Experiment` 组成了新的 `EvoStep`，加入到 `evolving_trace` 中。

这样，`core` 目录下的这些主要组件就构成了一个完整的、自动化的、迭代式的研发循环。

---
接下来，我将为 `scenario.py`, `proposal.py`, `developer.py` 添加代码注释。

## 2.8 实验与任务 (`experiment.py`) 详解

`experiment.py` 文件定义了构成RD-Agent研发流程基本单元的类：`Task` (任务)、`Workspace` (工作空间) 和 `Experiment` (实验)。这些类是智能体进行具体“开发”和“执行”活动的操作对象。

### `Task` 和 `AbsTask`
- **`AbsTask(ABC)`**: 任务的抽象基类。
    - **属性**:
        - `name: str`: 任务的名称。
        - `version: int`: 任务的版本，默认为1。用于区分不同类型或阶段的任务（例如，Qlib任务与Kaggle任务的执行方式可能不同）。
    - **抽象方法**:
        - `get_task_information(self) -> str`: 返回一个字符串，唯一标识该任务，可能用于缓存或索引。
- **`Task(AbsTask)`**: `AbsTask` 的具体实现。
    - **额外属性**:
        - `description: str`: 对任务的详细描述。
    - `get_task_information()`: 实现方法，通常返回任务名称和描述的组合。

### `Workspace` 和 `FBWorkspace`
- **`Workspace(ABC, Generic[ASpecificTask, ASpecificFeedback])`**: 工作空间的抽象基类。
    - **概念**: 工作空间是存放特定任务实现（如代码、配置文件、数据链接等）的地方。它是动态的，会随着开发者的工作而演进。
    - **泛型参数**: `ASpecificTask` (此工作空间针对的任务类型)，`ASpecificFeedback` (与此工作空间关联的反馈类型)。
    - **属性**:
        - `target_task: ASpecificTask | None`: 此工作空间关联的目标任务。
        - `feedback: ASpecificFeedback | None`: 对此工作空间状态或内容的反馈。
        - `running_info: RunningInfo`: 一个 `RunningInfo` 数据对象，用于存储执行结果 (`result`) 和运行时间 (`running_time`)。
    - **抽象方法**:
        - `execute(self, *args: Any, **kwargs: Any) -> object | None`: 执行工作空间中的任务/代码。
        - `copy(self) -> Workspace`: 创建工作空间的副本（通常是深拷贝），用于保存快照或进行分支探索。
        - `all_codes(self) -> str` (属性): 以字符串形式返回工作空间中的所有代码内容。
- **`FBWorkspace(Workspace)`**: 基于文件系统的工作空间 (File-Based Workspace)。
    - **实现方式**: 将任务的实现具化为一个磁盘上的文件夹。这个文件夹包含代码文件、数据文件（或其链接）、以及执行后产生的输出文件。
    - **关键属性**:
        - `file_dict: dict[str, Any]`: 一个字典，键是文件在工作空间中的相对路径（字符串），值是文件内容（字符串）或特殊标记（如 `DEL_KEY`）。这是工作空间状态的核心表示。
        - `workspace_path: Path`: 工作空间文件夹在磁盘上的实际路径。通常是一个自动生成的唯一路径。
    - **核心方法**:
        - `prepare()`: 创建工作空间文件夹。
        - `inject_files(**files: str)`: 将 `files` 字典中提供的文件内容写入到工作空间文件夹中。如果文件值为 `FBWorkspace.DEL_KEY` (一个特殊字符串 `__DEL__`)，则删除对应文件。同时更新 `self.file_dict`。
        - `link_all_files_in_folder_to_workspace(data_path: Path, workspace_path: Path)` (静态方法): 将指定数据文件夹 `data_path` 中的所有文件链接（符号链接或硬链接，取决于操作系统）到工作空间路径 `workspace_path` 下。
        - `get_files() -> list[Path]`: 返回工作空间文件夹中所有文件的 `Path` 对象列表。
        - `inject_code_from_folder(folder_path: Path)`: 从一个外部文件夹加载代码文件到当前工作空间的 `file_dict` 并写入磁盘。
        - `inject_code_from_file_dict(workspace: FBWorkspace)`: 从另一个 `FBWorkspace` 实例的 `file_dict` 复制文件。
        - `clear()`: 清空工作空间（删除文件夹，清空 `file_dict`）。
        - `before_execute()`: 在执行前确保工作空间已准备好（调用 `prepare()` 和 `inject_files(**self.file_dict)`）。
        - `run(self, env: Env, entry: str) -> EnvResult`: **核心执行方法**。
            - 输入: `env: Env` (一个定义了执行环境的对象，例如Docker环境，来自 `utils.env`)，`entry: str` (执行的入口命令或脚本)。
            - 操作: 确保工作空间文件就绪后，调用 `env.run()` 在指定环境中执行命令。
            - 输出: `EnvResult` 对象，包含 `stdout` (标准输出), `exit_code` (退出码), `running_time` (运行时间) 等。`stdout` 会经过过滤和缩减处理。
        - `execute(self, env: Env, entry: str) -> str`: `run` 方法的包装，仅返回处理后的 `stdout`。
    - `all_codes` (属性实现): 返回 `file_dict` 中所有 `.py` 文件（不包括测试文件）的内容的格式化字符串。
    - `get_codes(pattern: str)`: 类似 `all_codes`，但只包括匹配特定正则表达式 `pattern` 的文件。

### `Experiment`
- **`Experiment(ABC, Generic[ASpecificTask, ASpecificWSForExperiment, ASpecificWSForSubTasks])`**: 实验的抽象基类。
    - **概念**: 一个实验代表了一次完整的研发尝试，它可能由一个或多个子任务 (`sub_tasks`) 构成。每个子任务及其实现（工作空间）都是实验的一部分。实验本身也可以有一个整体的工作空间。
    - **泛型参数**:
        - `ASpecificTask`: 子任务的具体类型。
        - `ASpecificWSForExperiment`: 实验级别工作空间的具体类型。
        - `ASpecificWSForSubTasks`: 子任务级别工作空间的具体类型。
    - **关键属性**:
        - `hypothesis: Hypothesis | None`: (可选) 生成此实验的原始假设 (来自 `proposal.py`)。
        - `sub_tasks: Sequence[ASpecificTask]`: 构成此实验的子任务序列。
        - `sub_workspace_list: list[ASpecificWSForSubTasks | None]`: 一个列表，与 `sub_tasks` 对应，存储每个子任务的工作空间实例。初始化时为 `None` 列表，由 `Developer` 填充。
        - `based_experiments: Sequence[ASpecificWSForExperiment]`: (可选) 当前实验所基于的先前实验（的工作空间）。用于追踪实验的演进或比较。
        - `experiment_workspace: ASpecificWSForExperiment | None`: (可选) 整个实验级别的工作空间，可能用于存放整合性的代码或结果。
        - `prop_dev_feedback: Feedback | None`: 用于在不同开发阶段或开发者之间传递的反馈信息。
        - `running_info: RunningInfo`: 存储整个实验的运行结果和时间。
        - `result` (属性): `running_info.result` 的便捷访问器和设置器。
        - `sub_results: dict[str, float]`: (TODO，未来可能移除) 用于存储子任务的量化结果。
        - `local_selection: tuple[int, ...] | None`: 用于支持并行多轨迹功能，记录此实验在特定轨迹分支上的选择信息。

### 类型变量和加载器
- **`ASpecificExp = TypeVar("ASpecificExp", bound=Experiment)`**: 特定实验类型的泛型变量。
- **`TaskOrExperiment = TypeVar("TaskOrExperiment", Task, Experiment)`**: 联合类型变量，表示可以是任务或实验。
- **`WsLoader(ABC, Generic[ASpecificTask, ASpecificWS])`**: 工作空间加载器的抽象基类。
    - `load(self, task: ASpecificTask) -> ASpecificWS`: 根据任务加载或初始化一个工作空间。
- **`Loader(ABC, Generic[TaskOrExperiment])`**: 更通用的加载器抽象基类，可以加载任务或实验。

**总结**:
`experiment.py` 为RD-Agent定义了执行具体研发活动所需的基本构件。`Task` 定义了要做什么，`Workspace` (尤其是 `FBWorkspace`) 提供了如何做和在哪做的机制（代码存储、文件管理、执行环境接口），而 `Experiment` 则将这些组织起来，代表一次完整的、可能包含多个步骤的研发尝试。这些构件与 `developer.py` 中的 `Developer` 和 `proposal.py` 中的流程紧密协作。

---
接下来，我将为 `experiment.py` 添加代码注释。

### `EvolvableSubjects`
```python
class EvolvableSubjects(EvaluableObj):
    """The target object to be evolved"""

    def clone(self) -> EvolvableSubjects:
        return copy.deepcopy(self)
```
- **中文解读**: “可进化主题/对象”。这是智能体在进化过程中操作和改进的核心目标。
- **继承**: 它继承自 `EvaluableObj` (定义在 `evaluation.py`)，表明这个对象是可以被评估的，评估结果将作为反馈指导进化。
- **关键方法**:
    - `clone()`: 创建一个对象的深拷贝。这在进化过程中非常重要，可以保留前一状态，或者在尝试不同进化路径时使用。

### `EvoStep`
```python
@dataclass
class EvoStep:
    """At a specific step,
    based on
    - previous trace
    - newly RAG knowledge `QueriedKnowledge`

    the EvolvableSubjects is evolved to a new one `EvolvableSubjects`.

    (optional) After evaluation, we get feedback `feedback`.
    """
    evolvable_subjects: EvolvableSubjects
    queried_knowledge: QueriedKnowledge | None = None
    feedback: Feedback | None = None
```
- **中文解读**: “进化步骤”。这是一个数据类，用于封装进化过程中一个完整迭代的信息。
- **属性**:
    - `evolvable_subjects`: 当前步骤进化后得到的 `EvolvableSubjects` 实例。
    - `queried_knowledge`: (可选) 在这一步进化时，从知识库中检索到的、辅助进化的知识。
    - `feedback`: (可选) 对当前 `evolvable_subjects` 进行评估后得到的反馈信息。

### `EvolvingStrategy`
```python
class EvolvingStrategy(ABC):
    def __init__(self, scen: Scenario) -> None:
        self.scen = scen

    @abstractmethod
    def evolve(
        self,
        *evo: EvolvableSubjects,
        evolving_trace: list[EvoStep] | None = None,
        queried_knowledge: QueriedKnowledge | None = None,
        **kwargs: Any,
    ) -> EvolvableSubjects:
        # ...
```
- **中文解读**: “进化策略”。这是一个抽象基类，定义了如何进行“进化”操作的接口。
- **核心方法 `evolve()`**:
    - **输入**:
        - `*evo`: 一个或多个当前的 `EvolvableSubjects` 实例。
        - `evolving_trace`: (可选) 包含过去所有 `EvoStep` 的列表，即历史进化轨迹。这使得策略可以从历史中学习。
        - `queried_knowledge`: (可选) 当前从知识库查询到的知识。
    - **输出**: 一个新的、经过改进的 `EvolvableSubjects` 实例。
- **子类化**: 具体的进化方式（例如，使用 LLM 生成新代码、调整模型参数等）将通过继承此类并实现 `evolve` 方法来定义。

### `RAGStrategy`
```python
class RAGStrategy(ABC):
    def __init__(self, knowledgebase: EvolvingKnowledgeBase) -> None:
        self.knowledgebase: EvolvingKnowledgeBase = knowledgebase

    @abstractmethod
    def query(
        self,
        evo: EvolvableSubjects,
        evolving_trace: list[EvoStep],
        **kwargs: Any,
    ) -> QueriedKnowledge | None:
        pass

    @abstractmethod
    def generate_knowledge(
        self,
        evolving_trace: list[EvoStep],
        *,
        return_knowledge: bool = False,
        **kwargs: Any,
    ) -> Knowledge | None:
        # ...
```
- **中文解读**: “检索增强生成策略”。这也是一个抽象基类，定义了如何与知识库交互以支持进化。
- **核心方法**:
    - `query()`: 根据当前的进化对象 (`evo`) 和进化历史 (`evolving_trace`)，从知识库中检索相关的知识。
    - `generate_knowledge()`: 基于进化历史，生成新的知识并（通常）更新到知识库中。这体现了知识库的动态学习能力。

## 2.3 进化智能体 (`evolving_agent.py`) 详解

该文件定义了实际执行进化循环的“智能体”。

### `EvoAgent`
```python
class EvoAgent(ABC, Generic[ASpecificEvaluator]):
    def __init__(self, max_loop: int, evolving_strategy: EvolvingStrategy) -> None:
        self.max_loop = max_loop
        self.evolving_strategy = evolving_strategy

    @abstractmethod
    def multistep_evolve(
        self,
        evo: EvolvableSubjects,
        eva: ASpecificEvaluator | Feedback,
    ) -> Generator[EvolvableSubjects, None, None]:
        # ...
```
- **中文解读**: “进化智能体”。抽象基类，定义了进化智能体的基本框架。
- **属性**:
    - `max_loop`: 最大进化迭代次数。
    - `evolving_strategy`: 该智能体采用的进化策略实例。
- **核心方法 `multistep_evolve()`**:
    - 这是一个**生成器 (Generator)**。在每次迭代（进化步骤）后，它会 `yield` 当前的 `EvolvableSubjects`。这允许调用者在每个步骤后介入，例如进行日志记录、保存中间状态或进行外部检查。
    - **输入**:
        - `evo`: 初始的 `EvolvableSubjects`。
        - `eva`: 一个评估器 (`Evaluator` 的子类) 或一个直接的 `Feedback` 对象。评估器用于对每步进化的结果进行打分。

### `RAGEvoAgent`
```python
class RAGEvoAgent(EvoAgent[RAGEvaluator]):
    def __init__(
        self,
        max_loop: int,
        evolving_strategy: EvolvingStrategy,
        rag: Any, # Should be RAGStrategy
        *,
        with_knowledge: bool = False,
        with_feedback: bool = True,
        knowledge_self_gen: bool = False,
    ) -> None:
        # ...
        self.rag = rag # RAGStrategy instance
        self.evolving_trace: list[EvoStep] = []
        # ...

    def multistep_evolve(
        self,
        evo: EvolvableSubjects,
        eva: RAGEvaluator | Feedback,
    ) -> Generator[EvolvableSubjects, None, None]:
        for evo_loop_id in tqdm(range(self.max_loop), "Implementing"):
            # ... (详细逻辑见源码)
            # 1. (Optional) Knowledge self-evolving: rag.generate_knowledge()
            # 2. (Optional) RAG Query: rag.query()
            # 3. Evolve: evolving_strategy.evolve()
            # 4. Pack results into EvoStep
            # 5. (Optional) Evaluation: eva.evaluate()
            # 6. Update trace
            # 7. Yield current evolvable_subjects
            # 8. Check completion
            # ...
```
- **中文解读**: “RAG进化智能体”。这是 `EvoAgent` 的一个具体实现，专门设计用于整合 RAG (Retrieval Augmented Generation) 能力。
- **增强功能**:
    - 它持有一个 `rag` 对象 (实现了 `RAGStrategy` 接口)，用于在进化过程中查询知识库和生成新知识。
    - `with_knowledge`: 布尔标志，控制是否在进化中使用 RAG 查询。
    - `with_feedback`: 布尔标志，控制是否在进化后进行评估并使用反馈。
    - `knowledge_self_gen`: 布尔标志，控制 RAG 策略是否在每轮进化前尝试自我生成/更新知识。
- **`multistep_evolve()` 实现**:
    - 该方法详细实现了进化循环。在一个 `for` 循环中（最多 `max_loop` 次）：
        1.  **知识自省/生成 (可选)**: 如果 `knowledge_self_gen` 为 `True`，调用 `self.rag.generate_knowledge()` 让知识库有机会基于当前所有历史进行学习和更新。
        2.  **知识查询 (可选)**: 如果 `with_knowledge` 为 `True`，调用 `self.rag.query()` 来获取与当前进化对象相关的知识。
        3.  **执行进化**: 调用 `self.evolving_strategy.evolve()`，将当前进化对象、历史轨迹和查询到的知识传入，得到新的进化对象。
        4.  **封装步骤信息**: 将进化结果、查询到的知识等封装成一个 `EvoStep` 对象。
        5.  **评估与反馈 (可选)**: 如果 `with_feedback` 为 `True`，使用评估器 `eva` 对新的进化对象进行评估，并将反馈信息存入 `EvoStep`。
        6.  **记录轨迹**: 将当前的 `EvoStep` 添加到 `self.evolving_trace` 列表中。
        7.  **产出当前结果**: `yield` 当前进化后的对象。
        8.  **检查终止条件**: 如果获得了反馈，并且反馈表明任务已完成 (例如，`feedback.finished()` 为 `True`)，则提前结束进化循环。

### 总结

`evolving_framework.py` 和 `evolving_agent.py` 共同定义了一个灵活且可扩展的进化系统。开发者可以通过实现不同的 `EvolvingStrategy`、`RAGStrategy` 和 `Evaluator` 来定制特定场景下的进化行为和知识利用方式。`RAGEvoAgent` 提供了一个集成了 RAG 的标准进化流程。

---
接下来，我将开始为这两个文件添加代码注释。Tool output for `create_file_with_block`:
