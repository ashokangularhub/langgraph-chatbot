import uuid
from langchain_core.messages import HumanMessage
import streamlit as st

from chatbotbackend import chatbotworkflow, list_threads, thread_title

st.set_page_config(page_title="LangGraph Chatbot", page_icon="🎃")
st.title("🎃 LangGraph Chatbot")


def generate_thread_id():
    return str(uuid.uuid4())


# if "thread_id" not in st.session_state:
#     st.session_state.thread_id = str(uuid.uuid4())

############# side bar #################
# with st.sidebar:
#     st.markdown(" ###Start new conversation")
#     st.code(st.session_state.thread_id, language=None)
#     if st.button("🚴‍♂️ new conversation"):
#         st.session_state.thread_id = str(uuid.uuid4())
#         st.rerun()

st.sidebar.title("LangGraph Chatbot")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()

if st.sidebar.button("Start New Chat"):
    st.session_state.thread_id = generate_thread_id()
    st.rerun()

st.sidebar.header("My conversations")
threads = list_threads()
if st.session_state.thread_id not in threads:
    threads.insert(0, st.session_state.thread_id)

for threadId in threads:
    label = thread_title(threadId)
    if st.sidebar.button(label, key=threadId, use_container_width=True,
                         type="primary" if threadId == st.session_state.thread_id else "secondary"):
        st.session_state.thread_id = threadId
        st.rerun()

############# side bar ################

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
    # Code to stream the assistant's response
    with st.chat_message("assistant"):
        def stream_response():
            for chunk, metadata in chatbotworkflow.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config, stream_mode="messages"
            ):
                if chunk.content:
                    yield chunk.content

        ai_reply = st.write_stream(stream_response)

        # code for non stream response
        # with st.spinner("Thinking..."):
        #     result = chatbotworkflow.invoke(
        #         {"messages": [{"role": "user", "content": user_input}]},
        #         config,
        #     )
        # ai_reply = result["messages"][-1].content
        # st.markdown(ai_reply)