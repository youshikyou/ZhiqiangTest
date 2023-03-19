import os

import openai

from format import format_output, load_incoming_package
from chat import ChatHistory

async def handle_question(websocket, path, config):

    recieved_package = await websocket.recv()
    incoming_package = load_incoming_package(recieved_package)

    chat_history_path = os.path.join(config["CHAT_HISTORY_DIR"], f"{incoming_package['sessionKey']}.bin")
    chat_history = ChatHistory.from_file(chat_history_path)
    message = incoming_package['content']
    try:
        message_decoded = message.decode('utf-8')
    except:
        message_decoded = message
    
    this_session = [{"role": "user", "content": message_decoded}]

    response = await connect_to_openai(websocket, config, incoming_package, chat_history + this_session)

    this_session.append({"role": "assistant", "content": response})
    new_chat_history = await ChatHistory.limit_chat_history(chat_history + this_session)
    ChatHistory.to_file(chat_history_path, new_chat_history)


async def connect_to_openai(websocket, config, incoming_package, chat_content):

    openai.api_key = config["API_KEY_1"]
    response = await openai.ChatCompletion.acreate(model=config["model"], messages=chat_content, stream=True)
    full_response = []
    async for message in response:
        try:
            delta_response = message.choices[0].delta.content
            await websocket.send(format_output(incoming_package, delta_response))
            full_response.append(delta_response)
        except AttributeError:
            pass
    await websocket.send(format_output(incoming_package, flag="1"))

    return " ".join(full_response)
