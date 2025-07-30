import os
import importlib
from .lib.change_directory import ModuleManager, wrapped_func
from solocompany import utils
import json
from ..address import Address, from_js_dict


params = utils.params


def ref_tools(address: Address|dict, config=None, working_directory=None):
    if isinstance(address, dict):
        address = from_js_dict(address)
    if config:
        execution_path_type = config.get("executionPathType", "codeFolder")
    else:
        execution_path_type = "codeFolder"
    ui_datas = config.get("uiDataMap", {}) if config else {}
    item_id = address.relative_path
    
    code_folder = address.to_fs_path()
    with open(code_folder + "/info.json", "r", encoding="utf-8") as f:
        name = json.load(f)["name"]
    if execution_path_type == 'codeFolder':
        working_directory = code_folder
        
    if not os.path.exists(code_folder):
        print(f"Tool {name}({item_id}) not found in:" + code_folder + "\n")
        return []

    try:
        with ModuleManager(code_folder) as manager:
            from solocompany.tool.tool_decorator import all_tools, clear_tools
            clear_tools()
            importlib.import_module("tool")
            export_tools = [tool for tool in all_tools]

    except Exception:
        import traceback
        print(f"Error loading tool {name}({item_id}): \n{traceback.format_exc()}")
        return []

    ret_export_tools = []
    for tool in export_tools:
        tool = wrapped_func(tool, working_directory, ui_datas)
            
        if tool.__doc__ is None:
            tool.__doc__ = "This tool is used to " + tool.__name__.replace("_", " ") + "."
        ret_export_tools.append(tool)

    return ret_export_tools



