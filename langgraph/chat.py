from dotenv import load_dotenv

from typing_extensions import TypedDict
import os
from typing import Annotated

from langgraph.graph import (StateGraph, START, END)
from langgraph.graph.message import (add_messages)
from langchain.chat_models import (init_chat_model)


# Load environment variables
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
    api_key = os.getenv("GEMINI_API_KEY")
)


# =========================
# NODES
# =========================

def chatbot(state: State):

    print(
        "\n\nInside chatbot node\n"
    )

    print(state)

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


def sample_node(state: State):

    print("\n\nInside sample node\n")

    print(state)

    return {
        "messages": [
            "Sample message appended"
        ]
    }


# =========================
# GRAPH BUILDER
# =========================

graph_builder = StateGraph(State)


# =========================
# REGISTER NODES
# =========================

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample_node", sample_node)


# =========================
# EDGES
# =========================

graph_builder.add_edge(START, "chatbot")

graph_builder.add_edge("chatbot", "sample_node")

graph_builder.add_edge("sample_node", END)


# =========================
# COMPILE GRAPH
# =========================

graph = graph_builder.compile()


# =========================
# INVOKE GRAPH
# =========================

updated_state = graph.invoke({
    "messages": [
        "Hi, my name is Aditya Yadav. Can you please introduce yourself?"
    ]
})


print("\n\nUpdated State\n")

print(updated_state)