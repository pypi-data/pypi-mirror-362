import os
import importlib
from .lib.change_directory import ModuleManager, wrapped_func
from solocompany import utils
import json
from ..address import Address, from_js_dict


params = utils.params


def ref_workflow(address: Address|dict, config=None):
    if isinstance(address, dict):
        address = from_js_dict(address)
    item_id = address.relative_path
    
    code_folder = address.to_fs_path()
    with open(code_folder + "/info.json", "r", encoding="utf-8") as f:
        name = json.load(f)["name"]
        
    if not os.path.exists(code_folder):
        print(f"Workflow {name}({item_id}) not found")
        return None

    try:
        with ModuleManager(code_folder) as manager:
            from solocompany.tool.tool_decorator import all_tools, clear_tools
            clear_tools()
            importlib.import_module("tool")
            export_tools = [tool for tool in all_tools]

    except Exception:
        import traceback
        print(f"Error loading workflow {name}({item_id}): \n{traceback.format_exc()}")
        return None

    assert len(export_tools) == 1, f"Workflow {name}({item_id}) should have only one tool"
    tool = wrapped_func(export_tools[0], code_folder)
    if tool.__doc__ is None:
        tool.__doc__ = "This tool is used to " + tool.__name__.replace("_", " ") + "."
    return tool
