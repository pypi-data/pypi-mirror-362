from .chat_base import handle_user_inputs
from .history import output_chat_history
from .interrupt import run_with_interrupt_check
from .lib import get_abilities
from .message import  clear_chat_data, CHAT_DATA, INPUT_MESSAGE
import json
import tempfile
import asyncio
from solocompany import utils

            
async def chat(member_setting_file: str):
    conversation_history = []
    with open(member_setting_file, encoding="utf-8") as f:
        member_setting = json.load(f)
    cwd = member_setting["specifiedWorkingDirectory"]
    if cwd is None:
        cwd = tempfile.mkdtemp()
    abilities, mcp_servers = await get_abilities(cwd, member_setting)
    while True:
        with open(member_setting_file, encoding="utf-8") as f:
            member_setting = json.load(f)
        clear_chat_data()
        input_text = input()
        if not input_text.startswith(INPUT_MESSAGE):
            raise ValueError("Invalid message")
        message = json.loads(input_text[len(INPUT_MESSAGE) :])
        user_input = message["content"]
        params = utils.params
        
        assert "interruptFile" in params
        asyncio.run(
            run_with_interrupt_check(
                conversation_history,
                user_input,
                cwd,
                abilities,
                mcp_servers,
                member_setting,
                member_setting_file,
                params["interruptFile"],
            )
        )
        output_chat_history(member_setting_file, conversation_history)


async def get_chat_response(member_setting_file: str, user_input: str):
    with open(member_setting_file, encoding="utf-8") as f:
        member_setting = json.load(f)
    cwd = tempfile.mkdtemp()
    abilities, mcp_servers = await get_abilities(cwd, member_setting)
    conversation_history = []
    asyncio.run(
        handle_user_inputs(
            conversation_history, user_input, cwd, abilities, mcp_servers, member_setting, member_setting_file
        )
    )
    return CHAT_DATA["info"]
