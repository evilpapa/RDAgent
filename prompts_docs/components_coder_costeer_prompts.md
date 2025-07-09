# 组件层：Coder CoSTEER 通用提示词

本文档解析定义在 `rdagent/components/coder/CoSTEER/prompts.yaml` 文件中的提示词。这些提示词主要用于 CoSTEER (Collaborative System for Task Execution and Evolutionary Refinement) Coder 组件的通用功能，例如任务分析和组件识别。

## 1. `analyze_component_prompt_v1_system` - 分析任务组件

-   **源文件路径**: `rdagent/components/coder/CoSTEER/prompts.yaml` (键: `analyze_component_prompt_v1_system`)
-   **主要用途**:
    指导 LLM 分析一个新的任务描述，并从一个预定义的组件列表中识别出该任务涉及到哪些组件。这有助于框架理解任务的构成，并可能用于后续的任务分派或工作流构建。
-   **关键输入变量 (Jinja2)**:
    -   `{{ all_component_content }}`: 字符串或结构化文本，包含了所有可用组件的列表及其描述。格式通常是 `component_index: component_description`。
-   **输出格式要求**:
    -   严格要求为 JSON 格式。
    -   期望的 JSON 结构示例:
        ```json
        {
            "component_no_list": [0, 2, 5] // 示例：表示任务涉及到索引为0, 2, 5的组件
        }
        ```
        其中 `component_no_list` 是一个包含所识别组件索引的列表。
-   **在流程中的位置**:
    -   此提示词可能在 CoSTEER Coder 接收到一个新的、较复杂的开发任务时被调用。
    -   在正式开始为每个子组件生成代码之前，通过此提示词对任务进行初步的分解和理解。
-   **设计说明**:
    -   这是一个 System Prompt，直接告诉 LLM 其任务是识别组件。
    -   通过提供 `all_component_content`，LLM 获得了所有候选组件的信息。
    -   强制要求 JSON 输出，便于程序直接使用识别结果。
    -   "v1" 后缀可能表示这是该提示词的第一个版本，后续可能会有迭代。

CoSTEER 架构本身强调协作和逐步求精。这类提示词有助于将一个宏观的开发请求（例如“为某个数据集构建一个完整的预测模型”）分解为与框架中已定义组件（如数据加载器、特征处理器、模型训练器、评估器等）相对应的子任务。然后，每个子任务可以由专门的 Coder 或提示词进一步处理。

目前 `rdagent/components/coder/CoSTEER/prompts.yaml` 中只包含这一个提示词。其他更具体的 Coder（如 `ModelCoder`, `FactorCoder`, `DataScience`场景下的各种Coder）会在它们各自的 `prompts.yaml` 文件中定义更专门化的提示词。
