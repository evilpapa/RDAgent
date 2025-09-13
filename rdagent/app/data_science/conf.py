from typing import Literal

from pydantic_settings import SettingsConfigDict

from rdagent.app.kaggle.conf import KaggleBasePropSetting


class DataScienceBasePropSetting(KaggleBasePropSetting):
    # TODO: Kaggle 设置应该是 DataScience 的子类
    model_config = SettingsConfigDict(env_prefix="DS_", protected_namespaces=())

    # 主要组件
    ## Scen
    scen: str = "rdagent.scenarios.data_science.scen.KaggleScen"
    """
    数据科学任务的场景类。
    - 对于 Kaggle 竞赛，请使用："rdagent.scenarios.data_science.scen.KaggleScen"
    - 对于自定义数据科学场景，请使用："rdagent.scenarios.data_science.scen.DataScienceScen"
    """

    planner: str = "rdagent.scenarios.data_science.proposal.exp_gen.planner.DSExpPlannerHandCraft"
    hypothesis_gen: str = "rdagent.scenarios.data_science.proposal.exp_gen.router.ParallelMultiTraceExpGen"
    trace_scheduler: str = "rdagent.scenarios.data_science.proposal.exp_gen.trace_scheduler.RoundRobinScheduler"
    """假设生成类"""

    summarizer: str = "rdagent.scenarios.data_science.dev.feedback.DSExperiment2Feedback"
    summarizer_init_kwargs: dict = {
        "version": "exp_feedback",
    }
    ## 工作流相关
    consecutive_errors: int = 5

    ## 编码相关
    coding_fail_reanalyze_threshold: int = 3

    debug_recommend_timeout: int = 600
    """在调试数据上运行的建议时间限制"""
    debug_timeout: int = 600
    """在调试数据上运行的超时限制"""
    full_recommend_timeout: int = 3600
    """在完整数据上运行的建议时间限制"""
    full_timeout: int = 3600
    """在完整数据上运行的超时限制"""

    #### 模型转储
    enable_model_dump: bool = False
    enable_doc_dev: bool = False
    model_dump_check_level: Literal["medium", "high"] = "medium"

    ### 特定功能

    ### notebook 集成
    enable_notebook_conversion: bool = False

    #### 启用规范
    spec_enabled: bool = True

    #### 提案相关
    # proposal_version: str = "v2" 已弃用

    coder_on_whole_pipeline: bool = True
    max_trace_hist: int = 3

    coder_max_loop: int = 10
    runner_max_loop: int = 3

    sample_data_by_LLM: bool = True
    use_raw_description: bool = False
    show_nan_columns: bool = False

    ### 知识库
    enable_knowledge_base: bool = False
    knowledge_base_version: str = "v1"
    knowledge_base_path: str | None = None
    idea_pool_json_path: str | None = None

    ### 每次循环后归档日志文件夹
    enable_log_archive: bool = True
    log_archive_path: str | None = None
    log_archive_temp_path: str | None = (
        None  # 这是为了存储中间 tar 文件，因为在本地存储中写入 tar 文件比复制到目标存储更可取
    )

    #### 测试相关评估
    eval_sub_dir: str = "eval"  # TODO: 修复我，这不是一个好名字
    """我们将使用 f"{DS_RD_SETTING.local_data_path}/{DS_RD_SETTING.eval_sub_dir}/{competition}"
    来查找评估测试提交的脚本"""

    """---以下是多跟踪的设置---"""

    ### 多跟踪相关
    max_trace_num: int = 1
    """合并前要增长的最大跟踪数"""

    scheduler_temperature: float = 1.0
    """用于 softmax 计算的跟踪调度程序的温度，在 ProbabilisticScheduler 中使用"""

    #### 多跟踪：检查点选择器
    selector_name: str = "rdagent.scenarios.data_science.proposal.exp_gen.select.expand.LatestCKPSelector"
    """要使用的选择器的名称"""
    sota_count_window: int = 5
    """要考虑 SOTA 计数的试验次数"""
    sota_count_threshold: int = 1
    """SOTA 计数的阈值"""

    #### 多跟踪：SOTA 实验选择器
    sota_exp_selector_name: str = "rdagent.scenarios.data_science.proposal.exp_gen.select.submit.GlobalSOTASelector"
    """要使用的 SOTA 实验选择器的名称"""

    ### 多跟踪：为多跟踪注入最优值
    # 在启动新的子跟踪时注入多样性
    enable_inject_diverse: bool = False

    # 在启动新的子跟踪时从其他跟踪注入多样性
    enable_cross_trace_diversity: bool = True
    """在启动新的子跟踪时启用跨跟踪多样性注入。
    这与用于非并行情况的 `enable_inject_diverse` 不同。"""

    diversity_injection_strategy: str = (
        "rdagent.scenarios.data_science.proposal.exp_gen.diversity_strategy.InjectUntilSOTAGainedStrategy"
    )
    """用于注入多样性上下文的策略。"""

    # 为多跟踪启用不同版本的 DSExpGen
    enable_multi_version_exp_gen: bool = False
    exp_gen_version_list: str = "v3,v2"

    #### 多跟踪：最终多跟踪合并的时间
    merge_hours: float = 0
    """合并时间"""

    #### 多跟踪：最大 SOTA 检索数，在 AutoSOTAexpSelector 中使用
    # 限制要检索的 SOTA 实验的数量，否则检索过多的 SOTA 实验将导致超出 LLM 的上下文窗口
    max_sota_retrieved_num: int = 10
    """在 LLM 调用中检索的 SOTA 实验的最大数量"""

    #### 在第一个 sota 实验前启用草稿
    enable_draft_before_first_sota: bool = False
    enable_planner: bool = False

    model_architecture_suggestion_time_percent: float = 0.75
    allow_longer_timeout: bool = False
    coder_enable_llm_decide_longer_timeout: bool = False
    runner_enable_llm_decide_longer_timeout: bool = False
    coder_longer_timeout_multiplier_upper: int = 3
    runner_longer_timeout_multiplier_upper: int = 2
    coder_timeout_increase_stage: float = 0.3
    runner_timeout_increase_stage: float = 0.3
    runner_timeout_increase_stage_patience: int = 2
    """在升级到下一个超时级别（阶段宽度）之前容忍的失败次数。每 'patience' 次失败，超时增加 'runner_timeout_increase_stage'"""
    show_hard_limit: bool = True

    #### 启用运行器代码更改摘要
    runner_enable_code_change_summary: bool = True

    ### 提案工作流相关

    #### 假设生成相关
    enable_simple_hypothesis: bool = False
    """如果为 true，则生成简单的假设，每个假设不超过 2 句话。"""

    enable_generate_unique_hypothesis: bool = False
    """启用生成唯一假设。如果为 True，则为每个组件生成唯一假设。如果为 False，则为每个组件生成唯一假设。"""

    #### 假设批判和重写
    enable_hypo_critique_rewrite: bool = False
    """启用假设批判和重写阶段以提高假设质量"""
    enable_scale_check: bool = False

    ##### 选择相关
    ratio_merge_or_ensemble: int = 70
    """被视为有效解决方案的合并或集成的比率"""
    llm_select_hypothesis: bool = False
    """是否使用 LLM 选择假设。如果为 True，则使用 LLM 选择；如果为 False，则使用现有的排名方法。"""

    #### 任务生成相关
    fix_seed_and_data_split: bool = False

    ensemble_time_upper_bound: bool = False


DS_RD_SETTING = DataScienceBasePropSetting()

# enable_cross_trace_diversity 和 llm_select_hypothesis 不应同时为 true
assert not (
    DS_RD_SETTING.enable_cross_trace_diversity and DS_RD_SETTING.llm_select_hypothesis
), "enable_cross_trace_diversity 和 llm_select_hypothesis 不能同时为 true"
