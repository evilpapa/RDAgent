from abc import ABC, abstractmethod # 从 abc 模块导入 ABC (抽象基类) 和 abstractmethod (抽象方法装饰器)
                                    # Import ABC (Abstract Base Class) and abstractmethod decorator from the abc module

from rdagent.core.experiment import Task # 从 experiment 模块导入 Task 类，用于类型提示
                                         # Import Task class from the experiment module for type hinting


class Scenario(ABC):
    """
    场景 (Scenario) 的抽象基类。
    Abstract base class for a Scenario.

    一个场景应包含该特定研发问题的所有上下文信息。
    A scenario should encapsulate all contextual information for a specific R&D problem.
    但不应包含与具体实现方法相关的配置（例如 RAG 参数等，这些应由具体组件处理）。
    However, it should not include configuration related to specific implementation methods
    (e.g., RAG parameters, which should be handled by specific components).
    """

    @property
    @abstractmethod
    def background(self) -> str:
        """
        提供场景的背景信息。
        Provides background information for the scenario.
        子类必须实现此属性。
        Subclasses must implement this property.

        :return: 场景背景描述字符串。
                 A string describing the scenario background.
        """
        raise NotImplementedError

    # TODO: 需要修改所有子类，使其覆盖 get_source_data_desc 而不是 source_data 属性。
    # We have to change all the sub classes to override get_source_data_desc instead of `source_data`
    def get_source_data_desc(self, task: Task | None = None) -> str:  # noqa: ARG002 (忽略未使用task参数的警告)
                                                                    # noqa: ARG002 (ignore warning for unused task parameter)
        """
        获取源数据的描述。
        Gets the description of the source data.

        数据的选择可能因手头的具体任务而异。
        The choice of data may vary based on the specific task at hand.
        因此，此方法可以接收一个可选的 `task` 参数，以便根据任务动态提供数据描述。
        Therefore, this method can accept an optional `task` parameter to dynamically provide
        data descriptions based on the task.

        :param task: (可选) 当前的任务对象。
                     (Optional) The current task object.
        :return: 源数据描述字符串，默认为空字符串。
                 A string describing the source data, defaults to an empty string.
        """
        return ""

    @property
    def source_data(self) -> str:
        """
        描述源数据的便捷属性。
        A convenient property for describing source data.
        它是 `get_source_data_desc()` 方法的一个简单包装。
        It's a simple wrapper around the `get_source_data_desc()` method.

        :return: 源数据描述字符串。
                 A string describing the source data.
        """
        return self.get_source_data_desc()

    # 注意：我们应该保持基类接口的简洁性。因此，一些先前的接口已被删除。
    # 如果某些特定功能仅在子类内部使用（没有外部调用），则不应在基类中定义它们。
    # NOTE: we should keep the interface simpler. So some previous interfaces are deleted.
    # If we need some specific function only used in the subclass(no external usage).
    # We should not set them in the base class

    @property
    @abstractmethod
    def rich_style_description(self) -> str:
        """
        提供用于展示的富文本样式的场景描述。
        Provides a rich-text style description of the scenario for presentation purposes.
        例如，可以包含 Markdown 或 HTML 标记，以便在 UI 中更好地显示。
        For example, it might contain Markdown or HTML tags for better display in a UI.
        子类必须实现此属性。
        Subclasses must implement this property.

        :return: 富文本样式的场景描述字符串。
                 A string containing the rich-text style scenario description.
        """
        raise NotImplementedError

    @abstractmethod
    def get_scenario_all_desc(
        self,
        task: Task | None = None, # 当前任务，可选
        filtered_tag: str | None = None, # 用于过滤描述内容的标签，可选
        simple_background: bool | None = None, # 是否使用简化的背景信息，可选
    ) -> str:
        """
        将场景的所有相关描述信息组合在一起，生成一个全面的描述文本。
        Combines all relevant descriptive information of the scenario to generate a comprehensive text.

        场景描述会根据当前执行的任务 (`task`) 而有所不同。
        The scenario description varies based on the task being performed.
        此方法是 LLM 理解任务上下文的主要输入之一。
        This method is one of the primary inputs for an LLM to understand the task context.
        子类必须实现此方法。
        Subclasses must implement this method.

        :param task: (可选) 当前的任务对象。
        :param filtered_tag: (可选) 用于筛选或聚焦描述特定方面的标签。
        :param simple_background: (可选) 如果为 True，则可能使用更简洁的背景描述。
        :return: 包含所有组合描述的字符串。
                 A string containing all combined descriptions.
        """
        raise NotImplementedError

    @property
    def experiment_setting(self) -> str | None:
        """
        获取实验设置的描述，并以富文本字符串形式返回。
        Gets the description of the experiment settings and returns it as a rich text string.
        例如，可以描述模型训练的超参数、评估指标等。
        For example, it can describe hyperparameters for model training, evaluation metrics, etc.
        默认返回 None，子类可以覆盖此属性以提供具体的实验设置描述。
        Defaults to None; subclasses can override this property to provide specific experiment setting descriptions.

        :return: 实验设置的富文本描述字符串，或 None。
                 A rich text string describing the experiment settings, or None.
        """
        return None
