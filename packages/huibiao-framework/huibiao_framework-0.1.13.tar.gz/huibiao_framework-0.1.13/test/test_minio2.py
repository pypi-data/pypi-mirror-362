import asyncio
from loguru import logger
from huibiao_framework.config import MinioConfig
from huibiao_framework.client import MinIOClient
from huibiao_framework.execption.minio import MinioClientConnectException


async def example_usage():
    client = MinIOClient()
    try:
        await client.init()
        objects = await client.list_objects(MinioConfig.BUCKET_NAME)
        buckets = await client.list_buckets()
        logger.info(f"buckets = {buckets}")
        logger.info(f"桶中的对象: {objects}")
    except MinioClientConnectException as e:
        logger.error(f"连接MinIO失败: {e.reason}")
        return
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(example_usage())