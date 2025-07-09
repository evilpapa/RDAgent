# RD-Agent 提示词 (Prompts) 文档

欢迎来到 RD-Agent 框架的提示词文档中心！

本文档集合旨在详细解析 RD-Agent 项目中使用的各类提示词 (Prompts)，这些提示词是驱动大语言模型 (LLM) 完成自动化研发任务的核心指令。

## 目的

-   **透明化**: 清晰展示在不同研发阶段和场景下，系统是如何与 LLM 进行交互的。
-   **可理解性**: 帮助开发者和研究人员理解每个提示词的设计目的、输入上下文和期望输出。
-   **可扩展性**: 为二次开发或定制新的研发场景提供参考，了解如何设计有效的提示词。

## 组织结构

本目录下的文档将按照提示词所在的模块或主要功能进行组织。每个 Markdown 文件通常对应一个或一组相关的 `prompts.yaml` 文件。

**主要分类可能包括**:

*   **通用组件提示词 (`rdagent/components/`)**:
    *   [提议组件提示词 (Proposal Prompts)](components_proposal_prompts.md) - `components/proposal/prompts.yaml`
    *   [Coder CoSTEER 通用提示词 (Coder CoSTEER Prompts)](components_coder_costeer_prompts.md) - `components/coder/CoSTEER/prompts.yaml`
    *   [模型编码器提示词 (Model Coder Prompts)](components_coder_model_prompts.md) - `components/coder/model_coder/prompts.yaml`
    *   [数据科学Coder提示词概览 (Data Science Coders Overview)](components_coder_data_science_prompts.md) - 涵盖 `components/coder/data_science/` 下各子组件 (model, feature, workflow, etc.)
    *   [因子编码器提示词 (Factor Coder Prompts)](components_coder_factor_prompts.md) - `components/coder/factor_coder/prompts.yaml`
*   **场景特定提示词 (`rdagent/scenarios/`)**:
    *   **Data Science (Kaggle) 场景**:
        *   [实验生成提示词 (Experiment Generation Prompts)](scenarios_data_science_exp_gen_prompts.md) - `scenarios/data_science/proposal/exp_gen/prompts.yaml`
        *   [开发阶段提示词 (Development Prompts)](scenarios_data_science_dev_prompts.md) - `scenarios/data_science/dev/prompts.yaml`
        *   [运行器提示词 (Runner Prompts)](scenarios_data_science_runner_prompts.md) - `scenarios/data_science/dev/runner/prompts.yaml`
        *   [场景上下文提示词 (Scenario Context Prompts)](scenarios_data_science_scen_prompts.md) - `scenarios/data_science/scen/prompts.yaml`
    *   **Qlib (量化金融) 场景**:
        *   [Qlib 通用提示词 (Qlib General Prompts)](scenarios_qlib_prompts.md) - `scenarios/qlib/prompts.yaml`
        *   [Qlib 实验相关提示词 (Qlib Experiment Prompts)](scenarios_qlib_experiment_prompts.md) - `scenarios/qlib/experiment/prompts.yaml`
        *   [Qlib 因子实验加载器提示词 (Qlib Factor Experiment Loader Prompts)](scenarios_qlib_factor_exp_loader_prompts.md) - `scenarios/qlib/factor_experiment_loader/prompts.yaml`
    *   **General Model (通用模型) 场景**:
        *   [通用模型场景提示词 (General Model Prompts)](scenarios_general_model_prompts.md) - `scenarios/general_model/prompts.yaml`
    *   **Kaggle (旧版或特定) 场景**: (注意与现代Data Science场景的区分和联系)
        *   [Kaggle 通用提示词 (Kaggle General Prompts)](scenarios_kaggle_prompts.md) - `scenarios/kaggle/prompts.yaml`
        *   [Kaggle 实验相关提示词 (Kaggle Experiment Prompts)](scenarios_kaggle_experiment_prompts.md) - `scenarios/kaggle/experiment/prompts.yaml`
        *   [Kaggle 知识管理提示词 (Kaggle Knowledge Management Prompts)](scenarios_kaggle_km_prompts.md) - `scenarios/kaggle/knowledge_management/prompts.yaml`
*   **应用特定提示词 (`rdagent/app/`)**:
    *   [应用层 Qlib R&D 循环提示词 (App Qlib RD Loop Prompts)](app_qlib_rd_loop_prompts.md) - `app/qlib_rd_loop/prompts.yaml`
    *   [应用层 CI 工具提示词 (App CI Prompts)](app_ci_prompts.md) - `app/CI/prompts.yaml`
    *   [应用层通用工具提示词 (App Utils Prompts)](app_utils_prompts.md) - `app/utils/prompts.yaml`
*   **工具类提示词 (`rdagent/utils/`)**:
    *   [工具 Agent 通用模板 (Utils Agent Tpl)](utils_agent_tpl.md) - `utils/agent/tpl.yaml`
    *   [工具层通用提示词 (Utils Prompts)](utils_prompts.md) - `utils/prompts.yaml`

## 如何阅读

每个具体的提示词文档将包含以下关键信息：

-   **源文件路径**: 该提示词定义在项目中的哪个 `.yaml` 文件。
-   **主要用途**: 提示词的目标和作用。
-   **关键输入变量**: Jinja2 模板中使用的主要变量及其含义。
-   **输出格式要求**: 对 LLM 输出格式的说明（如 JSON Schema）。
-   **在流程中的位置**: 该提示词在整体研发流程中的调用时机。这一部分会尽量关联到框架的核心执行流程，例如在 `DataScienceRDLoop` 中的哪个阶段被调用，或者被哪个核心组件（如 `HypothesisGen`, `Developer` 等）使用。
-   **设计说明 (可选)**: 关于该提示词设计的额外注解。

**与框架执行流程的关联**:

这些提示词并非孤立存在，而是深度嵌入在 RD-Agent 的自动化研发循环中。理解一个提示词的最佳方式是结合其在整个框架执行流程中的具体作用。

-   关于**核心框架组件**（如 `EvoAgent`, `Proposal`, `Developer` 等）如何驱动研发流程，请参考 `learn/core_module.md`。
-   关于一个**具体的端到端场景示例**（如Data Science Kaggle竞赛），请参考 `learn/scenario_data_science_walkthrough.md`，其中描述了从提议到反馈的完整循环，各个阶段都可能涉及到此处文档化的提示词。
-   关于RD-Agent中**Prompt工程的一般性原则和技巧**，可以参考 `learn/prompt_engineering_insights.md`。

通过结合阅读 `learn/` 目录下的框架和流程分析文档，以及本 `prompts_docs/` 目录下的具体提示词解析，您将能更全面和深入地理解 RD-Agent 的工作机制。

---
*本提示词文档由 AI 助手辅助生成和整理。*
