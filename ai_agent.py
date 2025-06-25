import os
import time

import requests
from dotenv import load_dotenv
from requests import Response

from const import BASE_XAI_URL, XAI_ENDPOINT, SYSTEM_MSG, XAI_MODELS_ENDPOINT, EXIT_OPTIONS, USER_INPUT_STR

load_dotenv()

api_key = os.getenv('XAI_API_KEY')
# xai_url = BASE_XAI_URL + XAI_ENDPOINT
xai_url = "https://api.x.ai/v1/chat/completions"
models_url = BASE_XAI_URL + XAI_MODELS_ENDPOINT

conversation = [SYSTEM_MSG]


def get_models(url: str, key: str) -> None:
    """ Function to print all available models from xAI. """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"}
    all_models = requests.get(models_url, headers=headers)
    data = all_models.json()

    for model in data['data']:
        print(model['id'])


def add_question_to_history(chat_history, question) -> None:
    chat_history.append(
        {"role": "user",
         "content": question
         })


def add_answer_to_history(history, _answer) -> None:
    history.append(
        {"role": "system",
         "content": _answer
         })


def get_last_question(history: list, sys_msg: list) -> list:
    return [sys_msg, history[-1]]


def get_bobs_response(history: list) -> Response:
    last_question = get_last_question(history, SYSTEM_MSG)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "grok-3-mini",
        # sends the whole history OR the last_question + system prompt. (for smaller token usage)
        "messages": history,
        #  same here, limit the response to 500 tokens.
        "max_completion_tokens": 500,
        #  smaller temp [0.0] -> more deterministic,
        #  bigger temp [0.7-1.0+] -> more creativity, also can make more errors
        "temperature": 0.7,
        "stream": True}

    response = requests.post(url=xai_url, headers=headers, json=payload)
    response.raise_for_status()

    # response as text
    # data = response.json()
    # message_as_txt = data['choices'][0]['message']['content']

    return response


def stream_response(resp):
    for line in resp.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith("data: "):
                data_str = decoded_line[len("data: "):]
                if data_str == "[DONE]":
                    break
                # Typically, the data is JSON with the partial content
                import json
                data_ = json.loads(data_str)
                # Extract the delta content from data
                delta = data_['choices'][0]['delta'].get('content', '')
                if delta:
                    time.sleep(0.03)
                    yield delta

# old version in terminal

while (user_input := input(USER_INPUT_STR)) not in EXIT_OPTIONS:
    add_question_to_history(conversation, user_input)
    answer = get_bobs_response(conversation)
    add_answer_to_history(conversation, answer)
    print(f'BOB answered:')
    for chunk in stream_response(answer):
        print(chunk, end='', flush=True)
    else:
        print()

# get_models(models_url, api_key)
