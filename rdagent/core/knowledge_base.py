from pathlib import Path # 用于处理文件路径

import dill as pickle  # type: ignore[import-untyped] # 使用 dill 进行序列化，它比标准 pickle 更强大
                        # Using dill for serialization, which is more powerful than standard pickle.
                        # type: ignore[import-untyped] 用于抑制 mypy 关于 dill 类型定义的警告。

from rdagent.log import rdagent_logger as logger # 导入日志记录器


class KnowledgeBase:
    """
    通用知识库基类。
    Generic base class for a knowledge base.

    提供将知识库内容持久化到磁盘以及从磁盘加载的基本功能。
    Provides basic functionality for persisting knowledge base content to disk and loading it from disk.
    知识以对象属性的形式存储。
    Knowledge is stored as attributes of the object.
    """
    def __init__(self, path: str | Path | None = None) -> None:
        """
        初始化知识库。
        Initializes the knowledge base.

        :param path: (可选) 知识库文件的路径。如果提供，将尝试从此路径加载数据。
                     (Optional) Path to the knowledge base file. If provided, attempts to load data from this path.
        """
        self.path: Path | None = Path(path) if path else None # 将字符串路径转换为 Path 对象
                                                              # Convert string path to Path object
        self.load() # 初始化时尝试加载已有的知识库内容
                    # Attempt to load existing knowledge base content upon initialization

    def load(self) -> None:
        """
        从指定的 `self.path` 加载知识库数据。
        Loads knowledge base data from the specified `self.path`.

        如果路径存在，它会使用 `dill` 反序列化文件内容，
        并将加载的数据（通常是一个字典或另一个对象的 `__dict__`）更新到当前实例的 `__dict__` 中。
        'path' 属性本身不会被覆盖。
        If the path exists, it deserializes the file content using `dill`
        and updates the current instance's `__dict__` with the loaded data
        (typically a dictionary or another object's `__dict__`).
        The 'path' attribute itself is not overwritten.
        """
        if self.path is not None and self.path.exists():
            try:
                with self.path.open("rb") as f: # 以二进制读模式打开文件
                                                # Open file in binary read mode
                    loaded_data = pickle.load(f) # 使用 dill 反序列化
                                                 # Deserialize using dill

                    # 根据加载的数据类型更新当前对象的属性
                    # Update attributes of the current object based on the type of loaded data
                    if isinstance(loaded_data, dict):
                        # 如果加载的是字典，则直接用其内容更新 (排除 "path")
                        # If a dictionary is loaded, update directly with its content (excluding "path")
                        self.__dict__.update({k: v for k, v in loaded_data.items() if k != "path"})
                    else:
                        # 如果加载的是其他对象实例，则用其 __dict__ 更新 (排除 "path")
                        # If another object instance is loaded, update with its __dict__ (excluding "path")
                        self.__dict__.update({k: v for k, v in loaded_data.__dict__.items() if k != "path"})
                logger.info(f"KnowledgeBase loaded from {self.path}")
            except Exception as e:
                logger.error(f"Failed to load KnowledgeBase from {self.path}: {e}")
        elif self.path is not None:
            logger.info(f"KnowledgeBase path {self.path} does not exist. Initializing an empty KnowledgeBase.")
        else:
            logger.info("KnowledgeBase path is not set. Initializing an empty KnowledgeBase.")


    def dump(self) -> None:
        """
        将当前知识库的内容序列化并保存到 `self.path` 指定的文件。
        Serializes the current knowledge base content and saves it to the file specified by `self.path`.

        它会将当前实例的 `__dict__` (即所有属性及其值) 使用 `dill` 保存。
        如果指定的路径的父目录不存在，会尝试创建它们。
        It saves the current instance's `__dict__` (i.e., all attributes and their values) using `dill`.
        If the parent directory of the specified path does not exist, it attempts to create it.
        """
        if self.path is not None:
            try:
                # 确保父目录存在
                # Ensure parent directory exists
                self.path.parent.mkdir(parents=True, exist_ok=True)
                with self.path.open("wb") as f: # 以二进制写模式打开文件
                                                # Open file in binary write mode
                    # 序列化整个对象的 __dict__ (所有实例属性)
                    # Serialize the entire object's __dict__ (all instance attributes)
                    pickle.dump(self.__dict__, f)
                logger.info(f"KnowledgeBase dumped to {self.path}")
            except Exception as e:
                logger.error(f"Failed to dump KnowledgeBase to {self.path}: {e}")
        else:
            # 如果路径未设置，则无法保存，记录警告日志
            # If the path is not set, it cannot be saved; log a warning.
            logger.warning("KnowledgeBase path is not set, dump operation failed.")
