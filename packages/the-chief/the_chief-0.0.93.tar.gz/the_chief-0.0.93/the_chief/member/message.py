import json


INPUT_MESSAGE = "INPUT_MESSAGE=>"
INTERRUPT_MESSAGE = "INTERRUPT_MESSAGE=>"
_OUTPUT_MESSAGE = "OUTPUT_MESSAGE=>"
_INFOMATION_MESSAGE = "INFOMATION_MESSAGE=>"
_LOG = "LOG=>"


CHAT_DATA = {"output": "", "info": ""}


def log(content, *args, end="\n", **kwargs):
    print(_LOG + content, *args, end=end, **kwargs)


def clear_chat_data():
    CHAT_DATA["output"] = ""
    CHAT_DATA["info"] = ""


def output(role, content):
    assert role == "assistant"
    CHAT_DATA["output"] = content
    print(
        _OUTPUT_MESSAGE
        + json.dumps({"role": role, "content": content}, ensure_ascii=False),
        flush=True
    )


def info(role, content):
    CHAT_DATA["info"] += content
    print(
        _INFOMATION_MESSAGE
        + json.dumps({"role": role, "content": content}, ensure_ascii=False),
        flush=True
    )
