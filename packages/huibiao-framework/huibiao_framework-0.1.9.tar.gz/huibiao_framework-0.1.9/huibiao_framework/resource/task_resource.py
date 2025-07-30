import os
from typing import Dict, Type, TypeVar

from huibiao_framework.config import TaskConfig
from huibiao_framework.utils.annotation import frozen_attrs

from .file_operator import BatchFileOperator, SingleFileOperator
from .resource import BatchFileResource, Resource, SingleFileResource

F = TypeVar("F", bound=SingleFileOperator)
R = TypeVar("R", bound=Resource)


@frozen_attrs("task_dir", "task_type", "task_id", "resource_dict")
class TaskResource:
    def __init__(self, task_type: str, task_id: str):
        self.task_dir = os.path.join(TaskConfig.TASK_RESOURCE_DIR, task_type, task_id)
        self.task_id = task_id
        self.task_type = task_type
        self.__resource_dict: Dict[str, R] = {}

    def __getitem__(self, item) -> R | None:
        if item in self.resource_dict:
            return self.resource_dict[item]
        else:
            return None

    @property
    def resource_dict(self) -> dict[str, R]:
        return self.__resource_dict

    def genSingleFileOperator(self, name: str, operator_cls: Type[F]) -> F:
        operator: SingleFileOperator = operator_cls(os.path.join(self.task_dir, name))
        if not name.endswith(operator.file_suffix()):
            # 自动补充文件后缀名
            name = name + operator.file_suffix()
        res = SingleFileResource(operator=operator)
        self.resource_dict[name] = res
        return operator

    def genBatchFileOperator(
        self, name: str, operator_cls: Type[F]
    ) -> BatchFileOperator:
        operator: BatchFileOperator = BatchFileOperator(
            folder=os.path.join(self.task_dir, name), operator_cls=operator_cls
        )
        res = BatchFileResource(operator=operator)
        self.resource_dict[name] = res
        return operator

    def load(self):
        for _, r in self.resource_dict.items():
            r.load()

    def save(self):
        for _, r in self.resource_dict.items():
            r.save()
