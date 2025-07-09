# 组件层：因子编码器 (Factor Coder) 相关提示词

本文档概述定义在 `rdagent/components/coder/factor_coder/prompts.yaml` 文件中的提示词。这些提示词主要由通用的因子编码器组件（例如 `FactorCoSTEER` 或类似为量化金融场景设计的因子生成和实现组件）使用，负责根据因子定义（通常包含数学公式和描述）生成可执行的代码。

## 提示词概览

-   **源文件路径**: `rdagent/components/coder/factor_coder/prompts.yaml`

-   **主要用途**:
    -   **代码生成**: 指导 LLM 将一个或多个金融因子（Alpha因子）的抽象定义（例如，数学表达式、文字描述、伪代码）转换为特定量化平台（如Qlib）或通用Python库（如Pandas, NumPy）的可执行代码。
    -   **遵循平台规范**: 确保生成的因子代码符合目标平台的API和数据结构要求（例如，Qlib中的表达式因子或Python函数因子）。
    -   **处理输入数据**: 指导LLM正确使用平台提供的行情数据接口（如开盘价、收盘价、成交量等基础数据字段）。
    -   **优化与健壮性 (可选)**: 可能包含对生成代码的性能、数值稳定性或异常处理的初步要求。

-   **关键输入变量 (通用预期)**:
    -   `{{ factor_definitions }}`: 一个或多个因子的详细定义。每个定义可能包含：
        -   `name`: 因子名称。
        -   `description`: 因子的逻辑或预期行为描述。
        -   `formula`: 因子的数学公式 (可能是LaTeX或伪代码形式)。
        -   `variables`: 公式中使用的变量及其含义（例如，`CLOSE` 代表收盘价，`VWAP` 代表成交量加权平均价）。
    -   `{{ platform_conventions }}`: (可选) 关于目标量化平台的特定编码约定或API使用说明。
    -   `{{ existing_code_examples }}`: (可选) 类似因子的已实现代码示例，供LLM参考。
    -   `{{ output_format_specification }}`: 对输出代码的特定格式或结构要求（例如，是否需要封装在特定类或函数中）。

-   **输出格式要求**:
    -   主要是目标平台（如Qlib）兼容的因子代码，或通用的Python代码。
    -   代码应能直接用于因子计算和后续的回测。
    -   可能伴随对每个因子代码的简要注释或说明。

-   **在流程中的位置**:
    -   当研发流程（尤其是在量化金融场景如Qlib中）涉及到新的因子挖掘和实现时，`FactorCoder` 组件会被调用。
    -   在 `Hypothesis2Experiment` 将一个“挖掘新因子”的假设转换为包含具体因子定义的 `Experiment` 对象后，这些因子定义会传递给 `FactorCoder`。
    -   `FactorCoder` 使用此类提示词与LLM交互，生成因子代码，并更新到实验的工作空间中。

-   **设计说明**:
    -   这些提示词需要准确传达金融因子的计算逻辑，包括对各种金融时间序列操作（如移动平均、相关性、排序、截面操作等）的理解。
    -   对于特定平台（如Qlib），提示词可能需要引导LLM使用平台提供的DSL（领域特定语言）或API。
    -   提示词可能需要处理一次生成多个因子代码的情况。
    -   Qlib场景下的 `rdagent/scenarios/qlib/prompts.yaml` 中的 `factor_experiment_output_format` 定义了因子实验任务的输入格式，这正是因子编码器提示词所要处理的输入。

**与Qlib场景的关联**:

在Qlib场景中，`rdagent/scenarios/qlib/prompts.yaml` 文件中的 `factor_experiment_output_format` 提示词（用于`Hypothesis2Experiment`阶段）会要求LLM输出包含因子描述、LaTeX公式和变量的JSON。这个JSON的输出，正是 `FactorCoder` 组件及其在此处讨论的提示词所接收的输入，用于将其“翻译”成Qlib可执行的因子代码。

**注意**: 此文档提供的是对该路径下提示词用途的通用预期。具体提示词条目和内容需查阅源文件。
