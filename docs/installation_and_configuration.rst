==============================
安装与配置
==============================

安装
============

**安装 RDAgent**：针对不同场景

- 对于纯粹的用户：请使用 ``pip install rdagent`` 来安装 RDAgent
- 对于开发用户：`参见开发 <development.html>`_

**安装 Docker**：RDAgent 专为研发而设计，其行为类似于人类研究员和开发人员。它可以在各种环境中编写和运行代码，主要使用 Docker 来执行代码。这使得其余的依赖项保持简单。用户在尝试大多数场景之前必须确保已安装 Docker。请参阅 `官方 🐳Docker 页面 <https://docs.docker.com/engine/install/>`_ 获取安装说明。
确保当前用户可以 **不使用 sudo** 运行 Docker 命令。您可以通过执行 `docker run hello-world` 来验证这一点。

LiteLLM 后端配置 (默认)
=======================================

.. note::
   🔥 **注意**：我们现在提供对 **DeepSeek** 模型的实验性支持！您可以使用 DeepSeek 的官方 API 进行经济高效的高性能推理。有关 DeepSeek 设置，请参见下面的配置示例。

选项 1：两种模型的统一 API base
------------------------------------------

   .. code-block:: Properties

      # 设置为 LiteLLM 支持的任何模型。
      CHAT_MODEL=gpt-4o 
      EMBEDDING_MODEL=text-embedding-3-small
      # 配置统一的 API base
      # 后端 api_key 完全遵循 litellm 的约定。
      OPENAI_API_BASE=<your_unified_api_base>
      OPENAI_API_KEY=<replace_with_your_openai_api_key>

选项 2：聊天和嵌入模型的独立 API base
----------------------------------------------------------

   .. code-block:: Properties

      # 设置为 LiteLLM 支持的任何模型。
      
      # 聊天模型:
      CHAT_MODEL=gpt-4o 
      OPENAI_API_BASE=<your_chat_api_base>
      OPENAI_API_KEY=<replace_with_your_openai_api_key>

      # 嵌入模型:
      # 以 siliconflow 为例，您可以使用其他提供商。
      # 注意：嵌入需要 litellm_proxy 前缀
      EMBEDDING_MODEL=litellm_proxy/BAAI/bge-large-en-v1.5
      LITELLM_PROXY_API_KEY=<replace_with_your_siliconflow_api_key>
      LITELLM_PROXY_API_BASE=https://api.siliconflow.cn/v1

配置示例：DeepSeek 设置
-------------------------------------

许多用户在设置 DeepSeek 时遇到配置错误。以下是一个完整的有效示例：

   .. code-block:: Properties

      # 聊天模型: 使用 DeepSeek 官方 API
      CHAT_MODEL=deepseek/deepseek-chat 
      DEEPSEEK_API_KEY=<replace_with_your_deepseek_api_key>

      # 嵌入模型: 使用 SiliconFlow 进行嵌入，因为 DeepSeek 没有嵌入模型。
      # 注意：嵌入需要 litellm_proxy 前缀
      EMBEDDING_MODEL=litellm_proxy/BAAI/bge-m3
      LITELLM_PROXY_API_KEY=<replace_with_your_siliconflow_api_key>
      LITELLM_PROXY_API_BASE=https://api.siliconflow.cn/v1

必要的参数包括：

- `CHAT_MODEL`: 聊天模型的模型名称。

- `EMBEDDING_MODEL`: 嵌入模型的模型名称。

- `OPENAI_API_BASE`: API 的基本 URL。如果 `EMBEDDING_MODEL` 不以 `litellm_proxy/` 开头，则此 URL 用于聊天和嵌入模型；否则，仅用于 `CHAT_MODEL`。

可选参数（如果您的嵌入模型由不同于 `CHAT_MODEL` 的提供商提供，则为必需）：

- `LITELLM_PROXY_API_KEY`: 嵌入模型的 API 密钥，如果 `EMBEDDING_MODEL` 以 `litellm_proxy/` 开头，则为必需。

- `LITELLM_PROXY_API_BASE`: 嵌入模型的基本 URL，如果 `EMBEDDING_MODEL` 以 `litellm_proxy/` 开头，则为必需。

**注意：** 如果您使用的嵌入模型来自与聊天模型不同的提供商，请记住在 `EMBEDDING_MODEL` 名称前添加 `litellm_proxy/` 前缀。


`CHAT_MODEL` 和 `EMBEDDING_MODEL` 参数将传递给 LiteLLM 的 completion 函数。

因此，在使用不同提供商提供的模型时，请首先查看 LiteLLM 的接口配置。模型名称必须与 LiteLLM 允许的名称匹配。

此外，您需要为相应的模型提供商设置其他参数，并且参数名称必须与 LiteLLM 要求的名称一致。

