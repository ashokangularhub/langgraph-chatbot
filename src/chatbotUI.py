import uuid
from langchain_core.messages import HumanMessage
import streamlit as st

from chatbotbackend import chatbotworkflow

st.set_page_config(page_title="LangGraph Chatbot", page_icon="🎃")
st.title("🎃 LangGraph Chatbot (short-term memory)")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

with st.sidebar:
    st.markdown(" ###Start new conversation")
    st.code(st.session_state.thread_id, language=None)
    if st.button("🚴‍♂️ new conversation"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

config = {"configurable": {"thread_id": st.session_state.thread_id}}

state = chatbotworkflow.get_state(config)
history = state.values.get("messages", []) if state.values else []

for message in history:
    role = "user" if message.type == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# --- Handle new user input --------------------------------------------------
user_input = st.chat_input("Type your message...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    ### Code to stream the assistant's response
    with st.chat_message("assistant"):
        def stream_response():
            for chunk, metadata in chatbotworkflow.stream(
                {"messages":[HumanMessage(content=user_input)]},
                config, stream_mode="messages"
            ):
                if chunk.content:
                    yield chunk.content

        ai_reply = st.write_stream(stream_response)

        ## code for non stream response
        # with st.spinner("Thinking..."):
        #     result = chatbotworkflow.invoke(
        #         {"messages": [{"role": "user", "content": user_input}]},
        #         config,
        #     )
        # ai_reply = result["messages"][-1].content
        # st.markdown(ai_reply)
