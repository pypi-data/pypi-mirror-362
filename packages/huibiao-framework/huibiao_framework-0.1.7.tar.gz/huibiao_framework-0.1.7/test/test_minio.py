import asyncio
from loguru import logger
from huibiao_framework.config import MinioConfig
from huibiao_framework.client import MinIOClient


async def example_usage():

    try:
        async with MinIOClient() as client:
            # 上传文件
            # await client.upload_file(MinioConfig.OSS_ENDPOINT, "test/testfile.txt", "testfile.txt")
            #
            # # 列出桶中的对象
            objects = await client.list_objects(MinioConfig.BUCKET_NAME)
            buckets = await client.list_buckets()
            logger.info(f"buckets = {buckets}")
            logger.info(f"桶中的对象: {objects}")


            await client.upload_file(MinioConfig.BUCKET_NAME, "task/testfile5.txt", "testfile.txt") # 不能从/开始

            # # 下载文件
            # await client.download_file(MinioConfig.BUCKET_NAME, "example.txt", "downloaded.txt")
            #
            # # 获取预签名URL
            # url = await client.get_object_url(MinioConfig.BUCKET_NAME, "example.txt")
            # logger.info(f"预签名URL: {url}")
            #
            # # 删除对象
            # await client.remove_object(MinioConfig.BUCKET_NAME, "example.txt")
            #
            # # 删除桶
            # await client.delete_bucket(await client.remove_object(MinioConfig.BUCKET_NAME, "example.txt")
            #
            # await client.close()
    except Exception as e:
        logger.error("error")
        raise e

if __name__ == "__main__":
    asyncio.run(example_usage())