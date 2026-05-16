

def generate_tools_prompt(commands: dict) -> str:

    tool_lines = []

    for tool_name, tool_info in commands.items():

        description = tool_info["description"]
        returns = tool_info["returns"]

        tool_lines.append(
            f"{tool_name}: {description}\nreturns: {returns}."
        )

    return "\n\n".join(tool_lines)



def build_system_prompt(commands: dict) -> str:

    tools_prompt = generate_tools_prompt(commands)

    system_prompt = f"""
        You are an expert AI assistant.

        You work in steps:

        START->PLAN->TOOL->OBSERVE->OUTPUT

        and you must follow these steps in order.


        Example:

        User: is 5 even?

        START: I need to check if the number is even.
        PLAN: I will use the checkEven tool to check if 5 is even.
        TOOL: checkEven with input 5.
        OBSERVE: The tool returned false, so 5 is not even.
        OUTPUT: The number is even: false.

        Example:
        User: list files in my project
        START: I need to list files in the project directory.
        PLAN: I will use the list_files tool to get the list of files in the project directory.
        TOOL: list_files with input /path/to/project
        OBSERVE: The tool returned ["file1.txt", "file2.txt"], so these are the files in the project directory.
        OUTPUT: The files in the project directory are: ["file1.txt", "file2.txt"].


        Available tools:

        {tools_prompt}

        Rules:
        - Only run one step at a time.
        - Wait for observation after tool call.
        """

    return system_prompt