# server.py
from mcp.server.fastmcp import FastMCP
import os

# # Create an MCP server
# mcp = FastMCP("Demo")


# # Add an addition tool
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a + b


# # Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"


mcp = FastMCP("AI sticky notes")

NOTES_FILE = "/Users/prakhar/Documents/personal-projects/MCP/mcp-server-demo/notes.txt"

def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")

@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note to the notes file.

    Args:
        message (str): The note to add.

    Returns:
        str: A confirmation message.
    """
    ensure_file()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return "Note added successfully!!"


@mcp.tool()
def read_notes() -> str:
    """
    Read and return all notes from the notes file.

    Returns:
        str: All notes as a single string separated by line breaks.
             if no notes are found, return "No notes found"
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    return content or "No notes found"


@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the latest note from the notes file.

    Returns:
        str: The latest note.
        if no notes are found, return "No notes found"
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else "No notes found"


@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a summary of the current notes.

    Returns:
        str: A summary of the current notes.
        if no notes are found, return "No notes found"
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    if not content:
        return "No notes found"
    return f"Summarize the current notes: {content}"


