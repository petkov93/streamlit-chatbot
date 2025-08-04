import streamlit as st

from ai_agent import add_question_to_history, add_answer_to_history, get_bobs_response, validate_xai_key
from const import USER_INPUT_STR, SYSTEM_MSG


def configure_page():
    st.set_page_config(
        page_title="Bob~Your personal AI assistant",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={
            "Get help": "https://github.com/petkov93/streamlit-chatbot",
            "Report a bug": "https://github.com/petkov93/streamlit-chatbot",
            "About": """
                ## Bob the AI assistant
                ### Powered using Groq, xAI and OpenAI
    
                **My GitHub**: https://github.com/petkov93/
    
                Simple but powerful chatbot made as a side project 
                while studying Python Fundamentals in SoftUni.
            """
        }
    )
def set_session_state():
    if 'conversation' not in st.session_state:
        st.session_state.conversation = [SYSTEM_MSG]
    if 'XAI_API_KEY' not in st.session_state:
        st.session_state['XAI_API_KEY'] = ''


def place_sidebar():
    if not st.session_state['XAI_API_KEY']:
        st.error('xAI API key not provided, enter it in the sidebar to continue!')
        with st.sidebar:
            with st.form('api_form', border=False, clear_on_submit=True, enter_to_submit=True):
                api_key = st.text_input('Enter Your API key here', type='password')
                submitted = st.form_submit_button('Submit')
                if submitted:
                    if validate_xai_key(api_key):
                        st.session_state['XAI_API_KEY'] = api_key
                        st.write(st.session_state['XAI_API_KEY'])
                        st.success('xAI API key set successfully!')
                        st.rerun(scope="app")
    else:
        with st.sidebar:
            st.success('xAI API key set successfully!')

def place_header():
    with st.container(border=True):
        st.title('⭐ BOB ⭐')
        st.header(body='the Brutally Obvious Bot.', divider=True)
        st.subheader("How Bob can be of service?")



def get_latest_messages(max_messages=10):
    latest = st.session_state.conversation[-max_messages:]
    return [(msg['role'], msg['content']) for msg in latest if msg['role'] != 'system']


def place_chat_window():
    latest_messages = get_latest_messages()
    with st.container(border=True):
        for role, msg in latest_messages:
            with st.chat_message(name=role):
                st.markdown(msg)


def get_input():
    if validate_xai_key(st.session_state['XAI_API_KEY']):
        prompt = st.chat_input(USER_INPUT_STR, disabled=False)
    else:
        prompt = st.chat_input('Enter xAI API key in the sidebar to continue!', disabled=True)
    return prompt


def run_web_app():
    configure_page()
    set_session_state()
    place_header()
    place_sidebar()
    question = get_input()
    if question:
        add_question_to_history(st.session_state.conversation, question)
        answer = get_bobs_response(st.session_state.conversation, st.session_state['XAI_API_KEY'])
        add_answer_to_history(st.session_state.conversation, answer)
        place_chat_window()

if __name__ == '__main__':
    run_web_app()

