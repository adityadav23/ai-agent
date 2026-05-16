from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
import os

from systemPrompt import build_system_prompt
from tools import COMMANDS

load_dotenv()


# =========================================================
# OUTPUT SCHEMA
# =========================================================

class AgentOutput(BaseModel):
    step: str
    input: Optional[str] = None
    content: Optional[str] = None
    tool: Optional[str] = None


# =========================================================
# CLIENT
# =========================================================

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# =========================================================
# PROMPT
# =========================================================

systemPrompt = build_system_prompt(COMMANDS)  

messageHistory = [
    {
        "role": "system",
        "content": systemPrompt
    }
]

STEP_FLOW = {
    "START": "PLAN",
    "PLAN": "TOOL",
    "TOOL": "OBSERVE",
    "OBSERVE": "OUTPUT",
}


# =========================================================
# USER INPUT
# =========================================================

userInput = input("Write prompt: ")

messageHistory.append({
    "role": "user",
    "content": userInput
})


# =========================================================
# AGENT LOOP
# =========================================================

for _ in range(6):

    response = client.beta.chat.completions.parse(
        model="gemini-3.1-flash-lite",
        messages=messageHistory,
        response_format=AgentOutput,
    )

    parsed = response.choices[0].message.parsed

    step = parsed.step
    tool = parsed.tool

    print(f"\nSTEP: {step}")
    print(parsed.model_dump_json(indent=2))

    # VERY IMPORTANT
    # Append assistant response properly
    messageHistory.append({
        "role": "assistant",
        "content": parsed.model_dump_json()
    })

    match step:
        case "START":
            continue

        case "PLAN":
            continue

        case "TOOL":
            tool_fn = COMMANDS[parsed.tool]["function"]

            tool_output = tool_fn(parsed.input)

            messageHistory.append({
                "role": "assistant",
                "content": str(tool_output)
            })

        case "OBSERVE":
            continue

        case "OUTPUT":

            print("\nFINAL OUTPUT:")
            print(parsed.content)

            break
