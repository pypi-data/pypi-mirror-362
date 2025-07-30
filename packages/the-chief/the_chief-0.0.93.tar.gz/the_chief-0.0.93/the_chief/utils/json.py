import json
import re

def convert_ts_to_python(key: str) -> str:
    """将 TypeScript 风格的命名（camelCase）转换为 Python 风格的命名（snake_case）"""
    # 处理连续大写的情况（如 'ID' -> 'i_d'）
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return s2

def convert_python_to_ts(key: str) -> str:
    """将 Python 风格的命名（snake_case）转换为 TypeScript 风格的命名（camelCase）"""
    parts = key.split('_')
    return parts[0] + ''.join(part.capitalize() for part in parts[1:])

def dumps(obj, convert_keys=None, ensure_ascii=False, **kwargs):
    """
    将 Python 对象序列化为 JSON 字符串
    
    :param obj: 要序列化的 Python 对象
    :param convert_keys: 键名转换方式，可选:
        - 'to_python': 将 camelCase 转为 snake_case
        - 'to_ts': 将 snake_case 转为 camelCase
        - None: 不转换 (默认)
    :param ensure_ascii: 是否确保 ASCII，设为 False 以支持 UTF-8
    :param kwargs: 传递给 json.dumps 的其他参数
    :return: JSON 字符串
    """
    if convert_keys not in (None, 'to_python', 'to_ts'):
        raise ValueError("convert_keys must be one of: None, 'to_python', 'to_ts'")
    
    def convert_item(item):
        if isinstance(item, dict):
            return {
                convert_key(k): convert_item(v)
                for k, v in item.items()
            }
        elif isinstance(item, (list, tuple)):
            return [convert_item(i) for i in item]
        return item
    
    def convert_key(key):
        if not isinstance(key, str):
            return key
        if convert_keys == 'to_python':
            return convert_ts_to_python(key)
        elif convert_keys == 'to_ts':
            return convert_python_to_ts(key)
        return key
    
    converted_obj = convert_item(obj)
    return json.dumps(converted_obj, ensure_ascii=ensure_ascii, **kwargs)

def loads(s, convert_keys=None, **kwargs):
    """
    将 JSON 字符串反序列化为 Python 对象
    
    :param s: JSON 字符串
    :param convert_keys: 键名转换方式，可选:
        - 'to_python': 将 camelCase 转为 snake_case
        - 'to_ts': 将 snake_case 转为 camelCase
        - None: 不转换 (默认)
    :param kwargs: 传递给 json.loads 的其他参数
    :return: Python 对象
    """
    if convert_keys not in (None, 'to_python', 'to_ts'):
        raise ValueError("convert_keys must be one of: None, 'to_python', 'to_ts'")
    
    obj = json.loads(s, **kwargs)
    
    def convert_item(item):
        if isinstance(item, dict):
            return {
                convert_key(k): convert_item(v)
                for k, v in item.items()
            }
        elif isinstance(item, (list, tuple)):
            return [convert_item(i) for i in item]
        return item
    
    def convert_key(key):
        if not isinstance(key, str):
            return key
        if convert_keys == 'to_python':
            return convert_ts_to_python(key)
        elif convert_keys == 'to_ts':
            return convert_python_to_ts(key)
        return key
    
    return convert_item(obj)

