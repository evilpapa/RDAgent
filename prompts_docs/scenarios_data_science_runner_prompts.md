# 数据科学场景：运行器 (Runner) 相关提示词

本文档解析定义在 `rdagent/scenarios/data_science/dev/runner/prompts.yaml` 文件中的提示词。这些提示词主要供数据科学场景下的 `DSCoSTEERRunner` 组件使用，可能涉及在实验运行前后对代码或环境进行分析、总结或生成必要脚本的场景。

目前，该文件内容如下：

```yaml
summary_code:
  system: |-
    Please provide a concise summary of the Python script. Your summary should be no more than 200 characters.
  user: |-
    {{code}}
```

## 1. `summary_code` - 代码摘要

-   **源文件路径**: `rdagent/scenarios/data_science/dev/runner/prompts.yaml` (键: `summary_code`)
-   **主要用途**:
    指导 LLM 为一段给定的 Python 脚本生成一个简洁的摘要。摘要的长度被限制在200个字符以内。
-   **关键输入变量 (Jinja2)**:
    -   `{{ code }}`: 字符串，包含需要被摘要的 Python 脚本的完整代码内容。
-   **输出格式要求**:
    -   纯文本格式的摘要，内容简洁，不超过200字符。
-   **在流程中的位置**:
    -   此提示词可能被 `DSCoSTEERRunner` 或相关组件在以下几种情况使用：
        -   在执行一个脚本之前，生成一个简短的描述用于日志记录或用户展示。
        -   在分析已有的代码库或实验工作空间时，为其中的脚本文件快速生成摘要信息。
        -   作为更复杂代码理解或文档生成任务的一个子步骤。
-   **设计说明**:
    -   System Prompt 直接明了地给出了任务（生成简洁摘要）和约束（不超过200字符）。
    -   User Prompt 简单地提供了待摘要的代码。
    -   这是一个相对简单和通用的代码处理提示词。

**注意**:

与实验生成 (`exp_gen`) 或开发阶段反馈 (`dev/prompts.yaml`) 中的复杂提示词相比，此文件中的 `summary_code` 提示词功能较为单一和基础。`DSCoSTEERRunner` 的核心功能是执行代码并收集结果，它对LLM的依赖可能更多地体现在解析配置文件、理解执行日志或根据执行结果生成初步报告（如果这些功能也由LLM辅助的话，对应的提示词可能在其他地方或未在此文件中体现）。

如果 `DSCoSTEERRunner` 需要更复杂的与LLM交互的功能（例如，根据代码动态生成执行命令、分析运行时错误并提出修复建议等），则可能会有更复杂的提示词定义。目前来看，这个文件只提供了一个基础的代码摘要功能。
