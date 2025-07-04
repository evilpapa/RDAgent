.. _data_copilot_fin:

=====================
金融数据 Copilot
=====================

**🤖自动量化交易与财报因子提取**
-----------------------------------------------------------------

📖 背景
~~~~~~~~~~~~~~
**研究报告**蕴含大量洞见，常揭示潜在因子，有助于量化策略开发。但报告数量庞大，如何高效提取有价值信息成为难题。

与其盲目复现报告因子，不如深入理解其构建逻辑。因子是否捕捉了市场本质？与已有因子有何差异？

因此，亟需系统化框架管理这一流程，**金融数据 Copilot** 应运而生。

🎬 `演示 <https://rdagent.azurewebsites.net/report_factor>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <div style="display: flex; justify-content: center; align-items: center;">
      <video width="600" controls>
        <source src="https://rdagent.azurewebsites.net/media/7b14b2bd3d8771da9cf7eb799b6d96729cec3d35c8d4f68060f3e2fd.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>

🌟 场景简介
~~~~~~~~~~~~~~~~
本场景演示了从财报中提取因子、实现并通过 Qlib 回测分析表现的全过程，持续扩展与优化因子库。

主要流程：

1. 假设生成 🔍
2. 因子创建 ✨
3. 因子实现 👨‍💻
4. Qlib 回测 📉
5. 反馈分析 🔍
6. 假设优化 ♻️

⚡ 快速上手
~~~~~~~~~~~~~~~~~

请参考 :doc:`../installation_and_configuration.zh` 完成依赖准备。

- 🐍 创建 Conda 环境
- 📦 安装 RDAgent
- 🚀 运行应用

🛠️ 模块用法
~~~~~~~~~~~~~~~~~~~~~

- **环境变量配置**

.. autopydantic_settings:: rdagent.app.qlib_rd_loop.conf.FactorFromReportPropSetting
    :settings-show-field-summary: False
    :show-inheritance:
    :exclude-members: Config

.. autopydantic_settings:: rdagent.components.coder.factor_coder.config.FactorCoSTEERSettings
    :settings-show-field-summary: False
    :members: coder_use_cache, data_folder, data_folder_debug, file_based_execution_timeout, select_method, max_loop, knowledge_base_path, new_knowledge_base_path
    :exclude-members: Config, python_bin, fail_task_trial_limit, v1_query_former_trace_limit, v1_query_similar_success_limit, v2_query_component_limit, v2_query_error_limit, v2_query_former_trace_limit, v2_error_summary, v2_knowledge_sampler
    :no-index:

