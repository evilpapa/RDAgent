.. _data_agent_fin:

=====================
金融数据智能体
=====================


**🤖 自动化量化交易与迭代因子演进**
-------------------------------------------------------------------

📖 背景
~~~~~~~~~~~~~~
在动态的量化交易世界中，**因子** 作为战略工具，使交易者能够利用市场无效性。
这些因子——从简单的指标如市盈率到复杂的模型如贴现现金流——是高精度预测股价的关键。

通过利用这些因子，量化交易者可以开发出复杂的策略，不仅能识别市场模式，还能显著提高交易效率和精度。
系统地分析和应用这些因子的能力是普通交易与真正的战略性市场操纵的区别所在。
这就是 **金融模型智能体** 发挥作用的地方。

🎥 `演示 <https://rdagent.azurewebsites.net/factor_loop>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <div style="display: flex; justify-content: center; align-items: center;">
      <video width="600" controls>
        <source src="https://rdagent.azurewebsites.net/media/65bb598f1372c1857ccbf09b2acf5d55830911625048c03102291098.mp4" type="video/mp4">
        您的浏览器不支持视频标签。
      </video>
    </div>


🌟 介绍
~~~~~~~~~~~~~~~~
在这个场景中，我们的智能体展示了假设生成、知识构建和决策的迭代过程。

它突出了金融因子如何通过持续的反馈和改进而演进。

以下是步骤的增强大纲：

**步骤 1：假设生成 🔍**

- 基于先前的实验分析和领域专业知识，生成并提出初步假设，并附有详尽的推理和财务理由。

**步骤 2：因子创建 ✨**

- 根据假设划分任务。
- 每个任务都涉及开发、定义和实现一个新的金融因子，包括其名称、描述、公式和变量。

**步骤 3：因子实现 👨‍💻**

- 根据描述实现因子代码，像开发人员一样对其进行演进。
- 定量验证新创建的因子。

**步骤 4：使用 Qlib 进行回测 📉**

- 将完整数据集集成到因子实现代码中，并准备因子库。
- 使用 Alpha158 加上新开发的因子和 Qlib 中的 LGBModel 进行回测，以评估新因子的有效性和性能。

+----------------+------------+----------------+----------------------------------------------------+
| 数据集        | 模型      | 因子        | 数据拆分                                         |
+================+============+================+====================================================+
| 沪深300         | LGBModel   | Alpha158 Plus  | +-----------+--------------------------+           |
|                |            |                | | 训练     | 2008-01-01 到 2014-12-31 |           |
|                |            |                | +-----------+--------------------------+           |
|                |            |                | | 验证     | 2015-01-01 到 2016-12-31 |           |
|                |            |                | +-----------+--------------------------+           |
|                |            |                | | 测试      | 2017-01-01 到 2020-08-01 |           |
|                |            |                | +-----------+--------------------------+           |
+----------------+------------+----------------+----------------------------------------------------+


**步骤 5：反馈分析 🔍**

- 分析回测结果以评估性能。
- 采纳反馈以完善假设并改进模型。

**步骤 6：假设完善 ♻️**

- 根据回测的反馈完善假设。
- 重复该过程以不断改进模型。

⚡ 快速开始
~~~~~~~~~~~~~~~~~

请参考 :doc:`../installation_and_configuration` 中的安装部分来准备您的系统依赖。

您可以通过运行以下命令来尝试我们的演示：

- 🐍 创建 Conda 环境

  - 使用 Python 创建一个新的 conda 环境（在我们的 CI 中，3.10 和 3.11 版本经过了充分测试）：

    .. code-block:: sh

          conda create -n rdagent python=3.10

  - 激活环境：

    .. code-block:: sh

        conda activate rdagent

- 📦 安装 RDAgent
  
  - 您可以从 PyPI 安装 RDAgent 包：

    .. code-block:: sh

        pip install rdagent

- 🚀 运行应用程序
    
  - 您可以通过使用以下命令直接运行应用程序：
    
    .. code-block:: sh

        rdagent fin_factor


🛠️ 模块使用
~~~~~~~~~~~~~~~~~~~~~

.. _Env Config: 

- **环境配置**

可以在 `.env` 文件中设置以下环境变量来自定义应用程序的行为：

.. autopydantic_settings:: rdagent.app.qlib_rd_loop.conf.FactorBasePropSetting
    :settings-show-field-summary: False
    :exclude-members: Config

.. autopydantic_settings:: rdagent.components.coder.factor_coder.config.FactorCoSTEERSettings
    :settings-show-field-summary: False
    :members: coder_use_cache, data_folder, data_folder_debug, file_based_execution_timeout, select_method, max_loop, knowledge_base_path, new_knowledge_base_path
    :exclude-members: Config, fail_task_trial_limit, v1_query_former_trace_limit, v1_query_similar_success_limit, v2_query_component_limit, v2_query_error_limit, v2_query_former_trace_limit, v2_error_summary, v2_knowledge_sampler
    :no-index:
