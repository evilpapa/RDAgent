# Qlib 场景：因子实验加载器 (Factor Experiment Loader) 相关提示词

本文档概述定义在 `rdagent/scenarios/qlib/factor_experiment_loader/prompts.yaml` 文件中的提示词。这些提示词用于 Qlib 量化金融场景下，辅助 `FactorExperimentLoader` 组件从非结构化或半结构化文本（如研究报告、论文摘要）中提取因子思想，并将其转换为初步的因子实验定义。

## 提示词概览

-   **源文件路径**: `rdagent/scenarios/qlib/factor_experiment_loader/prompts.yaml`

-   **主要用途**:
    -   **因子思想提取**: 指导 LLM 阅读提供的文本材料（如研报片段），识别并抽取出其中描述的潜在因子构建思路、计算逻辑或关键变量。
    -   **结构化转换**: 将提取出的非结构化因子思想，转换为结构化的表示，通常是为了生成符合 `rdagent/scenarios/qlib/prompts.yaml` 中 `factor_experiment_output_format` 要求的初步因子定义（包含描述、可能的公式雏形、变量等）。
    -   **信息补全与澄清 (可能)**: 如果原始文本信息不完整，提示词可能引导LLM尝试推断缺失信息或提出需要澄清的问题。

-   **关键输入变量 (通用预期)**:
    -   `{{ document_text }}`: 包含因子思想的原始文本内容（例如，研究报告的一段）。
    -   `{{ existing_factors }}`: (可选) 已知的因子列表或知识库中的因子信息，帮助LLM避免重复或进行关联。
    -   `{{ qlib_data_fields }}`: (可选) Qlib平台可用的基础数据字段列表（如 `"$open"`, `"$close"`, `"$volume"`），帮助LLM将因子思想映射到可用数据。
    -   `{{ output_format_specification }}`: 对输出的结构化因子定义的格式要求，可能参考 `factor_experiment_output_format`。

-   **输出格式要求**:
    -   主要是结构化的因子定义，通常是JSON格式，包含因子名称（可能由LLM生成或从文本提取）、描述、初步的公式（可能是自然语言描述或伪代码）、以及识别出的关键变量。
    -   目标是生成可以作为 `FactorCoder` 输入的因子定义。

-   **在流程中的位置**:
    -   当用户提供外部文档（如研报PDF）并希望从中自动挖掘因子时，`FactorExperimentLoader` 组件及其关联的提示词会被调用。
    -   这是因子挖掘流程的一个早期阶段，处于从原始信息到可执行因子代码的中间步骤。其输出通常会传递给更专门的因子假设生成或实验设计流程。

-   **设计说明**:
    -   这类提示词需要LLM具备较强的自然语言理解能力，能够从复杂的金融文本中筛选和提炼核心的因子构建逻辑。
    -   可能需要引导LLM区分真正的因子描述和文本中的背景信息、市场评论等。
    -   由于原始文本的多样性和不规范性，提示词设计需要具有一定的鲁棒性。

**与整体流程的关联**:

`FactorExperimentLoader` 通过这些提示词，实现了从外部知识源（如研报）到内部结构化因子定义的初步转换。这为后续的自动化因子研究（假设生成、实验设计、代码生成、回测评估）提供了有价值的起点，扩展了RD-Agent因子来源的多样性。其输出可以被Qlib场景下的 `HypothesisGen` 或 `Hypothesis2Experiment` 组件进一步处理。
