# 组件层：数据科学 Coder 相关提示词 (概览)

本文档概述分布在 `rdagent/components/coder/data_science/` 目录下各子组件（如 `model`, `feature`, `workflow`, `raw_data_loader`, `pipeline`, `ensemble`, `share`）中 `prompts.yaml` 文件的通用目的。

## 提示词分布与主要用途

数据科学场景下的 Coder 组件非常细化，每个组件通常有其专属的 `prompts.yaml` 文件，用于指导 LLM 完成该组件的核心任务。

-   **源文件路径 (示例)**:
    -   `rdagent/components/coder/data_science/model/prompts.yaml`
    -   `rdagent/components/coder/data_science/feature/prompts.yaml`
    -   `rdagent/components/coder/data_science/workflow/prompts.yaml`
    -   `rdagent/components/coder/data_science/raw_data_loader/prompts.yaml`
    -   `rdagent/components/coder/data_science/pipeline/prompts.yaml`
    -   `rdagent/components/coder/data_science/ensemble/prompts.yaml`
    -   `rdagent/components/coder/data_science/share/prompts.yaml` (可能包含共享的提示片段或通用任务)

-   **通用主要用途**:
    -   **代码生成与实现**: 针对数据科学流程中的特定环节（数据加载、特征工程、模型训练、集成、工作流编排、完整流水线构建），根据任务描述（通常来自 `DSExperiment` 对象中的 `Task` 定义）和上下文信息，生成相应的 Python 代码。
    -   **遵循接口与规范**: 确保生成的代码符合预定义的组件接口、数据格式或特定库（如 Pandas, Scikit-learn, PyTorch/TensorFlow）的使用规范。
    -   **代码修改与迭代**: 基于先前尝试的反馈（如错误信息、性能评估、SOTA对比），指导LLM修改或优化已有的代码。
    -   **任务理解与澄清**: (可能) 包含一些用于让LLM确认或澄清模糊任务需求的提示词。
    -   **格式化输出**: 部分提示词可能要求LLM以特定格式（如JSON）输出除了代码之外的元信息，如参数配置、代码解释等。

-   **关键输入变量 (通用预期)**:
    -   `{{ task_description }}` 或 `{{ component_task }}`: 当前组件需要完成的具体任务描述。
    -   `{{ scenario_description }}`: 整体数据科学场景（如Kaggle竞赛）的描述。
    -   `{{ existing_code }}` / `{{ workspace_code }}`: (可选) 当前工作空间中已有的相关代码。
    -   `{{ sota_code }}` / `{{ sota_solution }}`: (可选) 当前最优方案的代码或描述，供参考或改进。
    -   `{{ historical_feedback }}`: (可选) 以往迭代中与此任务或组件相关的反馈。
    -   `{{ data_summary }}` / `{{ feature_list }}`: (可选) 关于数据或特征的统计信息或列表。
    -   `{{ required_imports }}` / `{{ function_signature }}`: (可选) 对生成代码的特定导入或函数签名的要求。

-   **输出格式要求**:
    -   主要输出是Python代码块。
    -   根据具体任务，可能还包括JSON格式的配置文件、参数建议、代码段的文字解释等。

-   **在流程中的位置**:
    -   这些提示词主要被 `DataScienceRDLoop` 的 `coding` 方法中调用的各个 `CoSTEER` Coder 组件（如 `ModelCoSTEER`, `FeatureCoSTEER` 等）使用。
    -   每个Coder组件根据分配到的具体 `Task` 类型，选择并格式化其对应的提示词，然后与LLM交互以生成或修改代码。

-   **设计说明**:
    -   数据科学场景的提示词通常非常注重细节，力求让LLM准确理解数据处理和模型构建的每一步。
    -   提示词会引导LLM使用数据科学领域常用的库和最佳实践。
    -   由于数据科学流程的复杂性和多样性，这些提示词可能具有高度的特化性，以适应不同类型的数据（表格、图像、文本）和任务（分类、回归、聚类）。
    -   `share/prompts.yaml` 可能包含被多个数据科学Coder组件复用的提示片段或通用指令。

**总结**:

`rdagent/components/coder/data_science/` 目录下的提示词是实现自动化数据科学工作流的核心。它们将高层次的实验目标（来自 `DSExperiment` 和 `Task`）分解为具体的编码任务，并指导LLM生成高质量、可执行的代码。理解这些提示词的设计有助于深入把握RD-Agent在数据科学应用中的具体实现方法。

**建议的进一步阅读**:

由于此目录下提示词众多且与具体组件功能紧密相关，建议结合对各个 `CoSTEER` Coder组件（如 `ModelCoSTEER`, `FeatureCoSTEER`）源码的阅读，来具体分析其对应的 `prompts.yaml` 文件，以便更深入地理解提示词是如何驱动代码生成和迭代的。参考 `learn/scenario_data_science_walkthrough.md` 中对这些Coder在流程中作用的描述。
