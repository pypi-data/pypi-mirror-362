
from .prompt import generate_user_task_prompt, get_system_prompt
from .message import info, output, CHAT_DATA
from openai.types.responses import ResponseTextDeltaEvent
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    ModelSettings,
)
from solocompany import utils
from collections import defaultdict



cfg = utils.read_json_file("llm.json")
BASE_URL = cfg["baseURL"]
API_KEY = cfg["apiKey"]
MODEL_NAME = cfg["model"]


client = AsyncOpenAI(base_url=BASE_URL,api_key=API_KEY)
set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)





async def handle_user_inputs(
    conversation_history, user_input, cwd, abilities, mcp_servers, member_setting, member_setting_file:str
):
    # 将用户消息添加到对话历史
    conversation_history.append(
        {
            "role": "user",
            "content": generate_user_task_prompt(
                conversation_history, cwd, user_input, member_setting_file
            ),
        }
    )

    server = None
    try:
        agent = Agent(
            name="Assistant",
            instructions=get_system_prompt(cwd, member_setting),
            tools=[function_tool(ability) for ability in abilities],
            mcp_servers=mcp_servers,
            model=MODEL_NAME,
            model_settings=ModelSettings(temperature=member_setting["temperature"]),
        )
        input_history = [{"role":"user","content": user_input}]
        result = Runner.run_streamed(agent, input=input_history)
        
        tool_name_dict = defaultdict(lambda : str)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                info("assistant", event.data.delta)
            elif event.type == "run_item_stream_event":
                raw_item = event.item.raw_item
                if event.item.type == "tool_call_item":
                    tool_name_dict[raw_item.call_id] = raw_item.name
                elif event.item.type == "tool_call_output_item":
                    tool_name = tool_name_dict[raw_item["call_id"]]
                    info("assistant", f"""\n\n<details class='tool-call'><summary>{tool_name}</summary>
                        <div class='tool-output'>{event.item.output}</div></details>\n\n""")
                        
                
        output("assistant", CHAT_DATA["info"])
        conversation_history.append({"role": "assistant", "content": CHAT_DATA["info"]})
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if server is not None:
            await server.__aexit__(None, None, None)
