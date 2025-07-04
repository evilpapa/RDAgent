==============
用户界面
==============

简介
============

RD-Agent 在研发过程中会生成一些日志。这些日志对于调试和理解研发流程非常有用，但仅查看终端日志不够直观。RD-Agent 提供了 Web 应用作为可视化界面，帮助你更直观地查看和理解研发流程。

快速演示
============

启动 Web 应用
-------------

在 `RD-Agent/` 目录下运行：

.. code-block:: bash

    rdagent ui --port <端口号> --log_dir <日志目录如 "log/"> [--debug]

这将在 `http://localhost:<端口号>` 启动 Web 应用。

**注意**：log_dir 参数非必需。你可以在 Web 应用中手动输入 log_path。如果设置了 log_dir 参数，可以在 Web 应用中方便地切换不同 log_path。

--debug 为可选参数，启用后侧边栏会显示“单步运行”按钮及保存对象信息。

使用 Web 应用
-----------

1. 打开侧边栏。

.. TODO: 更新这些内容

2. 选择你要展示的场景。预设场景包括：
    - Qlib 模型
    - Qlib 因子
    - 数据挖掘
    - 论文模型
    - Kaggle

3. 点击 `Config⚙️` 按钮并输入日志路径（如设置了 log_dir，可在下拉列表中选择 log_path）。

4. 点击 Config⚙️ 下方按钮展示场景执行流程。按钮包括：
    - All Loops：展示完整场景执行流程。
    - Next Loop：展示一次完整 **R&D 循环**。
    - One Evolving：展示一次 **development** 阶段的进化步骤。
    - refresh logs：清除已显示日志。

