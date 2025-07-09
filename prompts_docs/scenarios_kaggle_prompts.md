# Kaggle (旧版/特定) 场景：通用提示词

本文档概述定义在 `rdagent/scenarios/kaggle/prompts.yaml` 文件中的提示词。这些提示词为RD-Agent在（可能是旧版或特定配置的）Kaggle竞赛场景下提供通用的指导。

**重要说明**: RD-Agent项目同时存在一个更现代且功能更丰富的“Data Science”场景（其提示词位于 `rdagent/scenarios/data_science/`下），该场景也主要针对Kaggle竞赛。因此，在理解 `rdagent/scenarios/kaggle/prompts.yaml` 时，需注意它与“Data Science”场景提示词之间的可能区别、联系或版本迭代关系。此处的“Kaggle场景”可能指一个较早的实现或一个与Data Science场景并存但有不同侧重点的配置。

## 提示词概览 (通用预期)

-   **源文件路径**: `rdagent/scenarios/kaggle/prompts.yaml`

-   **主要用途 (基于通用Kaggle竞赛流程的推测)**:
    -   **任务理解与规划**: 指导 LLM 理解特定Kaggle竞赛的目标、评估指标、数据特点，并可能生成初步的解决思路或高层计划。
    -   **数据探索与预处理建议**: 针对竞赛数据，让 LLM 提出数据探索步骤、可视化想法、以及数据清洗和预处理策略。
    -   **特征工程想法**: 引导 LLM 基于数据特性和竞赛目标，构思新的特征。
    -   **模型选择建议**: 根据任务类型（分类、回归等）和数据规模，推荐合适的模型类别或具体模型。
    -   **代码片段生成/补全**: (可能) 为上述某些步骤（如特定特征的计算、简单模型的训练代码框架）生成代码片段。
    -   **结果分析与迭代方向**: 分析模型在验证集上的表现，或对照排行榜，提出下一步的改进方向。

-   **关键输入变量 (通用预期)**:
    -   `{{ competition_description }}`: Kaggle竞赛的官方描述文本。
    -   `{{ data_files_summary }}`: 训练集、测试集等数据文件的基本信息（如列名、数据类型、缺失值统计等）。
    -   `{{ evaluation_metric }}`: 竞赛的官方评估指标。
    -   `{{ current_solution_code }}`: (可选) 当前已有的解决方案代码。
    -   `{{ leaderboard_status }}`: (可选) 当前在排行榜上的位置或与SOTA方案的差距。
    -   `{{ previous_attempts_feedback }}`: (可选) 以往提交或实验的反馈。

-   **输出格式要求**:
    -   可能是自然语言的分析、建议、计划。
    -   也可能包含结构化的输出（如JSON格式的特征列表、模型参数建议）或代码片段。

-   **在流程中的位置**:
    -   这些提示词可能被一个专门的 `KaggleRDLoop` 或类似的Kaggle场景控制器在研发流程的各个阶段调用。
    -   与 `DataScienceRDLoop` 中的 `direct_exp_gen` 和 `exp_feedback` 等核心提示词相比，这里的提示词功能划分可能不同，或者更侧重于人机协作中的“建议”和“分析”而非完全自动化的端到端执行。

-   **设计说明**:
    -   提示词设计需要平衡LLM的创造性与Kaggle竞赛的实用性。
    -   可能需要引导LLM关注竞赛的限制（如时间限制、提交通用格式）。

**与Data Science场景的关系**:

建议在深入研究这些提示词时，与 `prompts_docs/scenarios_data_science_*.md` 系列文档进行对比阅读。这有助于理解：
1.  两个场景在功能上是否有重叠。
2.  `scenarios/kaggle/prompts.yaml` 是否为 `scenarios/data_science/` 下提示词的早期版本或一个不同的分支。
3.  它们在自动化程度、LLM扮演的角色、以及与框架其他组件（如Coder、Runner）的交互方式上是否存在差异。

**注意**: 此文档提供的是对该路径下提示词用途的通用预期。具体提示词条目和内容需查阅源文件。
