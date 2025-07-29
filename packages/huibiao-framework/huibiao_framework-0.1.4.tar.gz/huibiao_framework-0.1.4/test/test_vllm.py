

# 使用示例
import asyncio

from huibiao_framework.client.huize_qwen32b_awq_client import HuiZeQwen32bQwqClient


async def main():
    # 方式1：使用上下文管理器（推荐，自动管理生命周期）
    async with HuiZeQwen32bQwqClient() as client:  # 实例化客户端
        result = await client.query("今天日期是什么？")
        result2 = await client.query("今天天气如何呢？")
        print("查询结果：", result, result2)

    # 方式2：手动管理生命周期
    # client = HuiZeQwen32bQwqClient()
    # try:
    #     result = await client.query("北京天气如何？")
    #     print("查询结果：", result)
    # finally:
    #     await client.close()

if __name__ == "__main__":
    asyncio.run(main())