# Qlib 场景：实验 (Experiment) 相关提示词

本文档概述定义在 `rdagent/scenarios/qlib/experiment/prompts.yaml` 文件中的提示词。这些提示词专门用于 Qlib 量化金融场景下，辅助处理与整个实验（Experiment）级别相关的任务，例如实验的总结、比较或从实验结果中提取关键信息。

## 提示词概览

-   **源文件路径**: `rdagent/scenarios/qlib/experiment/prompts.yaml`

-   **主要用途**:
    -   **实验结果解析与总结**: 指导 LLM 分析 Qlib 实验运行后产生的复杂结果（例如，包含多个回测指标的报告、图表数据的文本表示），并提取关键性能指标或生成人类可读的摘要。
    -   **实验对比**: (可能) 包含用于比较不同实验（例如，当前实验与SOTA实验）性能差异的提示词。
    -   **元数据提取**: 从实验配置或结果中提取重要的元数据，用于记录或指导后续决策。
    -   **失败分析 (初步)**: (可能) 对失败的实验运行（基于日志或错误信息），进行初步的原因分析。

-   **关键输入变量 (通用预期)**:
    -   `{{ qlib_report }}`: Qlib实验运行后生成的详细性能报告（可能是文本格式或结构化数据）。
    -   `{{ experiment_configuration }}`: 当前实验的配置信息（例如，模型参数、因子列表、回测周期）。
    -   `{{ experiment_logs }}`: (可选) 实验运行过程中的日志文件内容。
    -   `{{ sota_experiment_summary }}`: (可选) 当前SOTA实验的摘要或关键指标，用于对比。

-   **输出格式要求**:
    -   可能是结构化的JSON（例如，提取的关键指标键值对）。
    -   也可能是自然语言的文本摘要。
    -   具体格式取决于提示词条目的具体设计。

-   **在流程中的位置**:
    -   这些提示词可能在 Qlib 场景的 `Experiment2Feedback` 组件中被使用，作为生成最终 `ExperimentFeedback` 的一部分。
    -   也可能被用于实验结果的展示、记录或在 `Trace` 对象中存储更结构化的实验信息。

-   **设计说明**:
    -   Qlib 的实验结果通常包含丰富的金融特定指标（IC, IR, Annualized Return, Max Drawdown, Rank IC等），提示词需要引导LLM正确理解和处理这些指标。
    -   提示词可能需要处理从Qlib生成的特定格式（如 ` flera` DataFrame的文本表示）中提取信息。
    -   与 `rdagent/scenarios/qlib/prompts.yaml` 中的反馈生成提示词（`factor_feedback_generation`, `model_feedback_generation`）相比，这里的提示词可能更侧重于对整个实验输出的通用性处理，而不是直接针对假设进行评估和提出新假设。

**注意**: 此文档提供的是对该路径下提示词用途的通用预期。具体提示词条目和内容需查阅源文件。例如，一个具体的提示词可能是“请从以下Qlib回测报告中提取年化收益率、最大回撤和IC均值”。
