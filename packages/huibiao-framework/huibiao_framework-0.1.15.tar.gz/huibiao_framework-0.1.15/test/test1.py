
from loguru import logger

try:
    1 / 0
except Exception as e:
    logger.error(f"错误, {str(e)}", e)
