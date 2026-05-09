import requests
import json


url = "http://localhost:11434/api/chat"


def stream_response(user_input=""):
    payload = {
    "model": "granite4.1:3b",
    "messages": [{
            "role": "user",
            "content": user_input
        }]
    }
    res = requests.post(url, json=payload, stream=True)

    print("response status code: ", res.status_code)
    if res.status_code == 200:
        response = ""
        print("Thinking...")
        for item in res.iter_lines(decode_unicode=True):
            if item:
                response += json.loads(item)['message']['content']
    
        print("Ai:", response)


while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    stream_response(user_input=user_input)
