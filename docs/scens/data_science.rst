.. _data_science_agent:

=======================
数据科学智能体
=======================

**🤖 自动化特征工程与模型调优演进**
------------------------------------------------------------------------------------------
数据科学智能体是一个能够自动执行特征工程和模型调优的智能体。它可用于解决各种数据科学问题，例如图像分类、时间序列预测和文本分类。

🌟 介绍
~~~~~~~~~~~~~~~~~~

在这个场景中，我们的自动化系统在一个持续的迭代过程中提出假设、选择行动、实现代码、进行验证并利用反馈。

目标是在验证集或 Kaggle 排行榜中自动优化性能指标，最终通过自主研发发现最高效的特征和模型。

以下是步骤的增强大纲：

**步骤 1：假设生成 🔍**

- 基于先前的实验分析和领域专业知识，生成并提出初步假设，并附有详尽的推理和财务理由。

**步骤 2：实验创建 ✨**

- 将假设转化为任务。
- 在特征工程或模型调优中选择一个具体行动。
- 开发、定义和实现一个新的特征或模型，包括其名称、描述和公式。

**步骤 3：模型/特征实现 👨‍💻**

- 根据详细描述实现模型代码。
- 像开发人员一样迭代地演进模型，确保准确性和效率。

**步骤 4：在测试集或 Kaggle 上进行验证 📉**

- 使用测试集或 Kaggle 数据集验证新开发的模型。
- 根据验证结果评估模型的有效性和性能。

**步骤 5：反馈分析 🔍**

- 分析验证结果以评估性能。
- 使用见解来完善假设并增强模型。

**步骤 6：假设完善 ♻️**

- 根据验证反馈调整假设。
- 迭代该过程以不断改进模型。

📖 数据科学背景
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在不断发展的人工智能领域，**数据科学** 代表了一种强大的范式，机器在其中跨越医疗、金融、物流和研究等不同领域进行自主探索、假设检验和模型开发。

**数据科学智能体** 是这一转变的核心引擎，使用户能够自动化整个机器学习工作流程：从假设生成到代码实现、验证和改进——所有这些都以性能反馈为指导。

通过利用 **数据科学智能体**，研究人员和开发人员可以加速实验周期。无论是微调自定义模型还是在像 Kaggle 这样的高风险基准测试中竞争，数据科学智能体都在智能、自主的发现中开辟了新的前沿。

🧭 示例指南 - 自定义数据集
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

🔧 **设置 RD-Agent 环境**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - 在开始之前，请确保您已正确安装 RD-Agent 并配置了 RD-Agent 的环境。如果您想了解如何安装和配置 RD-Agent，请参阅 `文档 <../installation_and_configuration.html>`_。

- 🔩 **在 .env 文件中设置环境变量**

  - 确定数据将存储的路径，并将其添加到 ``.env`` 文件中。

  .. code-block:: sh

    dotenv set DS_LOCAL_DATA_PATH <你的本地目录>/ds_data
    dotenv set DS_SCEN rdagent.scenarios.data_science.scen.DataScienceScen

