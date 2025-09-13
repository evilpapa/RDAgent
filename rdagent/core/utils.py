from __future__ import annotations

import functools
import importlib
import json
import multiprocessing as mp
import pickle
import random
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar, NoReturn, cast

from filelock import FileLock
from fuzzywuzzy import fuzz  # type: ignore[import-untyped]

from rdagent.core.conf import RD_AGENT_SETTINGS
from rdagent.oai.llm_conf import LLM_SETTINGS


class RDAgentException(Exception):  # noqa: N818
    pass


class SingletonBaseClass:
    """
    因为我们尝试支持使用 `class A(SingletonBaseClass)` 而不是 `A(metaclass=SingletonMeta)` 来定义单例，所以这个类是必要的。
    """

    _instance_dict: ClassVar[dict] = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        # 由于很难对齐使用 args 和 kwargs 的差异调用，我们严格要求在单例中使用 kwargs
        if args:
            # TODO: 这个限制可以解决。
            exception_message = "请仅在单例中使用 kwargs 以避免误解。"
            raise RDAgentException(exception_message)
        class_name = [(-1, f"{cls.__module__}.{cls.__name__}")]
        args_l = [(i, args[i]) for i in args]
        kwargs_l = sorted(kwargs.items())
        all_args = class_name + args_l + kwargs_l
        kwargs_hash = hash(tuple(all_args))
        if kwargs_hash not in cls._instance_dict:
            cls._instance_dict[kwargs_hash] = super().__new__(cls)  # Corrected call
        return cls._instance_dict[kwargs_hash]

    def __reduce__(self) -> NoReturn:
        """
        注意：
        当从 pickle 加载对象时，__new__ 方法不会收到它初始化时使用的 `kwargs`
        。这使得检索正确的单例对象变得困难。
        因此，我们使其不可 pickle。
        """
        msg = f"无法 pickle {self.__class__.__name__} 的实例"
        raise pickle.PicklingError(msg)


def parse_json(response: str) -> Any:
    try:
        return json.loads(response)
    except json.decoder.JSONDecodeError:
        pass
    error_message = f"Failed to parse response: {response}, please report it or help us to fix it."
    raise ValueError(error_message)


def similarity(text1: str, text2: str) -> int:
    text1 = text1 if isinstance(text1, str) else ""
    text2 = text2 if isinstance(text2, str) else ""

    # Maybe we can use other similarity algorithm such as tfidf
    return cast("int", fuzz.ratio(text1, text2))  # mypy does not regard it as int


def import_class(class_path: str) -> Any:
    """
    Parameters
    ----------
    class_path : str
        class path like"scripts.factor_implementation.baselines.naive.one_shot.OneshotFactorGen"

    Returns
    -------
        class of `class_path`
    """
    module_path, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


class CacheSeedGen:
    """
    它是一个全局种子生成器，用于生成一系列种子。
    这将支持 `use_auto_chat_cache_seed_gen` 功能声明

    注意：
    - 此种子专门用于缓存，与常规种子不同。
    - 如果删除了缓存，设置相同的种子将不会产生相同的 QA 跟踪。
    """

    def __init__(self) -> None:
        self.set_seed(LLM_SETTINGS.init_chat_cache_seed)

    def set_seed(self, seed: int) -> None:
        random.seed(seed)

    def get_next_seed(self) -> int:
        """generate next random int"""
        return random.randint(0, 10000)  # noqa: S311


LLM_CACHE_SEED_GEN = CacheSeedGen()


def _subprocess_wrapper(f: Callable, seed: int, args: list) -> Any:
    """
    它是一个函数包装器。为了确保子进程具有固定的起始种子。
    """

    LLM_CACHE_SEED_GEN.set_seed(seed)
    return f(*args)


def multiprocessing_wrapper(func_calls: list[tuple[Callable, tuple]], n: int) -> list:
    """它将使用多处理来调用 func_calls 中的函数，并使用给定的参数。
    结果等于 `return  [f(*args) for f, args in func_calls]`
    如果 `n=1`，它将不会调用多处理

    注意：
    我们与 chat_cache_seed 功能合作
    我们确保即使有多个种子，也能获得相同的种子跟踪

    参数
    ----------
    func_calls : List[Tuple[Callable, Tuple]]
        函数及其参数的列表
    n : int
        子进程的数量

    返回
    -------
    list

    """
    if n == 1 or max(1, min(n, len(func_calls))) == 1:
        return [f(*args) for f, args in func_calls]

    with mp.Pool(processes=max(1, min(n, len(func_calls)))) as pool:
        results = [
            pool.apply_async(_subprocess_wrapper, args=(f, LLM_CACHE_SEED_GEN.get_next_seed(), args))
            for f, args in func_calls
        ]
        return [result.get() for result in results]


def cache_with_pickle(hash_func: Callable, post_process_func: Callable | None = None, force: bool = False) -> Callable:
    """
    此装饰器将使用 pickle 缓存函数的返回值。
    缓存键由 hash_func 生成。哈希函数返回一个字符串或 None。
    如果它返回 None，则不会使用缓存。缓存将存储在由 RD_AGENT_SETTINGS.pickle_cache_folder_path_str 指定的文件夹中，名称为 hash_key.pkl。
    post_process_func 将使用原始参数和缓存的结果调用，以便每个调用者都有机会处理缓存的结果。post_process_func 应返回最终结果。

    参数
    ----------
    hash_func : Callable
        用于为缓存生成哈希键的函数。
    post_process_func : Callable | None, optional
        用于处理缓存结果的函数，默认为 None。
    force : bool, optional
        如果为 True，即使 RD_AGENT_SETTINGS.cache_with_pickle 为 False，也会使用缓存，默认为 False。
    """

    def cache_decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def cache_wrapper(*args: Any, **kwargs: Any) -> Any:
            if not RD_AGENT_SETTINGS.cache_with_pickle and not force:
                return func(*args, **kwargs)

            target_folder = Path(RD_AGENT_SETTINGS.pickle_cache_folder_path_str) / f"{func.__module__}.{func.__name__}"
            target_folder.mkdir(parents=True, exist_ok=True)
            hash_key = hash_func(*args, **kwargs)

            if hash_key is None:
                return func(*args, **kwargs)

            cache_file = target_folder / f"{hash_key}.pkl"
            lock_file = target_folder / f"{hash_key}.lock"

            if cache_file.exists():
                with cache_file.open("rb") as f:
                    cached_res = pickle.load(f)
                return post_process_func(*args, cached_res=cached_res, **kwargs) if post_process_func else cached_res

            if RD_AGENT_SETTINGS.use_file_lock:
                with FileLock(lock_file):
                    result = func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            with cache_file.open("wb") as f:
                pickle.dump(result, f)

            return result

        return cache_wrapper

    return cache_decorator
