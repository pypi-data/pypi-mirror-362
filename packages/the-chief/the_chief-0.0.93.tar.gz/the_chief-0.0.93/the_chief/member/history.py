import datetime
import os


def output_chat_history(member_setting_file, chat_history):
    try:
        current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_history_folder = os.path.join(os.path.dirname(member_setting_file), "chatHistory")
        os.makedirs(chat_history_folder, exist_ok=True)
        chat_history_file = os.path.join(chat_history_folder, current_time_str + "_no_subject.txt")
        with open(chat_history_file, 'w', encoding='utf-8') as f:
            for chat in chat_history:
                f.write(chat["role"] + ":\n" + chat["content"] + "\n\n")
    except Exception as e:
            print(f"Error writing chat history to file: {e}")
        