📥 **准备自定义数据集**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - 数据科学竞赛数据集通常由两部分组成：``竞赛数据集`` 和 ``评估数据集``。（我们提供一个名为 `arf-12-hours-prediction-task` 的自定义数据集的 `示例 <https://github.com/microsoft/RD-Agent/tree/main/rdagent/scenarios/data_science/example>`_ 作为参考。）
    
    - ``竞赛数据集`` 包含 **训练数据**、**测试数据**、**描述文件**、**格式化提交文件**、**数据采样代码**。
    
    - ``评估数据集`` 包含 **标准答案文件**、**数据检查代码** 和 **分数计算代码**。

  - 我们以 ``arf-12-hours-prediction-task`` 数据为例，介绍竞赛数据集的准备工作流程。
  
    - 创建一个 ``ds_data/source_data/arf-12-hours-prediction-task`` 文件夹，用于存储您的原始数据集。

      - ``arf-12-hours-prediction-task`` 竞赛的原始文件有两个：``ARF_12h.csv`` 和 ``X.npz``。
    
    - 创建一个 ``ds_data/source_data/arf-12-hours-prediction-task/prepare.py`` 文件，将您的原始数据拆分为 **训练数据**、**测试数据**、**格式化提交文件** 和 **标准答案文件**。（您需要根据您的原始数据编写一个脚本。）
      
      - 以下显示了 ``arf-12-hours-prediction-task`` 原始数据的预处理代码。

      .. literalinclude:: ../../rdagent/scenarios/data_science/example/source_data/arf-12-hours-prediction-task/prepare.py
        :language: python
        :caption: ds_data/source_data/arf-12-hours-prediction-task/prepare.py
        :linenos:

      - 程序执行结束时，``ds_data`` 文件夹结构将如下所示：

      .. code-block:: text

        ds_data
        ├── arf-12-hours-prediction-task
        │   ├── train
        │   │   ├── ARF_12h.csv
        │   │   └── X.npz
        │   ├── test
        │   │   ├── ARF_12h.csv
        │   │   └── X.npz
        │   └── sample_submission.csv
        ├── eval
        │   └── arf-12-hours-prediction-task
        │       └── submission_test.csv
        └── source_data
            └── arf-12-hours-prediction-task
                ├── ARF_12h.csv
                ├── prepare.py
                └── X.npz

    - 创建一个 ``ds_data/arf-12-hours-prediction-task/description.md`` 文件来描述您的竞赛、目标、数据集和其他信息。

      - 以下显示了 ``arf-12-hours-prediction-task`` 的描述文件

      .. literalinclude:: ../../rdagent/scenarios/data_science/example/arf-12-hours-prediction-task/description.md
        :language: markdown
        :caption: ds_data/arf-12-hours-prediction-task/description.md
        :linenos:

    - 创建一个 ``ds_data/arf-12-hours-prediction-task/sample.py`` 文件来构建调试样本数据。

      - 以下显示了基于 ``arf-12-hours-prediction-task`` 数据集实现构建调试样本数据的脚本。

      .. literalinclude:: ../../rdagent/scenarios/data_science/example/arf-12-hours-prediction-task/sample.py
        :language: markdown
        :caption: ds_data/arf-12-hours-prediction-task/sample.py
        :linenos:

    - 创建一个 ``ds_data/eval/arf-12-hours-prediction-task/valid.py`` 文件，用于检查提交文件的有效性，以确保其格式与参考文件一致。

      - 以下显示了基于 ``arf-12-hours-prediction-task`` 数据检查提交有效性的脚本。

      .. literalinclude:: ../../rdagent/scenarios/data_science/example/eval/arf-12-hours-prediction-task/valid.py
        :language: markdown
        :caption: ds_data/eval/arf-12-hours-prediction-task/valid.py
        :linenos:

    - 创建一个 ``ds_data/eval/arf-12-hours-prediction-task/grade.py`` 文件，用于根据提交文件和 **标准答案文件** 计算分数，并以 JSON 格式输出结果。

      - 以下显示了基于 ``arf-12-hours-prediction-task`` 数据实现的评分脚本。

      .. literalinclude:: ../../rdagent/scenarios/data_science/example/eval/arf-12-hours-prediction-task/grade.py
        :language: markdown
        :caption: ds_data/eval/arf-12-hours-prediction-task/grade.py
        :linenos:

  - 至此，您已经创建了一个完整的数据集。正确的数据集结构应如下所示。

    .. code-block:: text

        ds_data
        ├── arf-12-hours-prediction-task
        │   ├── train
        │   │   ├── ARF_12h.csv
        │   │   └── X.npz
        │   ├── test
        │   │   ├── ARF_12h.csv
        │   │   └── X.npz
        │   ├── description.md
        │   ├── sample_submission.csv
        │   └── sample.py
        ├── eval
        │   └── arf-12-hours-prediction-task
        │       ├── grade.py
        │       ├── submission_test.csv
        │       └── valid.py
        └── source_data
            └── arf-12-hours-prediction-task
                ├── ARF_12h.csv
                ├── prepare.py
                └── X.npz

  - 以上显示了完整的数据集创建工作流程，其中一些文件不是必需的，在实践中您可以根据自己的需要自定义数据集。

    - 如果我们不需要测试集分数，那么我们可以选择不在准备代码中生成 **格式化提交文件** 和 **标准答案文件**，也不需要编写 **数据检查代码** 和 **分数计算代码**。

    - **数据采样代码** 也可以根据实际需要创建，如果您不提供 **数据采样代码**，RD-Agent 将在运行时交给 LLM 采样。

      - 在默认的采样方法 (``create_debug_data``) 中，默认的采样比例 (参数: ``min_frac``) 是 1%，如果 1% 的数据少于 5，则将采样 5 个数据 (参数: ``min_num``)，您可以通过调整这两个参数来调整采样比例。

        - 如果您有自定义的数据采样代码，您需要在运行前将 ``.env`` 文件中的 ``DS_SAMPLE_DATA_BY_LLM`` 设置为 ``False`` (默认为 True)，这样程序在运行时将使用自定义的采样代码，您只需在命令行中执行此行代码：

          .. code-block:: sh

            dotenv set DS_SAMPLE_DATA_BY_LLM False

        - 此外，我们在 `rdagent.scenarios.data_science.debug.data.create_debug_data <https://github.com/microsoft/RD-Agent/blob/main/rdagent/scenarios/data_science/debug/data.py#L605>`_ 中提供了一种数据采样方法，在此方法中，默认的采样比例 (参数: ``min_frac``) 是 1%，如果 1% 的数据少于 5，则将采样 5 个数据 (参数: ``min_num``)，您可以通过以下两种方式使用此方法。

          - 您可以在 ``.env`` 文件中将 ``DS_SAMPLE_DATA_BY_LLM`` 设置为 ``False``，这样程序在运行时将使用 RD-Agent 提供的采样代码。

            .. code-block:: sh

              dotenv set DS_SAMPLE_DATA_BY_LLM False

          - 如果您认为 RD-Agent 提供的接收采样方法中的参数不合适，您可以在以下命令中自定义参数并运行它，并在 ``.env`` 中将 ``DS_SAMPLE_DATA_BY_LLM`` 设置为 ``False``，这样程序在运行时将使用您提供的采样数据。

            .. code-block:: sh

              python rdagent/app/data_science/debug.py --dataset_path <dataset path> --competition <competiton_name> --min_frac <sampling ratio> --min_num <minimum number of sampling>
              dotenv set DS_SAMPLE_DATA_BY_LLM False

  - 如果您不需要测试集的分数，并将数据采样留给 LLM，或者您使用 RD-Agent 提供的采样方法，那么您只需要准备一个最小的数据集。最简单的数据集结构应如下所示。

    .. code-block:: text

        ds_data
        ├── arf-12-hours-prediction-task
        │   ├── train
        │   │   ├── ARF_12h.csv
        │   │   └── X.npz
        │   ├── test
        │   │   ├── ARF_12h.csv
        │   │   └── X.npz
        │   └── description.md
        └── source_data
            └── arf-12-hours-prediction-task
                ├── ARF_12h.csv
                ├── prepare.py
                └── X.npz

  - 我们根据上述描述准备了一个数据集供您参考。您可以使用以下命令下载它。

    .. code-block:: sh

      wget https://github.com/SunsetWolf/rdagent_resource/releases/download/ds_data/arf-12-hours-prediction-task.zip

