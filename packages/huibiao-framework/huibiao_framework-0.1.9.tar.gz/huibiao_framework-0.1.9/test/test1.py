import asyncio
import time

from huibiao_framework.utils.time_cost_utils import function_time_cost
@function_time_cost(step_name="测试异步函数")
async def async_fun():
    await asyncio.sleep(1)
    print("coro")

@function_time_cost(step_name="测试同步函数")
def myfun():
    time.sleep(1)



# 调用
myfun()
asyncio.run(async_fun())