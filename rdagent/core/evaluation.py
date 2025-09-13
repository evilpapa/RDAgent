"""
它有望在不同的框架之间共享。
"""

from abc import ABC, abstractmethod


class Feedback:
    """
    设计原则：
        它将更像一个 **dataclass**。
        反馈的构建过程应该在评估器中
    """

    def is_acceptable(self) -> bool:
        """
        有时，解决方案已经可以接受，但我们仍然希望对其进行优化。
        因此，我们使用不同的逻辑来确定解决方案是否可接受或已完成。
        """
        return self.__bool__()

    def finished(self) -> bool:
        """
        在某些实现中，任务可能会多次失败，导致智能体跳过实现。
        因此，跳过和成功都表示任务已完成。
        """
        return self.__bool__()

    def __bool__(self) -> bool:
        return True


class EvaluableObj:
    """
    一组可评估的信息。可以包括以下内容。
    - 任务
    - 解决方案
    - 真实情况
    """


class Evaluator(ABC):
    """
    设计原则：

        它应该涵盖从原始信息构建反馈的过程。
            通常，反馈的构建将分为两个阶段。
            1. 原始信息，包括 stdout 和工作区（反馈本身将处理此问题）
            2. 高级/摘要反馈信息。（评估将处理此问题）
    """

    @abstractmethod
    def evaluate(
        self,
        eo: EvaluableObj,
    ) -> Feedback:
        raise NotImplementedError