例如，如果您使用的是 DeepSeek 模型，则需要进行如下设置：

   .. code-block:: Properties

      # 对于某些模型，LiteLLM 要求在模型名称前加上前缀。
      CHAT_MODEL=deepseek/deepseek-chat
      DEEPSEEK_API_KEY=<replace_with_your_deepseek_api_key>

此外，当您使用推理模型时，响应可能包含思考过程。对于这种情况，您需要设置以下环境变量：
   
   .. code-block:: Properties
      
      REASONING_THINK_RM=True

有关 LiteLLM 要求的更多详细信息，请参阅 `官方 LiteLLM 文档 <https://docs.litellm.ai/docs>`_。

配置示例 2：Azure OpenAI 设置
-------------------------------------------
以下是专门针对 Azure OpenAI 的示例配置，基于 `官方 LiteLLM 文档 <https://docs.litellm.ai/docs>`_：

如果您正在使用 Azure OpenAI，以下是使用 Python SDK 的一个有效示例，遵循 `LiteLLM Azure OpenAI 文档 <https://docs.litellm.ai/docs/providers/azure/>`_：

   .. code-block:: Properties

      from litellm import completion
      import os
      
      # 设置 Azure OpenAI 环境变量
      os.environ["AZURE_API_KEY"] = "<your_azure_api_key>"
      os.environ["AZURE_API_BASE"] = "<your_azure_api_base>"
      os.environ["AZURE_API_VERSION"] = "<version>"
      
      # 向您的 Azure 部署发出请求
      response = completion(
        "azure/<your_deployment_name>",
        messages = [{ "content": "Hello, how are you?", "role": "user" }]
      )

为了与上面的 Python SDK 示例保持一致，您可以根据 `response` 模型设置配置 `CHAT_MODEL`，并通过将相应的 `os.environ` 变量写入本地 `.env` 文件来使用它们，如下所示：

   .. code-block:: Properties

      cat << EOF > .env
      # 聊天模型: 通过 LiteLLM 的 Azure OpenAI
      CHAT_MODEL=azure/<your_deployment_name>
      AZURE_API_BASE=https://<your_azure_base>.openai.azure.com/
      AZURE_API_KEY=<your_azure_api_key>
      AZURE_API_VERSION=<version>
      
      # 嵌入模型: 通过 litellm_proxy 使用 SiliconFlow
      EMBEDDING_MODEL=litellm_proxy/BAAI/bge-large-en-v1.5
      LITELLM_PROXY_API_KEY=<your_siliconflow_api_key>
      LITELLM_PROXY_API_BASE=https://api.siliconflow.cn/v1
      EOF

此配置允许您通过 LiteLLM 调用 Azure OpenAI，同时使用外部提供商（例如 SiliconFlow）进行嵌入。

如果您的 `Azure OpenAI API Key` 支持 `embedding model`，您可以参考以下配置示例。

   .. code-block:: Properties

      cat << EOF  > .env
      EMBEDDING_MODEL=azure/<支持嵌入的模型部署>
      CHAT_MODEL=azure/<您的部署名称>
      AZURE_API_KEY=<replace_with_your_openai_api_key>
      AZURE_API_BASE=<your_unified_api_base>
      AZURE_API_VERSION=<azure api version>

配置 (已弃用)
=========================

要运行该应用程序，请在项目的根目录中创建一个 `.env` 文件，并根据您的要求添加环境变量。

如果您使用的是此已弃用版本，则应将 `BACKEND` 设置为 `rdagent.oai.backend.DeprecBackend`。

   .. code-block:: Properties

      BACKEND=rdagent.oai.backend.DeprecBackend

以下是您可以使用的其他一些配置选项：

OpenAI API
------------

这是使用 OpenAI API 的用户的标准配置。

   .. code-block:: Properties

      OPENAI_API_KEY=<your_api_key>
      EMBEDDING_MODEL=text-embedding-3-small
      CHAT_MODEL=gpt-4-turbo

Azure OpenAI
------------

以下环境变量是使用 OpenAI API 的用户的标准配置选项。

   .. code-block:: Properties

      USE_AZURE=True

      EMBEDDING_OPENAI_API_KEY=<replace_with_your_azure_openai_api_key>
      EMBEDDING_AZURE_API_BASE=  # Azure OpenAI API 的端点。
      EMBEDDING_AZURE_API_VERSION=  # Azure OpenAI API 的版本。
      EMBEDDING_MODEL=text-embedding-3-small

      CHAT_OPENAI_API_KEY=<replace_with_your_azure_openai_api_key>
      CHAT_AZURE_API_BASE=  # Azure OpenAI API 的端点。
      CHAT_AZURE_API_VERSION=  # Azure OpenAI API 的版本。
      CHAT_MODEL=  # Azure OpenAI API 的模型名称。

使用 Azure 令牌提供程序
------------------------

