import os
from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from loguru import logger

from huibiao_framework.utils.annotation import frozen_attrs

D = TypeVar("D")


class FileOperator(ABC):
    @abstractmethod
    def load(self, **kwargs):
        """
        从本地加载文件
        """
        pass

    @abstractmethod
    def save(self, **kwargs):
        """
        保存文件到本地
        """
        pass


@frozen_attrs("path")
class SingleFileOperator(Generic[D], FileOperator):
    """
    文件操作抽象类
    """

    def __init__(self, path: str):
        if path is None:
            raise ValueError("Path cannot be None")
        if not path.endswith(self.file_suffix()):
            raise ValueError(f"Path must end with {self.file_suffix()}")

        # 创建目录
        os.makedirs(os.path.dirname(path), exist_ok=True)

        self.path = path
        self.__data: D = None

    @property
    def data(self) -> D:
        """
        获取数据
        """
        return self.get_data()

    def get_data(self) -> D:
        if self.__data is None:
            self.load()
        return self.__data

    def set_data(self, data: D):
        self.__data = data

    @classmethod
    @abstractmethod
    def file_suffix(cls) -> str:
        """子类必须实现此类方法，对丁文件的后缀名，不能包含点"""
        pass

    def exists(self) -> bool:
        return os.path.exists(self.path)

    @staticmethod
    def ignore_if_path_not_exists(func):
        """
        实现一些拦截功能
        """

        def wrapper(instance: "SingleFileOperator", *args, **kwargs):
            if os.path.exists(instance.path):
                return func(instance, *args, **kwargs)  # 路径存在，正常执行
            else:
                logger.warning(f"{instance.path} 不存在，忽略")

        return wrapper


F = TypeVar("F", bound=SingleFileOperator)


@frozen_attrs("folder", "operator_cls", "operator_list")
class BatchFileOperator(FileOperator):
    def __init__(self, folder, operator_cls: Type[F]):
        os.makedirs(folder, exist_ok=True)
        self.folder = folder
        self.operator_cls: Type[F] = operator_cls
        self.operator_list: List[F] = []

        for _p in self.path:
            self.operator_list.append(operator_cls(path=_p))

    def __getitem__(self, idx) -> F:
        return self.operator_list[idx]

    def __len__(self):
        return len(self.operator_list)

    def genAppendPath(self):
        return os.path.join(
            self.folder, f"{len(self)}.{self.operator_cls.file_suffix()}"
        )

    def append(self, data) -> F:
        new_resource_item: Type[F] = self.operator_cls(path=self.genAppendPath())
        new_resource_item.set_data(data)
        self.operator_list.append(new_resource_item)
        return new_resource_item

    def load(self, **kwargs):
        for r in self.operator_list:
            r.load(**kwargs)

    def save(self, **kwargs):
        for r in self.operator_list:
            r.save(**kwargs)

    @property
    def path(self) -> List[str]:
        return [
            os.path.join(self.folder, r)
            for r in os.listdir(self.folder)
            if r.endswith(self.operator_cls.file_suffix())
        ]
