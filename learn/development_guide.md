# RD-Agent 开发者指南

本文档根据官方 `docs/development.rst` 整理，并补充了其他相关信息，旨在为希望参与 RD-Agent 开发或从源码构建的开发者提供指导。

## 1. 获取源码

如果您希望体验最新版本、进行定制开发或为 RD-Agent 贡献代码，首先需要从 GitHub 克隆项目仓库：

```bash
git clone https://github.com/microsoft/RD-Agent.git
cd RD-Agent
```

## 2. 开发环境准备

项目提供了一个 `Makefile` 来简化开发环境的配置和代码质量检查。

### 2.1 设置开发环境

执行以下命令来安装所有开发所需的依赖项 (包括测试、lint工具等)：

```bash
make dev
```

这通常会创建一个虚拟环境（如果项目配置了的话，例如使用 Poetry 或 PDM），并安装 `requirements/dev.txt` 或 `pyproject.toml` 中定义的开发依赖。

### 2.2 代码风格检查与静态分析

为了保持代码库的质量和一致性，项目集成了一系列 linting 和静态分析工具。

-   **运行检查**:
    ```bash
    make lint
    ```
    此命令会运行诸如 Flake8, MyPy, Ruff, Black, iSort 等工具（具体工具取决于项目配置）来检查代码风格、类型错误和潜在bug。

-   **自动修复**:
    部分代码风格问题（如格式化、导入排序）可以通过工具自动修复。
    ```bash
    make auto-lint
    ```
    建议在提交代码前运行此命令。

## 3. 理解项目代码结构

项目的代码结构设计旨在实现模块化和可扩展性。详细的目录结构及其说明，请参见 [框架概述文档中的代码结构概览](framework_overview.md#16-项目代码结构概览-源自-docsdevelopmentrst)。

## 4. 贡献代码

如果您希望为 RD-Agent 贡献代码，请遵循以下一般步骤：

1.  **查阅贡献指南**: 项目根目录通常会有一个 `CONTRIBUTING.md` 文件，其中详细说明了贡献流程、行为准则、PR (Pull Request) 要求等。请务必仔细阅读。
2.  **Fork仓库**: 在 GitHub 上将主仓库 fork到您自己的账户下。
3.  **创建分支**: 从最新的 `main` 或 `develop` 分支（根据项目指引）创建一个新的特性分支或修复分支。分支命名建议清晰明了，例如 `feat/add-new-component` 或 `fix/resolve-issue-123`。
4.  **进行开发**:
    -   编写您的代码，确保遵循项目的代码风格和设计原则。
    -   为新功能添加单元测试和集成测试。
    -   确保所有测试通过 (`make test` 或类似命令)。
    -   运行 `make lint` 和 `make auto-lint` 确保代码质量。
5.  **编写提交信息**: 遵循清晰、规范的提交信息格式。项目可能使用 Conventional Commits 规范。
6.  **发起Pull Request**:
    -   将您的分支推送到您 fork 的仓库。
    -   在 GitHub 上向 RD-Agent 主仓库的相应分支发起 Pull Request。
    -   在 PR 描述中清晰说明您的更改内容、动机以及如何测试。关联相关的 Issue (如果存在)。
7.  **代码审查与合并**: 等待项目维护者审查您的代码。根据反馈进行修改，直至代码被接受并合并。

## 5. 其他约定

-   **配置文件**: 模块、应用或项目的配置文件通常命名为 `conf.py`。
-   **日志**: 注意使用项目统一的日志系统（通常通过 `rdagent.log.rdagent_logger` 获取）进行日志记录。
-   **异常处理**: 使用 `rdagent.core.exception` 中定义的自定义异常，或创建新的有意义的异常类。

---

本开发者指南提供了参与 RD-Agent 开发的基本信息。更详细或特定的开发规范请参考项目中的 `CONTRIBUTING.md` 或其他开发者文档。
