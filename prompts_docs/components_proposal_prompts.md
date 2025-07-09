# 组件层：提议 (Proposal) 相关提示词

本文档解析定义在 `rdagent/components/proposal/prompts.yaml` 文件中的提示词。这些提示词是 RD-Agent 核心提议流程（“R”阶段，Research）的基础，用于生成新的研究假设 (Hypothesis) 和将假设转化为具体的实验设计 (Experiment)。

## 1. `hypothesis_gen` - 假设生成

-   **源文件路径**: `rdagent/components/proposal/prompts.yaml` (键: `hypothesis_gen`)
-   **主要用途**:
    指导 LLM 分析历史实验数据、现有知识和特定场景信息，以生成新的、有价值的研究假设。LLM 需要反思先前实验的成败，并据此提出优化现有方法或探索全新方向的建议。
-   **关键输入变量 (Jinja2)**:
    -   `{{ targets }}`: 字符串，描述当前研发工作的具体目标（例如，“financial factors”, “machine learning models”）。
    -   `{{ scenario }}`: 字符串，当前研发场景的详细描述。
    -   `{{ hypothesis_and_feedback }}`: 字符串，格式化的历史假设及其反馈列表。循环遍历历史 `(hypothesis, feedback)` 对。
    -   `{{ last_hypothesis_and_feedback }}`: 字符串，格式化的最后一次试验的假设和反馈。
    -   `{{ sota_hypothesis_and_feedback }}`: 字符串，格式化的当前最优（SOTA）方案的假设和反馈。
    -   `{{ RAG }}`: (可选) 字符串，通过 RAG (Retrieval Augmented Generation) 系统检索到的相关知识。
    -   `{{ hypothesis_specification }}`: (可选) 字符串，用户或系统提供的对生成假设的额外具体要求或约束。
    -   `{{ hypothesis_output_format }}`: 字符串，定义了期望 LLM 输出假设的格式（通常是 JSON Schema 的描述或示例）。
-   **输出格式要求**:
    通常要求为 JSON 格式，具体结构由 `{{ hypothesis_output_format }}` 定义。可能包含字段如 `"hypothesis"` (假设陈述), `"reason"` (理由), `"component"` (相关组件) 等。
-   **在流程中的位置**:
    通常在 `rdagent.core.proposal.HypothesisGen` 的子类中被调用（详见 [`learn/core_module.md`](../learn/core_module.md#核心流程抽象类) 中对 `HypothesisGen` 的描述）。这是研发迭代循环的起点（“R”阶段——Research/Proposal）。
-   **设计说明**:
    -   System Prompt 引导 LLM 扮演分析者和创新者的角色。
    -   User Prompt 提供了丰富的历史上下文和（可选的）外部知识，帮助 LLM 做出有根据的判断。
    -   强调了对 `hypothesis_specification` 的遵守。

## 2. `hypothesis2experiment` - 假设到实验的转换

-   **源文件路径**: `rdagent/components/proposal/prompts.yaml` (键: `hypothesis2experiment`)
-   **主要用途**:
    指导 LLM 将一个（通常由 `hypothesis_gen` 生成的）抽象的研究假设，转化为一个具体的、可操作的实验设计或任务描述。
-   **关键输入变量 (Jinja2)**:
    -   `{{ targets }}`: 字符串，研发目标。
    -   `{{ scenario }}`: 字符串，当前研发场景的描述。
    -   `{{ target_hypothesis }}`: 字符串或对象，当前需要为其设计实验的目标假设。
    -   `{{ hypothesis_and_feedback }}`: 字符串，历史假设及反馈。
    -   `{{ last_hypothesis_and_feedback }}`: 字符串, 最新的历史假设和反馈。
    -   `{{ sota_hypothesis_and_feedback }}`: 字符串，SOTA 方案的假设和反馈。
    -   `{{ experiment_output_format }}`: 字符串，定义了期望 LLM 输出实验设计的格式（通常是 JSON Schema）。
-   **输出格式要求**:
    通常要求为 JSON 格式，具体结构由 `{{ experiment_output_format }}` 定义。可能包含字段如任务描述、主要步骤、所需参数、预期产出等，这些信息将用于构建 `rdagent.core.experiment.Experiment` 对象。
-   **在流程中的位置**:
    通常在 `rdagent.core.proposal.Hypothesis2Experiment` 的子类中被调用（详见 [`learn/core_module.md`](../learn/core_module.md#核心流程抽象类) 中对 `Hypothesis2Experiment` 的描述），紧随假设生成之后，用于将抽象想法具体化为可执行的实验蓝图。
-   **设计说明**:
    -   System Prompt 明确了任务是将假设转化为实验设计。
    -   User Prompt 提供了目标假设和相关的历史上下文，帮助 LLM 理解假设的来源和意义，从而设计出更合理的实验。

这些通用提议组件的提示词为框架提供了一套标准化的方法来构思新的研发方向并将其实验化，是整个自动化研发流程的基础。特定场景下的提示词可能会对这些通用提示词进行定制或扩展。
