==============================
基准测试
==============================

介绍
=============

对研发能力进行基准测试是该领域的一个关键研究问题。我们正在不断探索对这些能力进行基准测试的方法。当前的基准测试列在此页面上。

开发能力基准测试
===================================

基准测试用于评估具有固定数据的因子的有效性。它主要包括以下步骤：

1. :ref:`读取并准备 eval_data <data>`

2. :ref:`声明要测试的方法并传递参数 <config>`

3. :ref:`声明评估方法并传递参数 <config>`

4. :ref:`运行评估 <run>`

5. :ref:`保存并显示结果 <show>`

配置
-------------
.. _config:

.. autopydantic_settings:: rdagent.components.benchmark.conf.BenchmarkSettings

示例
+++++++
.. _example:

``bench_test_round`` 的默认值为 10，运行大约需要 2 小时。要将其从 ``10`` 修改为 ``2``，请如下所示在 .env 文件中调整环境变量。

.. code-block:: Properties

      BENCHMARK_BENCH_TEST_ROUND=2

数据格式
-------------
.. _data:

``bench_data_path`` 中的示例数据是一个字典，其中每个键代表一个因子名称。与每个键关联的值是包含以下信息的因子数据：

- **description**: 因子的文本描述。
- **formulation**: 表示模型公式的 LaTeX 公式。
- **variables**: 因子中涉及的变量字典。
- **Category**: 因子的类别或分类。
- **Difficulty**: 实现或理解因子的难度级别。
- **gt_code**: 与因子关联的一段代码。

以下是此数据格式的示例：

.. literalinclude:: ../../rdagent/components/benchmark/example.json
   :language: json

确保将数据放置在 ``FACTOR_COSTEER_SETTINGS.data_folder_debug`` 中。数据文件应为 ``.h5`` 或 ``.md`` 格式，并且不得存储在任何子文件夹中。LLM-Agents 将审查文件内容并实施任务。

.. TODO: 添加一个脚本以自动在 `rdagent/app/quant_factor_benchmark/data` 文件夹中生成数据。

运行基准测试
-------------
.. _run:

完成 :doc:`../installation_and_configuration` 后启动基准测试。

.. code-block:: Properties

      dotenv run -- python rdagent/app/benchmark/factor/eval.py

完成后，将生成一个 pkl 文件，其路径将打印在控制台的最后一行。

显示结果
-------------
.. _show:

``analysis.py`` 脚本从 pkl 文件中读取数据并将其转换为图像。修改 ``rdagent/app/quant_factor_benchmark/analysis.py`` 中的 Python 代码以指定 pkl 文件的路径和 png 文件的输出路径。

.. code-block:: Properties

      dotenv run -- python rdagent/app/benchmark/factor/analysis.py <log/path to.pkl>

一个 png 文件将保存到指定路径，如下所示。

.. image:: ../_static/benchmark.png

相关论文
-------------

- `迈向以数据为中心的自动化研发 <https://arxiv.org/abs/2404.11276>`_:
  我们开发了一个名为 RD2Bench 的综合基准来评估数据和模型研发能力。该基准包括一系列概述模型特征或结构的任务。这些任务用于评估 LLM-Agents 实现它们的能力。

.. code-block:: bibtex

    @misc{chen2024datacentric,
        title={Towards Data-Centric Automatic R&D},
        author={Haotian Chen and Xinjie Shen and Zeqi Ye and Wenjun Feng and Haoxue Wang and Xiao Yang and Xu Yang and Weiqing Liu and Jiang Bian},
        year={2024},
        eprint={2404.11276},
        archivePrefix={arXiv},
        primaryClass={cs.AI}
    }

.. image:: https://github.com/user-attachments/assets/494f55d3-de9e-4e73-ba3d-a787e8f9e841

要复制论文中详述的基准，请查阅以下文件中列出的因子：`RD2bench.json <../_static/RD2bench.json>`_。
请注意，在评估结果时使用 ``only_correct_format=False``。
