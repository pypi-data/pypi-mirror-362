import os
import sys
import importlib
import functools
import traceback
from .call_func import call_func
from solocompany import utils

    
class ChangeDirectoryAndPath:
    def __init__(self, working_directory, insert_sys_path=True, chdir=True):
        self.working_directory = working_directory
        self.old_path = None
        self.insert_sys_path = insert_sys_path
        self.chdir = chdir

    def __enter__(self):
        self.old_path = os.getcwd()
        if self.insert_sys_path:
            sys.path.insert(0, self.working_directory)
        if self.chdir:
            os.chdir(self.working_directory)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.working_directory in sys.path and self.insert_sys_path:
            sys.path.remove(self.working_directory)
        if self.chdir:
            os.chdir(self.old_path)
        

class ModuleManager:
    """Context manager for handling module imports and sys.modules state."""

    def __init__(self, module_path):
        self.module_path = module_path
        self.original_modules = sys.modules.copy()

    def __enter__(self):
        """Enter the runtime context related to this object."""
        self.change_dir = ChangeDirectoryAndPath(self.module_path, 
                                                 insert_sys_path=True, 
                                                 chdir=False)
        self.change_dir.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object."""
        self.change_dir.__exit__(exc_type, exc_value, traceback)
        self.cleanup_modules()

    def cleanup_modules(self):
        """Restore the original sys.modules state."""
        importlib.invalidate_caches()
        for key in list(sys.modules.keys()):
            if key not in self.original_modules:
                del sys.modules[key]
                

def wrapped_func(func, working_directory:str, ui_datas=None):
    def _wrapped(*args, **kwargs):
        old_ui_datas = utils.params["uiDataMap"]
        if ui_datas is not None:
            params = utils.params
            params["uiDataMap"] = ui_datas
        with ChangeDirectoryAndPath(working_directory, 
                                    insert_sys_path=False,
                                    chdir=True):
            try:
                result = call_func(func, args, kwargs)
            except Exception as e:
                print(f"Call function {func.__name__} error: {str(e)}")
                traceback.print_exc()
                raise
        if ui_datas is not None:
            params["uiDataMap"] = old_ui_datas
        return result
    
    wrapped_function = functools.wraps(func)(_wrapped)
    return wrapped_function

