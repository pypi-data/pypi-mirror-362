from lib2to3.btm_matcher import BMNode

import redis.asyncio as redis
from huibiao_framework.config import RedisConfig


class HuibiaoAsyncRedisClientFactory:
    """
    基于redis.asyncio版本的redis客户端工厂，维护一个连接池，从连接池中获取redis客户端
    """

    __connection_pool: redis.ConnectionPool = None

    @classmethod
    def __init_pool(cls):
        if cls.__connection_pool is not None:
            return

        pool = redis.ConnectionPool
        if RedisConfig.REDIS_MODE == "single":
            pool = redis.ConnectionPool(
                host=RedisConfig.REDIS_HOST,
                port=RedisConfig.REDIS_PORT,
                db=RedisConfig.REDIS_DB,
            )
        elif RedisConfig.REDIS_MODE == "sentinel":
            pass
        elif RedisConfig.REDIS_MODE == "cluster":
            pass  # todo

        cls.__connection_pool = pool

    # @classmethod
    # def get_client(cls):
    #
    #
    #
    #     if not cls.__client is not None:
    #         pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
    #         redis.ConnectionPool(host="localhost", port=6379, db=0)
    #
    #         redis_client = redis.Redis(host="localhost", port=6370, db=0, password="123456")
    #
    #     return cls.__client
