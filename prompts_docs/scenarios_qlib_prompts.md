# Qlib (量化金融) 场景提示词

本文档解析定义在 `rdagent/scenarios/qlib/prompts.yaml` 文件中的提示词。这些提示词是为 RD-Agent 在 Qlib 量化金融场景下进行因子挖掘、模型研究和策略优化而量身定制的。它们指导 LLM 理解金融市场的特性、Qlib 平台的使用，并生成符合量化研究范式的假设、实验和反馈。

## 核心提示词与功能

`rdagent/scenarios/qlib/prompts.yaml` 文件包含了多个针对不同阶段的提示词条目：

### 1. 假设生成相关 (`hypothesis_output_format`, `factor_hypothesis_output_format`, `model_hypothesis_specification`, `factor_hypothesis_specification`, `hypothesis_output_format_with_action`)

-   **主要用途**:
    -   指导 LLM 生成针对因子 (Factor) 或模型 (Model) 的研究假设。
    -   提供了非常具体的规范和输出格式要求。
-   **关键输入变量 (通用)**:
    -   `{{ scenario }}`: Qlib 场景的描述，可能包含市场数据特点、目标（如最大化IC值、年化收益等）。
    -   `{{ hypothesis_and_feedback }}` (Jinja loop): 历史的假设、实验任务、回测结果（IC、年化收益、最大回撤）、观察、对假设的评估、决策等。
    -   `{{ last_hypothesis_and_feedback }}`: 最后一次试验的详细信息，包括训练日志，并提示LLM分析训练过程。
    -   `{{ sota_hypothesis_and_feedback }}`: 当前最优（SOTA）方案的详细信息。
    -   `{{ hypothesis_specification }}` (用于 `hypothesis_output_format_with_action`): 额外的假设生成指令。
-   **输出格式要求**:
    -   均要求严格的 JSON 格式。
    -   `hypothesis_output_format`: 通用假设输出，包含 `"hypothesis"` (假设陈述) 和 `"reason"` (理由)。
    -   `factor_hypothesis_output_format`: 因子假设输出，包含 `"hypothesis"` 和 `"reason"`，但针对因子生成场景。
    -   `hypothesis_output_format_with_action`: 包含一个额外的 `"action"` 字段 (`"factor"` 或 `"model"`)，让 LLM 决策下一步是关注因子还是模型，然后是假设和理由。
-   **特定指导 (Specifications)**:
    -   **`model_hypothesis_specification`**: 对模型假设生成的详细指导：
        -   分析历史实验进展，找出先前模型设计的不足（参数、架构、创新性）。
        -   参考 SOTA 和最新实验，可优化或提新想法。
        -   初期可实现简单架构，若多次未达SOTA则探索全新方向。
        -   **核心关注 PyTorch 模型架构** (层配置、激活函数、正则化等)，可对时序数据提出创新转换，但**避免特征处理和优化策略**。
        -   探索自定义架构，力求达到顶级AI会议的创新水平。
    -   **`factor_hypothesis_specification`**: 对因子假设生成的详细指导：
        -   **每次生成1-5个因子**，平衡简单与复杂性，充分利用财务数据。
        -   从简单有效因子开始，简述理由，初期避免复杂组合。
        -   逐步增加复杂性（如机器学习因子、多维原始数据因子），仅在简单因子验证后再组合。
        -   若多次未超越SOTA则转向新方向（可从简单因子开始）。
        -   **注意避免重新实现已在SOTA库中的因子**。
        -   无论生成多少因子，只回复一组假设和理由。
-   **在流程中的位置**:
    -   用于 Qlib 场景下的 `HypothesisGen` 组件，是“R”阶段的核心。
    -   `action_gen` 可能先被调用以确定研发焦点。

### 2. 实验设计相关 (`factor_experiment_output_format`, `model_experiment_output_format`)

-   **主要用途**:
    -   将LLM生成的因子或模型假设，转换为具体的、结构化的实验任务描述。
-   **输出格式要求**:
    -   **`factor_experiment_output_format`**: 要求为每个提出的因子提供一个JSON对象，包含：
        -   `"description"`: 因子描述，以类型开头 (如 `[动量因子]`)。
        -   `"formulation"`: 因子的 LaTeX 数学公式。
        -   `"variables"`: 一个字典，键是因子公式中使用的变量或函数名，值是其描述。
        -   **特别强调**: "此处不要添加省略号(...)或任何可能导致JSON解析错误的填充文本！"
    -   **`model_experiment_output_format`**: 要求为提出的模型（目前限制为一个）提供一个JSON对象，包含：
        -   `"description"`: 模型详细描述。
        -   `"formulation"`: 模型公式的 LaTeX 表示。
        -   `"architecture"`: 模型架构的详细描述 (例如，神经网络层、树结构)。
        -   `"variables"`: 公式中关键变量的描述。
        -   `"hyperparameters"`: 模型特定的超参数及其值。
        -   `"training_hyperparameters"`: 训练相关的超参数 (如 `n_epochs`, `lr`, `early_stop`, `batch_size`, `weight_decay`)，提供了参考值但LLM可修改。
        -   `"model_type"`: "表格型" 或 "时间序列型"。
