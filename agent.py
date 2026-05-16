from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional
import os

load_dotenv()


class AgentOutput(BaseModel):
    step: str = Field(..., description="The step of the agent's reasoning process.")
    input: Optional[str] = Field(None, description="The input provided to the tool, if any.")
    content: Optional[str] = Field(None, description="The content of the agent's response.")
    tool: Optional[str] = Field(None, description="The tool used by the agent, if any.")


api_key = os.getenv("GEMINI_API_KEY")

def checkEven(number: int) -> bool:
    return number%2 == 0

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

systemPrompt = """
You are an expert AI assistant.

You work in steps:

START
PLAN
TOOL
OBSERVE
OUTPUT

Available tools:

checkEven: Takes a number as input and returns whether it is even or not.
returns a boolean.
Rules:
- Only run one step at a time.
- Wait for observation after tool call.
"""

messageHistory = [
    {"role": "system", "content": systemPrompt}
]

userInput = input("Enter a number to check if it's even: ")
messageHistory.append({"role": "user", "content": f"{userInput} i want to check if this number is even."})

availableTools = {
    "checkEven": checkEven
}


for _ in range(1):

    response = client.chat.completions.parse(
        model = "gemini-3.1-flash-lite",
        messages = messageHistory,
        response_format = AgentOutput,
    )
    step = response.choices[0].message.parsed.step  
    tool = response.choices[0].message.parsed.tool

    print(f"Step: {step}")
    print(response.choices[0].message.parsed.content)

    match step:
        case "START":
            messageHistory.append({"role": "user", "content": response.choices[0].message.parsed.content})
            continue
        case "PLAN":
            messageHistory.append({"role": "user", "content": response.choices[0].message.parsed.content})
            continue
        case "TOOL":
            if tool in availableTools:
                toolOutput = availableTools[tool](int(userInput))
                messageHistory.append({"role": "user", "content": f"Tool output: {toolOutput}"})
            else:
                messageHistory.append({"role": "user", "content": f"Tool {tool} not found."})
            continue
        case "OBSERVE":
            messageHistory.append({"role": "user", "content": response.choices[0].message.parsed.content})
            continue
        case "OUTPUT":
            print(f"The number is even: {response.choices[0].message.parsed.content}")
            break

parsed = response.choices[0].message.parsed


print(parsed.model_dump_json(indent=2))