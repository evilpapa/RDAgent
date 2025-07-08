# 3.1 场景示例：数据科学 (Data Science) Kaggle 竞赛流程解析

本节将以数据科学（特指Kaggle竞赛）场景为例，分析 RD-Agent 如何通过其核心组件和流程自动化完成一个典型的机器学习项目。

## 1. 入口与初始化

- **命令行入口**: `rdagent/app/data_science/loop.py` 中的 `main()` 函数是用户与数据科学智能体交互的起点。用户可以通过命令行参数指定诸如Kaggle竞赛名称 (`competition`)、是否从断点恢复 (`path`, `checkout`)、运行的迭代次数 (`loop_n`, `step_n`) 等。
- **核心循环类**: `DataScienceRDLoop` (定义在 `rdagent/scenarios/data_science/loop.py`) 是此场景下 R&D 循环的具体实现。`main()` 函数会实例化或加载此类。
- **配置加载**: 相关的配置信息（如LLM参数、特定场景参数）会通过 `DS_RD_SETTING` (来自 `rdagent/app/data_science/conf.py`) 和 `RD_AGENT_SETTINGS` (来自 `rdagent/core/conf.py`) 加载。
- **组件初始化**: 在 `DataScienceRDLoop.__init__()` 中，会进行以下关键组件的初始化：
    - **场景 (`Scenario`)**: 根据竞赛名称实例化一个特定的场景对象 (例如，一个实现了 `rdagent/core/scenario/Scenario` 接口的Kaggle竞赛场景类)。
    - **实验生成器 (`ExpGen`)**: 例如 `DSProposalV1ExpGen` 或 `DSProposalV2ExpGen`，负责提出新的实验方案。
    - **选择器 (`CheckpointSelector`, `SOTAexpSelector`)**: 用于从历史轨迹中选择下一步的起点和最终的最佳方案。
    - **轨迹记录器 (`DSTrace`)**: 用于记录整个研发过程中的所有实验和反馈。
    - **知识库 (`DSKnowledgeBase`)**: (可选) 用于存储和检索从先前经验中学到的知识。
    - **Coder组件**: 一系列基于 `CoSTEER` 架构的编码器，每个针对数据科学流程中的一个特定环节：
        - `DataLoaderCoSTEER`: 负责数据加载和初步预处理。
        - `FeatureCoSTEER`: 负责特征工程。
        - `ModelCoSTEER`: 负责模型选择、训练和调优。
        - `EnsembleCoSTEER`: 负责集成学习。
        - `WorkflowCoSTEER`: 负责将不同部分串联成工作流。
        - `PipelineCoSTEER`: 负责构建和管理整个端到端的数据科学流水线。
    - **运行器 (`DSCoSTEERRunner`)**: 负责在特定环境（通常是Docker）中执行由Coder生成的代码。
    - **反馈生成器 (`DSExperiment2Feedback`)**: 负责分析实验结果并生成结构化的反馈。

## 2. R&D 迭代循环

`DataScienceRDLoop` 继承自 `RDLoop`，其核心 `run()` 方法会按顺序驱动以下几个阶段的执行：

### 阶段一：提议 (Proposal Generation - `direct_exp_gen` 方法)

1.  **SOTA与检查点选择**:
    - `SOTAexpSelector` 从历史轨迹 `trace` 中选出当前最佳的实验（State-of-the-Art, SOTA）。
    - `CheckpointSelector` 根据预设策略（例如，从最新的成功实验、从特定分支、或从头开始）选择一个历史实验作为当前迭代的起点或父节点。这个选择会更新 `trace.current_selection`。
