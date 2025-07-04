.. _data_science_agent:

=======================
数据科学智能体
=======================

**🤖自动特征工程与模型调优进化**
------------------------------------------------------------------------------------------
数据科学智能体可自动完成特征工程与模型调优，适用于图像分类、时序预测、文本分类等多种数据科学任务。

🧑‍💻 示例指南
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 🛠️ **环境准备**

  - 请确保已正确安装并配置 RD-Agent。安装与配置方法请参考 `文档 <../installation_and_configuration.zh.html>`_。

- ⚙️ **.env 文件环境变量设置**

  - 设置数据存储路径并写入 ``.env`` 文件。

  .. code-block:: sh

    dotenv set DS_LOCAL_DATA_PATH <你的本地目录>/ds_data
    dotenv set DS_SCEN rdagent.scenarios.data_science.scen.DataScienceScen

- 📦 **准备竞赛数据**

  - 竞赛数据通常包含描述文件、数据集和评测脚本。可参考 ``rdagent/scenarios/data_science/example``。

    - **目录结构示例**

      .. code-block:: text

        ds_data
        └── eval
        |   └── custom_data
        |       ├── grade.py
        |       ├── valid.py
        |       └── test.csv
        └── custom_data
            ├── train.csv
            ├── test.csv
            ├── sample_submission.csv
            ├── description.md
            └── sample.py

- 🛠️ **自定义数据集环境变量设置**

  .. code-block:: sh

      dotenv set DS_SCEN rdagent.scenarios.data_science.scen.DataScienceScen
      dotenv set DS_LOCAL_DATA_PATH rdagent/scenarios/data_science/example
      dotenv set DS_IF_USING_MLE_DATA False
      dotenv set DS_CODER_ON_WHOLE_PIPELINE True
      dotenv set DS_CODER_COSTEER_ENV_TYPE docker

- 🚀 **运行应用**

  .. code-block:: sh

      rdagent data_science --competition <竞赛ID>

  .. code-block:: sh

      dotenv run -- python rdagent/log/mle_summary.py grade <日志路径>

- 📊 **可视化研发流程**

  .. code-block:: sh

      streamlit run rdagent/log/ui/dsapp.py

- 🏆 **MLE-bench 指南**

  - MLE-bench 是用于评测 AI 系统 ML 工程能力的基准，包含 75 个 Kaggle 竞赛。
  - 设置 ``DS_IF_USING_MLE_DATA`` 为 True 可自动下载数据。
  - 需配置 Kaggle API。

- ⚙️ **MLE-bench 环境变量设置**

  .. code-block:: sh

      dotenv set DS_LOCAL_DATA_PATH <你的本地目录>/ds_data
      dotenv set DS_IF_USING_MLE_DATA True

- ⚙️ **运行环境配置**

  .. code-block:: sh

      dotenv set DS_CODER_COSTEER_ENV_TYPE docker

- 🚀 **运行应用**

  .. code-block:: sh

      rdagent data_science --competition <竞赛ID>

- 📊 **可视化研发流程**

  .. code-block:: sh

      streamlit run rdagent/log/ui/dsapp.py

- **更多说明**

  - 可在研发阶段组合不同 LLM 模型。
  - 通过设置 ``LITELLM_CHAT_MODEL_MAP`` 环境变量自定义开发阶段模型。

