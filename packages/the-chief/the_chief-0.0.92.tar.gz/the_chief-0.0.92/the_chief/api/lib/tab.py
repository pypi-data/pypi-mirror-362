import os
from .view import ViewCls, WorkflowCls
import time
from solocompany import utils
import json
from typing import Union
from solocompany.address import Address, from_js_dict, to_js_dict

socket = utils.socket
params = utils.params


class TabCls:
    def open_workflow(self, address: Address|dict, wait_for_open=True) -> WorkflowCls:
        if isinstance(address, dict):
            address = from_js_dict(address)
        item_path = address.to_fs_path()
        info_path = os.path.join(item_path, "info.json")
        with open(info_path, "r", encoding="utf-8") as f:
            info = json.load(f)
        address  = Address("Workflow", item_path)
        socket.post("add-tab", {"address": to_js_dict(address), "name": info["name"]})
        if wait_for_open:
            self.wait_for_tab_open(address)
        return WorkflowCls(address)
    
    def open_tab(self, address:Address|dict, wait_for_open=True):
        if isinstance(address, dict):
            address = from_js_dict(address)
        item_path = address.to_fs_path()
        info_path = os.path.join(item_path, "info.json")
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                info = json.load(f)
            socket.post("add-tab", {"address": to_js_dict(address), "name": info["name"]})
        else:
            socket.post("add-tab", {"address": to_js_dict(address), "name": item_path})
        if wait_for_open:
            self.wait_for_tab_open(address)
        return ViewCls(address)

    def wait_for_tab_open(self, item: Union[Address, dict, ViewCls]):
        times = 0
        while not self.is_tab_open(item):
            time.sleep(0.01)
            times += 1
            if times > 1000:
                raise Exception("Tab open timeout")

    def get_active(self) -> Address:
        result = socket.post_and_recv_result("get-active-tab", {})
        return from_js_dict(result)

    def get_all(self) -> list[Address]:
        results = socket.post_and_recv_result("get-all-tabs", {})
        results = [from_js_dict(result) for result in results]
        return results

    def close_tab(self, item: Union[Address, dict, ViewCls]):
        if isinstance(item, dict):
            item = from_js_dict(item)
        elif isinstance(item, ViewCls):
            item = item.address
        self.wait_for_tab_open(item)
        socket.post("close-tab", {"address": to_js_dict(item)})

    def switch_tab(self, item: Union[Address, dict, ViewCls]):
        if isinstance(item, dict):
            item = from_js_dict(item)
        elif isinstance(item, ViewCls):
            item = item.address
        self.wait_for_tab_open(item)
        socket.post("switchTab", {"address": to_js_dict(item)})

    def is_tab_open(self, item: Union[Address, dict, ViewCls]):
        if isinstance(item, dict):
            item = from_js_dict(item)
        elif isinstance(item, ViewCls):
            item = item.address
        result = socket.post_and_recv_result("is-tab-open", {"address": to_js_dict(item)})
        return result

    def pin_tab(self, item: Union[Address, dict, ViewCls]):
        if isinstance(item, dict):
            item = from_js_dict(item)
        elif isinstance(item, ViewCls):
            item = item.address
        self.wait_for_tab_open(item)
        socket.post("pin-tab", {"address": to_js_dict(item)})

    def unpin_tab(self, item: Union[Address, dict, ViewCls]):
        if isinstance(item, dict):
            item = from_js_dict(item)
        elif isinstance(item, ViewCls):
            item = item.address
        self.wait_for_tab_open(item)
        socket.post("unpin-tab", {"address": to_js_dict(item)})
