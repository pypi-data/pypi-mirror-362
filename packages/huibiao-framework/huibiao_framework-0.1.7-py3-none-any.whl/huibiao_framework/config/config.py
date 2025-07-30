from dotenv import load_dotenv

from huibiao_framework.utils.meta_class import OsAttrMeta

load_dotenv(".env")


class TaskConfig(metaclass=OsAttrMeta):
    TASK_RESOURCE_DIR: str = "/task_resource"


class MinioConfig(metaclass=OsAttrMeta):
    ENDPOINT: str
    AK: str
    SK: str
    BUCKET_NAME: str = "huibiao"
    OSS_SECURE: bool = False


class ModelConfig(metaclass=OsAttrMeta):
    REQUEST_URL: str = "http://vllm-qwen-32b.model.hhht.ctcdn.cn:9080/common/query"
    IMAGE_OCR_TYY_URL: str
    LAYOUT_DETECTION_TYY_URL: str
    DOCUMENT_PARSER_TYY_URL: str
    CONVERT_TO_PDF_URL: str