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








