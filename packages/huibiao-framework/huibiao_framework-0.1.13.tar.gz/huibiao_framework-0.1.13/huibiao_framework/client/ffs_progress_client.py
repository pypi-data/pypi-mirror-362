from typing import Optional
import aiohttp
from loguru import logger

from huibiao_framework.config import FfcsConfig
from huibiao_framework.execption.ffcs import FfcsSendProgressError
from .data_model.ffcs import ProgressSend


class FfcsClient:
    """
    福富客户端 - 异步实现
    """

    def __init__(
        self,
        client: Optional[aiohttp.ClientSession] = None,
        max_retry: int = 3,
        retry_interval_sec: int = 3,
    ):
        self.__session = client
        self.__max_retry = max_retry
        self.__retry_interval_sec = retry_interval_sec

    async def send_progress(
        self, progress_dto: ProgressSend.RequestDto, reqid
    ) -> Optional[ProgressSend.ResponseVo]:
        url = FfcsConfig.PROGRESS_URL
        request_body: dict = progress_dto.model_dump()

        headers = {"Content-Type": "application/json", "x-request-id": reqid}
        try:
            async with self.__session.post(
                url, json=request_body, headers=headers
            ) as response:
                logger.debug(f"发送进度请求，reqid={reqid}，dto={request_body}")
                response_data = await response.json()
                vo = ProgressSend.ResponseVo(**response_data)
                logger.debug(f"发送进度成功，reqid={reqid}，vo={vo}")
                return vo
        except Exception as e:
            logger.error(f"发送进度失败，dto={request_body}, {str(e)}")
            raise FfcsSendProgressError(reason=str(e), e=e, reqid=reqid)
