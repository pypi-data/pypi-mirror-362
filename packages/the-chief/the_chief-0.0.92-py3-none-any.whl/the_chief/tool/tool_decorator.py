all_tools = []


def tool(func=None):
    def decorator(f):
        all_tools.append(f)
        return f

    if func is not None:
        return decorator(func)
    return decorator


single_process_tool = tool


def multi_process_tool(func=None):
    def decorator(f):
        all_tools.append(f)
        return f

    if func is not None:
        return decorator(func)
    return decorator


def generator_tool(func=None):
    def decorator(f):
        all_tools.append(f)
        return f

    if func is not None:
        return decorator(func)
    return decorator


def compatibility_tool(func=None):
    def decorator(f):
        all_tools.append(f)
        return f

    if func is not None:
        return decorator(func)
    return decorator


def clear_tools():
    all_tools.clear()
