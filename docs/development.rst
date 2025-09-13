=========================
对于开发
=========================

如果您想尝试最新版本或为 RD-Agent 做出贡献。您可以从源代码安装并按照此页面中的命令进行操作。

   .. code-block:: bash

      git clone https://github.com/microsoft/RD-Agent


🔧准备开发
=========================

- 设置开发环境。

   .. code-block:: bash

      make dev

- 运行 linting 和检查。

   .. code-block:: bash

      make lint


- 一些 linting 问题可以自动修复。我们在 Makefile 中添加了一个命令以便于使用。

   .. code-block:: bash

      make auto-lint



代码结构
=========================

.. code-block:: text

    📂 src
    ➥ 📂 <项目名称>: 避免命名空间冲突
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

   * - 文件夹名称
     - 描述
   * - 📁 core
     - 系统的核心框架。所有类都应该是抽象的，通常不能直接使用。
   * - 📁 component/A
     - 其他人（例如，场景）可以使用的有用组件。核心类的许多子类都位于此处。
   * - 📁 scenarios/X
     - 特定场景的具体功能（通常基于组件或核心构建）。这些模块通常在不同场景之间不可重用。
   * - 📁 app
     - 特定场景的应用程序（通常基于组件或场景构建）。删除其中任何一个都不会影响系统的完整性或其他场景。
   * - 📁 scripts
     - 快速而粗糙的东西。这些是核心、组件、场景和应用程序的候选者。



约定
===========


文件命名约定
----------------------

.. list-table::
   :header-rows: 1

   * - 名称
     - 描述
   * - `conf.py`
     - 模块、应用程序和项目的配置。

.. <!-- TODO: 重命名文件 -->
