# RD-Agent 中的 Prompt 工程观察与技巧

RD-Agent 作为一个基于大语言模型 (LLM) 的自动化研发框架，其核心驱动力之一来自于精心设计的 Prompt。通过分析项目中各模块（尤其是 `components` 和 `scenarios` 下）的 `prompts.yaml` 文件，我们可以总结出一些通用的 Prompt 工程原则和技巧，这对于理解框架行为和进行二次开发都非常有价值。

## 1. 清晰的角色设定 (Role Setting)

很多 Prompt（尤其是在 System Prompt 中）会首先为 LLM设定一个明确的角色。

-   **示例**:
    -   数据科学场景 (`direct_exp_gen`): "You are a world-class data scientist and machine learning engineer..."
    -   Qlib 场景 (`model_feedback_generation`): "You are a professional quantitative analysis assistant in a top hedge fund."
-   **作用**: 角色设定有助于引导 LLM 以特定的知识背景、思考模式和语气风格来完成任务，从而提高输出的专业性和相关性。

## 2. 丰富的上下文供给 (Rich Context Provision)

高质量的 Prompt 通常会向 LLM 提供充足且相关的上下文信息。

-   **类型**:
    -   **场景描述 (`{{ scenario }}`)**: 告知 LLM 当前任务的宏观背景。
    -   **历史实验与反馈 (`{{ hypothesis_and_feedback }}`, `{{ exp_and_feedback_list_desc }}`)**: 让 LLM 从过去的成功和失败中学习，避免重复错误，并进行迭代改进。
    -   **当前SOTA方案 (`{{ sota_hypothesis_and_feedback }}`, `{{ sota_exp_desc }}`)**: 作为当前最优解，供 LLM 参考和尝试超越。
    -   **任务/组件规格 (`{{ hypothesis_specification }}`, `{{ task_specification }}`, `{{ component_desc }}`)**: 明确当前任务的具体要求、接口或约束。
    -   **RAG检索知识 (`{{ RAG }}`)**: (如果启用) 从知识库中检索到的相关信息，辅助 LLM决策。
    -   **当前工作区代码 (`{{ workspace_code }}`)**: 在编码或代码修改任务中，提供现有代码作为基础。
-   **作用**: 上下文越丰富、越相关，LLM 就越能理解任务的细微之处，从而生成更精准、更有价值的输出。

## 3. 结构化输出要求 (Structured Output)

为了方便程序后续解析和使用 LLM 的输出，许多 Prompt (尤其是在复杂任务中) 会要求 LLM 以结构化的格式（主要是 JSON）返回结果。

-   **方法**:
    -   在 Prompt 中明确指出 "The output should follow JSON format. The schema is as follows:"。
    -   提供详细的 JSON Schema 或字段描述 (`{{ xxx_output_format }}`)，说明每个键的含义、数据类型和期望内容。
    -   在 `prompts.yaml` 文件中，通过内嵌的 `output_format` 子部分来定义这些 Schema。
-   **示例 (Data Science - `output_format.hypothesis`)**:
    ```yaml
    # (部分示例)
    # hypothesis: "A concise, testable statement..."
    # reason: "A brief explanation..."
    # concise_reason: "Two-line summary..."
    ```
-   **作用**: 结构化输出使得框架可以稳定地提取 LLM 返回的关键信息，并将其用于后续的逻辑判断、数据存储或传递给其他组件。

## 4. 迭代式反馈与引导 (Iterative Feedback and Guidance)

Prompt 的设计充分考虑了 RD-Agent 的迭代式研发流程。

-   **机制**:
    -   将前几轮的假设、实验代码、运行结果和生成的反馈作为输入，传递给负责生成新假设或新实验方案的 Prompt。
    -   Prompt 会明确指示 LLM 分析这些历史信息，例如：“分析以前的实验，反思每个实验中做出的决策，并考虑为什么决策为 true 的实验成功，而决策为 false 的实验失败。然后，思考如何进一步改进...”
    -   在某些反馈生成 Prompt 中（如 Qlib 的 `factor_feedback_generation`），会直接要求 LLM “建议改进或新方向”。
-   **作用**: 这种设计使得 LLM 能够参与到整个“观察-思考-行动-反思”的闭环中，实现能力的逐步进化。

## 5. 明确的指令、约束与提示 (Clear Instructions, Constraints, and Hints)

为了使 LLM 的输出更符合预期，Prompt 中包含了大量明确的指令、约束和有针对性的提示。

-   **指令示例**:
    -   "如果 hypothesis_specification 概述了您需要遵循的下一步，请确保遵守这些指示。" (强制遵循外部指令)
    -   "请按照以下格式生成输出..." (格式要求)
    -   "避免生成类似任务...以避免同样的错误并提高效率。" (行为规避)
-   **约束示例**:
    -   Qlib 因子生成: "每次生成1-5个因子。"
    -   Qlib 模型生成: "专注于PyTorch模型的架构。不要进行任何特征特定的处理。"
    -   JSON 字段描述中的长度限制或内容要求，如 "通常用两到三句话表述"。
-   **提示示例**:
    -   Data Science 模型生成失败提示: "如果失败是由于超出时间限制或内存约束，请从最小的模型大小开始，或选择具有显著较低时间或空间复杂性的替代算法或方法，而不是使用神经网络。"
    -   Qlib 因子生成: "最初避免复杂或组合因子。" "在对传统模型进行足够的试验后，力求在时间序列建模方面实现可与顶级AI会议...相媲美的创新。"
-   **作用**: 这些细致的引导有助于约束 LLM 的“创造力”在有效范围内，减少不相关或低质量输出的概率，使其行为更符合研发流程的需要。

## 6. 模板引擎的运用 (Template Engine - Jinja2)

所有 Prompt 都以 YAML 格式存储，并大量使用 Jinja2 模板语法（如 `{{ variable }}`, `{% if ... %}`, `{% for ... %}`）。

-   **优势**:
    -   **动态性**: 可以根据程序运行时的具体上下文动态构建 Prompt 内容。
    -   **可重用性**: 可以定义通用的 Prompt 结构，并通过变量填充适应不同情况。
    -   **可维护性**: 将 Prompt 文本与业务逻辑代码分离，便于修改和管理 Prompt。
    -   **条件与循环**: 可以根据条件包含或排除某些 Prompt片段，或循环生成列表信息（如历史实验）。
-   **示例**:
    ```yaml
    # system_prompt: |-
    #   用户正在为数据驱动的研发过程中的 {{ targets }} 生成新的假设。
    #   {{ targets }} 用于以下场景：
    #   {{ scenario }}
    #   {% if hypothesis_specification %}
    #   为了帮助您制定新的假设，用户提供了一些额外信息：{{ hypothesis_specification }}。
    #   {% endif %}
    ```

## 总结

RD-Agent 中的 Prompt 设计是其成功的关键因素之一。通过上述原则和技巧的综合运用，框架能够有效地引导 LLM 在复杂的研发流程中扮演不同角色、处理多样化的任务，并生成符合预期的、可用的输出。对于希望深入理解或扩展 RD-Agent 功能的开发者而言，研究这些 Prompt 的设计思路将大有裨益。
