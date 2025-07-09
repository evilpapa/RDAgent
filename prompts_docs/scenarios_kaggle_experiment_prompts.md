# Kaggle (旧版/特定) 场景：实验 (Experiment) 相关提示词

本文档概述定义在 `rdagent/scenarios/kaggle/experiment/prompts.yaml` 文件中的提示词。这些提示词专门用于处理RD-Agent在（可能是旧版或特定配置的）Kaggle竞赛场景下，与单个实验（Experiment）相关的具体任务。

**重要说明**: 请参考 `prompts_docs/scenarios_kaggle_prompts.md` 中关于此Kaggle场景与现代“Data Science”场景关系的说明。此处的“实验”相关提示词可能与 `rdagent/scenarios/data_science/experiment/` 或 `rdagent/scenarios/data_science/proposal/exp_gen/` 下的提示词在功能或设计上有所不同。

## 提示词概览 (通用预期)

-   **源文件路径**: `rdagent/scenarios/kaggle/experiment/prompts.yaml`

-   **主要用途 (基于通用Kaggle实验流程的推测)**:
    -   **实验设计细化**: 将一个高层次的实验想法（可能来自 `rdagent/scenarios/kaggle/prompts.yaml` 中的通用规划提示词）细化为更具体的实验步骤、参数配置或代码实现要点。
    -   **实验代码生成/修改**: 针对实验中的特定部分（如某个模型的训练脚本、特定特征的处理函数），指导LLM生成或修改代码。
    -   **结果记录与格式化**: (可能) 包含用于将实验运行的原始输出（如日志、指标）转换为结构化记录或标准提交格式的提示词。
    -   **实验复现性检查**: (可能) 引导LLM分析实验设置和代码，以评估其复现性，或生成用于复现的说明。

-   **关键输入变量 (通用预期)**:
    -   `{{ experiment_idea }}`: 对当前实验核心想法的描述。
    -   `{{ task_type }}`: 实验任务的类型（例如，“model_training”, “feature_generation”, “submission_creation”）。
    -   `{{ input_data_description }}`: 实验所用输入数据的描述。
    -   `{{ specific_parameters }}`: (可选) 用户或先前步骤指定的实验参数。
    -   `{{ code_template_or_existing }}`: (可选) 用于生成或修改代码的代码模板或现有代码。
    -   `{{ raw_results }}`: (可选) 实验运行后的原始结果数据。

-   **输出格式要求**:
    -   可能是具体的代码块、配置文件内容、JSON格式的实验记录，或步骤化的操作指南。

-   **在流程中的位置**:
    -   这些提示词可能在一个Kaggle场景特定的 `Experiment` 类或其关联的 `Developer` / `Runner` 组件内部被调用。
    -   用于处理从实验概念到具体实现，再到结果整理的各个环节。

-   **设计说明**:
    -   可能更侧重于实验执行的具体细节，而非高层次的策略生成。
    -   提示词需要能处理Kaggle竞赛中常见的各种任务类型和数据模态。

**对比与进一步分析**:

为了更准确地理解这些提示词的作用，建议：
1.  直接阅读 `rdagent/scenarios/kaggle/experiment/prompts.yaml` 的源文件内容。
2.  查找这些提示词在 `rdagent/scenarios/kaggle/` 目录下其他Python代码（如可能的 `developer.py`, `experiment.py` 或 `loop.py` 实现）中的调用位置。
3.  与 `DataScience` 场景下对应的实验处理提示词（如 `rdagent/scenarios/data_science/proposal/exp_gen/prompts.yaml` 中的 `direct_exp_gen` 的任务设计部分，或 `rdagent/scenarios/data_science/dev/prompts.yaml` 中的 `exp_feedback`）进行比较，找出其独特之处。

**注意**: 此文档提供的是对该路径下提示词用途的通用预期。具体提示词条目和内容需查阅源文件。
