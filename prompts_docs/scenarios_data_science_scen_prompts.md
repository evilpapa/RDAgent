# 数据科学场景：场景上下文 (Scenario Context) 相关提示词

本文档解析定义在 `rdagent/scenarios/data_science/scen/prompts.yaml` 文件中的提示词。这些提示词主要用于辅助 `DataScienceScen` 类（或其子类）构建和提供场景上下文信息，这些信息随后会被其他核心提示词（如实验生成、反馈分析的提示词）作为输入变量（例如 `{{ scenario }}`）使用。

目前，该文件内容如下：

```yaml
description_gen:
  system: |-
    You are a helpful assistant. You are good at reading the competition description and summarizing the key information.
    Please provide a concise summary of the competition. Your summary should be no more than 200 characters.
  user: |-
    {{comp_desc}}
```

## 1. `description_gen` - 竞赛描述摘要生成

-   **源文件路径**: `rdagent/scenarios/data_science/scen/prompts.yaml` (键: `description_gen`)
-   **主要用途**:
    指导 LLM 阅读一段Kaggle竞赛的描述文本，并为其生成一个简洁的摘要。摘要的长度被限制在200个字符以内。
-   **关键输入变量 (Jinja2)**:
    -   `{{ comp_desc }}`: 字符串，包含Kaggle竞赛的完整描述文本。这通常是从竞赛页面的 "Description" 部分获取的内容。
-   **输出格式要求**:
    -   纯文本格式的摘要，内容简洁，不超过200字符。
-   **在流程中的位置**:
    -   此提示词主要由 `DataScienceScen` 类（定义在 `rdagent/scenarios/data_science/scen/utils.py` 或类似位置的场景实现类）在初始化或准备场景描述时调用。
    -   当 `DataScienceScen` 对象需要为其 `background` 属性或 `get_scenario_all_desc()` 方法准备一部分关于竞赛核心内容的简洁摘要时，可能会使用这个提示词。
    -   生成的摘要随后会成为其他更复杂提示词中 `{{ scenario }}` 变量内容的一部分，帮助其他LLM任务快速把握竞赛主旨。
-   **设计说明**:
    -   System Prompt 为 LLM 设定了“擅长阅读和总结竞赛描述的助手”角色，并给出了明确的长度限制。
    -   User Prompt 直接提供了原始的竞赛描述文本。
    -   这是一个辅助性的提示词，目的是从可能很长的竞赛描述中提取最核心的信息，供后续的Agent使用，避免让核心Agent直接处理过长的原始描述，从而提高效率和聚焦度。

**总结**:

`rdagent/scenarios/data_science/scen/prompts.yaml` 中的提示词（目前只有一个 `description_gen`）主要是为了场景对象 (`DataScienceScen`) 自身服务的，用于预处理和构建其需要向外提供的场景描述信息。这些经过LLM初步摘要或结构化的信息，能够让核心的研发流程中的LLM调用（如实验生成、反馈分析）更加高效和准确。它们是构建高质量 `{{ scenario }}` 上下文变量的幕后助手。
