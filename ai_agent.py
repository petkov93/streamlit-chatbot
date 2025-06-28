import os
import time
import json
import requests
from requests import Response

from const import xAI_URL, COMPLETIONS_ENDPOINT, SYSTEM_MSG, MODELS_ENDPOINT, EXIT_OPTIONS, USER_INPUT_STR, GROQ_URL, \
    OPENAI_URL

# xai_url = BASE_XAI_URL + XAI_ENDPOINT
xai_url = "https://api.x.ai/v1/chat/completions"
xai_models_url = xAI_URL + MODELS_ENDPOINT
groq_models_url = GROQ_URL + MODELS_ENDPOINT


def check_api_provider():
    available_urls = [xAI_URL, OPENAI_URL, GROQ_URL]
    ...


def get_models(url: str, key: str) -> (bool, list):
    """
    Tries to get the available models from the given URL using the provided API key.

    If the request returns status code 200, the API key is considered valid,
    and the list of models is returned. Otherwise, returns False and an empty list.

    :param url: str - The API URL.
    :param key: str - The API key to check.
    :return: tuple:
        - is_valid (bool): Whether the API key is valid.
        - models (list): List of available models (empty if invalid).
    """
    models = []
    is_valid = False
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for model in data['data']:
            models.append(model)
    return is_valid, models


def add_question_to_history(chat_history, question) -> None:
    chat_history.append(
        {"role": "user",
         "content": question
         })


def add_answer_to_history(history, _answer) -> None:
    history.append(
        {"role": "assistant",
         "content": _answer
         })


def get_last_question(history: list, sys_msg: list) -> list:
    return [sys_msg, history[-1]]


def get_bobs_response(history: list, api_key: str) -> Response:
    last_question = get_last_question(history, SYSTEM_MSG)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "grok-3-mini",
        # sends the whole history OR the last_question + system prompt. (for smaller token usage)
        "messages": history,
        #  same here, limit the response to 500 tokens.
        # "max_completion_tokens": 850,
        #  smaller temp [0.0] -> more deterministic,
        #  bigger temp [0.7-1.0+] -> more creativity, also can make more errors
        "temperature": 0.7,
        # stream=True causes too much trouble  for now :D
        "stream": False
    }
    response = requests.post(url=xai_url, headers=headers, json=payload)
    response.raise_for_status()
    # response as text
    data = response.json()
    message = data['choices'][0]['message']['content']
    # return response
    return message

def stream_response(resp: Response):
    for line in resp.iter_lines():
        if line:
            try:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    data_str = decoded_line[len("data: "):]
                    if data_str == "[DONE]":
                        break
                    data_ = json.loads(data_str)
                    # Extract the delta content from data
                    delta = data_['choices'][0]['delta']
                    if 'content' in delta:
                        yield delta['content']
            except Exception as e:
                yield f'[Error in stream {e}]'

# old version in terminal
# def main():
#     while (user_input := input(USER_INPUT_STR)) not in EXIT_OPTIONS:
#         add_question_to_history(conversation, user_input)
#         answer = get_bobs_response(conversation)
#         add_answer_to_history(conversation, answer)
#         print(f'BOB answered:')
#         for chunk in stream_response(answer):
#             print(chunk, end='', flush=True)
#         else:
#             print()

#
# if __name__ == '__main__':
#     get_models(groq_models_url, g)