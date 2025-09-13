# 更新日志

## [0.7.0](https://github.com/microsoft/RD-Agent/compare/v0.6.1...v0.7.0) (2025-07-08)


### 功能

* 添加代码更改摘要 ([#1000](https://github.com/microsoft/RD-Agent/issues/1000)) ([937ec26](https://github.com/microsoft/RD-Agent/commit/937ec263b215928633822c4d76ad4e47442c8198))
* 添加 hide_base_name 选项并更新数据文件夹提示 ([#1004](https://github.com/microsoft/RD-Agent/issues/1004)) ([2f61fa8](https://github.com/microsoft/RD-Agent/commit/2f61fa8cd90c91ad29f320ce9ea6c49f49ac9111))
* 为 DS 场景实验添加了运行时间统计 ([#1007](https://github.com/microsoft/RD-Agent/issues/1007)) ([030abd8](https://github.com/microsoft/RD-Agent/commit/030abd87191377641a678c80852f5ecad84e7a6e))
* 合并代码摘要并支持更多跟踪 ([#1025](https://github.com/microsoft/RD-Agent/issues/1025)) ([48201e7](https://github.com/microsoft/RD-Agent/commit/48201e79b55ff5a98dad51702a7d0ac6b1ddc9eb))
* 显示第一轮演进的代码差异 ([#1009](https://github.com/microsoft/RD-Agent/issues/1009)) ([4844622](https://github.com/microsoft/RD-Agent/commit/4844622e5fd28d7cbaabd9d7888f8204c60b76b3))
* 在整个数据上尝试编码器 ([#1017](https://github.com/microsoft/RD-Agent/issues/1017)) ([4973e05](https://github.com/microsoft/RD-Agent/commit/4973e0532248c6172eec3bb70dffda052af2d14f))


### 错误修复

* 修复 DS 评估中的一个小错误 ([#1012](https://github.com/microsoft/RD-Agent/issues/1012)) ([5a520e9](https://github.com/microsoft/RD-Agent/commit/5a520e9d44899d44fddc0f2e5571596223161b71))
* 修复 quant scen 中的一些错误 ([#1026](https://github.com/microsoft/RD-Agent/issues/1026)) ([7b34d41](https://github.com/microsoft/RD-Agent/commit/7b34d418642d1c0c2986db9ecf6a5d9bc22cc3da))
* 支持对 Deepseek 模型的实验性支持并更新有关配置的文档 ([#1024](https://github.com/microsoft/RD-Agent/issues/1024)) ([35cfc19](https://github.com/microsoft/RD-Agent/commit/35cfc193f9b35d786aeb7585334427ad358c982f))

## [0.6.1](https://github.com/microsoft/RD-Agent/compare/v0.6.0...v0.6.1) (2025-06-28)


### 错误修复

* 修复挂载问题 ([#1001](https://github.com/microsoft/RD-Agent/issues/1001)) ([4ae2f13](https://github.com/microsoft/RD-Agent/commit/4ae2f1303dfcbaea53d459be7c8e85bf85ce5f4f))
* 处理错误的 dag_parant 索引的错误 ([#996](https://github.com/microsoft/RD-Agent/issues/996)) ([bda12ff](https://github.com/microsoft/RD-Agent/commit/bda12ffecf9ae116e0d04eece0c6a1b61413d916))
* 改进日志文件夹排序和选择的用户体验 ([#993](https://github.com/microsoft/RD-Agent/issues/993)) ([b116807](https://github.com/microsoft/RD-Agent/commit/b11680777f116b6c40f9e535e0da10c186c95050))

## [0.6.0](https://github.com/microsoft/RD-Agent/compare/v0.5.0...v0.6.0) (2025-06-26)


### 功能

* 多跟踪的异步机制 ([#981](https://github.com/microsoft/RD-Agent/issues/981)) ([9e60c32](https://github.com/microsoft/RD-Agent/commit/9e60c32cf348481eb55617809c059c359d7603b8))


### 错误修复

* 将异步添加到 direct_exp_gen 以避免无限循环 ([#992](https://github.com/microsoft/RD-Agent/issues/992)) ([78c203d](https://github.com/microsoft/RD-Agent/commit/78c203d8eefbba67fc120b35cb25e85b2200ac49))
* docker 容器清理以防止累积和系统减速 ([#975](https://github.com/microsoft/RD-Agent/issues/975)) ([05cf094](https://github.com/microsoft/RD-Agent/commit/05cf094913e48c903c8a4476d6c609d8bfa10681))
* 修复一个错误并更新文档 ([#978](https://github.com/microsoft/RD-Agent/issues/978)) ([d1ae9e1](https://github.com/microsoft/RD-Agent/commit/d1ae9e1dcc2ccd1ffe05cb1c6db3e905fa70425c))
* 合并 datascience v3 和 v2 ([#974](https://github.com/microsoft/RD-Agent/issues/974)) ([1ba7548](https://github.com/microsoft/RD-Agent/commit/1ba754853ce2010ce1cb0bbd217b67689fa1ebdf))
* 优化细节 ([#979](https://github.com/microsoft/RD-Agent/issues/979)) ([25caa3d](https://github.com/microsoft/RD-Agent/commit/25caa3d00c255286dce27915b9355987b87ed2e8))
* 优化提示 ([#987](https://github.com/microsoft/RD-Agent/issues/987)) ([76df96e](https://github.com/microsoft/RD-Agent/commit/76df96ee88212a8aee7f518b9cacf80591dc2939))

## [0.5.0](https://github.com/microsoft/RD-Agent/compare/v0.4.0...v0.5.0) (2025-06-18)


### 功能

* 为 score_df 中的值是否为 NaN 添加检查 ([#756](https://github.com/microsoft/RD-Agent/issues/756)) ([d9cc780](https://github.com/microsoft/RD-Agent/commit/d9cc78098beb27f3a1bf2f2d461302db177b7d41))
* 添加竞赛级别过滤器并将常量提取到 utils ([#869](https://github.com/microsoft/RD-Agent/issues/869)) ([b40b605](https://github.com/microsoft/RD-Agent/commit/b40b6055368e6c72d8435352104b1c281b06da7f))
* 添加 DocDev 用于自动生成工作区文档 ([#781](https://github.com/microsoft/RD-Agent/issues/781)) ([bcba6ea](https://github.com/microsoft/RD-Agent/commit/bcba6eac32684ebb267c93b4e85dbfa9561d15d1))
* 添加起草流程 ([#832](https://github.com/microsoft/RD-Agent/issues/832)) ([efedddf](https://github.com/microsoft/RD-Agent/commit/efedddf39bc19221fdffc2e39ee0a09097fc82b0))
* 将 last_exp_fb 添加到 DSTrace 并更新反馈检索用法 ([#910](https://github.com/microsoft/RD-Agent/issues/910)) ([10531fd](https://github.com/microsoft/RD-Agent/commit/10531fda9438c6915b26d5013bd2413e1333ceb9))
* 在 RD 循环中添加 mlflow 记录器以进行日志记录 ([#815](https://github.com/microsoft/RD-Agent/issues/815)) ([b91b54f](https://github.com/microsoft/RD-Agent/commit/b91b54f355c26b751087d0c14774f466e82866de))
* 添加朴素实验生成器并更新提案配置 ([#759](https://github.com/microsoft/RD-Agent/issues/759)) ([75494f4](https://github.com/microsoft/RD-Agent/commit/75494f4fed5bc845acfd7f7bacef385f0f96c514))
* 添加 RD-Agent-Quant 场景 ([#838](https://github.com/microsoft/RD-Agent/issues/838)) ([6e42d52](https://github.com/microsoft/RD-Agent/commit/6e42d523a85df67aa13927abbf0894564c71880e))
* 向 LiteLLMAPIBackend 和 LLMSett… 添加 reasoning_effort 参数 ([#754](https://github.com/microsoft/RD-Agent/issues/754)) ([113889f](https://github.com/microsoft/RD-Agent/commit/113889fefe9b09aaea1b564704c81664b8f77ec5))
* 在反馈中添加审阅者 ([#765](https://github.com/microsoft/RD-Agent/issues/765)) ([1a95bee](https://github.com/microsoft/RD-Agent/commit/1a95bee6aa6bc6f45fdeb484f3a6f81caa273038))
* 高级检查点选择器 ([#790](https://github.com/microsoft/RD-Agent/issues/790)) ([50ea033](https://github.com/microsoft/RD-Agent/commit/50ea0336e93d8cb39fb871e81a3f61abdf293bc7))
* 归档工作区中的 python 和 csv 文件以维护结果 ([#814](https://github.com/microsoft/RD-Agent/issues/814)) ([67d0e01](https://github.com/microsoft/RD-Agent/commit/67d0e01e7c9237da1371d93cbf9d86f5f46faac4))
* 检查点选择 ([#744](https://github.com/microsoft/RD-Agent/issues/744)) ([a15a06a](https://github.com/microsoft/RD-Agent/commit/a15a06ad643977db59d7cac9da52e637cf80395a))
* 自定义数据 ([#810](https://github.com/microsoft/RD-Agent/issues/810)) ([6322916](https://github.com/microsoft/RD-Agent/commit/632291608cf605bd8bcfcab0017824823bdecdb8))
* 转储模型 ([#776](https://github.com/microsoft/RD-Agent/issues/776)) ([b49481e](https://github.com/microsoft/RD-Agent/commit/b49481e073e6f536d2b1b3bd2d01229ed05abdea))
* 允许多个跟踪设置不同版本的 idea-proposal ([#895](https://github.com/microsoft/RD-Agent/issues/895)) ([236c28f](https://github.com/microsoft/RD-Agent/commit/236c28f29c6bc5da62129632e464bbc32056ebdb))
* 增强与更多 LLM 模型的兼容性 ([#905](https://github.com/microsoft/RD-Agent/issues/905)) ([8800624](https://github.com/microsoft/RD-Agent/commit/8800624ad4749d6e798785a082c9f94c306792ef))
* idea pool 集成到 exp_gen 并向 RD-Agent 添加计时器和向 RD-loops 添加暂停-恢复功能 ([#795](https://github.com/microsoft/RD-Agent/issues/795)) ([e62aefa](https://github.com/microsoft/RD-Agent/commit/e62aefa56e34ff45a8ed033f7bf28b95c8e63656))
* joblib 缓存 ([#749](https://github.com/microsoft/RD-Agent/issues/749)) ([83a0411](https://github.com/microsoft/RD-Agent/commit/83a041148ff908871b1906f9e6889d80ab513412))
* 将 api 状态记录到 mlflow ([#860](https://github.com/microsoft/RD-Agent/issues/860)) ([049921b](https://github.com/microsoft/RD-Agent/commit/049921b beb0b4ed0ba1ab7508d9857d2c1e729349))
* 在 CoSTEER 演进中断前记录达到最大时间限制 ([#921](https://github.com/microsoft/RD-Agent/issues/921)) ([837fff2](https://github.com/microsoft/RD-Agent/commit/837fff29096fefe1369d386ef8a860395b737173))
* 将失败和成功的跟踪合并在一起 ([#766](https://github.com/microsoft/RD-Agent/issues/766)) ([3a2aa8c](https://github.com/microsoft/RD-Agent/commit/3a2aa8cf0102647950b2dfc0007c118b0c799cd4))
* 选择性合并 ([#888](https://github.com/microsoft/RD-Agent/issues/888)) ([06ba314](https://github.com/microsoft/RD-Agent/commit/06ba314ff0f91e7e78e8d456c719ac3194a8c774))
* 多跟踪在线合并 ([#886](https://github.com/microsoft/RD-Agent/issues/886)) ([2112d67](https://github.com/microsoft/RD-Agent/commit/2112d676d0938de6fea163b2e5eb9c36771e7041))
* 新的提案（结构化输出）提示 ([#887](https://github.com/microsoft/RD-Agent/issues/887)) ([150796a](https://github.com/microsoft/RD-Agent/commit/150796aaa72eaa5037fd7db8e785058fbc4d4967))
* 基于 asyncio 的并行循环运行 ([#932](https://github.com/microsoft/RD-Agent/issues/932)) ([c63e207](https://github.com/microsoft/RD-Agent/commit/c63e2071f3179feef69f88061c0172cb5c3157f2))
* 在管道中的多个部分提出假设 ([#827](https://github.com/microsoft/RD-Agent/issues/827)) ([acb0e21](https://github.com/microsoft/RD-Agent/commit/acb0e21a331410d044849e12e2887f41e5ff1c3a))
* 带进度的拉取镜像 ([#777](https://github.com/microsoft/RD-Agent/issues/777)) ([5cad086](https://github.com/microsoft/RD-Agent/commit/5cad0860204ede974533dc7bdc9808cfd135fa24))
* 在 api 调用超时时引发错误 ([#793](https://github.com/microsoft/RD-Agent/issues/793)) ([eafd4df](https://github.com/microsoft/RD-Agent/commit/eafd4dfc6263f19a8cdaf27498a1d07b43815306))
* 引发策略冲突 ([#894](https://github.com/microsoft/RD-Agent/issues/894)) ([5b9d007](https://github.com/microsoft/RD-Agent/commit/5b9d0072aebe15369e9a0010af83e71684baeae7))
* 重新分析竞赛信息和管道编码评估器提示 ([#837](https://github.com/microsoft/RD-Agent/issues/837)) ([f7b5258](https://github.com/microsoft/RD-Agent/commit/f7b52580080c75d311355bcc6193b49495801809))
* 优化合并 ([#842](https://github.com/microsoft/RD-Agent/issues/842)) ([99463b4](https://github.com/microsoft/RD-Agent/commit/99463b46819b3a0dcb2bb12a823a9cdf7ec560b4))
* 优化提示 ([#760](https://github.com/microsoft/RD-Agent/issues/760)) ([a91b182](https://github.com/microsoft/RD-Agent/commit/a91b182c4c9510eb34e4aab956588e909fa5d70b))
* 将硬编码的缓存路径替换为动态的 cache_path 配置 ([#952](https://github.com/microsoft/RD-Agent/issues/952)) ([db56894](https://github.com/microsoft/RD-Agent/commit/db568947f1084a80d603718f5a13fdbd72b90a47))
* 将草稿阶段恢复为假设选择中的软衰减 ([#849](https://github.com/microsoft/RD-Agent/issues/849)) ([d41db0c](https://github.com/microsoft/RD-Agent/commit/d41db0ca357b07091825ebd9d18c303b6db3cc6a))
* 跟踪合并 ([#836](https://github.com/microsoft/RD-Agent/issues/836)) ([a3d5473](https://github.com/microsoft/RD-Agent/commit/a3d547369e408a05cff570c1239b6320be40418d))
* 按时间截断 ([#863](https://github.com/microsoft/RD-Agent/issues/863)) ([2b9427a](https://github.com/microsoft/RD-Agent/commit/2b9427ae036ffe1e28a717502f45500fe91fe5ac))
* 更新提示以改进某些 LLM 模型的 json 响应格式 ([#928](https://github.com/microsoft/RD-Agent/issues/928)) ([0b84709](https://github.com/microsoft/RD-Agent/commit/0b84709e59c7abb9754961cd17cc9673fcf508aa))
* 在不同部分使用不同的聊天模型 ([#822](https://github.com/microsoft/RD-Agent/issues/822)) ([c052ea6](https://github.com/microsoft/RD-Agent/commit/c052ea6d1f8948183a4a6ebc873ec01b57373cce))


### 错误修复

* 'DSProposalV2ExpGen' 对象没有属性 'COMPONENT_TASK_MAP… ([#950](https://github.com/microsoft/RD-Agent/issues/950)) ([e353895](https://github.com/microsoft/RD-Agent/commit/e353895251f231fee85abdcb1b22b022a577af77))
* 使 UI 适应模拟跟踪 ([#841](https://github.com/microsoft/RD-Agent/issues/841)) ([8a5754c](https://github.com/microsoft/RD-Agent/commit/8a5754c9b9c9410d0943aeed777a93c13422e54a))
* 在 env shell 命令中的 chmod 后添加缺少的分号 ([#955](https://github.com/microsoft/RD-Agent/issues/955)) ([1128eaa](https://github.com/microsoft/RD-Agent/commit/1128eaa89ec1dcab4a05ef50d64c7f7e6aae88a8))
* 在 api 超时错误时向计时器添加时间 ([#826](https://github.com/microsoft/RD-Agent/issues/826)) ([f45d6ae](https://github.com/microsoft/RD-Agent/commit/f45d6ae6595c1c39b389485b637a0ae53ffc8782))
* 将 wait_retry 添加到 exp_gen v2 ([#783](https://github.com/microsoft/RD-Agent/issues/783)) ([b9fb7cf](https://github.com/microsoft/RD-Agent/commit/b9fb7cf4e3070062d91b5b67d0f10d6266b45142))
* 调整 ds_trace 查找并将 stderr 重定向添加到 mlebench 命令 ([#853](https://github.com/microsoft/RD-Agent/issues/853)) ([4e53108](https://github.com/microsoft/RD-Agent/commit/4e53108e020db719b39cba3a67e0c6dae3de19cf))
* 对齐 competion_full_desc 和 scenario_all_desc，删除问题提案中的冗余信息 ([#808](https://github.com/microsoft/RD-Agent/issues/808)) ([76d8536](https://github.com/microsoft/RD-Agent/commit/76d8536d9ec53952383019306781d49cb3e9f75c))
* 计时器启动中的错误修复 ([#807](https://github.com/microsoft/RD-Agent/issues/807)) ([9af7161](https://github.com/microsoft/RD-Agent/commit/9af7161eb57bdd2e24b072335e9d185951c32472))
* 问题识别中的错误 ([#806](https://github.com/microsoft/RD-Agent/issues/806)) ([e1d5a29](https://github.com/microsoft/RD-Agent/commit/e1d5a2914046476f2f10d5884ed3c3ff956d65ff))
* conda 错误信息 ([#941](https://github.com/microsoft/RD-Agent/issues/941)) ([fd39a94](https://github.com/microsoft/RD-Agent/commit/fd39a947763fb4a9be87b907c399bebe384df505))
* 在 LiteLLM 后端计算失败时将成本默认为 NaN ([#912](https://github.com/microsoft/RD-Agent/issues/912)) ([51a4048](https://github.com/microsoft/RD-Agent/commit/51a4048129cbfbc3b84bcf50fd8866fafb3e2da3))
* ds 跟踪 ([#929](https://github.com/microsoft/RD-Agent/issues/929)) ([127e441](https://github.com/microsoft/RD-Agent/commit/127e441602e21a46d6313ff39133ab8ca841937e))
* 在管道编码器和运行器中测试重复的模型名称 ([#763](https://github.com/microsoft/RD-Agent/issues/763)) ([be3ee9d](https://github.com/microsoft/RD-Agent/commit/be3ee9da9882edda3c06ff7d1099d1bbda2203c3))
* 过滤系统元数据目录并初始化缺失的 DSTrace 属性 ([#946](https://github.com/microsoft/RD-Agent/issues/946)) ([10050ef](https://github.com/microsoft/RD-Agent/commit/10050ef368ae7ec07cbf20ac4e52e21c2875eaab))
* 修复 docker 结果提取中的一个错误 ([#824](https://github.com/microsoft/RD-Agent/issues/824)) ([e1c0f98](https://github.com/microsoft/RD-Agent/commit/e1c0f9826abcbc11dda215a600a2637c9ac6e984))
* 修复竞赛指标方向 ([#784](https://github.com/microsoft/RD-Agent/issues/784)) ([3be0057](https://github.com/microsoft/RD-Agent/commit/3be0057556f46c899065ee1c7f9bafe33e79249c))
* 修复模型输入形状错误和 costeer_model 错误 ([#821](https://github.com/microsoft/RD-Agent/issues/821)) ([b34bd89](https://github.com/microsoft/RD-Agent/commit/b34bd895d6d9c326aab85856a15be0cb72b2c4c8))
* 修复一些小错误 ([#758](https://github.com/microsoft/RD-Agent/issues/758)) ([963f96e](https://github.com/microsoft/RD-Agent/commit/963f96e5596bee04074135c2a0e31a8adc39ad8c))
* 修复 qlib 场景中的一些小错误 ([#817](https://github.com/microsoft/RD-Agent/issues/817)) ([79962a7](https://github.com/microsoft/RD-Agent/commit/79962a7ca40c77a3997a68da9ad1b5ab16728483))
* 修复 stdout 正则表达式匹配中的错误 ([#890](https://github.com/microsoft/RD-Agent/issues/890)) ([ee57e37](https://github.com/microsoft/RD-Agent/commit/ee57e37a22af874b262c033d1606dbe7799706db))
* 修复多跟踪在线合并中 Exceed-LLM-Context 的错误 ([#892](https://github.com/microsoft/RD-Agent/issues/892)) ([f760a3e](https://github.com/microsoft/RD-Agent/commit/f760a3eff7bd927a31e4958ed2f706312e83e3e3))
* 修复问题权重错误 ([#898](https://github.com/microsoft/RD-Agent/issues/898)) ([013d79f](https://github.com/microsoft/RD-Agent/commit/013d79f12060e908aeb57c3eb1bb56eea86df086))
* 修复了由文档构建引起的 CI 执行失败 ([#857](https://github.com/microsoft/RD-Agent/issues/857)) ([5c116b2](https://github.com/microsoft/RD-Agent/commit/5c116b24ce727f6ed9ef39d5aa5b60442038c344))
* 获取 aerial-cactus-identification 的 metric_direction ([#970](https://github.com/microsoft/RD-Agent/issues/970)) ([70dc62d](https://github.com/microsoft/RD-Agent/commit/70dc62de5fbd4272ecda1b6fcbcf898b3624a991))
* T 的导入路径 ([#787](https://github.com/microsoft/RD-Agent/issues/787)) ([ac008a6](https://github.com/microsoft/RD-Agent/commit/ac008a61d03b4737ab3d994024e922839d8f3fe1))
* 改进评估对齐检查（例如小规模微调） ([#802](https://github.com/microsoft/RD-Agent/issues/802)) ([d391578](https://github.com/microsoft/RD-Agent/commit/d3915788082de640a4ce1eea6d2e607319b89c3e))
* 改进文件树和 _walk 符号链接处理 ([#877](https://github.com/microsoft/RD-Agent/issues/877)) ([516cb69](https://github.com/microsoft/RD-Agent/commit/516cb69357483ddd99f84b221a056d8491c34f9b))
* 日志信息 ([#965](https://github.com/microsoft/RD-Agent/issues/965)) ([f1dbc21](https://github.com/microsoft/RD-Agent/commit/f1dbc2100498e22c8e5edbb2e4563c99c3d54775))
* 主要错误 ([#938](https://github.com/microsoft/RD-Agent/issues/938)) ([c6d34d6](https://github.com/microsoft/RD-Agent/commit/c6d34d67b8aedf5496bf6a875915ce657fc58448))
* 不存在的变量 test_eval.py ([#847](https://github.com/microsoft/RD-Agent/issues/847)) ([4948c38](https://github.com/microsoft/RD-Agent/commit/4948c38560f4cf021d9354b201b22dfa5ccb9441))
* 优化反馈提示 ([#901](https://github.com/microsoft/RD-Agent/issues/901)) ([12bb2c4](https://github.com/microsoft/RD-Agent/commit/12bb2c4a1494b9aa29962905abb5e433a60eb716))
* 优化假设提案中的时间/内存约束提示 ([#856](https://github.com/microsoft/RD-Agent/issues/856)) ([51ce8ef](https://github.com/microsoft/RD-Agent/commit/51ce8ef84b4fe6590ce20599a56eee596f2f04e6))
* 在 FBWorkspace 类的 env.run_ret_code 调用中设置 PYTHONPATH ([#755](https://github.com/microsoft/RD-Agent/issues/755)) ([68b5018](https://github.com/microsoft/RD-Agent/commit/68b501889caca754f27b57d9ab6f72184e93b15c))
* task_gen 以便更好地理解 ([#752](https://github.com/microsoft/RD-Agent/issues/752)) ([6bfc1e5](https://github.com/microsoft/RD-Agent/commit/6bfc1e570449ee69ac110a4ced9a7cecbc0e6a73))
* 跟踪列表但是 ([#852](https://github.com/microsoft/RD-Agent/issues/852)) ([32cdc57](https://github.com/microsoft/RD-Agent/commit/32cdc575bde103d71a358d4d99bd413076328ebd))
* 工作流中的拼写错误 ([#861](https://github.com/microsoft/RD-Agent/issues/861)) ([0e54c9f](https://github.com/microsoft/RD-Agent/commit/0e54c9fe41d25a4cc45ab9e61bb2c2c01b854751))
* 更新 DS 环境设置，包括竞赛容量和超时 ([#878](https://github.com/microsoft/RD-Agent/issues/878)) ([816ada0](https://github.com/microsoft/RD-Agent/commit/816ada096afabe90578672b0e61b656802a30b62))
* 更新 feedback.py ([#772](https://github.com/microsoft/RD-Agent/issues/772)) ([133778c](https://github.com/microsoft/RD-Agent/commit/133778c67ee3349f1c2fe029bcf6a9ee14568efe))
* 更新 metric direction 以返回布尔值 ([#791](https://github.com/microsoft/RD-Agent/issues/791)) ([0bf365e](https://github.com/microsoft/RD-Agent/commit/0bf365e7830aa86d2350b9d1c47410af46b3a7e8))
* 在 DS 场景中将 runner max loop 更新为 1 ([#820](https://github.com/microsoft/RD-Agent/issues/820)) ([3da378e](https://github.com/microsoft/RD-Agent/commit/3da378e986e8b776a17dbc694d29ef211192ed3e))
* 为缺少提交和分数文件使用回退消息 ([#882](https://github.com/microsoft/RD-Agent/issues/882)) ([898fdea](https://github.com/microsoft/RD-Agent/commit/898fdeae80801d537ebc5c4a3b7df9de74c3403a))
* 使用简单的 stdout 和 stderr ([#966](https://github.com/microsoft/RD-Agent/issues/966)) ([0b1c445](https://github.com/microsoft/RD-Agent/commit/0b1c445f1f0c212887ffff9f8fac44236df3607c))
* 使用跟踪计数作为索引 ([#909](https://github.com/microsoft/RD-Agent/issues/909)) ([b87de56](https://github.com/microsoft/RD-Agent/commit/b87de56e54b206b3aada53850804474eff80b96d))
* 错误的变量 test_eval.py ([#846](https://github.com/microsoft/RD-Agent/issues/846)) ([808ea6c](https://github.com/microsoft/RD-Agent/commit/808ea6cba541e60c35dd283cee9098ce46f2a59e))

## [0.4.0](https://github.com/microsoft/RD-Agent/compare/v0.3.0...v0.4.0) (2025-04-04)


### 功能

* (Kaggle) 为竞赛添加基础模板：tabular-playground-series-may-2022 ([#481](https://github.com/microsoft/RD-Agent/issues/481)) ([f3405ca](https://github.com/microsoft/RD-Agent/commit/f3405ca732eb0ddca8e18ea72f69cbd86055c4ab))
* 一个统一的 CoSTEER 以适应更多场景 ([#491](https://github.com/microsoft/RD-Agent/issues/491)) ([cddbd02](https://github.com/microsoft/RD-Agent/commit/cddbd02e3ad3ccf6ad01443777319dc5c7eb08a7))
* 添加一个新竞赛 ([#474](https://github.com/microsoft/RD-Agent/issues/474)) ([2fc0d77](https://github.com/microsoft/RD-Agent/commit/2fc0d77c485a31f647e21f4578e2e326f7032964))
* 添加一个工具，用于将工作区文件保存到特定文件夹 ([#728](https://github.com/microsoft/RD-Agent/issues/728)) ([bca864b](https://github.com/microsoft/RD-Agent/commit/bca864b7edeafe3f88405efb695ca8acad6252f8))
* 添加基线分数统计 ([#590](https://github.com/microsoft/RD-Agent/issues/590)) ([2948026](https://github.com/microsoft/RD-Agent/commit/2948026c390d067b643f8c8247c1447f1dc023e4))
* 为 env.py 中的 Docker 卷添加可配置的卷模式 ([#537](https://github.com/microsoft/RD-Agent/issues/537)) ([642a022](https://github.com/microsoft/RD-Agent/commit/642a02239431411b91959f23e69b454997ca75d5))
* 为语义搜索添加约束标签 ([#680](https://github.com/microsoft/RD-Agent/issues/680)) ([0584cfc](https://github.com/microsoft/RD-Agent/commit/0584cfcd13ca1a62c85390ea2ee7574370748d31))
* 将交叉验证添加到工作流 ([#700](https://github.com/microsoft/RD-Agent/issues/700)) ([82e9b00](https://github.com/microsoft/RD-Agent/commit/82e9b00be62b01673353a7aaa3ab0e2e3ecaf3ca))
* 添加 describe_data_folder_v2 ([#738](https://github.com/microsoft/RD-Agent/issues/738)) ([bc8e846](https://github.com/microsoft/RD-Agent/commit/bc8e8460e0246321792ff3347b1b8905416ad075))
* 为加载函数添加 do_truncate 控制 ([#656](https://github.com/microsoft/RD-Agent/issues/656)) ([2b960a5](https://github.com/microsoft/RD-Agent/commit/2b960a58dfdeba69522a0f72ecf0975bb6ae87ee))
* 为加载函数添加 do_truncate 控制 ([#656](https://github.com/microsoft/RD-Agent/issues/656)) ([2b960a5](https://github.com/microsoft/RD-Agent/commit/2b960a58dfdeba69522a0f72ecf0975bb6ae87ee))
* 将 eda 添加到数据科学场景 ([#639](https://github.com/microsoft/RD-Agent/issues/639)) ([35aa479](https://github.com/microsoft/RD-Agent/commit/35aa479f00edf118d43ec228e0a84c155332957a))
* 添加假设指南和基于规则的排名 ([#746](https://github.com/microsoft/RD-Agent/issues/746)) ([c077b82](https://github.com/microsoft/RD-Agent/commit/c077b8239cc72904c4bc450845ed2a11aa5445f0))
* 为 shrink_text 函数和设置添加行长限制 ([#715](https://github.com/microsoft/RD-Agent/issues/715)) ([75ed5e1](https://github.com/microsoft/RD-Agent/commit/75ed5e1c2ce1bf20bb55190c10a4134e04694d2b))
* 向主循环添加 loop_n 参数 ([#611](https://github.com/microsoft/RD-Agent/issues/611)) ([778c166](https://github.com/microsoft/RD-Agent/commit/778c166962250e3b9e7ad85de37f62297d370b45))
* 在数据科学中为 costeer 添加最大时间配置 ([#645](https://github.com/microsoft/RD-Agent/issues/645)) ([534686c](https://github.com/microsoft/RD-Agent/commit/534686c2ba7d9fa979c0762ad3177c36f6d7f4cb))
* 添加 mlebench 提交验证器 ([#545](https://github.com/microsoft/RD-Agent/issues/545)) ([712d94a](https://github.com/microsoft/RD-Agent/commit/712d94a7d6f22187fc3d18bd434e71ec6997aa9f))
* 添加模型移除并调整一些框架逻辑 ([#681](https://github.com/microsoft/RD-Agent/issues/681)) ([1edf881](https://github.com/microsoft/RD-Agent/commit/1edf881c63512d351c0dd074d7a1c0965ff3119b))
* 向 LoopBase 的加载函数添加 output_path ([#628](https://github.com/microsoft/RD-Agent/issues/628)) ([dd33726](https://github.com/microsoft/RD-Agent/commit/dd33726ac5de75dc2030d193d457d59490b3361e))
* 添加管道编码器 ([#742](https://github.com/microsoft/RD-Agent/issues/742)) ([759f295](https://github.com/microsoft/RD-Agent/commit/759f295dbf1224e177006e72d694e42dd6f372b6))
* 将排名添加到报告（mle_summary） ([#665](https://github.com/microsoft/RD-Agent/issues/665)) ([13f7922](https://github.com/microsoft/RD-Agent/commit/13f7922aaae9e4143aac4ad08ec1c556c2faf04e))
* 添加重启并修复解压 ([#538](https://github.com/microsoft/RD-Agent/issues/538)) ([ed2c7d1](https://github.com/microsoft/RD-Agent/commit/ed2c7d175f1f44ca06ad7a63b08da12f6c4df9ab))
* 使用 wait_retry 装饰器添加重试机制并重构差异生成 ([#572](https://github.com/microsoft/RD-Agent/issues/572)) ([de1cd72](https://github.com/microsoft/RD-Agent/commit/de1cd72f068ebd1e1bd5bc2ad2b12ae484d54831))
* 将 CSV 的形状添加到数据集描述中 ([#561](https://github.com/microsoft/RD-Agent/issues/561)) ([a10c881](https://github.com/microsoft/RD-Agent/commit/a10c881bd86796e6167257ad26dd165f7e46d813))
* 在数据科学运行器中添加超时设置和清理步骤 ([#539](https://github.com/microsoft/RD-Agent/issues/539)) ([295abd5](https://github.com/microsoft/RD-Agent/commit/295abd56f7b58055bd27b247dfed47eb85e9b0cd))
* 向 api 后端添加类型检查器并对齐 litellm 和旧后端 ([#647](https://github.com/microsoft/RD-Agent/issues/647)) ([d38eae9](https://github.com/microsoft/RD-Agent/commit/d38eae986a0ba69d71288fa09fcc21e227551a02))
* 对齐 mlebench 数据和评估并在 kaggle 工作流上进行多项修复 ([#477](https://github.com/microsoft/RD-Agent/issues/477)) ([f6c522b](https://github.com/microsoft/RD-Agent/commit/f6c522b651db3c1f6af6815347589917f46e433a))
* **后端：** 集成 LiteLLM API 后端 ([#564](https://github.com/microsoft/RD-Agent/issues/564)) ([f477687](https://github.com/microsoft/RD-Agent/commit/f4776879c76a213d53875b307c94be1ea5cfd9ba))
* 基础数据科学场景 UI ([#525](https://github.com/microsoft/RD-Agent/issues/525)) ([39917b3](https://github.com/microsoft/RD-Agent/commit/39917b354b22a8488a17396fe2245cb41e3def03))
* condaenv 和完整的 docker 环境 ([#668](https://github.com/microsoft/RD-Agent/issues/668)) ([084dd6d](https://github.com/microsoft/RD-Agent/commit/084dd6d748a89492ea0888acb316b9bb9efeb62f))
* 差异模式修复 ([#569](https://github.com/microsoft/RD-Agent/issues/569)) ([0c509f5](https://github.com/microsoft/RD-Agent/commit/0c509f599ce19303b44d8192ec3eb634c24992d6))
* 显示 LLM 提示 ([#676](https://github.com/microsoft/RD-Agent/issues/676)) ([8c93bba](https://github.com/microsoft/RD-Agent/commit/8c93bba82e185edcf4204cc574df5f41bcdfa9d2))
* 在评估测试中动态查找和使用示例提交文件 ([#542](https://github.com/microsoft/RD-Agent/issues/542)) ([5f12b44](https://github.com/microsoft/RD-Agent/commit/5f12b44c89dd26b250e914192f9beb2da38fb3ab))
* 端到端优化 ([#473](https://github.com/microsoft/RD-Agent/issues/473)) ([d41343a](https://github.com/microsoft/RD-Agent/commit/d41343a63d87bf3479f5ec30745ea788580495bf))
* 增强评估脚本，包括文件清理和详细的提交检查 ([#529](https://github.com/microsoft/RD-Agent/issues/529)) ([cf2ff92](https://github.com/microsoft/RD-Agent/commit/cf2ff9213d3a8b0fad64df7cae0c35f996d72e27))
* 排除无效的会话日志文件夹 ([#554](https://github.com/microsoft/RD-Agent/issues/554)) ([fa86e4d](https://github.com/microsoft/RD-Agent/commit/fa86e4d1805000e0e5779c662ccbb5273fda623c))
* 改进框架自适应调整模型的能力 ([#629](https://github.com/microsoft/RD-Agent/issues/629)) ([93806f3](https://github.com/microsoft/RD-Agent/commit/93806f33a1e0f29a125e29303d4b984a9817c3c0))
* 在聊天和嵌入上独立使用 use_azure_token_provider ([#452](https://github.com/microsoft/RD-Agent/issues/452)) ([d223004](https://github.com/microsoft/RD-Agent/commit/d223004917692e231b251330cbc8676081d5a10d))
* 集成 azure deepseek r1 ([#591](https://github.com/microsoft/RD-Agent/issues/591)) ([e79ce5c](https://github.com/microsoft/RD-Agent/commit/e79ce5c38539138abe04eb9809fbde437e97bbb7))
* kaggle 重构 ([#489](https://github.com/microsoft/RD-Agent/issues/489)) ([1b057d0](https://github.com/microsoft/RD-Agent/commit/1b057d0d63a861fba4b3cb59c6c5fc1a0e3da383))
* **kaggle：** kaggle 场景中的几项更新 ([#476](https://github.com/microsoft/RD-Agent/issues/476)) ([245d211](https://github.com/microsoft/RD-Agent/commit/245d211dcbfb18ebcc554247a0e3a8dbecf6f3bd))
* 加载器提示并简化 YAML 加载和更新数据加载器规范 ([#736](https://github.com/microsoft/RD-Agent/issues/736)) ([86f8bbf](https://github.com/microsoft/RD-Agent/commit/86f8bbf15895e7c198f9bc395d055ca5f02a5bb6))
* 使规范可选 ([#719](https://github.com/microsoft/RD-Agent/issues/719)) ([a16b70f](https://github.com/microsoft/RD-Agent/commit/a16b70ff34c66d7e1c4c7ff5236eca8e7d8abea9))
* 在 LLM 设置中使系统提示角色可自定义 ([#632](https://github.com/microsoft/RD-Agent/issues/632)) ([e4acd92](https://github.com/microsoft/RD-Agent/commit/e4acd92cc5eec6db5c29cb2d4788020fb89099b7))
* 多个日志文件夹，替换工作区路径中的“epxx” ([#555](https://github.com/microsoft/RD-Agent/issues/555)) ([8a69c9c](https://github.com/microsoft/RD-Agent/commit/8a69c9c9630860c9b644356e1f71654aea222328))
* 新的 exp gen v2 实现 ([#725](https://github.com/microsoft/RD-Agent/issues/725)) ([5dcc2d5](https://github.com/microsoft/RD-Agent/commit/5dcc2d5fa63bbe9ae8c4817d9b40b77600440edb))
* new-york-city-taxi-fare-prediction_template ([#488](https://github.com/microsoft/RD-Agent/issues/488)) ([a9caab7](https://github.com/microsoft/RD-Agent/commit/a9caab7bc5dc86f395a008e523355922137aef17))
* o1-preview 的输出规范更改 ([#666](https://github.com/microsoft/RD-Agent/issues/666)) ([22894bd](https://github.com/microsoft/RD-Agent/commit/22894bdbee26b9cad73646d2975857787e515f75))
* 通用数据科学重构 ([#498](https://github.com/microsoft/RD-Agent/issues/498)) ([7002dc4](https://github.com/microsoft/RD-Agent/commit/7002dc4981a4f72096b438d2fe4fd9ff268c54f3))
* 优化 qlib_factor_from_report 的逻辑 ([#463](https://github.com/microsoft/RD-Agent/issues/463)) ([21348d8](https://github.com/microsoft/RD-Agent/commit/21348d89e0e0eec1b4fab4e7a497f1eb34b8fe72))
* 在 gpt-4o 和 llama 3.1 上运行基准测试 ([#497](https://github.com/microsoft/RD-Agent/issues/497)) ([64af0b5](https://github.com/microsoft/RD-Agent/commit/64af0b5529b687cce8b5b7a1893946e15edca626))
* 摘要和 UI 更新 ([#581](https://github.com/microsoft/RD-Agent/issues/581)) ([efa51f9](https://github.com/microsoft/RD-Agent/commit/efa51f9c259a06fe219f3137f0a1005e50d2bfdd))
* 一些 kaggle 竞赛的模板更改 ([#484](https://github.com/microsoft/RD-Agent/issues/484)) ([2e38000](https://github.com/microsoft/RD-Agent/commit/2e38000091030811fc081d72016c7bbadf7efd50))
* 在 LiteLLMAPIBackend 中跟踪和记录累积的完成成本 ([#727](https://github.com/microsoft/RD-Agent/issues/727)) ([b294a95](https://github.com/microsoft/RD-Agent/commit/b294a95e0b7b2ef96af355cebac92d9c87f3acab))
* 更新数据科学组件的提示和描述 ([#731](https://github.com/microsoft/RD-Agent/issues/731)) ([c20e226](https://github.com/microsoft/RD-Agent/commit/c20e226c3e7771c9fcd1c879a8937e4694dc03eb))
* data_science 编码器测试的变量打印工具 ([#658](https://github.com/microsoft/RD-Agent/issues/658)) ([116c061](https://github.com/microsoft/RD-Agent/commit/116c06190b01f0b621c021726a1be23458ab1154))


### 错误修复

* qlib 场景中的一个默认配置 ([#503](https://github.com/microsoft/RD-Agent/issues/503)) ([d64a228](https://github.com/microsoft/RD-Agent/commit/d64a228525cbedd7687c1e06132eacd0d0647697))
* exp_gen 中的一个小错误 ([#606](https://github.com/microsoft/RD-Agent/issues/606)) ([f734dde](https://github.com/microsoft/RD-Agent/commit/f734dde0b0101e13f38151468c8ddf9e23af26ac))
* 在重试生成模型代码时添加检查 ([#699](https://github.com/microsoft/RD-Agent/issues/699)) ([3b82f15](https://github.com/microsoft/RD-Agent/commit/3b82f159474087902d3c6007d370e3282b549015))
* 在日志处理中添加 DSExperiment 类型检查和目录验证… ([#535](https://github.com/microsoft/RD-Agent/issues/535)) ([f59b12c](https://github.com/microsoft/RD-Agent/commit/f59b12c9cc9afde82b74bc133797ff1396678627))
* 添加集成测试，在工作流规范中更改为“如果可能，使用交叉验证” ([#634](https://github.com/microsoft/RD-Agent/issues/634)) ([acc97a8](https://github.com/microsoft/RD-Agent/commit/acc97a8217253497afedcfa829902b4432e1031e))
* 为 cache_with_pickle 添加 force 参数并在获取 kaggle 排行榜时使用缓存 ([#687](https://github.com/microsoft/RD-Agent/issues/687)) ([c8841e5](https://github.com/microsoft/RD-Agent/commit/c8841e590a925200859acba9fda4a17d4c3aa1c7))
* 为有效分数添加指标名称检查 ([#724](https://github.com/microsoft/RD-Agent/issues/724)) ([acc2ffb](https://github.com/microsoft/RD-Agent/commit/acc2ffbde4df3b53654559d14cd035ee6be6b35e))
* 为 DockerEnv 中的 GPU 设备检查添加重试机制 ([#573](https://github.com/microsoft/RD-Agent/issues/573)) ([a780cfb](https://github.com/microsoft/RD-Agent/commit/a780cfb621dc487cc17072bfd4aedd7d581249ab))
* 在 ensemble_test 中添加 scores.csv 检查 ([#567](https://github.com/microsoft/RD-Agent/issues/567)) ([01808b4](https://github.com/microsoft/RD-Agent/commit/01808b47c314d1daffacc0a65e0ab934a1c41d65))
* 添加 stdout 上下文长度设置并改进文本收缩逻辑 ([#559](https://github.com/microsoft/RD-Agent/issues/559)) ([4ac26a6](https://github.com/microsoft/RD-Agent/commit/4ac26a65c1f18f7513480dd562566c8a96298aa7))
* 对齐组件名称 ([#701](https://github.com/microsoft/RD-Agent/issues/701)) ([295a114](https://github.com/microsoft/RD-Agent/commit/295a1148c53d00b716b2d540573a7f43e7e2d762))
* 自动继续的小错误 ([#598](https://github.com/microsoft/RD-Agent/issues/598)) ([75eaecf](https://github.com/microsoft/RD-Agent/commit/75eaecf36b9f70dfc2d7fedd35836acdb05f89d6))
* 避免在集成评估提示中使用 try-except ([#637](https://github.com/microsoft/RD-Agent/issues/637)) ([5c58d6e](https://github.com/microsoft/RD-Agent/commit/5c58d6e524ef848024578033ab6d47bc9b220822))
* 在不使用时避免因缺少 llama 安装而发出警告 ([#509](https://github.com/microsoft/RD-Agent/issues/509)) ([5ec3422](https://github.com/microsoft/RD-Agent/commit/5ec342224c2c8c4cf591f1eae673e25b14218726))
* 将 devault 更改为 default ([#688](https://github.com/microsoft/RD-Agent/issues/688)) ([7f401cd](https://github.com/microsoft/RD-Agent/commit/7f401cd1c3b333285acf6d6e57654f4b9f0cb6c5))
* 更改集成测试 ([#622](https://github.com/microsoft/RD-Agent/issues/622)) ([5de3595](https://github.com/microsoft/RD-Agent/commit/5de35953ed0d3e2e1f4dff0e0522f2d6475079ec))
* 更改日志文件夹的摘要信息 ([#552](https://github.com/microsoft/RD-Agent/issues/552)) ([0eb258d](https://github.com/microsoft/RD-Agent/commit/0eb258d734e9a1280a238b9a6f63eb33047ee0a7))
* 澄清一个模糊的解释 ([#705](https://github.com/microsoft/RD-Agent/issues/705)) ([5dbfc68](https://github.com/microsoft/RD-Agent/commit/5dbfc6859cbf6cc31932dae30cf05506108fc871))
* 澄清 cross_validation ([#644](https://github.com/microsoft/RD-Agent/issues/644)) ([906993e](https://github.com/microsoft/RD-Agent/commit/906993ef6482f88131d1af46f5bc66a77034b549))
* 编码器提示和模型测试文本 ([#583](https://github.com/microsoft/RD-Agent/issues/583)) ([0a41227](https://github.com/microsoft/RD-Agent/commit/0a41227f267050feaeeb47ddd4d749643eb9f198))
* 纠正配置继承关系 ([#671](https://github.com/microsoft/RD-Agent/issues/671)) ([30b1ff8](https://github.com/microsoft/RD-Agent/commit/30b1ff8e1ce59b741e0b81481962063014641c0b))
* 默认 emb 模型 ([#702](https://github.com/microsoft/RD-Agent/issues/702)) ([4329a72](https://github.com/microsoft/RD-Agent/commit/4329a722832a201b3fa6f9d8f9d8d46f78110410))
* DSExpGen 类中的 direct_exp_gen 到 json_target_type ([#661](https://github.com/microsoft/RD-Agent/issues/661)) ([428b74a](https://github.com/microsoft/RD-Agent/commit/428b74a988157ea864ebb40e828bd9f67589c863))
* docker 错误将触发重试，数据科学运行器循环设置为 3 ([#602](https://github.com/microsoft/RD-Agent/issues/602)) ([ad785e0](https://github.com/microsoft/RD-Agent/commit/ad785e03d5db05d9191d5e772e184532835a787b))
* 确保预期类型 ([#593](https://github.com/microsoft/RD-Agent/issues/593)) ([098a9a6](https://github.com/microsoft/RD-Agent/commit/098a9a6618f70fa8dd276b9014b9e7ba9621553b))
* 在 ds UI 中过滤空的日志跟踪 ([#533](https://github.com/microsoft/RD-Agent/issues/533)) ([1a2057c](https://github.com/microsoft/RD-Agent/commit/1a2057c9fc11edc4637f0baaa6dd226eb049c36e))
* 修复交叉验证中的一个错误 ([#618](https://github.com/microsoft/RD-Agent/issues/618)) ([05a4f10](https://github.com/microsoft/RD-Agent/commit/05a4f101e0b64b860ad03294619b2350004657e8))
* 修复集成测试脚本中的一个错误 ([#713](https://github.com/microsoft/RD-Agent/issues/713)) ([ad32100](https://github.com/microsoft/RD-Agent/commit/ad321000acbd9291d22fe03a9c60e57c70511c73))
* 修复初始任务中的一个错误 ([#635](https://github.com/microsoft/RD-Agent/issues/635)) ([edb552e](https://github.com/microsoft/RD-Agent/commit/edb552ed283119444f357fbd0b6170b2ad97712a))
* 修复 kaggle conf 中的一个错误 ([#459](https://github.com/microsoft/RD-Agent/issues/459)) ([b4ed32b](https://github.com/microsoft/RD-Agent/commit/b4ed32b17ef07d8557450063765585a48d5fcd32))
* 修复 progress_bar 过滤器中的一个错误 ([#712](https://github.com/microsoft/RD-Agent/issues/712)) ([ba5a84d](https://github.com/microsoft/RD-Agent/commit/ba5a84dee59c39cc2a8c0d428a82da1f899ce537))
* 修复提案中的一个错误（将上一个循环的异常添加到上一个任务描述中） ([#596](https://github.com/microsoft/RD-Agent/issues/596)) ([419186f](https://github.com/microsoft/RD-Agent/commit/419186ffb985fe5a0aa0f7fe59c7a223e355492e))
* 修复正则表达式异常处理中的一个错误 ([#734](https://github.com/microsoft/RD-Agent/issues/734)) ([67d3702](https://github.com/microsoft/RD-Agent/commit/67d37027bbcd7294a5890a350fe16fe78e0dfa77))
* 修复阈值分数显示中的一个错误 ([#592](https://github.com/microsoft/RD-Agent/issues/592)) ([0b0a2dc](https://github.com/microsoft/RD-Agent/commit/0b0a2dc512a5560a66464ad49de25d362d0dc17e))
* 修复与集成中的 model_name 相关的错误 ([#692](https://github.com/microsoft/RD-Agent/issues/692)) ([c6ce473](https://github.com/microsoft/RD-Agent/commit/c6ce4733f32578298abe0b60f9d82611b793cc09))
* 修复一个小错误 ([#694](https://github.com/microsoft/RD-Agent/issues/694)) ([1405d8d](https://github.com/microsoft/RD-Agent/commit/1405d8dafd99ecde6f3ba9dd76133d8830d03b47))
* 修复 model_coder 提示中的一个错误 ([#690](https://github.com/microsoft/RD-Agent/issues/690)) ([4528826](https://github.com/microsoft/RD-Agent/commit/452882674e915dbd9e3399c26c70ce5bb86d012c))
* 修复 docker 中 combined_factors_df.pkl 未加载的问题 ([#697](https://github.com/microsoft/RD-Agent/issues/697)) ([3984b99](https://github.com/microsoft/RD-Agent/commit/3984b995aa74318b40de7712e100d4de5cc95b11))
* 修复文档构建错误 ([#711](https://github.com/microsoft/RD-Agent/issues/711)) ([c9e1d32](https://github.com/microsoft/RD-Agent/commit/c9e1d32d6b63560350cc7cb799c3a908e2c04e42))
* 修复 ExtendedSettingsConfigDict 不起作用的问题 ([#660](https://github.com/microsoft/RD-Agent/issues/660)) ([3a877f3](https://github.com/microsoft/RD-Agent/commit/3a877f383b908da8d027560714030b201946bb76))
* 修复 kaggle 模板路径错误 ([#747](https://github.com/microsoft/RD-Agent/issues/747)) ([3b3f504](https://github.com/microsoft/RD-Agent/commit/3b3f5041514baf741fe2d4613fa651fb5d9c002d))
* 修复 KeyError direct_exp_gen ([#735](https://github.com/microsoft/RD-Agent/issues/735)) ([7200682](https://github.com/microsoft/RD-Agent/commit/7200682ac4e60d3910c29a4f7c4a37b3d24e4224))
* 修复一些错误（集成输出、HPO、模型调整） ([#648](https://github.com/microsoft/RD-Agent/issues/648)) ([818ee29](https://github.com/microsoft/RD-Agent/commit/818ee29f8e5d4765b9801463b85b42ee9516ec33))
* 修复集成组件中的一些错误 ([#595](https://github.com/microsoft/RD-Agent/issues/595)) ([c0990ab](https://github.com/microsoft/RD-Agent/commit/c0990abb06c73ae062d9a50f50cdfd6d04aded22))
* 修复工作流单元测试中的一些错误 ([#624](https://github.com/microsoft/RD-Agent/issues/624)) ([f845dcc](https://github.com/microsoft/RD-Agent/commit/f845dcc0ee1b059b8b32485ad46bb90c7ae0fa78))
* 修复 direct_exp_gen 中的一些描述错误 ([#698](https://github.com/microsoft/RD-Agent/issues/698)) ([dfaacb6](https://github.com/microsoft/RD-Agent/commit/dfaacb6d06e5d5f55e950d7177570d1efebf958f))
* 修复一些小错误并添加 AutoML 和交叉验证 ([#604](https://github.com/microsoft/RD-Agent/issues/604)) ([18c5ef2](https://github.com/microsoft/RD-Agent/commit/18c5ef268d40efe7bb9ee18aa0d250732bdda6fa))
* 修复提交文件搜索并在 env.py 中添加 TODO ([#544](https://github.com/microsoft/RD-Agent/issues/544)) ([54d930e](https://github.com/microsoft/RD-Agent/commit/54d930e91e629f0fc2f8bdd0d0d62fcad1e99a9c))
* 修复任务返回字典格式错误的问题 ([#558](https://github.com/microsoft/RD-Agent/issues/558)) ([2008244](https://github.com/microsoft/RD-Agent/commit/20082440a249dd0e5a7026c2d98c9de0288dd400))
* 修复五个组件的编码器和评估器中的错误 ([#576](https://github.com/microsoft/RD-Agent/issues/576)) ([c487f83](https://github.com/microsoft/RD-Agent/commit/c487f835b651cdc40b95bbbe4efcb9a617be9e40))
* 处理百分比计算中的除零问题 ([#550](https://github.com/microsoft/RD-Agent/issues/550)) ([de16c91](https://github.com/microsoft/RD-Agent/commit/de16c915e1716ef8cee43ce41069ea1a09cf1f24))
* 处理 filter_progress_bar 函数中的无效正则表达式模式 ([#579](https://github.com/microsoft/RD-Agent/issues/579)) ([b0daee0](https://github.com/microsoft/RD-Agent/commit/b0daee0d90e193ca1d028e01c31ebf368af89601))
* 处理解析 uri 相对路径时的 ValueError ([#585](https://github.com/microsoft/RD-Agent/issues/585)) ([4c7765a](https://github.com/microsoft/RD-Agent/commit/4c7765a12bda5dcfd9af72b292853d9bc28c5baf))
* 在缓存键生成中包含数据信息 ([#566](https://github.com/microsoft/RD-Agent/issues/566)) ([26dda46](https://github.com/microsoft/RD-Agent/commit/26dda4682b7b643c164589057cb568a4d9e55e17))
* 保留一些 txt 文件 ([#557](https://github.com/microsoft/RD-Agent/issues/557)) ([54aba85](https://github.com/microsoft/RD-Agent/commit/54aba851c9fa194e318d37700307df59e06c6c84))
* mle_score 保存问题 ([#674](https://github.com/microsoft/RD-Agent/issues/674)) ([ca2e478](https://github.com/microsoft/RD-Agent/commit/ca2e478cf25c2c8511d5f027e32f8a98fc8e3a07))
* 将 docker 超时消息移动到 __run() ([#620](https://github.com/microsoft/RD-Agent/issues/620)) ([585f4f9](https://github.com/microsoft/RD-Agent/commit/585f4f96e09f70d00eb397c10bf49c09973111df))
* 将 mlebench 检查移动到运行器 ([#556](https://github.com/microsoft/RD-Agent/issues/556)) ([b0f7965](https://github.com/microsoft/RD-Agent/commit/b0f7965f650638273710302efee2e5da037368a2))
* 将 next_component_required 逻辑移动到 DSTrace 类并准确实现 ([#612](https://github.com/microsoft/RD-Agent/issues/612)) ([c20d311](https://github.com/microsoft/RD-Agent/commit/c20d311792f33b2ccccb466c6ec3155ff8be3213))
* 修补奇怪的 azure 部署 ([#494](https://github.com/microsoft/RD-Agent/issues/494)) ([89c50ae](https://github.com/microsoft/RD-Agent/commit/89c50aee2ec8bfd1cb23767ddf7dcdd023daac8b))
* qlib 和其他场景错误 ([#636](https://github.com/microsoft/RD-Agent/issues/636)) ([98de31d](https://github.com/microsoft/RD-Agent/commit/98de31d4e577c8c450c9694f73a755c19af571f7))
* 优化提示以在初始阶段生成最简单的任务 ([#546](https://github.com/microsoft/RD-Agent/issues/546)) ([9d6feed](https://github.com/microsoft/RD-Agent/commit/9d6feed28ce034db48482d8d9741ef8c72f4bddc))
* 将 API 调用替换为 build_cls_from_json_with_retry 函数 ([#548](https://github.com/microsoft/RD-Agent/issues/548)) ([eb72a47](https://github.com/microsoft/RD-Agent/commit/eb72a47fbf9c88dacea9691b8d7e92610492d190))
* 将集成测试代码中的“len()”函数替换为支持各种数据类型 ([#739](https://github.com/microsoft/RD-Agent/issues/739)) ([ab9c7b9](https://github.com/microsoft/RD-Agent/commit/ab9c7b955f78c5de7ec08a6c1a012a76badbdd0e))
* 如果 create_embedding 收到字符串输入，则返回 1D 嵌入 ([#670](https://github.com/microsoft/RD-Agent/issues/670)) ([4a9c318](https://github.com/microsoft/RD-Agent/commit/4a9c3180ae4a4b043b1b4a89f51ee69cb6843142))
* rich.print 在输出中包含某些控制字符时出错 ([#684](https://github.com/microsoft/RD-Agent/issues/684)) ([ec0cb2a](https://github.com/microsoft/RD-Agent/commit/ec0cb2a032824023dcd04a3acc93202471d1f90a))
* 首次完成时可运行并将方法重命名为 next_incomplete_component 以提高清晰度 ([#615](https://github.com/microsoft/RD-Agent/issues/615)) ([93d9f63](https://github.com/microsoft/RD-Agent/commit/93d9f63369a78f78e1a67ab548923bb994d1d3b4))
* 运行器 COSTEER 评估器 ([#693](https://github.com/microsoft/RD-Agent/issues/693)) ([6a379ec](https://github.com/microsoft/RD-Agent/commit/6a379ec9b84d4e4944f1e412347aae4f5a93d476))
* 为正在运行的实验仅保存一个 mle_score pkl ([#675](https://github.com/microsoft/RD-Agent/issues/675)) ([f87ab67](https://github.com/microsoft/RD-Agent/commit/f87ab676b73cce82bd9f997ac779e31c571b53c4))
* 在 Env.run 方法中为'entry'参数设置默认值 ([#643](https://github.com/microsoft/RD-Agent/issues/643)) ([e50d242](https://github.com/microsoft/RD-Agent/commit/e50d2424b849e4181d6ca02e9cace90236665924))
* 排序文件名以进行缓存复制 ([#588](https://github.com/microsoft/RD-Agent/issues/588)) ([7158410](https://github.com/microsoft/RD-Agent/commit/7158410fbfdd84052f9a69cf1e04e09ac07ca598))
* sota 比较逻辑 ([#608](https://github.com/microsoft/RD-Agent/issues/608)) ([3575372](https://github.com/microsoft/RD-Agent/commit/35753722c0800d62855faeab996d513e62cfe7de))
* 目标 json 类型和轮次 ([#662](https://github.com/microsoft/RD-Agent/issues/662)) ([58cb58f](https://github.com/microsoft/RD-Agent/commit/58cb58f966a1db26f5ea9662a54ba12bc921ee24))
* 模板错误 ([#456](https://github.com/microsoft/RD-Agent/issues/456)) ([434a868](https://github.com/microsoft/RD-Agent/commit/434a8687eeda77e27b4938fb19694c15858ee446))
* dsapp 中显示的跟踪摘要 df ([#551](https://github.com/microsoft/RD-Agent/issues/551)) ([177096d](https://github.com/microsoft/RD-Agent/commit/177096d55fecb8c7dab9650ef8f5a31024cd4c1c))
* 解压 kaggle 数据 ([#464](https://github.com/microsoft/RD-Agent/issues/464)) ([3a9fc8e](https://github.com/microsoft/RD-Agent/commit/3a9fc8e73337d3757267b6f4482499499a1b6792))

## [0.3.0](https://github.com/microsoft/RD-Agent/compare/v0.2.1...v0.3.0) (2024-10-21)


### 功能

* 为 kaggle 添加新模板 ([#289](https://github.com/microsoft/RD-Agent/issues/289)) ([eee3ab5](https://github.com/microsoft/RD-Agent/commit/eee3ab5b25198224826cb7a8a17eab28bd5d1f7d))
* 为 kaggle 场景添加下载 submission.csv 按钮 ([#317](https://github.com/microsoft/RD-Agent/issues/317)) ([dcdcbe4](https://github.com/microsoft/RD-Agent/commit/dcdcbe46b4858bfb133ae3cca056e7f602d5cf63))
* 添加 kaggle 命令 ([#271](https://github.com/microsoft/RD-Agent/issues/271)) ([0938394](https://github.com/microsoft/RD-Agent/commit/0938394b7084ffbf3294d8c23d2d34bf7322ca0b))
* 添加 kaggle tpl: feedback-prize ([#331](https://github.com/microsoft/RD-Agent/issues/331)) ([a288e39](https://github.com/microsoft/RD-Agent/commit/a288e399e6b0beec62729bd7d46b98a55de5ab79))
* 为 kaggle 添加更多模板 ([#291](https://github.com/microsoft/RD-Agent/issues/291)) ([da752ec](https://github.com/microsoft/RD-Agent/commit/da752ec806e6f5f5679bc27ac1c072ed9a319251))
* 将普通 rag 添加到框架中 ([#360](https://github.com/microsoft/RD-Agent/issues/360)) ([91b0b1f](https://github.com/microsoft/RD-Agent/commit/91b0b1f66c3c1bf757cb64c4cfbdcaafe59eab74))
* 添加 qlib_factor_strategy ([#307](https://github.com/microsoft/RD-Agent/issues/307)) ([f8f59ff](https://github.com/microsoft/RD-Agent/commit/f8f59ff0a1be4428a68c8c27f220aabad0b6c9f0))
* 在 kaggle 场景中添加排名 ([#401](https://github.com/microsoft/RD-Agent/issues/401)) ([b16b4be](https://github.com/microsoft/RD-Agent/commit/b16b4beb402e0c27dfb39ee9d2a120f1b56d447c))
* 为 RDLoop 中的每个步骤和循环添加运行时测量。 ([#281](https://github.com/microsoft/RD-Agent/issues/281)) ([83058c8](https://github.com/microsoft/RD-Agent/commit/83058c864ceeec413dd29bf501030d5a7bd34679))
* 添加 s3e11 kaggle 模板 ([#324](https://github.com/microsoft/RD-Agent/issues/324)) ([8c57524](https://github.com/microsoft/RD-Agent/commit/8c57524bead1c8f655a08763d608eb7a6dd5975e))
* 添加了 RepoAnalyzer 以支持工作区的自动摘要 ([#264](https://github.com/microsoft/RD-Agent/issues/264)) ([0bd349a](https://github.com/microsoft/RD-Agent/commit/0bd349af50b9b881ba1774bdeb4d723529ef2aa9))
* 添加了在 Kaggle 场景中加载和存储 RAG 的支持。 ([#269](https://github.com/microsoft/RD-Agent/issues/269)) ([c4895de](https://github.com/microsoft/RD-Agent/commit/c4895de83f1ed000e563d42b3468a6bd9e5a4965))
* 宣布 Discord 和微信 ([#367](https://github.com/microsoft/RD-Agent/issues/367)) ([acac507](https://github.com/microsoft/RD-Agent/commit/acac5078a103b71afa6bd6c053b0766a6a7e609d))
* 在一个 kaggle RDLoop 后自动提交结果 ([#345](https://github.com/microsoft/RD-Agent/issues/345)) ([ab55d70](https://github.com/microsoft/RD-Agent/commit/ab55d7052b53a928b84dc5d5d0d2999d90ca9056))
* 更好的反馈和评估 ([#346](https://github.com/microsoft/RD-Agent/issues/346)) ([cc9a8c1](https://github.com/microsoft/RD-Agent/commit/cc9a8c1eab3ca89f8c1e5de4a2bb4e7fcc0cc615))
* 基于任务的动态场景 ([#392](https://github.com/microsoft/RD-Agent/issues/392)) ([665a037](https://github.com/microsoft/RD-Agent/commit/665a037e4fd7326c450e3fa0d0605eea26fd9ef3))
* 因子实现搜索增强 ([#294](https://github.com/microsoft/RD-Agent/issues/294)) ([4ecf25f](https://github.com/microsoft/RD-Agent/commit/4ecf25f0acf2389a172b14d3dab20895daf2ab89))
* 特征选择 v3 以支持所有操作 ([#280](https://github.com/microsoft/RD-Agent/issues/280)) ([0047641](https://github.com/microsoft/RD-Agent/commit/00476413fbf00e36e71ab3ccb48d4e766b6ccf4d))
* 修复一些错误并添加原始特征的描述 ([#259](https://github.com/microsoft/RD-Agent/issues/259)) ([1a5f45a](https://github.com/microsoft/RD-Agent/commit/1a5f45a40d821c017bdba14af8c93710707c5ea5))
* 获取 kaggle 笔记本和讨论文本用于 RAG ([#371](https://github.com/microsoft/RD-Agent/issues/371)) ([cead345](https://github.com/microsoft/RD-Agent/commit/cead3450a14bf4b142ac988c27fa098c7656a95c))
* Iceberge 竞赛 ([#372](https://github.com/microsoft/RD-Agent/issues/372)) ([c10ea4f](https://github.com/microsoft/RD-Agent/commit/c10ea4f5d4cc56a75b47cf23c7084ee189ba1a25))
* 实现隔离的模型特征选择循环 ([#370](https://github.com/microsoft/RD-Agent/issues/370)) ([cf1292d](https://github.com/microsoft/RD-Agent/commit/cf1292de1a0153ca14ea64971e73a1c93f7d89e3))
* KAGGLE 场景中 Graph RAG 的初始版本 ([#301](https://github.com/microsoft/RD-Agent/issues/301)) ([fd3c0fd](https://github.com/microsoft/RD-Agent/commit/fd3c0fd26eff7d3be72fa4f2a234e33b9f796627))
* 将 RAG 集成到 Kaggle 场景中。 ([#262](https://github.com/microsoft/RD-Agent/issues/262)) ([be0e48a](https://github.com/microsoft/RD-Agent/commit/be0e48a7dfbee2b5d2947d09115db5db2e5266f1))
* Kaggle 循环更新（特征和模型） ([#241](https://github.com/microsoft/RD-Agent/issues/241)) ([4cf22a6](https://github.com/microsoft/RD-Agent/commit/4cf22a65c964123b4267569ee02c0c7094c54ca4))
* kaggle 模板相关 ([#287](https://github.com/microsoft/RD-Agent/issues/287)) ([785fdc1](https://github.com/microsoft/RD-Agent/commit/785fdc144d16fa8454b7c9d2e53e78fe7f22a29a))
* 用于调整和选择的模型上下文 ([#284](https://github.com/microsoft/RD-Agent/issues/284)) ([f2831e7](https://github.com/microsoft/RD-Agent/commit/f2831e7442510668b0ca75953b3359894803ef3c))
* 修改 FactorRowCountEvaluator 和 FactorIndexEvaluator 以返回比率 ([#328](https://github.com/microsoft/RD-Agent/issues/328)) ([8f43f8e](https://github.com/microsoft/RD-Agent/commit/8f43f8e87a92e05b541e925910608606ec8f6c4b))
* 新竞赛 - Optiver ([#356](https://github.com/microsoft/RD-Agent/issues/356)) ([3705efe](https://github.com/microsoft/RD-Agent/commit/3705efe3b923748655a57d76b7a236e54d361831))
* s3e11 的随机森林 ([#347](https://github.com/microsoft/RD-Agent/issues/347)) ([b57846d](https://github.com/microsoft/RD-Agent/commit/b57846d29314e9a5967945d1b4895f0f48c0f5ce))
* 优化模型描述中的代码并修复 feedback.py 中的一些错误 ([#288](https://github.com/microsoft/RD-Agent/issues/288)) ([5b124d7](https://github.com/microsoft/RD-Agent/commit/5b124d7372137e4c613eb2749ddcc773922cc7b6))
* 优化几个 Kaggle 竞赛中的模板 ([#343](https://github.com/microsoft/RD-Agent/issues/343)) ([034f238](https://github.com/microsoft/RD-Agent/commit/034f238ed5ec351486b21250eabc75114961936c))
* 修订以支持更好的假设提出 ([#390](https://github.com/microsoft/RD-Agent/issues/390)) ([c55ec0a](https://github.com/microsoft/RD-Agent/commit/c55ec0a0f577bbf7fc6228f7b87d2089ded83b31))
* 在演示中显示工作区 ([#348](https://github.com/microsoft/RD-Agent/issues/348)) ([ddf567c](https://github.com/microsoft/RD-Agent/commit/ddf567c551b553788be022e9312c209ef6137d64))
* 支持多输出 ([#330](https://github.com/microsoft/RD-Agent/issues/330)) ([3d36c45](https://github.com/microsoft/RD-Agent/commit/3d36c452ff0983800e5343834cc69f24a508ea70))
* 支持 COVID-19 竞赛 ([#374](https://github.com/microsoft/RD-Agent/issues/374)) ([a1b63db](https://github.com/microsoft/RD-Agent/commit/a1b63db79600edc9a74ba713c9d0be290214a592))
* 支持 Mnist 竞赛 ([#375](https://github.com/microsoft/RD-Agent/issues/375)) ([e958a34](https://github.com/microsoft/RD-Agent/commit/e958a34f5632a46ac43bff8e0d07d6ed020fdfc2))
* 支持模型规范 ([#319](https://github.com/microsoft/RD-Agent/issues/319)) ([e126471](https://github.com/microsoft/RD-Agent/commit/e1264719e10b76158a91cd0ef331848e7c2de7c7))
* 支持 RD-Agent 的各种 Kaggle 竞赛和场景 ([#409](https://github.com/microsoft/RD-Agent/issues/409)) ([75eea22](https://github.com/microsoft/RD-Agent/commit/75eea22cc3d4e6f5a94c88cce915e27c507f8c50))
* kaggle 模板 ([#308](https://github.com/microsoft/RD-Agent/issues/308)) ([ff97cf0](https://github.com/microsoft/RD-Agent/commit/ff97cf0155ab6941e4b5cf7d103575f934b70dc9))
* 使用 LLM 缓存时使用自动生成的种子 ([#441](https://github.com/microsoft/RD-Agent/issues/441)) ([ca15365](https://github.com/microsoft/RD-Agent/commit/ca15365d23eeb094f42cf3dc8f5269b2f1c42bd3))
* 使用统一的 pickle 缓存器并将 llm 配置移动到隔离的配置中 ([#424](https://github.com/microsoft/RD-Agent/issues/424)) ([2879ecf](https://github.com/microsoft/RD-Agent/commit/2879ecff816d97688b60909a79c7e568d42608a1))
* xgboost gpu 加速 ([#359](https://github.com/microsoft/RD-Agent/issues/359)) ([56a5b8f](https://github.com/microsoft/RD-Agent/commit/56a5b8f9b2c6726cc64ec5b04b4ce7935d59b572))


### 错误修复

* developer 的一个 bug 并编辑 s4e8 模板 ([#338](https://github.com/microsoft/RD-Agent/issues/338)) ([f12ce72](https://github.com/microsoft/RD-Agent/commit/f12ce726e7de96d478a232a3c27f92439820f8b4))
* 主动引发的错误也被视为负面反馈。 ([#268](https://github.com/microsoft/RD-Agent/issues/268)) ([46ec908](https://github.com/microsoft/RD-Agent/commit/46ec908e3594ac5e4cdc4057268e2f8800f5ed1f))
* 保存预处理缓存文件的错误 ([#310](https://github.com/microsoft/RD-Agent/issues/310)) ([5fb0608](https://github.com/microsoft/RD-Agent/commit/5fb0608f39f113cc9807fb1f381284a0bd4da318))
* 缓存 ([#383](https://github.com/microsoft/RD-Agent/issues/383)) ([f2a6e75](https://github.com/microsoft/RD-Agent/commit/f2a6e75b36ca96f7733b9c2a7154ac67bd2d7c6f))
* 更改 kaggle 竞赛信息爬虫的 css 标签 ([#306](https://github.com/microsoft/RD-Agent/issues/306)) ([1e3d38b](https://github.com/microsoft/RD-Agent/commit/1e3d38bf1ca3654f3a90ff392ecba1dbb4e80224))
* 调试 dsagent ([#387](https://github.com/microsoft/RD-Agent/issues/387)) ([8fe9511](https://github.com/microsoft/RD-Agent/commit/8fe9511e606ba148c66f384add6ab94857079541))
* eval_method 无法捕获运行因子错误 ([#260](https://github.com/microsoft/RD-Agent/issues/260)) ([2aaab31](https://github.com/microsoft/RD-Agent/commit/2aaab317ccb7a0121063bcd85fc36c21c7b8a391))
* 修复竞赛指标评估中的一个错误 ([#407](https://github.com/microsoft/RD-Agent/issues/407)) ([94c47d6](https://github.com/microsoft/RD-Agent/commit/94c47d6fd5c3e38fc786a83e6d0d05e8d04498f3))
* 修复 mini case 中的一个错误 ([#389](https://github.com/microsoft/RD-Agent/issues/389)) ([e75bb57](https://github.com/microsoft/RD-Agent/commit/e75bb5746f63933b750406bbd34ee63c5ba76b9f))
* 修复模型调整反馈中的一个错误 ([#316](https://github.com/microsoft/RD-Agent/issues/316)) ([8aa088d](https://github.com/microsoft/RD-Agent/commit/8aa088da2dc7525a3970c01d01987246f47d6238))
* 修复 scenario.py 中的一个错误 ([#388](https://github.com/microsoft/RD-Agent/issues/388)) ([999a1eb](https://github.com/microsoft/RD-Agent/commit/999a1eb0eff9088e1b02419db741db4acf8d9ff7))
* 修复模型输入格式中的一个错误 ([#327](https://github.com/microsoft/RD-Agent/issues/327)) ([8f0574e](https://github.com/microsoft/RD-Agent/commit/8f0574eaaadb245b8c38e09ad4821306996d926f))
* 修复缓存中使用模块名和函数名作为唯一文件夹名的一个小错误 ([#429](https://github.com/microsoft/RD-Agent/issues/429)) ([4f8134a](https://github.com/microsoft/RD-Agent/commit/4f8134a697d952f7ac824d7ebeec64bbc4545ab3))
* 修复一个拼写错误 ([#362](https://github.com/microsoft/RD-Agent/issues/362)) ([9fafabd](https://github.com/microsoft/RD-Agent/commit/9fafabdf321b818bdd2211a2324d50cd0ebe1c1f))
* 修复缓存结果逻辑 ([#430](https://github.com/microsoft/RD-Agent/issues/430)) ([5e34263](https://github.com/microsoft/RD-Agent/commit/5e342637dcc862679fd0642c6ba9ef048c984845))
* 修复命令注入 ([#421](https://github.com/microsoft/RD-Agent/issues/421)) ([52f30a6](https://github.com/microsoft/RD-Agent/commit/52f30a6184af1295be15e855a80b84bc424fc75d))
* 修复 json 加载错误 ([#386](https://github.com/microsoft/RD-Agent/issues/386)) ([bba55fb](https://github.com/microsoft/RD-Agent/commit/bba55fb48fe105f4847c1b9c476eedc80835f523))
* 修复 feedback.py 中的一些错误并优化提示 ([#292](https://github.com/microsoft/RD-Agent/issues/292)) ([d834052](https://github.com/microsoft/RD-Agent/commit/d8340527f133dcc649d599d90d6402eddd37859e))
* 修复知识库中的一些错误 ([#378](https://github.com/microsoft/RD-Agent/issues/378)) ([fa6ff8e](https://github.com/microsoft/RD-Agent/commit/fa6ff8e591cf1847df77d73116649c5623161573))
* 修复 rag 中的一些错误 ([#399](https://github.com/microsoft/RD-Agent/issues/399)) ([194215c](https://github.com/microsoft/RD-Agent/commit/194215c4559aee5b6ece18d65c95fb30968e2db6))
* 修复整个循环中的一些错误 ([#274](https://github.com/microsoft/RD-Agent/issues/274)) ([8a564ec](https://github.com/microsoft/RD-Agent/commit/8a564ece1d87b27ee98b76db317935e802468965))
* 修复 scenario.py、proposal.py 和 runner.py 以及几个复杂竞赛场景中的一些错误 ([#365](https://github.com/microsoft/RD-Agent/issues/365)) ([2e383b1](https://github.com/microsoft/RD-Agent/commit/2e383b175d8448a67cb470f4e3ae8977d8ec6b5b))
* 改进 kaggle 循环中的执行时间 ([#279](https://github.com/microsoft/RD-Agent/issues/279)) ([4c8f998](https://github.com/microsoft/RD-Agent/commit/4c8f998c76f1e983a5687d2c65d3251750f2a9a0))
* kaggle 数据挂载问题 ([#297](https://github.com/microsoft/RD-Agent/issues/297)) ([795df31](https://github.com/microsoft/RD-Agent/commit/795df311e3f93cd2f3fb51ba5698adaf10f6bd62))
* Optiver 修复 ([#357](https://github.com/microsoft/RD-Agent/issues/357)) ([b054017](https://github.com/microsoft/RD-Agent/commit/b054017463af0d1784407030f2477d212118f341))
* bench 中的部分错误 ([#368](https://github.com/microsoft/RD-Agent/issues/368)) ([af9808f](https://github.com/microsoft/RD-Agent/commit/af9808f98736a2df07e121c2f6d7bfeb7b7d3581))
* 预处理输出格式和一些拼写错误 ([#358](https://github.com/microsoft/RD-Agent/issues/358)) ([b8b2cd6](https://github.com/microsoft/RD-Agent/commit/b8b2cd6ccd3b27aa73de847e50899a8a53b71b8f))
* rag 保存文件 ([#385](https://github.com/microsoft/RD-Agent/issues/385)) ([1cb01dd](https://github.com/microsoft/RD-Agent/commit/1cb01dd6fe595f2f5fb86487601326611dd1a57a))
* 在循环中没有指标时在演示中引发错误 ([#313](https://github.com/microsoft/RD-Agent/issues/313)) ([e46a78e](https://github.com/microsoft/RD-Agent/commit/e46a78eb69271cb19978aab2f3b976c2870ca082))
* 重构 Bench ([#302](https://github.com/microsoft/RD-Agent/issues/302)) ([78a87f6](https://github.com/microsoft/RD-Agent/commit/78a87f624780ff67c0fa995ae4692678a120f99c))
* 优化一些代码 ([#353](https://github.com/microsoft/RD-Agent/issues/353)) ([866c2e6](https://github.com/microsoft/RD-Agent/commit/866c2e63ffa3876a3d16ad37f96da41d0558b714))
* 优化提示 ([#286](https://github.com/microsoft/RD-Agent/issues/286)) ([77966c4](https://github.com/microsoft/RD-Agent/commit/77966c4f5e9f492c437c5b4b78d89c0f875ef0d8))
* 优化 ucb 算法 ([#406](https://github.com/microsoft/RD-Agent/issues/406)) ([14f7d97](https://github.com/microsoft/RD-Agent/commit/14f7d976e03c92d6e727524e0cdad8a03b585016))
* 恢复模型并使 SOTA 模型可用于 COSTEER ([#351](https://github.com/microsoft/RD-Agent/issues/351)) ([3b7437b](https://github.com/microsoft/RD-Agent/commit/3b7437b87e685188259779cd85a78a0b592de9de))
* 停止在 docker env print 中使用标记 ([#336](https://github.com/microsoft/RD-Agent/issues/336)) ([3009889](https://github.com/microsoft/RD-Agent/commit/3009889b5e2605b5427c76f3084e0e58026bb5ae))
* 支持种子并修复绝对路径 ([#278](https://github.com/microsoft/RD-Agent/issues/278)) ([26352e1](https://github.com/microsoft/RD-Agent/commit/26352e13121cad5be95c0de78bb9f5dda4330614))
* kaggle foreset 和 s4e9 的模板 ([#334](https://github.com/microsoft/RD-Agent/issues/334)) ([2393a41](https://github.com/microsoft/RD-Agent/commit/2393a41e7237615ced2c3fdd5c49308236b9f276))
* 测试 kaggle 方法 ([#296](https://github.com/microsoft/RD-Agent/issues/296)) ([91a6196](https://github.com/microsoft/RD-Agent/commit/91a619618be1d7db660ea2b413a78dfaba9417a1))
* 更新代码以修复模型缓存 md5 哈希中的一个小错误 ([#303](https://github.com/microsoft/RD-Agent/issues/303)) ([b00e4dc](https://github.com/microsoft/RD-Agent/commit/b00e4dc2eff5b16029a2a12a6589eadac5cfd148))
* 更新新的特征工程代码格式 ([#272](https://github.com/microsoft/RD-Agent/issues/272)) ([7850b80](https://github.com/microsoft/RD-Agent/commit/7850b8006a7c89d22629b345b4f361b0f35bc60d))
* 更新 prompts.yaml 以仅约束一种模型类型 ([#341](https://github.com/microsoft/RD-Agent/issues/341)) ([5b5dfee](https://github.com/microsoft/RD-Agent/commit/5b5dfeefbc7eb9dcbd9923544005c5d281262c03))
* 更新 runner.py 以修复一个小错误 ([#282](https://github.com/microsoft/RD-Agent/issues/282)) ([8aef3ab](https://github.com/microsoft/RD-Agent/commit/8aef3abcecd6002bd4bfeedcbe2c786d8bbfe2be))
* 在模型 costeer 中使用固定文件名并修复缓存 ([#311](https://github.com/microsoft/RD-Agent/issues/311)) ([1f910a5](https://github.com/microsoft/RD-Agent/commit/1f910a5248bc576895ed66c2f7b2c3e046a2bc28))


### 性能改进

* 对因子 costeer 进行一些小升级以提高性能 ([#420](https://github.com/microsoft/RD-Agent/issues/420)) ([9eb931f](https://github.com/microsoft/RD-Agent/commit/9eb931ffd971f252380dbd33ad1db259a4f229fd))


### 恢复

* 恢复功能：因子实现搜索增强 ([#294](https://github.com/microsoft/RD-Agent/issues/294)) ([#305](https://github.com/microsoft/RD-Agent/issues/305)) ([f663cf4](https://github.com/microsoft/RD-Agent/commit/f663cf42a2f75cd52aef1c6b18be7c27f0641fed))

## [0.2.1](https://github.com/microsoft/RD-Agent/compare/v0.2.0...v0.2.1) (2024-09-10)


### 错误修复

* 配置中的默认模型值 ([#256](https://github.com/microsoft/RD-Agent/issues/256)) ([c097585](https://github.com/microsoft/RD-Agent/commit/c097585f631f401c2c0966f6ad4c17286924f011))
* 修复_dotenv_错误 ([#257](https://github.com/microsoft/RD-Agent/issues/257)) ([923063c](https://github.com/microsoft/RD-Agent/commit/923063c1fd957c4ed42e97272c72b5e9545451dc))
* readme ([#248](https://github.com/microsoft/RD-Agent/issues/248)) ([8cede22](https://github.com/microsoft/RD-Agent/commit/8cede2209922876490148459e1134da828e1fda0))

## [0.2.0](https://github.com/microsoft/RD-Agent/compare/v0.1.0...v0.2.0) (2024-09-07)


### 功能

* 添加收集信息 ([#233](https://github.com/microsoft/RD-Agent/issues/233)) ([89f4af9](https://github.com/microsoft/RD-Agent/commit/89f4af90fb4d95a0689bf9efc8ffd9326469c0aa))
* 为 kaggle 场景添加交叉验证 ([#236](https://github.com/microsoft/RD-Agent/issues/236)) ([e0b03ba](https://github.com/microsoft/RD-Agent/commit/e0b03ba6b5c3d9aa552b99d470e106d4e348e64d))
* 为 docker 环境添加进度状态 ([#215](https://github.com/microsoft/RD-Agent/issues/215)) ([538d4ef](https://github.com/microsoft/RD-Agent/commit/538d4ef2e52de795b90d3f75b2e1e877ab85c18d))
* 添加了 Kaggle 场景的循环代码。 ([#211](https://github.com/microsoft/RD-Agent/issues/211)) ([975c327](https://github.com/microsoft/RD-Agent/commit/975c32715e51aec6b49537401f5fc59115e04a01))
* 演示显示效果和用法 ([#162](https://github.com/microsoft/RD-Agent/issues/162)) ([8cf122a](https://github.com/microsoft/RD-Agent/commit/8cf122a0155f434fa4477ae7a6d616b5caecd3e0))
* 框架的试运行 ([#227](https://github.com/microsoft/RD-Agent/issues/227)) ([e9b103e](https://github.com/microsoft/RD-Agent/commit/e9b103e684fdd2b98cd1a89971a3fce2d6e884a1))
* 支持 kaggle 场景的更多模型 ([#223](https://github.com/microsoft/RD-Agent/issues/223)) ([e3a9659](https://github.com/microsoft/RD-Agent/commit/e3a96598c0720fe092ec86d7ca8c195c7d6bcc72))
* 更新 model_experiment.py 以支持基本 EDA ([#220](https://github.com/microsoft/RD-Agent/issues/220)) ([bf2684c](https://github.com/microsoft/RD-Agent/commit/bf2684c4d55ab8e1048ac0291695475ad53b0cd6))


### 错误修复

* 修复 llm 调用中的一些错误 ([#217](https://github.com/microsoft/RD-Agent/issues/217)) ([7b010f8](https://github.com/microsoft/RD-Agent/commit/7b010f8b5940aba65a58f1d78192aa80bcd0e654))
* 包依赖。 ([#234](https://github.com/microsoft/RD-Agent/issues/234)) ([46be295](https://github.com/microsoft/RD-Agent/commit/46be2952952af534fd8d98a656c704c688d7cbdd))
* 删除无用行 ([#177](https://github.com/microsoft/RD-Agent/issues/177)) ([64e9a8e](https://github.com/microsoft/RD-Agent/commit/64e9a8e39a2072a962111db18f5b9565df5b0176))

## [0.1.0](https://github.com/microsoft/RD-Agent/compare/v0.0.1...v0.1.0) (2024-08-09)


### 功能

* 添加 rdagent 的入口。 ([#187](https://github.com/microsoft/RD-Agent/issues/187)) ([121b6d9](https://github.com/microsoft/RD-Agent/commit/121b6d98de38cd03be30cbee47b40baf39a2b60b))
* 更改 ui 入口 ([#197](https://github.com/microsoft/RD-Agent/issues/197)) ([fa5d335](https://github.com/microsoft/RD-Agent/commit/fa5d3354d22240888f4fc4007d9834f7424632aa))
* 删除 pdf 并启用在线 pdf 阅读 ([#183](https://github.com/microsoft/RD-Agent/issues/183)) ([18c0501](https://github.com/microsoft/RD-Agent/commit/18c05016a23d694c7b12759cf1322562dcffc56a))


### 错误修复

* 修复 readme 中的一个失败 href ([#189](https://github.com/microsoft/RD-Agent/issues/189)) ([1b89218](https://github.com/microsoft/RD-Agent/commit/1b89218f6bc697494f4a1b8a42ad18963002714f))
* 修复快速入门问题 ([#191](https://github.com/microsoft/RD-Agent/issues/191)) ([44f61bf](https://github.com/microsoft/RD-Agent/commit/44f61bfa1058a8efb59ca48b7f1417765aeea33e))
* 更新 readme.md 中的命令行 ([#192](https://github.com/microsoft/RD-Agent/issues/192)) ([9c45d24](https://github.com/microsoft/RD-Agent/commit/9c45d24a192da02f7d9765cb001097da1bc36c61))

## 0.0.1 (2024-08-08)


### 功能

* 为场景实验添加描述。 ([#174](https://github.com/microsoft/RD-Agent/issues/174)) ([fbd8c6d](https://github.com/microsoft/RD-Agent/commit/fbd8c6d87e1424c08997103b8e8fbf264858c4ed))
* 添加了 QlibFactorFromReportScenario 并改进了 report-factor 循环。 ([#161](https://github.com/microsoft/RD-Agent/issues/161)) ([882c79b](https://github.com/microsoft/RD-Agent/commit/882c79bf11583980e646b130f71cfa20201ffc7b))
* 过滤与先前实现的特征高度相关的特征 ([#145](https://github.com/microsoft/RD-Agent/issues/145)) ([e818326](https://github.com/microsoft/RD-Agent/commit/e818326422740e04a4863f7c3c18744dde2ad98f))
* 在前端场景显示中删除多余的“关键步骤”部分。 ([#169](https://github.com/microsoft/RD-Agent/issues/169)) ([e767005](https://github.com/microsoft/RD-Agent/commit/e76700513bee29232c93b97414419df330d9be8d))
* 用于不同场景的 streamlit webapp 演示 ([#135](https://github.com/microsoft/RD-Agent/issues/135)) ([d8da7db](https://github.com/microsoft/RD-Agent/commit/d8da7db865e6653fc4740efee9a843b69bd79699))
* 上传文档，更新提示和一些用于模型演示的代码 ([#144](https://github.com/microsoft/RD-Agent/issues/144)) ([529f935](https://github.com/microsoft/RD-Agent/commit/529f935aa98623f0dc1dda29eecee3ef738dd446))


### 错误修复

* 为任务编码失败添加框架处理。 ([#176](https://github.com/microsoft/RD-Agent/issues/176)) ([5e14fa5](https://github.com/microsoft/RD-Agent/commit/5e14fa54a9dd30a94aebe2643b8c9a3b85517a11))
* 全面更新因子提取。 ([#143](https://github.com/microsoft/RD-Agent/issues/143)) ([b5ea040](https://github.com/microsoft/RD-Agent/commit/b5ea04019fd5fa15c0f8b9a7e4f18f490f7057d4))
* 第一轮应用文件夹清理 ([#166](https://github.com/microsoft/RD-Agent/issues/166)) ([6a5a750](https://github.com/microsoft/RD-Agent/commit/6a5a75021912927deb5e8e4c7ad3ec4b51bfc788))
* 修复 pickle 问题 ([#140](https://github.com/microsoft/RD-Agent/issues/140)) ([7ee4258](https://github.com/microsoft/RD-Agent/commit/7ee42587b60d94417f34332cee395cf210dc8a0e))
* 修复发布 CI ([#165](https://github.com/microsoft/RD-Agent/issues/165)) ([85d6a5e](https://github.com/microsoft/RD-Agent/commit/85d6a5ed91113fda34ae079b23c89aa24acd2cb2))
* 修复发布 CI 错误 ([#160](https://github.com/microsoft/RD-Agent/issues/160)) ([1c9f8ef](https://github.com/microsoft/RD-Agent/commit/1c9f8ef287961731944acc9008496b4dddeddca7))
* 修复数据挖掘场景中的几个错误 ([#147](https://github.com/microsoft/RD-Agent/issues/147)) ([b233380](https://github.com/microsoft/RD-Agent/commit/b233380e2c66fb030db39424f0f040c86e37f5c4))
* 修复 report-factor 循环中的一些小错误 ([#152](https://github.com/microsoft/RD-Agent/issues/152)) ([a79f9f9](https://github.com/microsoft/RD-Agent/commit/a79f9f93406aff6305a76e6a6abd3852642e4c62))
* 修复_发布_ci_错误 ([#150](https://github.com/microsoft/RD-Agent/issues/150)) ([4f82e99](https://github.com/microsoft/RD-Agent/commit/4f82e9960a2638af9d831581185ddd3bac5711fc))
* 修复了重构过程中引入的一些错误。 ([#167](https://github.com/microsoft/RD-Agent/issues/167)) ([f8f1445](https://github.com/microsoft/RD-Agent/commit/f8f1445283fb89aefeb2918243c35a219a51a56c))
* 优化因子循环中的一些提示。 ([#158](https://github.com/microsoft/RD-Agent/issues/158)) ([c2c1330](https://github.com/microsoft/RD-Agent/commit/c2c13300b9ad315a663ec2d0eada414e56c6f54f))


### 其他杂务

* 发布 0.0.1 ([1feacd3](https://github.com/microsoft/RD-Agent/commit/1feacd39b21193de11e9bbecf880ddf96d7c261c))
