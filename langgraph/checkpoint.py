import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import (StateGraph,START,END)

from langgraph.graph.message import (add_messages)
from langchain.chat_models import (init_chat_model)
from langgraph.checkpoint.mongodb import (MongoDBSaver)

load_dotenv()

# =========================
# STATE
# =========================

class State(TypedDict):
    messages: Annotated[
        list,
        add_messages
    ]


# =========================
# LLM
# =========================

llm = init_chat_model(
    model="gemini-3.1-flash-lite",
    model_provider="google_genai",
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================
# NODE
# =========================

def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}    


# =========================
# GRAPH BUILDER
# =========================

graph_builder = StateGraph(State)


# =========================
# REGISTER NODE
# =========================

graph_builder.add_node("chatbot",chatbot)


# =========================
# EDGES
# =========================

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)


# =========================
# COMPILE GRAPH
# =========================

def compile_graph_with_checkpointer(checkpointer):

    return graph_builder.compile(checkpointer=checkpointer)    


# =========================
# MONGODB CHECKPOINTER
# =========================
DB_URI = "mongodb://admin:admin@localhost:27017"

with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph = compile_graph_with_checkpointer(checkpointer)

    config = {
        "configurable": {
            "thread_id": "aditya"
        }
    }

    updated_state = graph.invoke(
        State({
            "messages": [
                "My name is Aditya."
            ]
        }),
        config
    )
    # =========================
    # STREAM EXECUTION
    # =========================

    for chunk in graph.stream(
        State({
            "messages": [
                "What is my name?"
            ]
        }),
        config,
        stream_mode="values"
    ):

        chunk["messages"][-1].pretty_print()