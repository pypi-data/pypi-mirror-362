import sys
import subprocess
import os
from solocompany import utils


socket = utils.socket


class WindowCls:

    def message(self, message: str, type: str = "info"):
        assert type in [
            "info",
            "warning",
            "success",
            "error",
        ], "type must be info, warning, success or error"
        if not isinstance(message, str):
            message = repr(message)
        socket.post("append-msg", {"message": message, "type": type})

    def confirm(self, title: str, message: str) -> bool:
        return socket.post_and_recv_result(
            "confirm", {"title": title, "message": message}
        )

    def input(self, title: str, message: str) -> str:
        return socket.post_and_recv_result(
            "input", {"title": title, "message": message}
        )

    def minimize(self):
        socket.post("minimize", {})

    def maximize(self):
        socket.post("maximize", {})

    def hide_window(self):
        socket.post("hideWindow", {})

    def get_slected_text(self) -> str:
        result = socket.post_and_recv_result("get-selected-text", {})
        return result

    def open_file_with_system(self, file_path, wait: bool):
        process_fn = subprocess.run if wait else subprocess.Popen
        if sys.platform.startswith("linux"):
            process_fn(["xdg-open", file_path])
        elif sys.platform.startswith("darwin"):
            process_fn(["open", file_path])
        elif sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):
            os.startfile(file_path)
        else:
            raise OSError("Unsupported operating system")

    def open_program(self, program_path, wait: bool):
        process_fn = subprocess.run if wait else subprocess.Popen
        process_fn([program_path])

    def execute_javaScript(self, js_code: str):
        result = socket.post_and_recv_result("executeJavaScript", {"code": js_code})
        if not result["ok"]:
            raise Exception(result["value"])
        return result["value"] if "value" in result else None
