from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START,END
from state import ChatbotState


load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", streaming=True)

def chatbot_response(state: ChatbotState):
    chats = state['messages']
    response = model.invoke(chats)
    return {"messages": [response]}

graph = StateGraph(ChatbotState)

graph.add_node('chatbot', chatbot_response)

graph.add_edge(START,'chatbot')
graph.add_edge('chatbot',END)

chatbot_checkpoint = InMemorySaver()
chatbotworkflow = graph.compile(checkpointer=chatbot_checkpoint)

def list_threads():
    """Thread ids, most recently active first."""

    # list(None) groups checkpoints by thread, so order by each thread's latest timestamp
    latest = {}
    for checkpoint in chatbot_checkpoint.list(None):
        threadid = checkpoint.config["configurable"]["thread_id"]
        ts = checkpoint.checkpoint["ts"]
        if ts > latest.get(threadid, ""):
            latest[threadid] = ts
    return sorted(latest, key=latest.get, reverse=True)

def thread_title(thread_id):
    """First user message, shortened, used as the label."""
    state = chatbotworkflow.get_state({"configurable":{"thread_id":thread_id}})
    msgs =  state.values.get("messages",[]) if state.values else []
    for msg in msgs:
        if msg.type == "human":
            return msg.content[:50]  # Return the first 50 characters of the message

    return "New Chat"  # Fallback if no human message is found





