import os.path
import time
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, final

from huibiao_framework.execption.resource_execption import (
    FolderResourceAlreadyExistException,
)
from huibiao_framework.utils.annotation import frozen_attrs
from huibiao_framework.utils.meta_class import ConstantClass

from .file_operator import BatchFileOperator, FileOperator, SingleFileOperator


class ResourceStatusTagConstant(ConstantClass):
    DONE = "__DONE"


F = TypeVar("F", bound=FileOperator)


@frozen_attrs("contribute_point", "__operator")
class Resource(Generic[F], ABC):
    def __init__(self, operator: F):
        self.__operator: F = operator

    @abstractmethod
    def is_completed(self, *args, **kwargs) -> bool:
        """
        该资源是否准备完毕
        """
        pass

    @abstractmethod
    def complete(self):
        pass

    @abstractmethod
    def path(self) -> str | List[str]:
        pass

    @property
    def operator(self) -> F:
        return self.__operator

    def load(self, **kwargs):
        self.__operator.load(**kwargs)

    def save(self, **kwargs):
        self.__operator.save(**kwargs)

    @abstractmethod
    def description(self) -> str:
        pass

    def __repr__(self):
        return self.description()

    def __str__(self):
        return self.description()


@frozen_attrs("operator")
class SingleFileResource(Resource[SingleFileOperator]):
    def __init__(self, operator: SingleFileOperator):
        super().__init__(operator)

    @final
    def is_completed(self, *args, **kwargs) -> bool:
        return self.operator.exists()

    @final
    def complete(self):
        """
        将资源设置为完成状态，不允许再更改
        """
        if not self.is_completed():
            self.save()

    def path(self) -> str:
        return self.operator.path

    def description(self) -> str:
        return f"{self.operator.__class__.__name__}[{self.operator.path}]"


@frozen_attrs("batch_operator", "complete_tag_path")
class BatchFileResource(Resource[BatchFileOperator]):
    def __init__(self, operator: BatchFileOperator):
        super().__init__(operator)
        self.complete_tag_path = os.path.join(
            self.operator.folder, ResourceStatusTagConstant.DONE
        )

    @property
    def folder(self) -> str:
        return self.operator.folder

    @final
    def is_completed(self) -> bool:
        return os.path.exists(self.complete_tag_path)

    @final
    def complete(self):
        if os.path.exists(self.complete_tag_path):
            raise FolderResourceAlreadyExistException(
                f"任务资源{self.operator.folder}已经完成"
            )
        with open(
            self.complete_tag_path,
            "w",
        ) as f:
            local_time = time.localtime(time.time())
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            f.write(formatted_time)  # 往目录下写入一个文件，包含当前时间

    @property
    def path(self) -> List[str]:
        return [
            os.path.join(self.operator.folder, r)
            for r in os.listdir(self.operator.folder)
            if r != ResourceStatusTagConstant.DONE
        ]

    def description(self) -> str:
        return f"{self.operator.__class__.__name__}[{self.operator.folder}]"
