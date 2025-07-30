import inspect
import asyncio
import nest_asyncio

nest_asyncio.apply() 

def call_func(func, args=None, kwargs=None):
    """
        args:是一个元组
        kwargs:是一个字典
    """
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    if inspect.isgeneratorfunction(func):
        return list(func(*args, **kwargs))
    elif inspect.isasyncgenfunction(func):
        async def collect_async_gen():
            return [item async for item in func(*args, **kwargs)]
        
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(collect_async_gen())
        else:
            async def run_async_gen():
                return await collect_async_gen()
            future = asyncio.ensure_future(run_async_gen())
            while not future.done():
                loop.run_until_complete(asyncio.sleep(0.1))  # 避免阻塞
            return future.result()
    elif inspect.iscoroutinefunction(func):
        coro = func(*args, **kwargs) if inspect.iscoroutinefunction(func) else func
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)
        else:
            async def run_coro():
                return await coro
            future = asyncio.ensure_future(run_coro())
            while not future.done():
                loop.run_until_complete(asyncio.sleep(0.1))  # 避免阻塞
            return future.result()
    else:
        return func(*args, **kwargs)