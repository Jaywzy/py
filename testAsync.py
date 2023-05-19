import asyncio

async def read(i):
    await asyncio.sleep(1)
    return i

async def testAsync():
    l = [1, 2, 3, 4, 5]
    for i in l:
        # print('i: ', i)
        p = await read(i)
        print('p: ', p)

loop = asyncio.get_event_loop()
loop.run_until_complete(testAsync())
loop.close()
print('end')