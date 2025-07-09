# 数据科学场景：开发阶段 (Development) 提示词

本文档解析定义在 `rdagent/scenarios/data_science/dev/prompts.yaml` 文件中的提示词。这些提示词主要用于数据科学（Kaggle竞赛）场景的“开发”后期阶段，特别是实验运行后的结果分析和反馈生成。

## 1. `exp_feedback` - 实验反馈生成

-   **源文件路径**: `rdagent/scenarios/data_science/dev/prompts.yaml` (键: `exp_feedback`)
-   **主要用途**:
    指导 LLM 对一个已执行完毕的数据科学实验进行全面分析，并生成结构化的反馈。这个反馈对于评估实验效果、验证假设、以及决定是否将当前实验结果采纳为新的SOTA (State-of-the-Art)至关重要。
-   **核心分析逻辑 (System Prompt中定义)**:
    LLM被要求遵循一个详细的多步骤分析过程：
    1.  **验证提交格式 (Submission Format Check)**:
        -   检查实验输出（如 `submission.csv`）是否符合竞赛要求的格式。
        -   如果格式错误，则明确指出问题、推荐纠正措施，并将 `"Replace Best Result"` 设为 `"no"`。反馈的 `reasoning` 以 `[Submission format error]` 开头。
        -   如果格式正确且是首次有效提交，则将 `"Replace Best Result"` 设为 `"yes"`。
    2.  **评估与竞赛要求的对齐情况 (Evaluation Alignment Check)**: (仅当格式正确时)
        -   分析实验设置和代码，判断是否存在可能导致验证集和测试集表现不一致的因素（例如，验证指标与官方不符、数据处理不一致、数据泄漏、易过拟合的策略等）。
        -   要求严格对照 `{{ scenario }}` 中定义的评估规则。
        -   如果发现不一致或结构性风险，需在 `Reasoning` 中记录（引用场景描述和代码，而非仅凭验证分数），将 `"Evaluation Aligned With Task"` 设为 `"no"`，`"Replace Best Result"` 设为 `"no"`。反馈的 `reasoning` 以 `[Evaluation error]` 开头。
    3.  **分析实验结果 (Experiment Result Analysis)**: (仅当格式和评估对齐均正确时)
        -   将当前实验的集成 (`ensemble`) 验证分数与SOTA的集成验证分数进行比较。
        -   根据比较结果（显著低于SOTA、显著高于SOTA）初步决定 `"Replace Best Result"` 的值。反馈的 `reasoning` 以 `[Experiment Analysis]` 开头。
        -   提示LLM注意，实验重点是最终集成结果，即使个别模型表现不佳或集成结果未超过最佳单模型，只要整体优于SOTA即可。
    4.  **分析代码质量 (Code Analysis - 当验证结果与SOTA相似时)**:
        -   如果当前集成验证分数与SOTA相似，则需要进一步比较代码质量来决定是否替换SOTA。
        -   比较标准包括：潜在过拟合风险、数据泄漏、是否使用最佳实践和高效建模技术、可解释性与领域知识对齐、资源效率（时间空间复杂度）。
        -   要求提供详细的代码分析，并在 `reasoning` 中以 `[Code Analysis]` 开头说明当前代码优于或劣于SOTA的原因。
-   **关键输入变量 (Jinja2 - User Prompt中)**:
    -   `{{ scenario }}`: 当前Kaggle竞赛场景的详细描述。
    -   `{{ sota_desc }}`: 当前SOTA解决方案的描述（可能包括代码摘要、性能结果等）。
    -   `{{ cur_exp }}`: 当前已执行完毕的 `DSExperiment` 对象。LLM可以从中获取：
        -   `cur_exp.pending_tasks_list[0][0].get_task_information()`: 当前实验关注的任务信息。
        -   `cur_exp.hypothesis`: 驱动当前实验的假设。
        -   `cur_exp.experiment_workspace.all_codes`: 当前实验的完整代码。
        -   `cur_exp.result`: 当前实验的运行结果（例如，包含各模型分数和集成模型分数的表格或字典）。
        -   `cur_exp.format_check_result`: (可选) 提交格式的检查结果。
    -   `{{ diff_edition }}`: (可选) 当前实验代码与SOTA方案代码的差异（diff格式）。
    -   `{{ cur_vs_sota_score }}`: (可选) 当前集成性能与SOTA结果的直接比较描述。
    -   `{{ feedback_desc }}`: 格式化的过去实验的反馈历史。
-   **输出格式要求**:
    -   严格要求为 JSON 格式。
    -   JSON Schema 示例（在System Prompt中提供）包含以下关键字段：
        -   `"Submission Format Check"`: ("yes" 或 "no")
        -   `"First Valid Submission"`: ("yes" 或 "no")
        -   `"Code Change Summary"`: (字符串) 对本次实验代码变更的总结。
        -   `"Observations"`: (字符串) 对当前和SOTA集成结果分数的总结和模式观察（限制句数，强调数据驱动）。
        -   `"Feedback for Hypothesis"`: (字符串) 对最初假设的确认或否定（限制句数）。
        -   `"Evaluation Aligned With Task"`: ("yes" 或 "no")
        -   `"Replace Best Result"`: ("yes" 或 "no")，核心决策：是否用当前结果替换SOTA。
        -   `"Reasoning"`: (字符串) 详细解释做出上述决策的原因，需按问题步骤以特定标记开头（如 `[Submission format error]`）。
-   **在流程中的位置**:
    -   在 `DataScienceRDLoop` 的 `feedback` 方法中被调用，通常由 `DSExperiment2Feedback` 组件（或类似角色的类）使用。
    -   在实验代码执行完成 (`running` 阶段) 之后，用于对实验结果进行深入分析和评估，生成指导后续迭代的反馈。这对应于 [数据科学场景演练文档](../learn/scenario_data_science_walkthrough.md#阶段四反馈-feedback-generation---feedback-方法) 中描述的“反馈”阶段。
-   **设计说明**:
    -   这是一个高度结构化和逻辑严谨的提示词，通过多步骤引导LLM进行细致的分析和决策。
    -   强调证据驱动的分析，要求LLM引用场景描述、代码实现或具体分数来支持其判断，而不仅仅是主观臆断。
    -   通过明确的输出JSON结构和各字段的填写指南，确保了反馈信息的全面性和可用性。
    -   对代码质量的考量（在性能相似时）体现了对解决方案鲁棒性和工程实践的重视。

此 `exp_feedback` 提示词是数据科学场景实现自动化评估和迭代优化的关键环节，它将原始的实验产出（代码、日志、分数）转化为机器可理解的、能驱动下一步行动的结构化知识。
