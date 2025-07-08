# RD-Agent 安装与配置指南

本文档根据官方文档 `docs/installation_and_configuration.rst` 整理，旨在为中文用户提供清晰的安装和配置指导。

## 1. 安装

### 1.1 安装 RD-Agent

-   **普通用户**:
    ```bash
    pip install rdagent
    ```
-   **开发者**:
    如果希望从源码安装、体验最新功能或参与贡献，请参考 `开发者指南 (development_guide.md)`。

### 1.2 安装 Docker

RD-Agent 在许多场景下依赖 Docker 来执行代码，以保证环境的一致性和简化依赖管理。

-   请访问 [官方 Docker 页面](https://docs.docker.com/engine/install/) 获取适合您操作系统的 Docker 安装说明。
-   **重要**: 确保当前用户可以**无需 `sudo`** 权限运行 Docker 命令。可以通过执行以下命令进行验证，如果能成功运行则表示配置正确：
    ```bash
    docker run hello-world
    ```

## 2. LLM 后端配置 (LiteLLM - 默认)

RD-Agent 默认使用 LiteLLM 作为与大语言模型 (LLM) 交互的后端，这提供了连接多种不同 LLM 服务提供商的灵活性。配置通常通过设置环境变量来完成，可以将这些变量保存在项目根目录下的 `.env` 文件中。

### 2.1 选项 1：统一 API Base

如果您的聊天模型和嵌入模型使用相同的 API 服务提供商和相同的 API 密钥：

```properties
# .env 文件内容示例

# 设置为 LiteLLM 支持的任意模型名称
CHAT_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small

# 配置统一的 API Base 和 Key
OPENAI_API_BASE=<你的统一API基础地址>
OPENAI_API_KEY=<你的API密钥>
```

### 2.2 选项 2：分别配置聊天与嵌入模型的 API Base

如果您的聊天模型和嵌入模型来自不同的服务提供商，或者需要使用不同的 API Key/Base：

```properties
# .env 文件内容示例

# --- 聊天模型配置 ---
CHAT_MODEL=gpt-4o
OPENAI_API_BASE=<你的聊天模型API基础地址>
OPENAI_API_KEY=<你的聊天模型API密钥>

# --- 嵌入模型配置 ---
# 注意：如果嵌入模型与聊天模型提供商不同，或需要单独指定 Endpoint/Key，
#       需在 EMBEDDING_MODEL 名称前加上 "litellm_proxy/" 前缀。
# 以 SiliconFlow 提供的 BAAI 模型为例：
EMBEDDING_MODEL=litellm_proxy/BAAI/bge-large-en-v1.5
LITELLM_PROXY_API_BASE=<你的嵌入模型API基础地址, 例如 https://api.siliconflow.cn/v1>
LITELLM_PROXY_API_KEY=<你的嵌入模型API密钥>
```

### 2.3 关键环境变量解释

-   `CHAT_MODEL`: (必需) 指定用于聊天的 LLM 模型名称。例如 `gpt-4o`, `deepseek/deepseek-chat`。
-   `EMBEDDING_MODEL`: (必需) 指定用于文本嵌入的 LLM 模型名称。例如 `text-embedding-3-small`, `litellm_proxy/BAAI/bge-large-en-v1.5`。
-   `OPENAI_API_BASE`: (必需)
    -   如果 `EMBEDDING_MODEL` **不以** `litellm_proxy/` 开头，则此 API Base 同时用于聊天模型和嵌入模型。
    -   如果 `EMBEDDING_MODEL` **以** `litellm_proxy/` 开头，则此 API Base **仅用于聊天模型**。
-   `OPENAI_API_KEY`: (必需) 与 `OPENAI_API_BASE` 对应的 API 密钥。

-   `LITELLM_PROXY_API_BASE`: (可选) **仅当** `EMBEDDING_MODEL` 以 `litellm_proxy/` 开头时**必需**。指定嵌入模型的 API 基础地址。
-   `LITELLM_PROXY_API_KEY`: (可选) **仅当** `EMBEDDING_MODEL` 以 `litellm_proxy/` 开头时**必需**。指定嵌入模型的 API 密钥。

### 2.4 其他提供商特定配置

-   **模型名称**: 务必确保 `CHAT_MODEL` 和 `EMBEDDING_MODEL` 中使用的模型名称与 [LiteLLM 官方支持的模型名称](https://docs.litellm.ai/docs/providers)完全一致。某些模型可能需要特定的前缀，如 `deepseek/deepseek-chat`。
-   **特定API Key**: 某些模型提供商（如 DeepSeek）可能需要其特有的 API 密钥环境变量。例如，使用 DeepSeek 模型时，除了设置 `CHAT_MODEL=deepseek/deepseek-chat`，还需设置 `DEEPSEEK_API_KEY=<你的DeepSeek API密钥>`。请参考 LiteLLM 文档中关于特定提供商的配置说明。

### 2.5 处理带思考过程的推理模型

如果使用的 LLM 在推理时会输出包含思考过程的中间步骤（例如，XML 标签如 `<think>...</think>`），则需要设置以下环境变量来确保框架能正确处理这些输出：

```properties
REASONING_THINK_RM=True
```

这将启用移除思考标签的逻辑。

---

**重要提示**:

-   配置文件 (`.env`)应放置在项目根目录下。
-   确保不要将包含敏感信息（如API密钥）的 `.env` 文件提交到公共代码仓库。建议将其添加到 `.gitignore` 文件中。
-   更多关于 LiteLLM 的高级配置和支持的模型列表，请查阅 [官方 LiteLLM 文档](https://docs.litellm.ai/docs)。
