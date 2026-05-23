import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory

load_dotenv()



config = {
    "version": "v1.1",

    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": os.getenv("GEMINI_API_KEY"),
            "model": "gemini-embedding-001",
            "output_dimensionality": 1536        
        }
    },

    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": os.getenv("GEMINI_API_KEY"),
            "model": "gemini-3.1-flash-lite"
            # or gemini-1.5-pro
        }
    },

    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

# MEMORY CLIENT

memory_client = Memory.from_config(config)

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# USER CONFIG

USER_ID = "aditya"


# CHAT LOOP
i = 0
while i<2:
    i += 1
    user_query = input("\nWhat do you want to ask?\n> ")


    # SEARCH RELEVANT MEMORIES
    search_results = memory_client.search(
    query=user_query,
    filters={"user_id": USER_ID}
)


    memories = []
    for memory in search_results["results"]:
        memories.append({
            "id": memory.get("id"),
            "memory": memory.get("memory")
        })

    print("\nFound Memories:\n")
    print(
        json.dumps(
            memories,
            indent=2
        )
    )


    # SYSTEM PROMPT
    system_prompt = f"""
    You are a helpful AI assistant.
    Here are relevant memories
    about the user:

    {json.dumps(memories, indent=2)}
    """

    # LLM RESPONSE
    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    ai_response = response \
        .choices[0] \
        .message.content


    print("\nAI Says:\n")
    print(ai_response)


    # SAVE MEMORY
    memory_client.add(
        messages=[
            {
                "role": "user",
                "content": user_query
            },
            {
                "role": "assistant",
                "content": ai_response
            }
        ],
        user_id=USER_ID
    )

    print("\nMemory Saved.\n")