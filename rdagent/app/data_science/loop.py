import asyncio
from pathlib import Path
from typing import Optional

import fire
import typer
from typing_extensions import Annotated

from rdagent.app.data_science.conf import DS_RD_SETTING
from rdagent.core.utils import import_class
from rdagent.log import rdagent_logger as logger
from rdagent.scenarios.data_science.loop import DataScienceRDLoop


def main(
    path: Optional[str] = None,
    checkout: Annotated[bool, typer.Option("--checkout/--no-checkout", "-c/-C")] = True,
    checkout_path: Optional[str] = None,
    step_n: Optional[int] = None,
    loop_n: Optional[int] = None,
    timeout: Optional[str] = None,
    competition="bms-molecular-translation",
    replace_timer=True,
    exp_gen_cls: Optional[str] = None,
):
    """

    参数
    ----------
    path :
        类似 `$LOG_PATH/__session__/1/0_propose` 的路径。这表示我们在完成循环 1 中的步骤 0 后恢复状态。
    checkout :
        用于控制日志会话路径。布尔类型，默认为 True。
        - 如果为 True，新循环将使用现有文件夹并清除给定路径对应的会话之后的会话日志。
        - 如果为 False，新循环将使用现有文件夹，但保留给定路径对应的会话之后的会话日志。
    checkout_path:
        如果提供了 checkout_path（或类似 Path 的 str），新循环将保存到该路径，而原始路径保持不变。
    step_n :
        要运行的步数；如果为 None，该过程将无限期运行，直到出现错误或 KeyboardInterrupt。
    loop_n :
        要运行的循环数；如果为 None，该过程将无限期运行，直到出现错误或 KeyboardInterrupt。
        - 如果当前循环未完成，它将被计为要完成的第一个循环。
        - 如果同时提供了 step_n 和 loop_n，则一旦任一条件满足，该过程就会停止。
    competition :
        竞赛名称。
    replace_timer :
        如果加载了会话，则确定是否用 session.timer 替换计时器。
    exp_gen_cls :
        当有不同阶段时，可以用新的提案替换 exp_gen。


    Kaggle 场景中模型的自动研发演进循环。
    您可以使用以下命令继续运行会话：
    .. code-block:: bash
        dotenv run -- python rdagent/app/data_science/loop.py [--competition titanic] $LOG_PATH/__session__/1/0_propose  --step_n 1   # `step_n` 是一个可选参数
        rdagent kaggle --competition playground-series-s4e8  # 推荐使用此命令。
    """
    if not checkout_path is None:
        checkout = Path(checkout_path)

    if competition is not None:
        DS_RD_SETTING.competition = competition

    if not DS_RD_SETTING.competition:
        logger.error("Please specify competition name.")

    if path is None:
        kaggle_loop = DataScienceRDLoop(DS_RD_SETTING)
    else:
        kaggle_loop: DataScienceRDLoop = DataScienceRDLoop.load(path, checkout=checkout, replace_timer=replace_timer)

    # 如果有新类，则替换 exp_gen
    if exp_gen_cls is not None:
        kaggle_loop.exp_gen = import_class(exp_gen_cls)(kaggle_loop.exp_gen.scen)

    asyncio.run(kaggle_loop.run(step_n=step_n, loop_n=loop_n, all_duration=timeout))


if __name__ == "__main__":
    fire.Fire(main)
