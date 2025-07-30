import os
from .department import get_department_path
from pathlib import Path


class Address:
    def __init__(
        self, 
        page: str, 
        relative_path: str, 
        department_name:str=None, 
        uuid:str=None,
        ip:str=None
    ):
        if department_name == '':
            department_name = None
        if uuid == '':
            uuid = None
        if ip == '':
            ip = None   
        self.page = page
        self.relative_path = relative_path
        self.department_name = department_name
        self.uuid = uuid
        self.ip = ip

    
    def to_fs_path(self, is_user=True):
        if not is_user:
            raise Exception("Remote address is not supported")
        if self.department_name is None:
            return Path(self.relative_path).as_posix()

        department_path = get_department_path(self.department_name)
        if department_path is None :
            raise Exception("Department not found: " + self.department_name)
        
        fs_path = os.path.join(department_path, "User", self.page, self.relative_path)
        return Path(fs_path).as_posix()
    
    
    
def from_js_dict(js_dict: dict):
    return Address(
        page=js_dict["page"],
        relative_path=js_dict["relativePath"],
        department_name=js_dict.get("departmentName"),
        uuid=js_dict.get("uuid"),
        ip=js_dict.get("ip")
    )
    
def to_js_dict(address: Address):
    return {
        "page": address.page,
        "relativePath": address.relative_path,
        "departmentName": address.department_name,
        "uuid": address.uuid,
        "ip": address.ip
        }