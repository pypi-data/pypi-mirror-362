import socket
import json
import uuid
from solocompany import utils


params = utils.params


class TcpSocket:
    def __init__(self):
        self.is_connected = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if params is not None:
            if "tcpPort" in params:
                self.socket.connect(("localhost", int(params["tcpPort"])))

    def post(self, subject, message):
        subject = "python-event:" + subject
        message = message.copy()
        message["subject"] = subject
        message = json.dumps(message)
        message_bytes = message.encode()
        message_length = len(message_bytes)
        message_length_bytes = message_length.to_bytes(4, byteorder='big')

        self.socket.sendall(message_length_bytes + message_bytes)

    def recv(self):
        # 接收消息长度
        message_length_bytes = self.socket.recv(4)
        message_length = int.from_bytes(message_length_bytes, byteorder='big')
        # 初始化接收到的消息
        message = b''
        # 循环接收直到收到完整的消息
        while len(message) < message_length:
            # 接收剩余的消息
            chunk = self.socket.recv(message_length - len(message))
            if not chunk:  # 如果没有接收到数据，则断开连接
                raise RuntimeError("Socket connection broken")
            message += chunk
        message = json.loads(message.decode())
        return message

    def post_and_recv_result(self, subject, message):
        message = message.copy()
        message["uid"] = str(uuid.uuid4())
        socket_subscribe(subject + ":" +  message["uid"]) # 先订阅,再发送,防止消息丢失
        self.post(subject, message)
        ret_val = self.recv()        
        result = ret_val["result"] if "result" in ret_val else None # 传输时，可能会丢失result字段，因此需要判断
        return result

    def close(self):
        if self.is_connected:
            self.is_connected = False

    def __del__(self):
        # 垃圾回收时自动关闭socket
        if self.is_connected:
            self.close()

    def __exit__(self, exc_type, exc_value, traceback):
        # with 语句块结束时自动触发的
        if self.is_connected:
            self.close()


socket = TcpSocket()

def socket_subscribe(subject: str):
    subject = "python-event:" + subject
    socket.post(subject, {"subscribe": subject})
    return socket