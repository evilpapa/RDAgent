=========================
开发者指南
=========================

如果你希望体验最新版本或为 RD-Agent 做贡献，可以从源码安装并按照本页命令操作。

   .. code-block:: bash

      git clone https://github.com/microsoft/RD-Agent


🛠开发环境准备
=========================

- 设置开发环境。

   .. code-block:: bash

      make dev

- 运行代码风格检查与静态分析。

   .. code-block:: bash

      make lint

- 部分代码风格问题可自动修复。Makefile 已内置相关命令，方便使用。

   .. code-block:: bash

      make auto-lint


代码结构
=========================

.. code-block:: text

    📂 src
    ➥ 📂 <项目名>（避免命名空间冲突）
      ➥ 📁 core
      ➥ 📁 components/A
      ➥ 📁 components/B
      ➥ 📁 components/C
      ➥ 📁 scenarios/X
      ➥ 📁 scenarios/Y
      ➥ 📂 app
    ➥ 📁 scripts

.. list-table::
   :header-rows: 1

   * - 文件夹名
     - 说明
   * - 📁 core
     - 系统核心框架。所有类应为抽象类，通常不能直接使用。
   * - 📁 component/A
     - 可复用组件（如场景模块）。许多 core 类的子类位于此处。
   * - 📁 scenarios/X
     - 针对特定场景的具体功能（通常基于组件或 core 构建）。这些模块通常难以跨场景复用。
   * - 📁 app
     - 针对特定场景的应用（通常基于组件或场景构建）。移除任何一个不会影响系统完整性或其他场景。
   * - 📁 scripts
     - 临时代码。可作为 core、components、scenarios、apps 的候选。



约定
===========

文件命名约定
----------------------

.. list-table::
   :header-rows: 1

   * - 文件名
     - 说明
   * - `conf.py`
     - 模块、应用、项目的配置文件。

.. <!-- TODO: 文件重命名 -->

