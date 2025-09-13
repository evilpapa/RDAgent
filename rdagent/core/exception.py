class WorkflowError(Exception):
    """
    表示当前循环无法处理的错误，阻止进一步进展的异常。
    """


class FormatError(WorkflowError):
    """
    经过多次尝试，我们无法以正确的格式获取答案以继续。
    """


class CoderError(WorkflowError):
    """
    在实现和运行代码时引发的异常。
    - 开始：FactorTask => FactorGenerator
    - 结束：执行后获取数据帧

    数据帧值中更详细的评估由评估器管理。
    """

    # 注意：它对应于 **组件** 的错误
    caused_by_timeout: bool = False  # 错误是否由超时引起


class CodeFormatError(CoderError):
    """
    由于格式错误，未找到生成的代码。
    """


class CustomRuntimeError(CoderError):
    """
    生成的代码无法执行脚本。
    """


class NoOutputError(CoderError):
    """
    代码无法生成输出文件。
    """


class RunnerError(Exception):
    """
    运行代码输出时引发的异常。
    """

    # 注意：它对应于整个 **项目** 的错误


FactorEmptyError = CoderError  # 未正确生成因子时引发的异常

ModelEmptyError = CoderError  # 未正确生成模型时引发的异常


class KaggleError(Exception):
    """
    调用 Kaggle API 时引发的异常
    """


class PolicyError(Exception):
    """
    由于内容管理策略而引发的异常
    """
