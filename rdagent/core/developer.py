from __future__ import annotations # 确保类型提示中的向前引用有效

from abc import ABC, abstractmethod # 导入抽象基类和抽象方法
from typing import TYPE_CHECKING, Generic # 导入类型提示相关的工具

from rdagent.core.experiment import ASpecificExp # 从实验模块导入特定实验类型变量

if TYPE_CHECKING: # 仅在类型检查时执行，避免循环导入
    from rdagent.core.scenario import Scenario # 从场景模块导入 Scenario 类


class Developer(ABC, Generic[ASpecificExp]):
    """
    开发者 (Developer) 的抽象基类。
    Abstract base class for a Developer.

    在 RD-Agent 框架中，"Developer" 通常指一个 AI 组件或智能体，
    负责实现、执行和完善一个实验（Experiment）。
    In the RD-Agent framework, "Developer" typically refers to an AI component or agent
    responsible for implementing, executing, and refining an Experiment.

    它是一个泛型类，可以针对特定类型的实验 (`ASpecificExp`) 进行参数化。
    It is a generic class parameterized for a specific type of experiment (`ASpecificExp`).
    """
    def __init__(self, scen: Scenario) -> None:
        """
        初始化开发者。
        Initializes the Developer.

        :param scen: 当前开发者操作所处的场景实例。
                     The scenario instance in which the developer is currently operating.
        """
        self.scen: Scenario = scen

    @abstractmethod
    def develop(self, exp: ASpecificExp) -> ASpecificExp:  # TODO: 移除返回值 (remove return value)
        """
        执行开发活动，处理传入的实验对象。
        Performs development activities, processing the incoming experiment object.

        任务生成器（或此处的开发者）应该接收一个实验对象作为输入。
        The Task Generator (or the Developer here) should take in an experiment object as input.

        不同任务的调度对于最终性能至关重要，因为它会影响学习过程。
        The schedule of different tasks is crucial for the final performance
        as it affects the learning process.

        当前约束 (Current constraints):
        - 开发者应该**就地修改 (inplace edit)** `exp` 对象，而不是返回一个新的值。
          The developer should **inplace edit** the `exp` object instead of returning a new value.
            - 原因：我们有很多用例会在开发过程中引发错误，但我们仍然需要访问 `exp` 中的中间结果。
              Reason: We have many use cases that raise errors during development,
                      but we still need to access the intermediate results in `exp`.
        - 因此，未来应该移除此方法的返回值。
          So, the return value should be removed in the future.

        职责 (Responsibilities):
        - 在对实验对象进行开发（例如，生成代码、运行、测试）后，更新该实验对象。
          Update the experiment object after developing on it (e.g., generating code, running, testing).
        - 如果开发者试图为未来的开发传递信息（例如，开发过程中的观察、遇到的问题），
          它应该在 `exp` 对象上设置一个 `ExperimentFeedback` 实例。
          If it tries to deliver a message for future development (e.g., observations during development, issues encountered),
          it should set an `ExperimentFeedback` instance on the `exp` object.

        :param exp: 需要被开发的实验对象。
                    The experiment object to be developed.
        :return: （当前）被开发后的实验对象。未来此返回值将被移除。
                 (Currently) The experiment object after development. This return value will be removed in the future.
        """
        # 默认错误消息，提示子类必须实现此方法
        # Default error message, indicating that subclasses must implement this method.
        error_message = "develop method is not implemented." # 原注释为 "generate method is not implemented."，修正为 develop
        raise NotImplementedError(error_message)
