import streamlit as st

from ai_agent import conversation, add_question_to_history, add_answer_to_history, get_bobs_response, stream_response
from const import USER_INPUT_STR

with st.sidebar:
    st.header('Chat history')
    st.divider()

with st.container(border=True):
    st.title('⭐ BOB ⭐', anchor=False)
    st.header(body='\nThe Brutally Obvious Bot.', divider=True)
    st.subheader("Welcome to Bob's world, how can I [not] be of service?")

prompt = st.chat_input(USER_INPUT_STR)
if prompt:
    add_question_to_history(conversation, prompt)
    with st.container(border=True):
        st.write(f"You asked:")
        with st.container(border=True):
            st.write(prompt)

    with st.container(border=True):
        with st.spinner('BOB is thinking...'):
            answer = get_bobs_response(conversation)
            st.write("BOB's answer: ")
            with st.container(border=True):
                last_answer = st.write_stream(stream_response(answer))
                add_answer_to_history(conversation, last_answer)
