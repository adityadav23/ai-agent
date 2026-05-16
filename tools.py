from pathlib import Path

# Base sandbox directory
BASE_DIR = Path("./").resolve()


# =========================================================
# HELPER
# =========================================================

def safe_path(path: str) -> Path:

    full_path = (BASE_DIR / path).resolve()

    # Prevent directory traversal
    if not str(full_path).startswith(str(BASE_DIR)):
        raise ValueError("Invalid path")

    return full_path


# =========================================================
# CREATE PROJECT
# =========================================================

def create_project(project_name: str) -> str:

    path = safe_path(project_name)

    path.mkdir(parents=True, exist_ok=True)

    return f"Project created: {path}"


# =========================================================
# CREATE FILE
# =========================================================

def create_file(file_path: str, content: str = "") -> str:

    path = safe_path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content)

    return f"File created: {path}"


# =========================================================
# READ FILE
# =========================================================

def read_file(file_path: str) -> str:

    path = safe_path(file_path)

    if not path.exists():
        return "File does not exist"

    return path.read_text()


# =========================================================
# UPDATE FILE
# =========================================================

def update_file(file_path: str, new_content: str) -> str:

    path = safe_path(file_path)

    if not path.exists():
        return "File does not exist"

    path.write_text(new_content)

    return "File updated successfully"


# =========================================================
# APPEND TO FILE
# =========================================================

def append_file(file_path: str, content: str) -> str:

    path = safe_path(file_path)

    with open(path, "a") as f:
        f.write(content)

    return "Content appended"


# =========================================================
# LIST FILES
# =========================================================

def list_files(directory: str = ""):

    path = safe_path(directory)

    return [str(p.relative_to(BASE_DIR)) for p in path.rglob("*")]


# # =========================================================
# # DELETE FILE
# # =========================================================

# def delete_file(file_path: str) -> str:

#     path = safe_path(file_path)

#     if path.exists():
#         path.unlink()
#         return "File deleted"

#     return "File not found"


def checkEven(input: str) -> bool:
    try:
        number = int(input)
    except ValueError:
        return False
    return number%2 == 0


COMMANDS = {
    "checkEven": {
        "function": checkEven,
        "description": "Takes a number as input and returns whether it is even or not.",
        "returns": "boolean"
    },

    "create_file": {
        "function": create_file,
        "description": "Creates a new file with given content.",
        "returns": "string"
    },

    "read_file": {
        "function": read_file,
        "description": "Reads content from a file.",
        "returns": "string"
    },
    "update_file": {
        "function": update_file,
        "description": "Updates content of a file.",
        "returns": "string"
    },
    "append_file": {
        "function": append_file,
        "description": "Appends content to a file.",
        "returns": "string"
    },
    "list_files": {
        "function": list_files,
        "description": "Lists all files in a directory.",
        "returns": "list of strings"
    },
    "create_project": {
        "function": create_project,
        "description": "Creates a new project (directory).",
        "returns": "string"
    }
}