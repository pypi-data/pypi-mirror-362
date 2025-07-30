from solocompany import utils


socket = utils.socket


class WebCls:
    def get_simplified_webpage(self, url: str) -> str:
        return socket.post_and_recv_result(
            "getSimplifiedWebpage", {"url": url}
        )