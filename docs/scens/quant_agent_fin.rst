.. _quant_agent_fin:

=====================
金融量化智能体
=====================


**🥇首个以数据为中心的量化多智能体框架 RD-Agent(Q)**
---------------------------------------------------------------------

R&D-Agent for Quantitative Finance，简称 **RD-Agent(Q)**，是第一个以数据为中心的多智能体框架，旨在通过协调的因子-模型协同优化来自动化量化策略的全栈研发。

您可以通过 `论文 <https://arxiv.org/abs/2505.15155>`_ 了解有关 **RD-Agent(Q)** 的更多详细信息。

⚡ 快速开始
~~~~~~~~~~~~~~~~~

在开始之前，请确保您已正确安装 RD-Agent 并配置了 RD-Agent 的环境。如果您想了解如何安装和配置 RD-Agent，请参阅 `文档 <../installation_and_configuration.html>`_。

然后，您可以通过运行以下命令来运行该框架：

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

        rdagent fin_quant


🛠️ 模块使用
~~~~~~~~~~~~~~~~~~~~~

.. _Env Config: 

- **环境配置**

可以在 `.env` 文件中设置以下环境变量来自定义应用程序的行为：

.. autopydantic_settings:: rdagent.app.qlib_rd_loop.conf.QuantBasePropSetting
    :settings-show-field-summary: False
    :exclude-members: Config

.. autopydantic_settings:: rdagent.components.coder.factor_coder.config.FactorCoSTEERSettings
    :settings-show-field-summary: False
    :members: coder_use_cache, data_folder, data_folder_debug, file_based_execution_timeout, select_method, max_loop, knowledge_base_path, new_knowledge_base_path
    :exclude-members: Config, fail_task_trial_limit, v1_query_former_trace_limit, v1_query_similar_success_limit, v2_query_component_limit, v2_query_error_limit, v2_query_former_trace_limit, v2_error_summary, v2_knowledge_sampler
    :no-index:

- **Qlib 配置**
    - `model_template` 和 `factor_template` 目录中的 `.yaml` 文件包含在 Qlib 框架内运行相应模型或因子的一些配置。以下是其内容和角色的概述：
        - **通用设置**：
            - **provider_uri**：指定本地 Qlib 数据路径，设置为 `~/.qlib/qlib_data/cn_data`。
            - **market**：配置为 `csi300`，代表沪深 300 指数成分股。
            - **benchmark**：设置为 `SH000300`，用于回测评估。
        
        - **数据处理**：
            - **start_time** 和 **end_time**：定义完整的数据范围，从 `2008-01-01` 到 `2022-08-01`。
            - **fit_start_time**：拟合模型的开始日期，设置为 `2008-01-01`。
            - **fit_end_time**：拟合模型的结束日期，设置为 `2014-12-31`。
            - **features 和 labels**：通过一个嵌套的数据加载器生成，该加载器结合了 `Alpha158DL`（用于工程特征，如 `RESI5`、`WVMA5`、`RSQR5`、`KLEN` 等）和一个加载预计算因子文件（`combined_factors_df.parquet`）的 `StaticDataLoader`。
            - **normalization**：该管道包括用于推理的 `RobustZScoreNorm`（带剪裁）和 `Fillna`，以及用于训练的 `DropnaLabel` 和 `CSZScoreNorm`。
        
        - **训练配置**：
            - **Model**：使用 `GeneralPTNN`，一个基于 PyTorch 的神经网络模型。
            - **数据集拆分**：
                - **train**：`2008-01-01` 到 `2014-12-31`
                - **valid**：`2015-01-01` 到 `2016-12-31`
                - **test**：`2017-01-01` 到 `2020-08-01`

        - **默认超参数**（可由命令行参数覆盖）：
            - **n_epochs**：`100`
            - **lr**：`2e-4`
            - **early_stop**：`10`
            - **batch_size**：`256`
            - **weight_decay**：`0.0`
            - **metric**：`loss`
            - **loss**：`mse`
            - **n_jobs**：`20`
            - **GPU**：`0`（如果可用，则使用 GPU 0）
            
        - **回测和评估**：
            - **strategy**：`TopkDropoutStrategy`，选择前 50 只股票并随机丢弃 5 只以引入探索。
            - **backtest period**：`2017-01-01` 到 `2020-08-01`
            - **initial capital**：`100,000,000`
            - **cost configuration**：包括开/平仓成本、最低交易成本和滑点控制。
            
        - **记录和分析**：
            - **SignalRecord**：记录预测信号。
            - **SigAnaRecord**：执行信号分析，不进行多空分离。
            - **PortAnaRecord**：使用配置的策略和回测设置进行投资组合分析。
