import os
from solocompany import utils
import json
import subprocess
import sys
from agents.mcp import MCPServerStdio, MCPServerSse 
from ..address import Address, from_js_dict

params = utils.params


def ref_mcp(address: Address|dict, config=None, working_directory=None):
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
        print(f"Mcp {name}({item_id}) not found")
        return None
    mcp_config_script = os.path.join(code_folder, "mcp_config.py")
    if not os.path.exists(mcp_config_script):
        print(f"Mcp {name}({item_id}) has no mcp_config.py")
        return None
    try:
        result = subprocess.run(
            [sys.executable, mcp_config_script], 
            capture_output=True,
            text=True,
            check=False,
            cwd=code_folder
        )
        return_code = result.returncode
        json_str = result.stdout
        error_output = result.stderr
        
        if return_code != 0:
            print(f"Error loading mcp {name}({item_id}): \n{error_output}")
            return None

        try:
            json_data = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Error decoding json from mcp {name}({item_id}): \n{json_str}")
            return None
        try:
            cwd = json_data["cwd"]
            if cwd:
                working_directory = cwd
        except:
            pass
        try:
            transport = json_data["transport"]
        except:
            print(f'Mcp {name}({item_id}) has no key "transport"')
            return None
        try:
            command = json_data["command"]
        except:
            print(f'Mcp {name}({item_id}) has no key "command"')
            return None
        try:
            args = json_data["args"]
            args = [arg.replace("$$WORKING_DIRECTORY$$", working_directory) for arg in args]
        except:
            print(f'Mcp {name}({item_id}) has no key "args"')
            return None
                
        if transport not in ["stdio", "sse"]:
            print(f"Mcp {name}({item_id}) has invalid transport {transport}")
            return None
        
        serverCls = MCPServerStdio if transport == "stdio" else MCPServerSse
        
        return serverCls(
            params={
                "command" : command,
                "args" : args,
                "cwd" : working_directory,
                "env" : None,
            },
            name = name,
            client_session_timeout_seconds=20
        )
        
    except Exception:
        import traceback
        print(f"Error loading mcp {name}({item_id}): \n{traceback.format_exc()}")
        return None