⚙️ **为自定义数据集设置环境**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. code-block:: sh

      dotenv set DS_SCEN rdagent.scenarios.data_science.scen.DataScienceScen
      dotenv set DS_LOCAL_DATA_PATH <你的本地目录>/ds_data
      dotenv set DS_CODER_ON_WHOLE_PIPELINE True

🚀 **运行应用程序**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - 🌏 您可以通过使用以下命令直接运行应用程序：
    
    .. code-block:: sh

        rdagent data_science --competition <竞赛 ID>

    - 以下显示了基于 ``arf-12-hours-prediction-task`` 数据运行的命令

      .. code-block:: sh

          rdagent data_science --competition arf-12-hours-prediction-task

  - 📈 可视化研发过程

    - 我们提供了一个 Web UI 来可视化日志。您只需运行：

      .. code-block:: sh

          rdagent ui --port <自定义端口> --log-dir <你的日志文件夹，如 "log/"> --data_science True

    - 然后您可以输入日志路径并可视化研发过程。

  - 🧪 对测试结果进行评分

    - 最后，关闭程序，并使用此命令获取测试集分数。

    .. code-block:: sh

      dotenv run -- python rdagent/log/mle_summary.py grade <url_to_log>

    此处，<url_to_log> 指的是运行期间生成的日志文件夹的父目录。

