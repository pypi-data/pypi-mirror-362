import asyncio
import os
import sys
import atexit
import time
import chardet


def better_kill(process, raiseError: bool):
    """优雅地终止进程，如果超时则强制终止"""
    try:
        process.terminate()  # 先尝试优雅终止
        time.sleep(5)  # 等待5秒
    except asyncio.TimeoutError:
        try:
            process.kill()  # 如果超时，强制终止
        except:
            if raiseError:
                raise
            else:
                pass
    except Exception as e:
        # print(f"Error while terminating process: {e}")
        if raiseError:
            raise
        else:
            pass



async def read_stream(stream, log, separator=b'\n'):
    def log_func(data):
        try:
            data = data.decode().strip()
            log(data)
        except:
            try:
                encoding = chardet.detect(data)['encoding']
                data = data.decode(encoding).strip()
            finally:
                log(data)

    while True:
        try:
            line = await stream.readuntil(separator)
            log_func(line)
        except asyncio.IncompleteReadError as e:
            # If the stream ends without a separator, output the remaining content
            if e.partial:
                log_func(e.partial)
            break
        except asyncio.LimitOverrunError as e:
            # If the separator is found but not within the limit, read the chunk
            chunk = await stream.read(e.consumed)
            log_func(chunk)




async def execute_script(script_path, *args, cwd=None, env=None):
    cwd = cwd or os.path.dirname(script_path)
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-u",
        script_path,
        *args,
        cwd=cwd,
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    return process


async def execute_script_and_block(script_path, log, *args, cwd=None, env=None):
    try:
        # 执行脚本
        process = await execute_script(script_path, *args, cwd=cwd, env=env)
    except Exception as e:
        better_kill(process, False)
        raise Exception(f"Failed to execute script: {e}")

    try:
        # 开始并行读取 stdout 和 stderr
        stdout_task = asyncio.create_task(read_stream(process.stdout, log))
        stderr_task = asyncio.create_task(read_stream(process.stderr, log))

        # 注册atexit处理程序
        async def cleanup():
            better_kill(process, False)
            stdout_task.cancel()
            stderr_task.cancel()
        atexit.register(cleanup)

        # 等待进程完成
        return_code = await process.wait()

        # 等待读取任务完成
        await stdout_task
        await stderr_task

    except Exception as e:
        better_kill(process, False)
        stdout_task.cancel()
        stderr_task.cancel()
        raise Exception(f"Error during script execution or stream reading: {e}")

    # 检查返回码
    if return_code != 0:
        better_kill(process, False)
        raise Exception("Error executing script, return code: {}".format(return_code))

    # 如果一切正常，返回成功
    return "success"



async def execute_script_no_block(script_path, log, *args, cwd=None, env=None):
    process = await execute_script(script_path, *args, cwd=cwd, env=env)

    # Start reading stdout and stderr in parallel
    stdout_task = asyncio.create_task(read_stream(process.stdout, log))
    stderr_task = asyncio.create_task(read_stream(process.stderr, log))

    # Register atexit handler to ensure process cleanup
    def cleanup():
        better_kill(process, False)
        stdout_task.cancel()
        stderr_task.cancel()

    atexit.register(cleanup)

    return process, stdout_task, stderr_task