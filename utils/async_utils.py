import asyncio


def create_async_task(function, *function_args):
    return asyncio.create_task(function(*function_args))


def get_async_tasks_results(async_tasks):
    return asyncio.gather(*async_tasks)
