import os
from collections import defaultdict
from pathlib import Path
from solocompany.reference.member import ref_member
from solocompany.reference.mcp import ref_mcp
from solocompany.reference.tool import ref_tools
from solocompany.reference.workflow import ref_workflow
from ..address import from_js_dict


async def get_abilities(cwd, member_setting):
    tool_call = member_setting["toolCall"]
    abilities = []
    mcp_servers = []
    
    item_list = tool_call["Member"]
    for item in item_list:
        item = ref_member(from_js_dict(item["address"]), item["config"])
        if item:
            abilities.append(item)
            
    item_list = tool_call["MCPTool"]
    for item in item_list:
        item = ref_mcp(from_js_dict(item["address"]), item["config"], cwd)
        if item:
            mcp_server = await item.__aenter__()
            mcp_servers.append(mcp_server)

    item_list = tool_call["Tool"]
    for item in item_list:
        items = ref_tools(from_js_dict(item["address"]), item["config"], cwd)
        abilities.extend(items)
    
    item_list = tool_call["Workflow"]
    for item in item_list:
        item = ref_workflow(from_js_dict(item["address"]), item["config"])
        if item:
            abilities.append(item)
    return abilities, mcp_servers


def resolve_relative_path(cwd:str, path_str: str) -> str:
    """返回基于CWD的规范化绝对路径"""
    path = Path(path_str)
    if path.is_absolute():
        return str(path.resolve())
    else:
        return str((Path(cwd) / path_str).resolve())


def read_local_file(file_path: str) -> str:
    """读取本地文件内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        import chardet

        with open(file_path, "rb") as f:
            rawdata = f.read()
            encoding = chardet.detect(rawdata)["encoding"]
            return rawdata.decode(encoding)


# 全局忽略列表
IGNORE_LIST = [
  'node_modules',
  '.git',
  '.vscode',
  '.idea',
  'gitServer',
  '.DS_Store',
  '$RECYCLE.BIN',
  '.Trash-1000',
  '.Spotlight-V100',
  '.Trashes',
  '.TemporaryItems',
  '.fseventsd',
  'System Volume Information',
  'pycache',
  'env',
  'venv',
  'target/dependency',
  'build/dependencies',
  'dist',
  'out',
  'bundle',
  'vendor',
  'tmp',
  'temp',
  'deps',
  'pkg',
  'Pods',
  'build',
  '.egg-info',
  '.venv',
  '__pycache__',
  '.vs',
  '.next',
  '.nuxt',
  '.cache',
  '.sass-cache',
  '.gradle',
  '.ipynb_checkpoints',
  '.pytest_cache',
  '.mypy_cache',
  '.tox',
  '.hg',
  '.svn',
  '.bzr',
  '.lock-wscript',
  '.wafpickle-[0-9]*',
  '.lock-waf_[0-9]*',
  '.Python',
  '.jupyter',
  '.vscode-test',
  '.history',
  '.yarn',
  '.yarn-cache',
  '.eslintcache',
  '.parcel-cache',
  '.cache-loader',
  '.nyc_output',
  '.node_repl_history',
  '.pnp.js',
  '.pnp',
  '.obsidian',
  ".husky",
  '.github',
  ".changeset"
]


def should_ignore(path):
    """检查路径是否在忽略列表中"""
    parts = path.split(os.sep)
    return any(part in IGNORE_LIST for part in parts)


def get_files_and_folders(root, recursive: bool):
    """递归获取所有文件和文件夹，并记录属性"""
    items = []

    # 使用 os.walk 遍历目录
    for dirpath, dirnames, filenames in os.walk(root):
        # 排除忽略列表中的路径
        if should_ignore(dirpath):
            continue

        # 记录文件夹
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            if not should_ignore(full_path):
                relative_path = os.path.relpath(full_path, root)
                is_empty = not os.listdir(full_path)
                depth = relative_path.count(os.sep)
                items.append(
                    (relative_path, "empty_folder" if is_empty else "folder", depth)
                )

        # 记录文件
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if not should_ignore(full_path):
                relative_path = os.path.relpath(full_path, root)
                depth = relative_path.count(os.sep)
                items.append((relative_path, "file", depth))

        # 如果 recursive 为 False，则只遍历当前目录，不进入子目录
        if not recursive:
            break

    return items


def format_filelist_str(items, limit):
    """根据limit格式化输出"""
    depth_groups = defaultdict(list)
    for item in items:
        depth_groups[item[2]].append(item)

    max_depth = max(depth_groups.keys(), default=0)
    show_list = []
    last_depth = 0

    # 浅层
    current_items = sorted(depth_groups[0], key=lambda x: x[0])
    overflow = len(current_items) > limit
    for item in current_items[:limit]:
        show_list.append(item)

    for depth in range(1, max_depth + 1):
        current_items = depth_groups[depth]
        if len(show_list) + len(current_items) <= limit:
            last_depth = depth
            for item in current_items:
                show_list.append(item)
        else:
            break

    result_str_list = []
    show_list.sort(key=lambda x: x[0])
    for item in show_list:
        if item[1] == "file":
            result_str_list.append(f"{item[0]}")
        elif item[1] == "folder" and item[2] == last_depth:
            result_str_list.append(f"{item[0]}/more...")
        else:
            result_str_list.append(f"{item[0]}/")
    if overflow:
        result_str_list.append("more...")

    return "\n".join(result_str_list)


def get_formatted_filelist_str(root: str, recursive: bool, limit=200):
    items = get_files_and_folders(root, recursive)
    return format_filelist_str(items, limit=limit)
