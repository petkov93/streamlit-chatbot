import time

import streamlit as st

from ai_agent import add_question_to_history, add_answer_to_history, get_bobs_response, get_models
from const import USER_INPUT_STR, SYSTEM_MSG, GROQ_URL, DISABLED_CHAT_STR


def configure_page():
    st.set_page_config(
        page_title="Bob~Your personal AI assistant",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            "Get help": "https://github.com/petkov93/streamlit-chatbot",
            "Report a bug": "https://github.com/petkov93/streamlit-chatbot",
            "About": """
                ## Bob the AI assistant
                ### Powered using Groq, xAI or OpenAI API
    
                **My GitHub**: https://github.com/petkov93/
    
                Simple but powerful chatbot made as a side project 
                while studying Python Fundamentals in SoftUni.

                    Made by Petko Petkov.
            """
        }
    )


def set_session_state_vars():
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = [SYSTEM_MSG]
    if 'API_KEY' not in st.session_state:
        st.session_state['API_KEY'] = ''
    if 'is_valid_api_key' not in st.session_state:
        st.session_state['is_valid_api_key'] = False
    if 'available_models' not in st.session_state:
        st.session_state['available_models'] = []
    if 'SELECTED_API_PROVIDER' not in st.session_state:
        st.session_state['SELECTED_API_PROVIDER'] = 'xAI'

def place_api_picker():
    if not st.session_state['SELECTED_API_PROVIDER']:
        st.radio(
            "Pick API provider below",
            key="SELECTED_API_PROVIDER",
            options=["OpenAI", "Groq", "xAI"])

def place_api_form():
        with st.form('api_form', clear_on_submit=True, enter_to_submit=True):
            api_key = st.text_input('Enter Your API key here', type='password')
            submitted = st.form_submit_button('Submit')
            if submitted:
                st.session_state['is_valid_api_key'], st.session_state['available_models'] = get_models(GROQ_URL, api_key)
                if st.session_state['is_valid_api_key']:
                    st.session_state['API_KEY'] = api_key
                    st.rerun(scope="app")
                else:
                    st.error('Invalid API key! Try again.')

def place_sidebar():
    with st.sidebar:
        place_api_picker()
        if not st.session_state['API_KEY']:
            current_provider = st.session_state['SELECTED_API_PROVIDER']
            st.error(f'{current_provider} API key not provided, enter it in the sidebar to continue!')
            place_api_form()
        else:
            st.success('API key set successfully!\nYou may proceed with your questions.')


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
                if role == 'user':
                    st.write(msg)
                # if its AI response use markdown
                else:
                    st.markdown(msg)


def place_input():
    if st.session_state['is_valid_api_key']:
        prompt = st.chat_input(USER_INPUT_STR, disabled=False)
    else:
        prompt = st.chat_input(DISABLED_CHAT_STR, disabled=True)
    return prompt


def run_web_app():
    configure_page()
    set_session_state_vars()
    place_header()
    place_sidebar()
    question = place_input()
    if question:
        add_question_to_history(st.session_state.conversation, question)
        answer = get_bobs_response(st.session_state.conversation, st.session_state['API_KEY'])
        add_answer_to_history(st.session_state.conversation, answer)
        place_chat_window()


if __name__ == '__main__':
    run_web_app()