2.  **实验生成**:
    - 调用 `ExpGen` 实例 (例如 `DSProposalV2ExpGen`) 的 `async_gen(trace, self)` 方法。
    - `ExpGen` 会分析 `trace` 中的历史信息（过去的实验、反馈、当前场景描述、知识库中的知识），并结合LLM的能力，**生成一个新的 `DSExperiment` 对象**。
    - 这个新的 `DSExperiment` 对象代表了一个“实验方案”或“研究想法”。它通常包含：
        - 一个或多个待解决的**子任务 (`sub_tasks`)**，例如：`DataLoaderTask`, `FeatureTask`, `ModelTask`。这些任务描述了接下来需要智能体完成的具体工作。
        - （可选）关联的 `Hypothesis` (原始想法)。
        - （可选）对先前实验的引用 (`based_experiments`)。
    - 例如，`ExpGen` 可能提议：“尝试使用LightGBM模型，并对特征A和B进行交叉组合”。这会转化为包含 `FeatureTask` 和 `ModelTask` 的 `DSExperiment`。

### 阶段二：编码 (Coding - `coding` 方法)

1.  **任务分发**:
    - 获取上一阶段生成的 `DSExperiment` 对象。
    - 遍历其实例属性 `pending_tasks_list` 中包含的每一个子任务 (`sub_tasks`，例如 `[FeatureTask(description="Create interaction features"), ModelTask(description="Train LightGBM")]`)。
2.  **Coder执行**:
    - 根据当前子任务的类型，将其分派给对应的 `CoSTEER` Coder 组件：
        - 如果是 `DataLoaderTask` -> `self.data_loader_coder.develop(exp)`
        - 如果是 `FeatureTask`    -> `self.feature_coder.develop(exp)`
        - 如果是 `ModelTask`      -> `self.model_coder.develop(exp)`
        - ...以此类推。
    - **`Coder.develop(exp)` 的核心工作**:
        - Coder（通常是一个基于LLM的智能体）会接收当前的 `DSExperiment` 对象（包含任务描述、历史代码、反馈等上下文）。
        - 它会**生成或修改代码**来实现这个子任务。例如，`FeatureCoSTEER` 可能会生成Python代码片段来实现特征交叉。
        - 生成的代码会被写入到与 `DSExperiment` 关联的 `FBWorkspace` (文件工作空间) 中。`FBWorkspace` 会管理这些代码文件（例如，`feature_engineering.py`, `model_training.py`）。
        - `DSExperiment` 对象会被**就地修改**，其 `sub_workspace_list` 中对应当前子任务的条目会被填充为包含生成代码的 `FBWorkspace` 实例。

### 阶段三：运行 (Running - `running` 方法)

1.  **执行准备**:
    - 获取经过 `coding` 阶段处理的 `DSExperiment` 对象。此时，其实验工作空间 (`experiment_workspace` 或 `sub_workspace_list` 中的工作空间) 应该已经包含了可执行的代码。
2.  **实验执行**:
    - 如果 `exp.is_ready_to_run()` 返回 `True` (表示所有必要的代码和配置已就绪)：
        - 调用 `self.runner.develop(exp)` (这里的 `runner` 是 `DSCoSTEERRunner` 实例)。
        - **`DSCoSTEERRunner.develop(exp)` 的核心工作**:
            - 它会获取 `DSExperiment` 中的工作空间 (`FBWorkspace`)。
            - 在一个预定义的环境中（通常是为Kaggle竞赛配置好的Docker容器，定义在 `rdagent/scenarios/data_science/sing_docker/`）执行工作空间中的代码。执行的入口点可能是一个主脚本（例如 `main.py` 或 `train.py`）。
            - 收集代码执行的标准输出 (stdout)、标准错误 (stderr)、退出码，以及任何生成的关键文件（如模型文件、预测结果文件 `submission.csv`、日志文件、性能指标文件）。
            - 这些运行结果会被更新回 `DSExperiment` 对象的 `running_info` 属性或其工作空间的特定位置。
3.  **文档化 (可选)**:
    - 如果启用了 `DS_RD_SETTING.enable_doc_dev`，则会调用 `self.docdev.develop(exp)` 来自动生成或更新与此实验相关的文档。

### 阶段四：反馈 (Feedback Generation - `feedback` 方法)

1.  **结果分析**:
    - 获取经过 `running` 阶段并已执行完毕的 `DSExperiment` 对象。
    - 调用 `self.summarizer.generate_feedback(exp, self.trace)` (这里的 `summarizer` 是 `DSExperiment2Feedback` 实例)。