-   **在流程中的位置**:
    -   用于 Qlib 场景下的 `Hypothesis2Experiment` 组件，将抽象假设转化为可由 `Developer` 实现的实验蓝图。

### 3. 反馈生成相关 (`factor_feedback_generation`, `model_feedback_generation`)

-   **主要用途**:
    -   指导 LLM 在因子或模型实验执行后，分析回测结果、训练日志等，并生成结构化的反馈。
-   **关键输入变量 (通用)**:
    -   `{{ scenario }}`: Qlib场景描述。
    -   `{{ hypothesis_text }}` 或 `{{ hypothesis.hypothesis }}` 和 `{{ hypothesis.reason }}`: 当前实验所验证的假设。
    -   `{{ task_details }}` (因子) 或 `{{ exp.sub_tasks[0].get_task_information() }}` (模型): 具体任务描述。
    -   `{{ combined_result }}` (因子) 或 `{{ exp_result }}` (模型): 当前实验的回测结果。
    -   `{{ sota_result }}`, `{{ sota_hypothesis }}`, `{{ sota_task }}`, `{{ sota_code }}`: SOTA方案的相关信息。
    -   `{{ exp.stdout }}` (模型): 模型的训练日志。
    -   `{{ exp.sub_workspace_list[0].file_dict.get("model.py") }}` (模型): 当前实验的模型代码。
-   **输出格式要求 (JSON)**:
    -   **因子反馈**:
        -   `"Observations"`: 整体观察。
        -   `"Feedback for Hypothesis"`: 对假设的反馈。
        -   `"New Hypothesis"`: 新的假设提议。
        -   `"Reasoning"`: 新假设的理由。
        -   `"Replace Best Result"`: ("是" 或 "否") 是否用当前结果替换SOTA。
    -   **模型反馈**:
        -   `"Observations"`: **首先分析训练日志**，然后总结当前与SOTA结果，限制句数，注重数据。
        -   `"Feedback for Hypothesis"`: 确认或反驳假设，限制句数。
        -   `"New Hypothesis"`: 修订后的假设，限制句数。
        -   `"Reasoning"`: 新假设的依据，限制句数。
        -   `"Decision"`: (true 或 false) 对当前实验路径的布尔决策。
-   **特定指导**:
    -   **因子反馈**:
        -   解释SOTA因子库的运作逻辑（SOTA因子会被保留和组合）。
        -   发展方向可以是新因子方向或优化现有方向（但避免重复实现已入库的SOTA因子）。
        -   任何小的年化收益率改进都应视为替换SOTA。
        -   与SOTA差距大时考虑新方向。
        -   注意因子是否真实现在实验中被测试。
    -   **模型反馈**:
        -   年化收益率改善是替换SOTA的主要标准。
        -   结果明显差于SOTA时考虑改变方向（如模型架构）。
-   **在流程中的位置**:
    -   用于 Qlib 场景下的 `Experiment2Feedback` 组件，在实验执行后生成反馈，完成研发闭环。

### 4. 决策生成 (`action_gen`)

-   **主要用途**: 指导 LLM 分析历史实验，并决策下一个实验迭代是应该专注于因子 (factor) 还是模型 (model)。
-   **角色设定**: "华尔街顶级对冲基金中最权威的定量研究员之一"。
-   **输出格式要求 (JSON)**:
    -   `{ "action": "factor" 或 "model" }`
-   **在流程中的位置**:
    -   可能在每个 R&D 大循环的开始，由更高层次的策略模块调用，以确定本轮迭代的重点是因子挖掘还是模型优化。其输出会影响后续假设生成和实验设计的方向。

## 总结

Qlib 场景的提示词体现了对量化金融领域知识的深度整合。它们不仅指导 LLM 完成通用的假设-实验-反馈循环，还包含了针对因子和模型这两大核心要素的非常具体和专业的生成规范、评估标准和迭代策略。结构化的输入输出（尤其是JSON和LaTeX）以及细致的引导语是确保LLM产出符合量化研究要求的关键。这些提示词的设计使得 RD-Agent 能够更专业、更深入地在量化投资领域进行自动化探索。
