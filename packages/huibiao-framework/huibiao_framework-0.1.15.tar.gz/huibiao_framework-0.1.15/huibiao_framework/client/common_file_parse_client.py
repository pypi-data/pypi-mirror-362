import time
import uuid
from typing import Optional
from huibiao_framework.config.config import ModelConfig
import aiohttp
from loguru import logger
import requests
import json
import os
import base64
from huibiao_framework.execption.ocr import (
    DocumentParseResponseCodeError,
    DocumentParseResponseFormatError,
)


def encode_base64_string(image_path):
    with open(image_path, "rb") as f:
        encoded_string = str(base64.urlsafe_b64encode(f.read()), "utf-8")
    return encoded_string


class DocumentParseClient:
    """
    convert_to_pdf的文件实现类（实例化版本，支持异步请求）
    url: http://host:port/convert
    request:
        params = {
            "FileName": file_name,
            'Dpi': 144,           # 分辨率设置为144 dpi 200dpi，dpi越大精度越高
            'UseFormula': False,  # True/False 是否启用公式识别，启用会增加耗时
            'PdfPwd':'',          # pdf为加密密码
            'PageStart': page_start,       # 开始页码
            'PageCount': page_count,      # 设置解析页数
            'TableFlavor': 'html',  # html/md 表格内容格式 html 或 markdown
            'ParseMode': 'auto',  # auto/scan  设置解析模式为scan模式时会强制进行ocr
            'ImageUpload': False,
            'ImageParse': False,
            }
        headers = {
                    "x-request-id": reqid
                    }

    response:

    """

    def __init__(self, section_id: str = ""):
        self.DOCUMENT_PARSER_TYY_URL = ModelConfig.DOCUMENT_PARSER_TYY_URL
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

    async def init(self) -> "DocumentParseClient":
        """初始化客户端（可选，会自动调用）"""
        await self._ensure_session()
        return self

    async def convert_to_pdf(
        self, pdf_path: str, page_count: int, page_start: int, reqid: str
    ) -> Optional[str]:
        """发送查询请求到转pdf模型（实例方法）"""

        # 确保会话可用
        await self._ensure_session()
        assert self.__session is not None, "会话初始化失败"
        start_time = time.time()
        try:
            file_name = os.path.basename(pdf_path)
            file = open(pdf_path, "rb")
            file_dict = {"File": file}
            params = {
                "FileName": file_name,
                "Dpi": 144,  # 分辨率设置为144 dpi 200dpi，dpi越大精度越高
                "UseFormula": False,  # True/False 是否启用公式识别，启用会增加耗时
                "PdfPwd": "",  # pdf为加密密码
                "PageStart": page_start,  # 开始页码
                "PageCount": page_count,  # 设置解析页数
                "TableFlavor": "html",  # html/md 表格内容格式 html 或 markdown
                "ParseMode": "auto",  # auto/scan  设置解析模式为scan模式时会强制进行ocr
                "ImageUpload": False,
                "ImageParse": False,
            }
            headers = {"x-request-id": reqid}
            # 发送异步POST请求
            async with self.__session.post(
                self.DOCUMENT_PARSER_TYY_URL,
                params=params,
                files=file_dict,
                headers=headers,
            ) as resp:
                sp_time = time.time() - start_time
                logger.debug(
                    f"DocumentParse[{self.session_id}],resp-{resp.status}, 响应时间: {sp_time:.2f}秒"
                )
                resp.raise_for_status()  # 检查HTTP状态码
                response_code = resp.status_code
                response_data = json.loads(resp.text)  # 异步解析JSON
        except aiohttp.ClientError as e:
            logger.error(f"DocumentParse[{self.session_id}]请求异常", e)
            raise e
        # 解析响应结果
        code: int = response_code
        if code != 200:
            logger.error(f"DocumentParse[{self.session_id}]响应失败，code={code}")
            raise DocumentParseResponseCodeError(code)
        if "result" not in response_data:
            logger.error(
                f"DocumentParse[{self.session_id}]响应格式异常, 缺少result字段"
            )
            raise DocumentParseResponseFormatError("响应体缺少result字段")

        return response_data["result"]

    async def close(self) -> None:
        """关闭aiohttp会话（释放资源，实例方法）"""
        if self.__session and not self.__is_closed:
            await self.__session.close()
            self.__session = None
            self.__is_closed = True
            logger.debug(f"DocumentParse[{self.session_id}]会话已关闭")

    async def __aenter__(self):
        """异步上下文管理器：进入时初始化会话（实例方法）"""
        await self.init()
        logger.debug(f"DocumentParse[{self.session_id}]模型会话已初始化")
        return self  # 返回实例本身

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器：退出时自动关闭会话（实例方法）"""
        await self.close()