🕹️ Kaggle 智能体
~~~~~~~~~~~~~~~~

📖 背景
^^^^^^^^^^^^^^

在数据科学竞赛领域，Kaggle 是最终的竞技场，数据爱好者在这里利用算法的力量来应对现实世界的挑战。
Kaggle 智能体是一个关键工具，使参与者能够无缝集成尖端模型和数据集，将原始数据转化为可操作的见解。

通过利用 **Kaggle 智能体**，数据科学家可以创建创新的解决方案，不仅能揭示隐藏的模式，还能在预测准确性和模型稳健性方面取得重大进展。

🧭 示例指南 - Kaggle 数据集
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

🛠️ 准备竞赛
""""""""""""""""""""""""""""""""""

- 🔨 **配置 Kaggle API**

  - 在 `Kaggle <https://www.kaggle.com/>`_ 网站上注册并登录。
  - 点击头像（通常在页面右上角）-> ``设置`` -> ``创建新令牌``，将下载一个名为 ``kaggle.json`` 的文件。
  - 将 ``kaggle.json`` 移动到 ``~/.config/kaggle/``
  - 修改 ``kaggle.json`` 文件的权限。

    .. code-block:: sh

      chmod 600 ~/.config/kaggle/kaggle.json

  - 有关 Kaggle API 设置的更多信息，请参阅 `Kaggle API <https://github.com/Kaggle/kaggle-api>`_。

- 🔩 **在 .env 文件中设置环境变量**

  - 确定数据将存储的路径，并将其添加到 ``.env`` 文件中。

  .. code-block:: sh

    mkdir -p <你的本地目录>/ds_data
    dotenv set KG_LOCAL_DATA_PATH <你的本地目录>/ds_data

- 🗳️ **加入竞赛**

  - 如果您的 Kaggle API 帐户尚未加入竞赛，您需要在运行程序之前加入竞赛。

    - 在竞赛详情页底部，您可以找到 ``加入竞赛`` 按钮，点击它并选择 ``我理解并接受`` 以加入竞赛。

    - 在下面的 **可用竞赛列表** 中，您可以跳转到竞赛详情页。

📥 准备竞赛数据集并设置 RD-Agent 环境
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

- 作为数据科学的一个子集，kaggle 的数据集仍然遵循数据科学的格式。基于此，根据是否受 **MLE-Bench** 支持，kaggle 数据集可分为两类。

  - 什么是 **MLE-Bench**？

    - **MLE-Bench** 是一个综合性基准，旨在使用真实世界的场景评估 AI 系统的 **机器学习工程** 能力。该数据集包括多个 Kaggle 竞赛。由于 Kaggle 不为这些竞赛提供保留的测试集，该基准包括用于将公开可用的训练数据拆分为新的训练集和测试集的准备脚本，以及用于每个竞赛的评分脚本，以准确评估提交分数。

  - 我正在参加的竞赛是否受 **MLE-Bench** 支持？

    - 您可以在 `这里 <https://github.com/openai/mle-bench/tree/main/mlebench/competitions>`_ 查看 **MLE-Bench** 支持的所有竞赛。

- 准备 **MLE-Bench** 支持的竞赛的数据集。

  - 如果您同意 **MLE-Bench** 标准，那么您不需要准备数据集，只需配置您的 ``.env`` 文件以自动下载数据集。

    - 配置环境变量，将 ``DS_IF_USING_MLE_DATA`` 添加到环境变量中，并将其设置为 ``True``。

      .. code-block:: sh

        dotenv set DS_IF_USING_MLE_DATA True

    - 配置环境变量，将 ``DS_SAMPLE_DATA_BY_LLM`` 添加到环境变量中，并将其设置为 ``True``。

      .. code-block:: sh

        dotenv set DS_SAMPLE_DATA_BY_LLM True

    - 配置环境变量，将 ``DS_SCEN`` 添加到环境变量中，并将其设置为 ``rdagent.scenarios.data_science.scen.KaggleScen``。

      .. code-block:: sh

        dotenv set DS_SCEN rdagent.scenarios.data_science.scen.KaggleScen

  - 至此，您已准备好开始运行您的竞赛，它将自动下载数据，LLM 将自动提取最小数据集。

    - 运行程序后，ds_data 文件夹的结构应如下所示（以 ``tabular-playground-series-dec-2021`` 竞赛为例）。

      .. code-block:: text

        ds_data
        ├── tabular-playground-series-dec-2021
        │   ├── description.md
        │   ├── sample_submission.csv
        │   ├── test.csv
        │   └── train.csv
        └── zip_files
            └── tabular-playground-series-dec-2021
                └── tabular-playground-series-dec-2021.zip

      - ``ds_data/zip_files`` 文件夹包含从 kaggle 网站下载的原始竞赛数据的 zip 文件。

  - 在运行时，RD-Agent 将自动构建在 `rdagent/scenarios/kaggle/docker/mle_bench_docker/Dockerfile <https://github.com/microsoft/RD-Agent/blob/main/rdagent/scenarios/kaggle/docker/mle_bench_docker/Dockerfile>`_ 中指定的 Docker 镜像。此镜像负责下载 MLE-Bench 所需的数据集和评分文件。

  注意：第一次运行可能比后续运行花费更长的时间，因为 Docker 镜像和数据是第一次下载和设置。

- 准备 **MLE-Bench** 不支持的竞赛的数据集。

  - 作为数据科学的一个子集，我们可以遵循数据科学数据集的格式和步骤来准备 kaggle 数据集。下面我们将以竞赛 ``playground-series-s4e9`` 为例，描述准备 kaggle 数据集的工作流程。
  
    - 创建一个 ``ds_data/source_data/playground-series-s4e9`` 文件夹，用于存储您的原始数据集。

      - ``playground-series-s4e9`` 竞赛的原始文件有两个：``train.csv``、``test.csv``、``sample_submission.csv``，有两种方法可以获取原始数据：

        - 您可以在 `kaggle 官方网站 <https://www.kaggle.com/competitions/playground-series-s4e9/data>`_ 上找到竞赛所需的原始数据。

        - 或者您可以使用命令行下载竞赛的原始数据，下载命令如下。

          .. code-block:: sh

            kaggle competitions download -c playground-series-s4e9

    - 创建一个 ``ds_data/source_data/playground-series-s4e9/prepare.py`` 文件，将您的原始数据拆分为 **训练数据**、**测试数据**、**格式化提交文件** 和 **标准答案文件**。（您需要根据您的原始数据编写一个脚本。）

      - 以下显示了 ``playground-series-s4e9`` 原始数据的预处理代码。

      .. literalinclude:: ../../rdagent/scenarios/data_science/example/source_data/playground-series-s4e9/prepare.py
        :language: python
        :caption: ds_data/source_data/playground-series-s4e9/prepare.py
        :linenos:

      - 程序执行结束时，``ds_data`` 文件夹结构将如下所示：

      .. code-block:: text

        ds_data
        ├── playground-series-s4e9
        │   ├── train.csv
        │   ├── test.csv
        │   └── sample_submission.csv
        ├── eval
        │   └── playground-series-s4e9
        │       └── submission_test.csv
        └── source_data
            └── playground-series-s4e9
                ├── prepare.py
                ├── sample_submission.csv
                ├── test.csv
                └── train.csv

    - 创建一个 ``ds_data/playground-series-s4e9/description.md`` 文件来描述您的竞赛、数据集描述和其他信息。我们可以从 Kaggle 网站找到 `竞赛描述信息 <https://www.kaggle.com/competitions/playground-series-s4e9/overview>`_ 和 `数据集描述信息 <https://www.kaggle.com/competitions/playground-series-s4e9/data>`_。

      - 以下显示了 ``playground-series-s4e9`` 的描述文件

        .. literalinclude:: ../../rdagent/scenarios/data_science/example/playground-series-s4e9/description.md
          :language: markdown
          :caption: ds_data/playground-series-s4e9/description.md
          :linenos:

    - 创建一个 ``ds_data/eval/playground-series-s4e9/valid.py`` 文件，用于检查提交文件的有效性，以确保其格式与参考文件一致。

      - 以下显示了基于 ``playground-series-s4e9`` 数据检查提交有效性的脚本。

      .. literalinclude:: ../../rdagent/scenarios/data_science/example/eval/playground-series-s4e9/valid.py
        :language: markdown
        :caption: ds_data/eval/playground-series-s4e9/valid.py
        :linenos:

    - 创建一个 ``ds_data/eval/playground-series-s4e9/grade.py`` 文件，用于根据提交文件和 **标准答案文件** 计算分数，并以 JSON 格式输出结果。

      - 以下显示了基于 ``playground-series-s4e9`` 数据实现的评分脚本。

      .. literalinclude:: ../../rdagent/scenarios/data_science/example/eval/playground-series-s4e9/grade.py
        :language: markdown
        :caption: ds_data/eval/playground-series-s4e9/grade.py
        :linenos:

  - 在这个例子中，我们没有创建 ``ds_data/eval/playground-series-s4e9/sample.py``，我们默认使用 RD-Agent 提供的采样方法。

  - 至此，您已经创建了一个完整的数据集。正确的数据集结构应如下所示。

    .. code-block:: text

        ds_data
        ├── playground-series-s4e9
        │   ├── train.csv
        │   ├── test.csv
        │   ├── description.md
        │   └── sample_submission.csv
        ├── eval
        │   └── playground-series-s4e9
        │       ├── grade.py
        │       ├── submission_test.csv
        │       └── valid.py
        └── source_data
            └── playground-series-s4e9
                ├── prepare.py
                ├── sample_submission.csv
                ├── test.csv
                └── train.csv

  - 我们根据上述描述准备了一个数据集供您参考。您可以使用以下命令下载它。

    .. code-block:: sh

      wget https://github.com/SunsetWolf/rdagent_resource/releases/download/ds_data/playground-series-s4e9.zip

  - 接下来，我们需要为 ``playground-series-s4e9`` 竞赛配置环境。您可以通过在命令行中执行以下命令来完成此操作。

    .. code-block:: sh

      dotenv set DS_IF_USING_MLE_DATA False
      dotenv set DS_SAMPLE_DATA_BY_LLM False
      dotenv set DS_SCEN rdagent.scenarios.data_science.scen.KaggleScen

🚀 **运行应用程序**
""""""""""""""""""""""""""""""""""""

  - 🌏 您可以通过使用以下命令直接运行应用程序：

    .. code-block:: sh

        rdagent data_science --competition <竞赛 ID>

    - 以下显示了基于 ``playground-series-s4e9`` 数据运行的命令

      .. code-block:: sh

          rdagent data_science --competition playground-series-s4e9

  - 📈 可视化研发过程

    - 我们提供了一个 Web UI 来可视化日志。您只需运行：

      .. code-block:: sh

          rdagent ui --port <自定义端口> --log-dir <你的日志文件夹，如 "log/"> --data_science True

    - 然后您可以输入日志路径并可视化研发过程。

  - 🧪 对测试结果进行评分

    - 最后，关闭程序，并使用此命令获取测试集分数。

    .. code-block:: sh

      dotenv run -- python rdagent/log/mle_summary.py grade <url_to_log>

    - 如果您在 ``ds_data/eval/playground-series-s4e9/grade.py`` 中配置了完整输出，或者如果您正在运行一个受 **MLE-Bench** 支持的竞赛，您还可以通过运行以下命令来汇总分数。

    .. code-block:: sh

      rdagent grade_summary --log-folder=<url_to_log>

    此处，<url_to_log> 指的是运行期间生成的日志文件夹的父目录。
