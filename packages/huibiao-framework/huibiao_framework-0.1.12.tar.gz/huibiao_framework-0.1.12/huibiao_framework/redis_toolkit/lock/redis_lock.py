import asyncio

import redis.asyncio as redis


class AsyncRedisLock:
    def __init__(self, lock_key: str, lock_value: str):
        self.client = redis.Redis(host="localhost", port=6370, db=0, password="123456")
        self.lock_key = lock_key
        self.lock_value = lock_value

    async def acquire(self, expire=10, retry_times=30, retry_delay=5):
        """使用 SETNX 原子性获取锁"""
        for _ in range(retry_times):
            # SET key value NX EX expire 等同于 SETNX + EXPIRE 原子操作
            acquired = await self.client.set(
                self.lock_key,
                self.lock_value,
                nx=True,  # 仅在键不存在时设置（SETNX 效果）
                ex=expire,  # 设置过期时间，防止死锁 秒
            )
            if acquired:
                return self.lock_value
            await asyncio.sleep(retry_delay)

        return None

    async def release(self, lock_key, lock_value):
        script = """
        if redis.call("GET", KEYS[1]) == ARGV[1] then
            return redis.call("DEL", KEYS[1])
        else
            return 0
        end
        """
        return await self.client.eval(script, 1, lock_key, lock_value)

    async def __aenter__(self):
        """支持 async with 语法"""
        return await self.acquire() if self.lock_key else None

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """支持 async with 语法"""
        await self.release(self.lock_key, self.lock_value)
