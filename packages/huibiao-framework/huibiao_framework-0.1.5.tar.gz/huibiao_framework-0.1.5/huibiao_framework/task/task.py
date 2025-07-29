import time
from abc import ABC, abstractmethod
from functools import wraps
from typing import Generic, List, Type, TypeVar

from loguru import logger

from huibiao_framework.resource import TaskResource
from huibiao_framework.task.resource_sync_minio import TaskResourceSyncMinio
from huibiao_framework.utils.annotation import frozen_attrs

TS = TypeVar("TS", bound=TaskResource)


@frozen_attrs("task_type", "request_id", "task_id")
class HuibiaoTask(Generic[TS], ABC):
    def __init__(
        self,
        *,
        task_type: str,
        task_id: str,
        request_id: str,
        task_resource_cls: Type[TS],
    ):
        self.task_id = task_id  # 即project id
        self.task_type = task_type
        self.request_id = request_id
        self.__resource: TS = task_resource_cls(task_type, task_id)
        self.__resource_sync_client = TaskResourceSyncMinio(
            task_resource=self.task_resource
        )

    @property
    def task_resource(self) -> TS:
        return self.__resource

    @property
    def task_desc(self):
        return f"[{self.task_type}][task_id={self.task_id}][reqid={self.request_id}]"

    def genSyncMinioClient(self) -> TaskResourceSyncMinio:
        return TaskResourceSyncMinio(task_resource=self.task_resource)

    async def init_task(self):
        await self.__resource_sync_client.init()
        # 其他前置操作，加载任务上下文，待实现

    async def upload_resource(self, resource_name: str):
        _resource_obj = self.task_resource[resource_name]
        await self.__resource_sync_client.upload_file(resource_name, _resource_obj)

    async def run_pipeline(self):
        await self.init_task()
        logger.info(f"{self.task_desc}任务初始化成功,开始执行任务")
        await self.pipeline()
        logger.info(f"{self.task_desc}任务完成")

    @abstractmethod
    async def pipeline(self):
        pass

    @staticmethod
    def StepAnnotation(
        step_name: str = None, *, depend: List[str] = None, output: str = None
    ):
        depend = list() if depend is None else depend

        def decorator(func):
            @wraps(func)
            async def wrapper(self: "HuibiaoTask[TS]", *args, **kwargs):
                name = step_name or func.__name__  # 步骤名

                do_task = False  # 是否执行任务的标志

                if output is not None:
                    if not self.task_resource[output].is_completed():
                        do_task = True
                    else:
                        logger.info(
                            f"{self.task_desc}任务[步骤{name}]产出资源[{output}]已完成"
                        )

                # 任务结束信号检测

                # 预加载资源 depend_resources
                if do_task:
                    # 加载依赖资源
                    for d_r in depend:
                        self.task_resource[d_r].load()

                    start = time.perf_counter()
                    result = await func(self, *args, **kwargs)
                    elapsed = time.perf_counter() - start
                    logger.info(
                        f"{self.task_desc}任务[步骤{name}]耗时: {elapsed:.6f} 秒"
                    )

                    # 标记资源完成 output_resources
                    if output is not None:
                        self.task_resource[output].complete()
                        # 将资源上传到minio
                        await self.upload_resource(output)  # todo 后续使用线程池实现

                    return result
                else:
                    logger.info(f"{self.task_desc}任务步骤[{name}]已完成，跳过该步骤")

            return wrapper

        return decorator
