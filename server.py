import streamlit as st

from ai_agent import add_question_to_history, add_answer_to_history, get_bobs_response
from const import USER_INPUT_STR, SYSTEM_MSG


def set_session_state():
    if 'conversation' not in st.session_state:
        st.session_state.conversation = [SYSTEM_MSG]


def place_sidebar():
    with st.sidebar:
        with st.form('api_form', border=True, clear_on_submit=True, enter_to_submit=True):
            api_key = st.text_input('Enter Your API key here', type='password')
            submitted = st.form_submit_button('Submit')
            if submitted:
                st.write('API key submitted successfully!')
                st.write(f'{api_key=}')


def place_header():
    with st.container(border=True):
        st.title('⭐ BOB ⭐')
        st.header(body='the Brutally Obvious Bot.', divider=True)
        st.subheader("Welcome to Bob's world, how can I [not] be of service?")



def get_latest_messages(max_messages=10):
    latest = st.session_state.conversation[-max_messages:]
    return [(msg['role'], msg['content']) for msg in latest if msg['role'] != 'system']


def place_chat_window():
    latest_messages = get_latest_messages()
    with st.container(border=True):
        for role, msg in latest_messages:
            with st.chat_message(name=role):
                st.markdown(msg)

def run_web_app():
    set_session_state()
    place_header()
    place_sidebar()
    prompt = st.chat_input(USER_INPUT_STR)
    if prompt:
        add_question_to_history(st.session_state.conversation, prompt)
        answer = get_bobs_response(st.session_state.conversation)
        add_answer_to_history(st.session_state.conversation, answer)
        place_chat_window()

if __name__ == '__main__':
    run_web_app()

