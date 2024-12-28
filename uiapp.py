import streamlit as st
import os
from  langchain_core.messages import HumanMessage, AIMessage
from src.agent import answer_the_question

os.environ["OPENAI_API_KEY"] = st.secrets["api_keys"]["OPENAI_API_KEY"]

if 'chat_history' not in st.session_state:
  st.session_state.chat_history = []

st.set_page_config(page_title='AI Second Brain', page_icon=":robot_face:")
st.title("🤖 Your AI Second Brain", False)
st.subheader("For some, it's even the first:)", False)

# #render message
# def render_messages():
#   for message in st.session_state.chat_history:
#     if isinstance(message, HumanMessage):
#       with st.chat_message('human'):
#         st.markdown(message.content)
#     else:
#       with st.chat_message('assistant'):
#         st.markdown(message.content)
# render_messages()

user_query = st.chat_input("Lost something again, honney?)")
if user_query is not None and user_query != "":
  st.session_state.chat_history.append(HumanMessage(user_query))

  with st.chat_message('human'):
    st.markdown(user_query)

  with st.spinner("Опять работа?"): 
    ai_response = answer_the_question(user_query)
    with st.chat_message('ai'):
      st.markdown(ai_response)
    st.session_state.chat_history.append(AIMessage(ai_response))

