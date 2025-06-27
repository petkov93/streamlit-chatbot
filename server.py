import streamlit as st

from ai_agent import conversation, add_question_to_history, add_answer_to_history, get_bobs_response
from const import USER_INPUT_STR

with st.sidebar:
    with st.form('api_form', border=True, clear_on_submit=True, enter_to_submit=True):
        api_key = st.text_input('Enter Your API key here', type='password')
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.write('API key submitted successfully!')
            st.write(f'{api_key=}')

with st.container(border=True):
    st.title('⭐ BOB ⭐')
    st.header(body='the Brutally Obvious Bot.', divider=True)
    st.subheader("Welcome to Bob's world, how can I [not] be of service?")

prompt = st.chat_input(USER_INPUT_STR)
if prompt:
    add_question_to_history(conversation, prompt)
    answer = get_bobs_response(conversation)
    add_answer_to_history(conversation, answer)
    with st.container(border=True):
        for msg in conversation:
            role = msg['role']
            if msg['role'] != 'system':
                message = msg['content']
                with st.chat_message(name=role):
                    st.markdown(message)

    # with st.spinner('BOB is thinking...'):
    #
    #     with st.chat_message(name='ai'):

