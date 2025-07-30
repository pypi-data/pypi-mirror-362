import time
from abc import ABC, abstractmethod
from functools import wraps
from typing import Generic, List, Type, TypeVar, Dict, Optional

import aiohttp
from loguru import logger

from huibiao_framework.client.data_model.ffcs import ProgressSend
from huibiao_framework.client.ffs_progress_client import FfcsClient
from huibiao_framework.execption.ffcs import FfcsSendProgressError
from huibiao_framework.resource import TaskResource
from huibiao_framework.task.resource_sync_minio import TaskResourceSyncMinio
from huibiao_framework.utils.annotation import frozen_attrs

TS = TypeVar("TS", bound=TaskResource)


def inner_step_annotation(step_name: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self: "HuibiaoTask[TS]"):
            start_time = time.perf_counter()
            try:
                await func(self)
            except Exception as e:
                logger.error(f"{self.step_log_str(step_name)}失败, {str(e)}")
                raise e
            finally:
                elapsed = time.perf_counter() - start_time
                logger.info(f"{self.step_log_str(step_name)}耗时: {elapsed:.6f} 秒")
                self._time_cost_record[step_name] = elapsed

        return wrapper

    return decorator


@frozen_attrs(
    "task_type", "request_id", "project_id", "progress_send_analyse_type", "record_id"
)
class HuibiaoTask(Generic[TS], ABC):
    def __init__(
        self,
        *,
        task_type: Optional[str] = None,
        project_id: Optional[str] = None,
        request_id: Optional[str] = None,
        record_id: Optional[str] = None,
        task_resource_cls: Type[TS],
        is_send_progress: bool = False,  # 是否发送进度
        progress_send_analyse_type: Optional[ProgressSend.AnalysisType],
    ):
        self.project_id = project_id
        self.task_type = task_type
        self.request_id = request_id
        self.record_id = record_id

        # 进度发送
        self.is_send_progress = is_send_progress
        self.progress_send_analyse_type = (
            progress_send_analyse_type  # 发送进度时需要指定一个任务类型
        )

        # 资源
        self.__resource: TS = task_resource_cls(task_type, project_id)
        self.__resource_sync_client = TaskResourceSyncMinio(
            task_resource=self.task_resource
        )

        # 耗时
        self._time_cost_record: Dict[str, float] = {}
        self.__time_cost_all: float = 0

    @property
    def task_resource(self) -> TS:
        return self.__resource

    @property
    def task_desc(self):
        return (
            f"[{self.task_type}][project_id={self.project_id}][reqid={self.request_id}]"
        )

    def genSyncMinioClient(self) -> TaskResourceSyncMinio:
        return TaskResourceSyncMinio(task_resource=self.task_resource)

    @inner_step_annotation("pipeline前置初始化")
    async def init_task(self):
        await self.__resource_sync_client.init()
        # 其他前置操作，加载任务上下文，待实现

    @inner_step_annotation("pipeline后置操作")
    async def post_action(self):
        """
        任务完成后的一些后处理步骤，后续丢到线程池里面执行
        """
        # 打印耗时
        step_time_cost_info = "\n".join(
            [f"{k} -> {v}" for k, v in self._time_cost_record.items()]
        )
        logger.info(f"{self.task_desc}整体耗时，分步耗时：{step_time_cost_info}")
        await self.__resource_sync_client.close()

    async def upload_resource(self, resource_name: str):
        _resource_obj = self.task_resource[resource_name]
        await self.__resource_sync_client.upload_file(resource_name, _resource_obj)

    async def run_pipeline(self):
        await self.init_task()
        logger.info(f"{self.task_desc}任务初始化成功,开始执行任务")
        start = time.perf_counter()
        try:
            result = await self.pipeline()
            logger.info(f"{self.task_desc}任务完成")
            return result
        except Exception as e:
            logger.error(f"{self.task_desc}任务失败", e)
            raise e
        finally:
            self._time_cost_record = time.perf_counter() - start
            await self.post_action()

    @abstractmethod
    async def pipeline(self):
        """
        算法同事实现该部分
        """
        pass

    def step_log_str(self, step_name):
        return f"{self.task_desc}的[{step_name}]步骤"

    async def send_progress(self, progress_send_dto: ProgressSend.RequestDto):
        if self.is_send_progress:
            progress_send_dto.projectId = self.project_id
            progress_send_dto.type = self.progress_send_analyse_type
            progress_send_dto.recordId = self.record_id
            async with aiohttp.ClientSession() as _session:
                client = FfcsClient(_session)
                return await client.send_progress(
                    progress_send_dto, reqid=self.request_id
                )

    @staticmethod
    def StepAnnotation(
        step_name: str = None,
        *,
        depend: List[str] = None,
        output: str = None,
        progress_send_dto: ProgressSend.RequestDto,
    ):
        depend = list() if depend is None else depend

        def decorator(func):
            @wraps(func)
            async def wrapper(self: "HuibiaoTask[TS]", *args, **kwargs):
                name = step_name or func.__name__  # 步骤名

                do_task = False  # 是否执行任务的标志
                elapsed: float = 0

                if output is not None:
                    if not self.task_resource[output].is_completed():
                        do_task = True
                    else:
                        logger.info(
                            f"{self.step_log_str(step_name)}产出资源[{output}]已完成"
                        )
                else:
                    do_task = True

                # 预加载资源 depend_resources
                if do_task:
                    # 加载依赖资源
                    for d_r in depend:
                        self.task_resource[d_r].load()

                    start = time.perf_counter()
                    try:
                        await func(self, *args, **kwargs)
                    except Exception as e:
                        logger.error(
                            f"{self.step_log_str(step_name)}失败: {elapsed:.6f} 秒"
                        )
                        raise e
                    finally:
                        elapsed = time.perf_counter() - start
                        logger.info(
                            f"{self.step_log_str(step_name)}完成，耗时: {elapsed:.6f} 秒"
                        )
                        self._time_cost_record[name] = elapsed

                    # 进度推送
                    if self.is_send_progress and progress_send_dto is not None:
                        try:
                            await self.send_progress(progress_send_dto)
                        except FfcsSendProgressError:
                            pass  # 进度推送失败时不报错，不阻塞

                    # 标记资源完成 output_resources
                    if output is not None:
                        self.task_resource[output].complete()
                        # 将资源上传到minio
                        await self.upload_resource(
                            output
                        )  # todo 后续使用线程池实现，或者整体pipe失败时后处理再上传
                else:
                    logger.info(f"{self.step_log_str(step_name)}已完成，跳过该步骤")
                    self._time_cost_record[name] = elapsed

            return wrapper

        return decorator
