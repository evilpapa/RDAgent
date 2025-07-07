.. _model_agent_fin:

=======================
金融模型智能体
=======================

**🤖自动量化交易与模型进化**
------------------------------------------------------------------------------------------

📖 背景
~~~~~~~~~~~~~~
在量化金融领域，因子发现与模型开发同等重要。虽然因子的发现备受关注，但模型的作用同样关键。策略效果不仅取决于因子，还取决于模型的集成与优化。

模型开发与优化过程复杂且需持续迭代，**金融模型智能体**正是为此而生。

🎬 `演示 <https://rdagent.azurewebsites.net/model_loop>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <div style="display: flex; justify-content: center; align-items: center;">
      <video width="600" controls>
        <source src="https://rdagent.azurewebsites.net/media/d85e8cab1da1cd3501d69ce837452f53a971a24911eae7bfa9237137.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>

🌟 场景简介
~~~~~~~~~~~~~~~~
本场景自动提出假设、构建模型、实现代码、回测并利用反馈持续优化，目标是自动优化 Qlib 指标，发现最优代码。

主要流程：

1. 假设生成 🔍
2. 模型创建 ✨
3. 模型实现 👨‍💻
4. Qlib 回测 📉
5. 反馈分析 🔍
6. 假设优化 ♻️

⚡ 快速上手
~~~~~~~~~~~~~~~~~

请参考 :doc:`../installation_and_configuration` 完成依赖准备。

- 🐍 创建 Conda 环境
- 📦 安装 RDAgent
- 🚀 运行应用

🛠️ 模块用法
~~~~~~~~~~~~~~~~~~~~~

- **环境变量配置**

.. autopydantic_settings:: rdagent.app.qlib_rd_loop.conf.ModelBasePropSetting
    :settings-show-field-summary: False
    :exclude-members: Config

- **Qlib 配置**
    - `model_template` 文件夹下的 `config.yaml` 包含模型运行所需配置，包括市场、特征、数据区间、超参数等。

