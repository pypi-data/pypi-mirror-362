import asyncio
import os
import atexit

from .chat_base import handle_user_inputs
from .message import clear_chat_data, CHAT_DATA


async def interrupt_raise_cancelled_error(interval, interrupt_file, chat_task):
    while True:
        await asyncio.sleep(interval)
        if os.path.exists(interrupt_file):
            os.remove(interrupt_file)
            chat_task.cancel()
            break



async def run_with_interrupt_check(
    conversation_history,
    user_input,
    cwd: str,
    abilities,
    mcp_servers,
    member_setting,
    member_setting_file:str,
    interrupt_file,
):
    clear_chat_data()
    try:
        chat_task = asyncio.create_task(
            handle_user_inputs(
                conversation_history,
                user_input,
                cwd,
                abilities,
                mcp_servers,
                member_setting,
                member_setting_file
            )
        )
        check_task = asyncio.create_task(
            interrupt_raise_cancelled_error(0.5, interrupt_file, chat_task)
        )
        def cleanup():
            chat_task.cancel()
            check_task.cancel()
        atexit.register(cleanup)
        result = await chat_task
        return result
    except asyncio.CancelledError:
        return CHAT_DATA["info"]
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return None  # 返回 None 或者处理异常后的结果
    finally:
        if not chat_task.done():
            chat_task.cancel()
        # 确保即使发生异常也会取消检查任务
        if not check_task.done():
            check_task.cancel()
            try:
                await check_task
            except asyncio.CancelledError:
                pass  # 忽略取消错误