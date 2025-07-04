==============================
安装与配置
==============================

安装
====

**安装 RDAgent**：针对不同场景

- 纯用户：请使用 ``pip install rdagent`` 安装 RDAgent
- 开发者用户：`参见开发文档 <development.html>`_

**安装 Docker**：RDAgent 旨在用于科研与开发，像人类研究者和开发者一样工作。它可以在多种环境下编写和运行代码，主要通过 Docker 执行代码，从而简化了依赖。用户在大多数场景下需确保已安装 Docker。请参考 `官方 🐳Docker 页面 <https://docs.docker.com/engine/install/>`_ 获取安装说明。
请确保当前用户可以**无需 sudo**运行 Docker 命令。你可以通过执行 `docker run hello-world` 验证。

LiteLLM 后端配置（默认）
========================

选项 1：统一 API base（适用于聊天与嵌入模型）
------------------------------------------

   .. code-block:: Properties

      # 设置为 LiteLLM 支持的任意模型。
      CHAT_MODEL=gpt-4o 
      EMBEDDING_MODEL=text-embedding-3-small
      # 配置统一 API base
      # 后端 api_key 完全遵循 litellm 规范。
      OPENAI_API_BASE=<你的统一 api base>
      OPENAI_API_KEY=<替换为你的 openai api key>

选项 2：分别配置聊天与嵌入模型的 API base
------------------------------------------

   .. code-block:: Properties

      # 设置为 LiteLLM 支持的任意模型。
      
      # 聊天模型：
      CHAT_MODEL=gpt-4o 
      OPENAI_API_BASE=<你的聊天 api base>
      OPENAI_API_KEY=<替换为你的 openai api key>

      # 嵌入模型：
      # 以 siliconflow 为例，也可用其他提供商。
      # 注意：嵌入模型需加 litellm_proxy 前缀
      EMBEDDING_MODEL=litellm_proxy/BAAI/bge-large-en-v1.5
      LITELLM_PROXY_API_KEY=<替换为你的 siliconflow api key>
      LITELLM_PROXY_API_BASE=https://api.siliconflow.cn/v1

必要参数包括：

- `CHAT_MODEL`：聊天模型名称。
- `EMBEDDING_MODEL`：嵌入模型名称。
- `OPENAI_API_BASE`：API 基础地址。如果 `EMBEDDING_MODEL` 未以 `litellm_proxy/` 开头，则用于聊天和嵌入模型；否则仅用于聊天模型。

可选参数（当嵌入模型与聊天模型提供商不同需填写）：

- `LITELLM_PROXY_API_KEY`：嵌入模型的 API key，若 `EMBEDDING_MODEL` 以 `litellm_proxy/` 开头则必填。
- `LITELLM_PROXY_API_BASE`：嵌入模型的 API base，若 `EMBEDDING_MODEL` 以 `litellm_proxy/` 开头则必填。

**注意：** 若嵌入模型与聊天模型来自不同提供商，需在 `EMBEDDING_MODEL` 名称前加 `litellm_proxy/` 前缀。

`CHAT_MODEL` 和 `EMBEDDING_MODEL` 参数会传递给 LiteLLM 的 completion 函数。

因此，使用不同提供商的模型时，请先查阅 LiteLLM 的接口配置，确保模型名称与 LiteLLM 支持的名称一致。

此外，还需为相应模型提供商设置额外参数，参数名需与 LiteLLM 要求一致。

例如，若使用 DeepSeek 模型，需如下设置：

   .. code-block:: Properties

      # 某些模型 LiteLLM 需加前缀。
      CHAT_MODEL=deepseek/deepseek-chat
      DEEPSEEK_API_KEY=<替换为你的 deepseek api key>

此外，若使用推理模型，返回结果可能包含思考过程。此时需设置如下环境变量：
   
   .. code-block:: Properties
      
      REASONING_THINK_RM=True

更多 LiteLLM 配置细节请参考 `官方 LiteLLM 文档 <https://docs.litellm.ai/docs>`_。
