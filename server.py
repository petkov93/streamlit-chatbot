import streamlit as st

from ai_agent import add_question_to_history, add_answer_to_history, get_bobs_response, validate_xai_key
from const import SYS_MESSAGES


def configure_page():
    st.set_page_config(
        page_title="Bob~Your personal AI assistant",
        layout="centered",
        initial_sidebar_state="expanded",
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
    if 'ai_mode' not in st.session_state:
        st.session_state['ai_mode'] = list(SYS_MESSAGES.keys())[0]

    if 'conversation' not in st.session_state:
        st.session_state.conversation = [SYS_MESSAGES[st.session_state['ai_mode']]]

    if 'XAI_API_KEY' not in st.session_state:
        try:
            st.session_state['XAI_API_KEY'] = st.secrets['api']['groq_key']
        except KeyError:
            st.session_state['XAI_API_KEY'] = ""


def set_ai_mode():
    st.session_state['conversation'] = [SYS_MESSAGES[st.session_state['ai_mode']]]


def place_sidebar():
    with st.sidebar:
        if not st.session_state['XAI_API_KEY']:
            st.error('xAI API key not provided, enter it in the sidebar to continue!')
            with st.form('api_form', border=False, clear_on_submit=True, enter_to_submit=True):
                api_key = st.text_input('Enter Your API key here', type='password')
                submitted = st.form_submit_button('Submit')
                if submitted and validate_xai_key(api_key):
                    st.session_state['XAI_API_KEY'] = api_key
                    st.success('xAI API key set successfully!')
                    st.rerun(scope="app")
        else:
            st.success('xAI API key set successfully!')
        st.radio(label="Pick AI mode:", options=list(SYS_MESSAGES.keys()), key='ai_mode', on_change=set_ai_mode)

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
        prompt = st.chat_input('Ask me anything..', disabled=False)
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

