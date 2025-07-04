.. _model_copilot_general:

======================
通用模型 Copilot
======================

**🤖自动模型研发协作助手**
--------------------------------------------------------

📖 背景
~~~~~~~~~~~~~~
AI 领域论文数量激增，带来大量新模型与方法，但复现与实现难度大。研究者常需从论文中提取关键信息并转化为可用代码，**通用模型 Copilot** 正是为此而生。

🎬 `演示 <https://rdagent.azurewebsites.net/report_model>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <div style="display: flex; justify-content: center; align-items: center;">
      <video width="600" controls>
        <source src="https://rdagent.azurewebsites.net/media/b35f904765b05099b0fcddbebe041a04f4d7bde239657e5fc24bf0cc.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>

🌟 场景简介
~~~~~~~~~~~~~~~~
本场景自动提出假设、构建模型、实现代码、回测并利用反馈持续优化，目标是自动优化 Qlib 指标，发现最优代码。

模型研发 Copilot 场景
~~~~~~~~~~~~~~~~~~~~~~~~~~
**概述**

本演示自动化提取并迭代开发论文模型，确保功能与正确性。支持表格、时序、图等多种数据类型，主要流程包括 Reader 与 Coder 两部分：

1. **Reader**
   - 解析论文，提取模型结构、参数与实现细节。
   - 利用大模型将内容转为结构化信息。

2. **进化 Coder**
   - 将结构化信息转为可执行 PyTorch 代码。
   - 通过进化机制确保张量形状正确，并用样例输入验证。
   - 迭代优化代码以符合论文规范。

**支持数据类型**
- 表格数据
- 时序数据
- 图数据

⚡ 快速上手
~~~~~~~~~~~~~~~~~

请参考 :doc:`../installation_and_configuration.zh` 完成依赖准备。

- 🐍 创建 Conda 环境
- 📦 安装 RDAgent
- 🚀 运行应用

