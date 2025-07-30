import json
from solocompany import utils
import json
import inspect


params = utils.params


def get_ui():
    if params is None or "uiDataMap" not in params:
        return {}
    stack = inspect.stack()
    stack_files = list(reversed([s.filename.replace("\\", "/") for s in stack]))
    match_ui_file = None
    for f in stack_files:
        for v in params["uiDataMap"]:
            if v == f:
                match_ui_file = v
                break
        if match_ui_file is not None:
            break

    if match_ui_file is None:
        return {}
    
    for i in range(10):
        try:
            return params["uiDataMap"][match_ui_file]
        except Exception as e:
            if i == 9:
                raise e
