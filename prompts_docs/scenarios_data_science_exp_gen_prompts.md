# 数据科学场景：实验生成 (Experiment Generation) 提示词

本文档解析定义在 `rdagent/scenarios/data_science/proposal/exp_gen/prompts.yaml` 文件中的提示词。这些提示词专门为数据科学（尤其是Kaggle竞赛）场景下的实验生成过程而设计，包括提出假设、设计任务，并指导LLM输出结构化的实验方案。

## 1. `direct_exp_gen` - 直接实验生成 (核心)

-   **源文件路径**: `rdagent/scenarios/data_science/proposal/exp_gen/prompts.yaml` (键: `direct_exp_gen`)
-   **主要用途**:
    这是一个多合一的提示词，指导 LLM 完成以下连续任务：
    1.  **角色扮演**: 扮演世界级数据科学家和机器学习工程师。
    2.  **假设提议 (Hypothesis Proposal)**: 针对当前聚焦的组件 (`{{ component }}`), 结合场景信息、历史实验和用户提供的额外规格说明 (`{{ hypothesis_specification }}`), 生成一个新的、可测试的假设。
    3.  **任务设计 (Task Design)**: 基于上一步生成的假设，设计一个具体的研发任务 (`{{ targets }}`)。任务的范围和接口由 `{{ task_specification }}` 限定。
    4.  **(可选) 工作流更新 (Workflow update)**: 如果 `{{ workflow_check }}` 为真，判断是否需要更新整体工作流，并提供简要描述。
-   **关键输入变量 (Jinja2)**:
    -   `{% include "scenarios.data_science.share:scen.role" %}`: (Jinja include) 可能用于包含一个共享的角色定义片段。
    -   `{{ component }}`: 字符串，当前需要 LLM 重点关注的研发组件 (例如, 'FeatureEng', 'Model')。
    -   `{{ scenario }}`: 字符串，当前Kaggle竞赛或其他数据科学场景的详细描述。
    -   `{{ hypothesis_specification }}`: 字符串，用户或系统提供的关于如何生成假设的额外指导或约束。
    -   `{{ hypothesis_output_format }}`: 字符串 (Jinja include `output_format.hypothesis`)，定义了假设提议部分期望的JSON输出格式。
    -   `{{ targets }}`: 字符串，当前任务设计阶段的目标（例如，"feature engineering task", "model training task"）。
    -   `{{ task_specification }}`: 字符串，描述了当前任务的接口或范围。
    -   `{{ task_output_format }}`: 字符串 (Jinja include `output_format.<target_component>`)，定义了任务设计部分期望的JSON输出格式（根据`targets`动态选择）。
    -   `{{ workflow_check }}`: 布尔值，指示是否需要考虑工作流更新。
    -   `{{ exp_and_feedback_list_desc }}`: 字符串，格式化的历史实验列表及其反馈。
    -   `{{ sota_exp_desc }}`: 字符串，当前最优（SOTA）方案的描述。
    -   `{{ last_exp_diff }}`: (可选) 字符串，最新实现与SOTA实现之间的代码差异 (diff格式)。
-   **输出格式要求**:
    -   整体要求是一个包含三个键的 JSON 对象：`"hypothesis_proposal"`, `"task_design"`, 和可选的 `"workflow_update"`。
    -   `"hypothesis_proposal"` 的值应符合 `{{ hypothesis_output_format }}` 定义的JSON结构。
    -   `"task_design"` 的值应符合 `{{ task_output_format }}` 定义的JSON结构。
    -   `"workflow_update"` 的值是一个简单的文本描述或 "No update needed"。
-   **在流程中的位置**:
    -   是 `DataScienceRDLoop` 中 `direct_exp_gen` 方法的核心驱动。这对应于 [数据科学场景演练文档](../learn/scenario_data_science_walkthrough.md#阶段一提议-proposal-generation---direct_exp_gen-方法) 中描述的“提议”阶段。
    -   在每次迭代开始时被调用，用于生成新的实验方向和具体任务。
-   **设计说明**:
    -   此提示词通过分步指导（Step1: Hypothesis, Step2: Task Design, Step3: Workflow）和明确的格式要求，将复杂的实验生成任务分解，提高了LLM输出的质量和可用性。
    -   包含针对模型任务的特定逻辑，例如在资源受限或模型库已存在表现不佳模型时如何决策。
    -   通过 `{% include %}` 指令复用了定义在同一文件末尾的各种 `output_format` 片段。

## 2. `component_gen` - 组件选择生成

-   **源文件路径**: `rdagent/scenarios/data_science/proposal/exp_gen/prompts.yaml` (键: `component_gen`)
-   **主要用途**:
    指导 LLM 在一次迭代完成后，根据历史实验和反馈，选择下一个最值得优化的组件。
-   **关键输入变量 (Jinja2)**:
    -   `{{ scenario }}`: 当前场景描述。
    -   `{{ sota_exp_desc }}`: SOTA方案描述。
    -   `{{ last_exp_diff }}`: (可选) 最新与SOTA的代码差异。
    -   `{{ component_desc }}`: 字符串，所有可选组件及其简要描述的列表。
    -   `{{ exp_and_feedback_list_desc }}`: 历史实验及反馈。
-   **输出格式要求**:
    -   JSON格式，遵循 `output_format.component` 定义的结构:
        ```json
        {
          "reason": "选择此组件的理由...",
          "component": "选择的组件名称 (如 'DataLoadSpec', 'FeatureEng', 'Model', etc.)"
        }
        ```
-   **在流程中的位置**:
    -   可能在 `DataScienceRDLoop` 的 `direct_exp_gen` 方法内部（作为其决策的一部分），或者由一个更高层次的策略模块调用，用于在 `direct_exp_gen` 提示词执行之前确定 `{{ component }}` 输入变量的值。
    -   其选择结果直接影响后续 `direct_exp_gen` 提示词中针对哪个组件进行假设提议和任务设计。
-   **设计说明**:
    -   要求 LLM 平衡探索（尝试新组件）和利用（优化已知有潜力的组件）。
    -   包含避免连续过多选择同一组件的提示，以防止陷入局部最优。

## 3. 辅助模板片段

此文件中还定义了一些被其他提示词 `{% include %}` 的辅助模板片段：

-   **`exp_and_feedback`**:
    -   用于格式化（最近10条）历史实验及其反馈，以便注入到User Prompt中。包含实验关注的任务、假设内容、观察、对假设的评估、以及决策。
-   **`hypothesis_specification`**:
    -   提供给LLM的关于如何形成一个好的假设的通用指南（精确、可测试、可操作、单一方向、基于SOTA）。
-   **`output_format` (及其子条目如 `component`, `hypothesis`, `data_loader`, `feature`, `model`, `ensemble`, `workflow`, `pipeline`)**:
    -   这是此文件中非常核心的部分，详细定义了各种LLM任务期望输出的JSON格式。每个子条目对应一种特定类型的输出（例如，`output_format.model` 定义了模型任务设计应输出的JSON结构，包括`model_name`, `description`等字段）。这些格式定义是确保LLM输出能被后续程序正确解析和使用的关键。

## 已弃用提示词 (Deprecated)

文件中标记为 `# It is deprecated now, please refer to direct_exp_gen` 的提示词，如 `hypothesis_gen` (此文件内的版本), `hypothesis_model`, `task_gen`, `task_gen_model`，表明它们已被功能更全面的 `direct_exp_gen` 所取代。在理解框架时，可以主要关注 `direct_exp_gen`。

这些提示词共同构成了数据科学场景下自动化实验设计和迭代的核心引擎，通过与LLM的精细交互，驱动整个研发流程。
