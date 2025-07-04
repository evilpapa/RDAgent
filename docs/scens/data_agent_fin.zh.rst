.. _data_agent_fin:

=====================
金融数据智能体
=====================


**🤖自动量化交易与因子进化**
-------------------------------------------------------------------

📖 背景
~~~~~~~~~~~~~~
在量化交易领域，**因子**是帮助交易者利用市场无效性的关键工具。这些因子从简单的市盈率到复杂的贴现现金流模型，都是高效预测股价的核心。

通过系统性分析和应用这些因子，量化交易者可开发出复杂策略，提升交易效率与精度。**金融模型智能体**正是为此而生。

🎬 `演示 <https://rdagent.azurewebsites.net/factor_loop>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <div style="display: flex; justify-content: center; align-items: center;">
      <video width="600" controls>
        <source src="https://rdagent.azurewebsites.net/media/65bb598f1372c1857ccbf09b2acf5d55830911625048c03102291098.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>


🌟 场景简介
~~~~~~~~~~~~~~~~
本场景展示了假设生成、知识构建与决策的迭代过程，突出因子如何通过持续反馈与优化不断进化。

主要流程：

**步骤 1：假设生成 🔍**
- 基于实验分析与领域知识提出初步假设。

**步骤 2：因子创建 ✨**
- 拆分任务，开发新因子，包括名称、描述、公式与变量。

**步骤 3：因子实现 👨‍💻**
- 按描述实现因子代码并定量验证。

**步骤 4：Qlib 回测 📉**
- 集成全量数据，准备因子库，使用 Qlib 回测。

+----------------+------------+----------------+----------------------------------------------------+
| 数据集         | 模型       | 因子           | 数据区间                                            |
+================+============+================+====================================================+
| CSI300         | LGBModel   | Alpha158 Plus  | 训练：2008-01-01~2014-12-31，验证：2015-01-01~2016-12-31，测试：2017-01-01~2020-08-01 |
+----------------+------------+----------------+----------------------------------------------------+

**步骤 5：反馈分析 🔍**
- 分析回测结果，优化模型。

**步骤 6：假设优化 ♻️**
- 基于反馈持续优化假设，循环迭代。

⚡ 快速上手
~~~~~~~~~~~~~~~~~

请参考 :doc:`../installation_and_configuration.zh` 完成依赖准备。

- 🐍 创建 Conda 环境
- 📦 安装 RDAgent
- 🚀 运行应用

🛠️ 模块用法
~~~~~~~~~~~~~~~~~~~~~

- **环境变量配置**

.. autopydantic_settings:: rdagent.app.qlib_rd_loop.conf.FactorBasePropSetting
    :settings-show-field-summary: False
    :exclude-members: Config

.. autopydantic_settings:: rdagent.components.coder.factor_coder.config.FactorCoSTEERSettings
    :settings-show-field-summary: False
    :members: coder_use_cache, data_folder, data_folder_debug, file_based_execution_timeout, select_method, max_loop, knowledge_base_path, new_knowledge_base_path
    :exclude-members: Config, fail_task_trial_limit, v1_query_former_trace_limit, v1_query_similar_success_limit, v2_query_component_limit, v2_query_error_limit, v2_query_former_trace_limit, v2_error_summary, v2_knowledge_sampler
    :no-index:

