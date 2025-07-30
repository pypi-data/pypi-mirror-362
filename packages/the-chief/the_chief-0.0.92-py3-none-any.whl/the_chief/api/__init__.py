from .lib.window import WindowCls
from .lib.tab import TabCls
from .lib.web import WebCls

class Api:
    def __init__(self) -> None:
        self.window = WindowCls()
        self.tab = TabCls()
        self.web = WebCls()

api = Api()
window = api.window
tab = api.tab
web = api.web

# from ps_view import ViewCls, WebsiteViewCls, FileViewCls, DirectoryViewCls, WorkflowCls