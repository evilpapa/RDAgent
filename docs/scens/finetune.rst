.. _finetune_agent:

=============================
微调现有模型
=============================

## **🎯 场景：在预训练模型上继续训练**

在此工作流程中，**数据科学智能体** 从一个 *先前训练过* 的模型（及其训练脚本）开始，对新数据执行额外的微调，然后重新使用更新后的权重进行后续的推理运行。

🚧 目录结构

您的竞赛文件夹（此处称为 ``custom_data``）必须包含一个名为 ``prev_model`` 的 **额外子目录**，您可以在其中保留旧权重和生成它们的代码：

.. code-block:: text

   ds_data
   └── custom_data
       ├── train.csv
       ├── test.csv
       ├── sample_submission.csv      # 可选
       ├── description.md             # 可选
       ├── sample.py                  # 可选
       └── prev_model                 # ← 新增
           ├── models/                #   先前的检查点 (例如 *.bin, *.pt, *.ckpt)
           └── main.py                  #   您之前使用的训练/推理脚本

如果您的竞赛提供自定义的评分/验证脚本，请将它们保留在 ``ds_data/eval/custom_data`` 下，与之前完全一样。

🔧 环境设置
~~~~~~~~~~~~~~~~~~~~~~

在 **.env** 中添加或更新以下变量（显示为示例）：

.. code-block:: sh

   # 所有数据科学运行都需要
   dotenv set DS_LOCAL_DATA_PATH <您的本地路径>/ds_data

   # 可选：选择 docker / conda 等
   dotenv set DS_CODER_COSTEER_ENV_TYPE docker

🚀 运行时如何工作

1. **首次运行**

   * `rdagent` 检测到 `prev_model/models`。
   * 它会加载最新的检查点，并根据在 `prev_model/*.py` 下找到的代码（或者如果您覆盖它，则使用您自己的管道）准备微调。
   * 微调后的权重将写入 `./workspace_input/models`。

2. **后续运行**

   * 当您执行 `python ./workspace_input/main.py` 时，脚本首先在 `./workspace_input/models` 中查找检查点。
   * 如果找到，它将 **跳过微调** 并直接进行预测/提交生成。

⏰ 管理超时


默认情况下：

* **调试循环**：1 小时 (``DS_DEBUG_TIMEOUT=3600`` 秒)
* **完整运行**：3 小时 (``DS_FULL_TIMEOUT=10800`` 秒)

在 **.env** 中覆盖任一值：

.. code-block:: sh

   # 给调试循环 45 分钟，完整循环 6 小时
   dotenv set DS_DEBUG_TIMEOUT 2700
   dotenv set DS_FULL_TIMEOUT 21600

- 🚀 **运行应用程序**

  - 您可以通过使用以下命令直接运行应用程序：
    
    .. code-block:: sh

        dotenv run -- python rdagent/app/finetune/data_science/loop.py --competition <竞赛 ID>

  - 然后，您可以运行与循环的每一轮相对应的测试集分数。

    .. code-block:: sh

        dotenv run -- python rdagent/log/mle_summary.py grade <url_to_log>

    此处，<url_to_log> 指的是运行期间生成的日志文件夹的父目录。

- 📥 **可视化研发过程**

  - 我们提供了一个 Web UI 来可视化日志。您只需运行：

    .. code-block:: sh

        streamlit run rdagent/log/ui/dsapp.py

  - 然后您可以输入日志路径并可视化研发过程。

🔍 MLE-bench 指南：通过 MLE-bench 运行机器学习工程
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 📝 **MLE-bench 概述**

  - MLE-bench 是一个综合性基准，旨在使用真实世界的场景评估 AI 系统的 ML 工程能力。该数据集包含 75 个 Kaggle 竞赛。由于 Kaggle 不为这些竞赛提供保留的测试集，该基准包括用于将公开可用的训练数据拆分为新的训练集和测试集的准备脚本，并为每个竞赛提供评分脚本以准确评估提交分数。

- 🔧 **为 MLE-bench 设置环境**

  - 在 MLE-bench 上运行 R&D-Agent 设计为完全自动化。无需手动下载和数据准备。只需将环境变量 ``DS_IF_USING_MLE_DATA`` 设置为 True。

  - 在运行时，R&D-Agent 将自动构建在 ``rdagent/scenarios/kaggle/docker/mle_bench_docker/Dockerfile`` 中指定的 Docker 镜像。此镜像负责下载 MLE-Bench 所需的数据集和评分文件。
  
  - 注意：第一次运行可能比后续运行花费更长的时间，因为 Docker 镜像和数据是第一次下载和设置。

    .. code-block:: sh

        dotenv set DS_LOCAL_DATA_PATH <您的本地目录>/ds_data
        dotenv set DS_IF_USING_MLE_DATA True

- 🔨 **配置 Kaggle API**

  - 下载 Kaggle 竞赛数据需要 Kaggle API。您可以通过以下步骤设置 Kaggle API：
  
    - 在 `Kaggle <https://www.kaggle.com/>`_ 网站上注册并登录。

    - 点击头像（通常在页面右上角）-> ``设置`` -> ``创建新令牌``，将下载一个名为 ``kaggle.json`` 的文件。

    - 将 ``kaggle.json`` 移动到 ``~/.config/kaggle/``

    - 修改 ``kaggle.json`` 文件的权限。

      .. code-block:: sh

        chmod 600 ~/.config/kaggle/kaggle.json

  - 有关 Kaggle API 设置的更多信息，请参阅 `Kaggle API <https://github.com/Kaggle/kaggle-api>`_。


- 🔩 **为 MLE-bench 设置环境变量**

  - 除了自动下载基准数据外，您还必须配置用于执行竞赛代码的运行时环境。
  - 使用环境变量 ``DS_CODER_COSTEER_ENV_TYPE`` 选择执行模式：
    
    • 当设置为 docker（默认）时，RD-Agent 利用官方的 Kaggle Docker 镜像（``gcr.io/kaggle-gpu-images/python:latest``）来确保所有必需的包都可用。
    • 如果您希望使用自定义的 Docker 设置，可以使用 ``DS_DOCKER_IMAGE`` 或 ``DS_DOCKERFILE_FOLDER_PATH`` 修改配置。
    • 或者，如果您的竞赛工作只需要基本的库，您可以将 ``DS_CODER_COSTEER_ENV_TYPE`` 设置为 conda。在此模式下，您必须创建一个名为“kaggle”的本地 conda 环境，并预安装必要的包。RD-Agent 将在此“kaggle”conda 环境中执行竞赛代码。

    .. code-block:: sh

      # 配置运行时环境：在 'docker'（默认）或 'conda' 之间选择
      dotenv set DS_CODER_COSTEER_ENV_TYPE docker

- **其他指导**

  - **在研发阶段组合不同的 LLM 模型**

    - 您可以在研发阶段组合不同的 LLM 模型。

    - 默认情况下，当您设置环境变量 ``CHAT_MODEL`` 时，它涵盖了两个研发阶段。在为开发阶段自定义模型时，您可以设置：
    
    .. code-block:: sh

      # 此示例将模型设置为“o3-mini”。对于某些模型，推理工作应设置为“None”。
      dotenv set LITELLM_CHAT_MODEL_MAP '{"coding":{"model":"o3-mini","reasoning_effort":"high"},"running":{"model":"o3-mini","reasoning_effort":"high"}}'
