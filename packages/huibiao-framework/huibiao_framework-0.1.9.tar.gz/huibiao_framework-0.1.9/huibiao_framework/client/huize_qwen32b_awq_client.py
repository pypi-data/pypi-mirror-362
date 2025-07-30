import time
import uuid
from typing import Optional

import aiohttp
from loguru import logger

from huibiao_framework.config.config import ModelConfig
from huibiao_framework.execption.vllm import (
    Qwen32bAwqResponseCodeError,
    Qwen32bAwqResponseFormatError,
)


class HuiZeQwen32bQwqClient:
    """
    慧泽Qwen-32B模型客户端（实例化版本，支持异步请求）
    url: http://vllm-qwen-32b.model.hhht.ctcdn.cn:9080/common/query
    request:
        {
        "Action": "NormalChat",
        "DoSample": true,
        "Messages": [
                {
                    "content": "请将下面这段英文翻译成中文：请将下面这段英文翻译成中文：I am a test。",
                    "role": "user"
                }
            ]
        }
    response:
        {
            "code": 0,
            "result": {
                "Output": "我是一个测试。",
                "TokenProbs": [
                    1.0
                ]
            },
            "message": "success"
        }
    """

    def __init__(self, section_id: str = ""):
        self.REQUEST_URL = ModelConfig.REQUEST_URL
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

    async def init(self) -> "HuiZeQwen32bQwqClient":
        """初始化客户端（可选，会自动调用）"""
        await self._ensure_session()
        return self

    async def query(self, prompt: str) -> Optional[str]:
        """发送查询请求到Qwen-32B模型（实例方法）"""
        # 处理过长prompt
        if len(prompt) > 16000:
            prompt = prompt[:7000] + prompt[-7000:]

        # 验证prompt有效性
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must be a non-empty string")

        # 确保会话可用
        await self._ensure_session()
        assert self.__session is not None, "会话初始化失败"

        # 构建请求数据
        messages = [{"role": "user", "content": prompt}]
        data = {"Action": "NormalChat", "Messages": messages}

        start_time = time.time()
        try:
            # 发送异步POST请求
            async with self.__session.post(self.REQUEST_URL, json=data) as resp:
                sp_time = time.time() - start_time
                logger.debug(
                    f"huizeQwen32b[{self.session_id}],resp-{resp.status},prompt长度{len(prompt)},响应时间: {sp_time:.2f}秒"
                )
                resp.raise_for_status()  # 检查HTTP状态码
                response_data = await resp.json()  # 异步解析JSON

        except aiohttp.ClientError as e:
            logger.error(f"HuiZeQwen32bQwq[{self.session_id}]请求异常", e)
            raise e

        # 解析响应结果
        code: int = response_data["code"]
        if code != 0:
            logger.error(f"huizeQwen32b[{self.session_id}]响应失败，code={code}")
            raise Qwen32bAwqResponseCodeError(code)
        if "result" not in response_data:
            logger.error(f"huizeQwen32b[{self.session_id}]响应格式异常, 缺少result字段")
            raise Qwen32bAwqResponseFormatError("响应体缺少result字段")
        if "Output" not in response_data["result"]:
            logger.error(
                f"huizeQwen32b[{self.session_id}]响应格式异常, 缺少result.Output字段"
            )
            raise Qwen32bAwqResponseFormatError("响应体缺少result.Output字段")

        # 处理返回内容
        str_input = response_data["result"]["Output"]
        str_input = str_input.split("</think>")[-1]

        return str_input

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
