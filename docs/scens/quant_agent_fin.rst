.. _quant_agent_fin:

=====================
金融量化智能体
=====================


**🥇首个数据驱动量化多智能体框架 RD-Agent(Q)**
---------------------------------------------------------------------

RD-Agent for Quantitative Finance，简称 **RD-Agent(Q)**，是首个数据驱动、面向量化策略全流程自动化的多智能体框架，实现因子-模型协同优化。

详细介绍可参考 `论文 <https://arxiv.org/abs/2505.15155>`_。

⚡ 快速上手
~~~~~~~~~~~~~~~~~

在开始前，请确保已正确安装并配置 RD-Agent。安装与配置方法请参考 `文档 <../installation_and_configuration.html>`_。

然后可通过以下命令运行框架：

- 🐍 创建 Conda 环境

  - 新建 conda 环境（推荐 Python 3.10/3.11）：

    .. code-block:: sh

          conda create -n rdagent python=3.10

  - 激活环境：

    .. code-block:: sh

        conda activate rdagent

- 📦 安装 RDAgent
  
  - 通过 PyPI 安装 RDAgent 包：

    .. code-block:: sh

        pip install rdagent

- 🚀 运行应用
    
  - 直接运行应用：
    
    .. code-block:: sh

        rdagent fin_quant


🛠️ 模块用法
~~~~~~~~~~~~~~~~~~~~~

.. _Env Config: 

- **环境变量配置**

可在 `.env` 文件中设置以下环境变量自定义应用行为：

.. autopydantic_settings:: rdagent.app.qlib_rd_loop.conf.QuantBasePropSetting
    :settings-show-field-summary: False
    :exclude-members: Config

.. autopydantic_settings:: rdagent.components.coder.factor_coder.config.FactorCoSTEERSettings
    :settings-show-field-summary: False
    :members: coder_use_cache, data_folder, data_folder_debug, file_based_execution_timeout, select_method, max_loop, knowledge_base_path, new_knowledge_base_path
    :exclude-members: Config, fail_task_trial_limit, v1_query_former_trace_limit, v1_query_similar_success_limit, v2_query_component_limit, v2_query_error_limit, v2_query_former_trace_limit, v2_error_summary, v2_knowledge_sampler
    :no-index:

- **Qlib 配置**
    - `model_template` 和 `factor_template` 目录下的 `.yaml` 文件包含 Qlib 运行所需配置。主要内容包括：
        - **provider_uri**：本地 Qlib 数据路径，默认为 `~/.qlib/qlib_data/cn_data`。
        - **market**：市场，配置为 `csi300`。
        - **benchmark**：回测基准，配置为 `SH000300`。
        
        - **数据处理**：
            - **start_time/end_time**：数据区间。
            - **fit_start_time/fit_end_time**：模型拟合区间。
            - **features/labels**：特征与标签生成方式。
            - **normalization**：归一化与缺失值处理。
        
        - **训练配置**：
            - **模型**：如 `GeneralPTNN`。
            - **数据集划分**：训练/验证/测试区间。
            - **超参数**：如 n_epochs、lr、batch_size 等。
        
        - **回测与评估**：
            - **策略**：如 `TopkDropoutStrategy`。
            - **回测区间、初始资金、成本配置**。
        
        - **记录与分析**：
            - **SignalRecord/SigAnaRecord/PortAnaRecord**。

