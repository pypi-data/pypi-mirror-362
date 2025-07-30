from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ProgressSend:
    class AnalysisType(str, Enum):
        """分析类型枚举"""

        ANALYZE = "analyze"  # 智析
        COMPARE = "compare"  # 相似比较
        DIFF_COMPARE = "diffCompare"  # 差异比较
        INQUIRE = "inquire"  # 智查
        WRITE = "write"  # 智写

    class RequestDto(BaseModel):
        progress: str
        step: str
        ratio: str
        type: Optional["ProgressSend.AnalysisType"]
        projectId: str
        recordId: str

    class ResponseVo(BaseModel):
        """API响应视图对象"""

        result: bool  # 操作结果状态 - True
        retCode: str  # 返回码 - 200
        detailMsg: str  # 详细消息 - 操作成功

        def is_success(self):
            return self.result and self.retCode == "200"
