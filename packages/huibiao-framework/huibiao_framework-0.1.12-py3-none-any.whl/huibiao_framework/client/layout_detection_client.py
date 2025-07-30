import time
import uuid
from typing import Optional
from huibiao_framework.config.config import ModelConfig
import aiohttp
from loguru import logger
import requests
import json
import base64
from huibiao_framework.execption.ocr import (
    LayoutDetectionResponseCodeError,
    LayoutDetectionResponseFormatError,
)


def encode_base64_string(image_path):
    with open(image_path, "rb") as f:
        encoded_string = str(base64.urlsafe_b64encode(f.read()), "utf-8")
    return encoded_string


class LayoutDetectionClient:
    """
    tender-ocr的文件实现类（实例化版本，支持异步请求）
    url: http://host:port/image_layout
    request:
        payload = {"data": encode_base64_string(file_path)}
        headers = {
                "Content-Type": "application/json",  # 根据需要设置内容类型
                "x-request-id": reqid
                }
    response:
        {
            "code": 0,
            "result": {
                "width": 1266,
                "height": 1806,
                "angle": 0,
                "version": "0.3.32",
                "layouts": [
                    {
                        "score": 0.983,
                        "type": "table",
                        "bbox": [
                                    [
                                        139,
                                        1128
                                    ],
                                    [
                                        1122,
                                        1128
                                    ],
                                    [
                                        1122,
                                        1618
                                    ],
                                    [
                                        139,
                                        1618
                                    ]
                                ]
                    },...
                ]
            }
        }
    """

    def __init__(self, section_id: str = ""):
        self.LAYOUT_DETECTION_TYY_URL = ModelConfig.LAYOUT_DETECTION_TYY_URL
        self.__session: Optional[aiohttp.ClientSession] = None  # 实例变量存储会话
        self.__is_closed = False  # 实例级别的关闭状态
        self.__session_id = section_id if section_id else uuid.uuid4()

    @property
    def session_id(self):
        return self.__session_id

    async def _ensure_session(self):
        """确保会话已初始化（实例方法）"""
        if self.__is_closed:
            raise RuntimeError("客户端已关闭，无法再使用，请重新创建实例")
        if not self.__session:
            self.__session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )

    async def init(self) -> "LayoutDetectionClient":
        """初始化客户端（可选，会自动调用）"""
        await self._ensure_session()
        return self

    async def layout_detection(self, image_path: str, reqid: str) -> Optional[str]:
        """发送查询请求到OCR模型（实例方法）"""

        file_path = image_path
        # 确保会话可用
        await self._ensure_session()
        assert self.__session is not None, "会话初始化失败"
        start_time = time.time()
        try:
            payload = {"data": encode_base64_string(file_path)}
            headers = {
                "Content-Type": "application/json",  # 根据需要设置内容类型
                "x-request-id": reqid,
            }
            # 发送异步POST请求
            async with self.__session.post(
                self.LAYOUT_DETECTION_TYY_URL, json=payload, headers=headers
            ) as resp:
                sp_time = time.time() - start_time
                logger.debug(
                    f"LayoutDetection[{self.session_id}],resp-{resp.status}, 响应时间: {sp_time:.2f}秒"
                )
                resp.raise_for_status()  # 检查HTTP状态码
                response_code = await resp.status_code
                response_data = await json.loads(resp.text)  # 异步解析JSON
        except aiohttp.ClientError as e:
            logger.error(f"LayoutDetection[{self.session_id}]请求异常", e)
            raise e
        # 解析响应结果
        code: int = response_code
        if code != 200:
            logger.error(f"LayoutDetection[{self.session_id}]响应失败，code={code}")
            raise LayoutDetectionResponseCodeError(code)
        if "result" not in response_data:
            logger.error(
                f"LayoutDetection[{self.session_id}]响应格式异常, 缺少result字段"
            )
            raise LayoutDetectionResponseFormatError("响应体缺少result字段")
        if "layouts" not in response_data["result"]:
            logger.error(
                f"LayoutDetection[{self.session_id}]响应格式异常, 缺少result.layouts字段"
            )
            raise LayoutDetectionResponseFormatError("响应体缺少result.layouts字段")
        return response_data["result"]["layouts"]

    async def close(self) -> None:
        """关闭aiohttp会话（释放资源，实例方法）"""
        if self.__session and not self.__is_closed:
            await self.__session.close()
            self.__session = None
            self.__is_closed = True
            logger.debug(f"HuiZeQwen32bQwq[{self.session_id}]会话已关闭")

    async def __aenter__(self):
        """异步上下文管理器：进入时初始化会话（实例方法）"""
        await self.init()
        logger.debug(f"HuiZeQwen32bQwq[{self.session_id}]模型会话已初始化")
        return self  # 返回实例本身

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器：退出时自动关闭会话（实例方法）"""
        await self.close()
