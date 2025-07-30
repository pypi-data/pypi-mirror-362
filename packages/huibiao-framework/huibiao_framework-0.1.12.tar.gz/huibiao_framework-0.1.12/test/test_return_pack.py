import asyncio


async def fun():
    return "a", 1

async def main():
    result = await fun()
    x, y = result
    print(y, x)


asyncio.run(main())