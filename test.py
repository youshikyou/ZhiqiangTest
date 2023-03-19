import asyncio
import websockets
import unicodedata
import threading, json, string, random


def random_sessionKey_generator(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str

SESSION_KEY = random_sessionKey_generator(10)

def format_input(content):

    data_format = {
        "role": "user",
        "userId": "345",
        "sessionKey": SESSION_KEY,
        "code": "whatever",
        "content": content
    }
    return json.dumps(data_format)

async def ask_question(websocket):
    session_content = []
    # Get question from user input
    question = input("Ask a question: ")
    session_content.append({'role': 'user', 'content': question})
    # normalized_question = unicodedata.normalize('NFKD', question)
    # encoded_question = normalized_question.encode('utf-8')
    await websocket.send(format_input(question))
    response = []
    while True:
        try:
            timeout = 300
            recv_text = await asyncio.wait_for(websocket.recv(), timeout=timeout)
            recv_package = json.loads(recv_text)

            if isinstance(recv_package, dict) and recv_package['flag'] == "0":
                print(recv_package['content'])
            else:
                break

            response.append(recv_package['content'])
                
        except asyncio.TimeoutError:
            # Dynamic adjustment of timeout value based on network conditions
            timeout += 10
            if timeout > 300:
                timeout = 300  # maximum timeout value = 5 minutes
            break
    
    session_content.append({'role': 'assistant', 'content': ''.join(response)})
    print(session_content)

async def connect_to_server(uri):
    while True:
        async with websockets.connect(uri, ping_interval=None) as websocket:
            asyncio.create_task(ask_question(websocket))
            await websocket.wait_closed()
            
#uri = "wss://8428-31-211-201-153.eu.ngrok.io"
#uri = "ws://4.tcp.eu.ngrok.io:19985"
uri = "ws://localhost:8765/"

asyncio.get_event_loop().run_until_complete(connect_to_server(uri))