2.  **`DSExperiment2Feedback.generate_feedback()` 的核心工作**:
    - 它会分析 `DSExperiment` 中的运行结果（例如，模型在验证集上的得分、代码是否成功运行、错误日志等）。
    - 结合历史轨迹 `trace` 和当前场景信息。
    - 生成一个结构化的 `ExperimentFeedback` 对象。此对象包含：
        - `decision: bool`: 对本次实验尝试的总体评价（例如，是否比之前的SOTA更好？是否值得继续这个方向？）。
        - `reason: str`: 做出此决策的原因。
        - `observations: str`: 从实验结果中得出的关键观察。
        - `hypothesis_evaluation: str`: 对最初驱动此实验的假设的评估。
        - `new_hypothesis: str`: (如果适用) 基于当前结果提出的新的或改进的假设，用于指导下一轮迭代。
        - 其他如 `code_change_summary`, `exception` 等。

### 阶段五：记录 (Recording - `record` 方法)

1.  **异常处理**: 检查上一个阶段是否发生异常，并相应地处理 `ExperimentFeedback`。
2.  **轨迹更新**:
    - 将当前迭代产生的 `(DSExperiment, ExperimentFeedback)` 对追加到 `self.trace.hist` 列表中。
    - 更新 `self.trace.dag_parent` 来记录当前实验与其父实验（检查点）的关系。
3.  **知识库更新 (可选)**:
    - 如果启用了知识库 (`DS_RD_SETTING.enable_knowledge_base`)，则调用 `self.trace.knowledge_base.dump()` 将更新后的知识（可能由RAG策略在`ExpGen`阶段学习到）持久化。
4.  **日志与工作空间归档 (可选)**:
    - 如果启用了归档 (`DS_RD_SETTING.enable_log_archive`)，则会将当前的日志文件和工作空间文件夹进行压缩和备份。
    - 为了节省空间，归档前可能会对工作空间进行清理，只保留必要的代码和结果文件。

## 3. 循环与终止

- RD-Agent 会重复执行上述R&D迭代循环（提议 -> 编码 -> 运行 -> 反馈 -> 记录）。
- 循环的终止条件由用户在启动时设置的参数（如 `loop_n`, `step_n`, `all_duration`）或内部错误/用户中断决定。
- 在每次循环中，智能体通过分析历史反馈和当前场景，不断迭代和优化其解决方案（代码、模型、特征等），力求在Kaggle竞赛中取得更好的成绩。

这个流程清晰地展示了RD-Agent如何模拟一个数据科学家的研发过程：从提出想法，到编写代码实现，到运行实验验证，再到分析结果并形成新的认知，从而驱动下一轮的探索和改进。各种 `CoSTEER` 组件、`Runner`、`Trace`、`Feedback` 机制是实现这一自动化闭环的关键。

## 4. Data Science 场景特定配置与运行

根据 `docs/scens/data_science.rst` 文档，运行数据科学智能体时，有一些特定的环境变量和命令需要注意。

### 4.1 环境变量设置 (通过 `.env` 文件或直接导出)

-   **数据存储路径**:
    ```bash
    # 示例：将数据存储在项目下的 ds_data 文件夹
    DS_LOCAL_DATA_PATH=<你的本地数据存储目录>/ds_data
    # 例如: dotenv set DS_LOCAL_DATA_PATH $(pwd)/ds_data
    ```
    RD-Agent会在此路径下查找或下载竞赛数据。

-   **场景类指定**:
    ```bash
    DS_SCEN=rdagent.scenarios.data_science.scen.DataScienceScen
    ```
    这个变量告诉框架使用哪个 Python 类来处理数据科学场景的特定逻辑。