如果您使用的是 Azure 令牌提供程序，则需要将 `CHAT_USE_AZURE_TOKEN_PROVIDER` 和 `EMBEDDING_USE_AZURE_TOKEN_PROVIDER` 环境变量设置为 `True`。然后
使用 `Azure 配置部分 <installation_and_configuration.html#azure-openai>`_ 中提供的环境变量。


☁️ Azure 配置
- 安装 Azure CLI：

   ```sh
   curl -L https://aka.ms/InstallAzureCli | bash
   ```

- 登录 Azure：

   ```sh
   az login --use-device-code
   ```

- `exit` 并重新登录到您的环境（此步骤可能不是必需的）。


配置列表
------------------

.. TODO: use `autodoc-pydantic` .

- OpenAI API 设置

+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| 配置选项              | 含义                                                         | 默认值           |
+===================================+=================================================================+=========================+
| OPENAI_API_KEY                    | 聊天和嵌入模型的 API 密钥                      | None                    |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| EMBEDDING_OPENAI_API_KEY          | 为嵌入模型使用不同的 API 密钥                     | None                    |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| CHAT_OPENAI_API_KEY               | 设置为聊天模型使用不同的 API 密钥                   | None                    |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| EMBEDDING_MODEL                   | 嵌入模型的名称                                     | text-embedding-3-small  |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| CHAT_MODEL                        | 聊天模型的名称                                          | gpt-4-turbo             |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| EMBEDDING_AZURE_API_BASE          | Azure OpenAI API 的基本 URL                               | None                    |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| EMBEDDING_AZURE_API_VERSION       | Azure OpenAI API 的版本                                 | None                    |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| CHAT_AZURE_API_BASE               | Azure OpenAI API 的基本 URL                               | None                    |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| CHAT_AZURE_API_VERSION            | Azure OpenAI API 的版本                                 | None                    |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| USE_AZURE                         | 如果您使用的是 Azure OpenAI，则为 True                              | False                   |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| CHAT_USE_AZURE_TOKEN_PROVIDER     | 如果您在聊天模型中使用 Azure 令牌提供程序，则为 True     | False                   |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+
| EMBEDDING_USE_AZURE_TOKEN_PROVIDER| 如果您在嵌入模型中使用 Azure 令牌提供程序，则为 True| False                   |
+-----------------------------------+-----------------------------------------------------------------+-------------------------+

- 全局设置

+-----------------------------+--------------------------------------------------+-------------------------+
| 配置选项        | 含义                                          | 默认值           |
+=============================+==================================================+=========================+
| max_retry                   | 重试的最大次数                 | 10                      |
+-----------------------------+--------------------------------------------------+-------------------------+
| retry_wait_seconds          | 重试前等待的秒数        | 1                       |
+-----------------------------+--------------------------------------------------+-------------------------+
+ log_trace_path              | 日志跟踪文件的路径                           | None                    |
+-----------------------------+--------------------------------------------------+-------------------------+
+ log_llm_chat_content        | 指示是否记录聊天内容的标志       | True                    |
+-----------------------------+--------------------------------------------------+-------------------------+


- 缓存设置

.. TODO: update Meaning for caches

+------------------------------+--------------------------------------------------+-------------------------+
| 配置选项         | 含义                                          | 默认值           |
+==============================+==================================================+=========================+
| dump_chat_cache              | 指示是否转储聊天缓存的标志         | False                   |
+------------------------------+--------------------------------------------------+-------------------------+
| dump_embedding_cache         | 指示是否转储嵌入缓存的标志    | False                   |
+------------------------------+--------------------------------------------------+-------------------------+
| use_chat_cache               | 指示是否使用聊天缓存的标志           | False                   |
+------------------------------+--------------------------------------------------+-------------------------+
| use_embedding_cache          | 指示是否使用嵌入缓存的标志      | False                   |
+------------------------------+--------------------------------------------------+-------------------------+
| prompt_cache_path            | 提示缓存的路径                             | ./prompt_cache.db       |
+------------------------------+--------------------------------------------------+-------------------------+
| max_past_message_include     | 要包括的最大过去消息数       | 10                      |
+------------------------------+--------------------------------------------------+-------------------------+




加载配置
---------------------

为方便用户，我们提供了一个名为 `rdagent` 的 CLI 界面，它会自动运行 `load_dotenv()` 从 `.env` 文件加载环境变量。
但是，默认情况下，此功能未为其他脚本启用。我们建议用户通过以下步骤加载环境：


- ⚙️ 环境配置
    - 将 `.env` 文件放置在与 `.env.example` 文件相同的目录中。
        - `.env.example` 文件包含使用 OpenAI API 的用户所需的环境变量（请注意，`.env.example` 是一个示例文件。`.env` 是最终将使用的文件。）

    - 导出 .env 文件中的每个变量：

      .. code-block:: sh

          export $(grep -v '^#' .env | xargs)
    
    - 如果要更改默认环境变量，可以参考上述配置并编辑 `.env` 文件。