-   **数据来源与处理方式**:
    -   **是否使用MLE-bench数据**:
        ```bash
        # 如果设置为 True，RD-Agent 会尝试自动从 MLE-bench 下载和准备数据
        # 这通常需要配置好 Kaggle API (见下文)
        DS_IF_USING_MLE_DATA=True
        # 如果使用自定义数据集 (如文档中示例)，则设置为 False
        # DS_IF_USING_MLE_DATA=False
        ```
    -   **Coder是否处理完整流水线**:
        ```bash
        # 如果为 True，则期望 Coder 组件能生成或处理从数据加载到提交的完整流水线代码
        DS_CODER_ON_WHOLE_PIPELINE=True
        ```
    -   **Coder执行环境类型**:
        ```bash
        # 指定 CoSTEER Coder 生成的代码在何种环境中执行，通常是 'docker'
        DS_CODER_COSTEER_ENV_TYPE=docker
        ```

-   **Kaggle API 配置 (使用 MLE-bench 或需要下载竞赛数据时)**:
    1.  登录 Kaggle 账户。
    2.  进入个人设置 (Account -> Settings)。
    3.  点击 "Create New Token" 下载 `kaggle.json` 文件。
    4.  将 `kaggle.json` 文件移动到 `~/.kaggle/` 目录下 (如果目录不存在则创建: `mkdir -p ~/.kaggle && mv kaggle.json ~/.kaggle/`)。
    5.  修改文件权限: `chmod 600 ~/.kaggle/kaggle.json`。
    6.  (重要) 确保您已通过Kaggle网站加入了目标竞赛，否则API可能无法下载数据。

-   **LLM模型定制 (可选)**:
    可以通过 `LITELLM_CHAT_MODEL_MAP` 环境变量为开发流程中的不同阶段（或不同Coder）指定不同的LLM模型。具体格式和用法需参考框架内部实现或更详细的文档。

### 4.2 运行命令

-   **启动数据科学智能体**:
    ```bash
    # 将 <竞赛ID> 替换为实际的 Kaggle 竞赛 ID，例如 sf-crime, titanic
    rdagent data_science --competition <竞赛ID>
    ```
    或者，如果通过 `dotenv` 管理 `.env` 文件并从源码运行：
    ```bash
    dotenv run -- python rdagent/app/data_science/loop.py --competition <竞赛ID>
    ```

-   **查看运行日志和结果**:
    -   **命令行日志**: RD-Agent 会在控制台输出详细的运行日志。
    -   **结构化日志与UI**:
        -   **评分/总结**:
            ```bash
            # 将 <日志路径> 替换为实际的日志输出目录 (通常是 log/ 或 .logs/)
            dotenv run -- python rdagent/log/mle_summary.py grade <日志路径>
            ```
        -   **可视化Web UI**: RD-Agent 提供了基于 Streamlit 的 Web UI 来可视化研发流程和结果。
            ```bash
            streamlit run rdagent/log/ui/dsapp.py -- --log_dir <你的日志目录>
            # 或者，如果 streamlit 在 conda 环境的 rdagent 中
            # conda activate rdagent
            # streamlit run rdagent/log/ui/dsapp.py -- --log_dir <你的日志目录>
            ```
            注意 `dsapp.py` 可能需要通过 `--log_dir` 参数指定日志目录。

### 4.3 自定义数据集示例结构

如果使用自定义数据集 (设置 `DS_IF_USING_MLE_DATA=False`)，数据应按特定结构组织，如 `docs/scens/data_science.rst` 中所示例：

```
<DS_LOCAL_DATA_PATH>/
├── eval/                     # 评估相关文件 (可选，用于本地自定义评估)
│   └── <competition_name>/
│       ├── grade.py          # 本地评分脚本
│       ├── valid.py          # (可能)验证集生成或处理脚本
│       └── test.csv          # (可能)用于本地验证的测试集标签 (如果与官方不同)
└── <competition_name>/       # 竞赛主数据文件夹
    ├── train.csv             # 训练数据
    ├── test.csv              # 测试数据 (无标签)
    ├── sample_submission.csv # 提交文件示例格式
    ├── description.md        # 竞赛描述文件 (RD-Agent可能会读取以理解任务)
    └── sample.py             # (可能)官方提供的简单基线代码示例
```

确保 `<DS_LOCAL_DATA_PATH>` 和 `<competition_name>` 与您的设置和实际情况相符。`description.md` 对Agent理解任务目标和数据格式可能很重要。
