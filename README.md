# AI Sticky Notes MCP Server

A simple note-taking system built with the Model Context Protocol (MCP) that allows AI assistants to create, read, and summarize notes.

## Overview

This project implements a lightweight note-taking system that demonstrates core MCP concepts with the following features:

- Add new notes to a central repository
- Read all existing notes
- Access the latest note
- Generate AI summaries of stored notes

The service is built using FastMCP, making it easy to integrate with AI assistants like Claude Desktop or Cursor.

## Prerequisites

- Python 3.8+
- `uv` package manager (https://github.com/astral-sh/uv)
- Claude Desktop (for using with Claude)
- Cursor IDE (for using with Cursor's AI assistant)

## Installation

### Clone the repository

```bash
git clone https://github.com/pi-prakhar/mcp-server-demo.git
cd mcp-server-demo
```

### Install dependencies

This project uses a pyproject.toml file with uv for dependency management. Install the dependencies with:

```bash
# Install dependencies using uv
uv pip install -e .
```

### Run the server

For development and testing:

```bash
uv run mcp dev main.py
```

To install the server for Claude Desktop:

```bash
uv run mcp install main.py
```

## Connecting to Claude Desktop

### Automatic setup

After running the installation command, you can set up Claude Desktop automatically:

```bash
mcp setup --app Claude
```

### Manual setup

Alternatively, edit the Claude Desktop configuration file:

- On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

Add the following to the configuration file:

```json
{
  "mcpServers": {
    "Demo": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/full/path/to/your/main.py"
      ]
    }
  }
}
```

> **Note:** If Claude reports errors finding the `uv` command, use the full path to the uv executable. To find the full path:
>
> ```bash
> # On macOS/Linux
> which uv
>
> # On Windows (Command Prompt)
> where uv
>
> # On Windows (PowerShell)
> Get-Command uv | Select-Object -ExpandProperty Source
> ```
>
> Then use the full path in your configuration:
>
> ```json
> {
>  "mcpServers": {
>    "Demo": {
>      "command": "/full/path/to/your/uv",
>      "args": [
>        "run",
>        "--with",
>        "mcp[cli]",
>        "mcp",
>        "run",
>        "/full/path/to/your/main.py"
>      ]
>    }
>  }
>}
> ```
> 
> Alternatively, you can create a symlink to uv in a directory that's in your PATH:
> ```bash
> # On macOS/Linux
> sudo ln -s /path/to/your/uv /usr/local/bin/uv
> 
> # On Windows (run Command Prompt as Administrator)
> mklink C:\Windows\System32\uv.exe C:\path\to\your\uv.exe
> ```

### Finalizing setup

1. After updating your configuration file, restart Claude Desktop
2. You should see a hammer icon in the bottom right corner of the input box
3. Click on the hammer to verify the AI Sticky Notes tools are available

## Integrating with Cursor

### Global Setup

1. Open Cursor IDE
2. Go to `Cursor Settings` > `Features` > `MCP`
3. Click on the `+ Add New MCP Server` button
4. Fill out the form:
   - **Type**: Select `stdio` as the transport
   - **Name**: Enter `ai-sticky-notes` or any descriptive name
   - **Command**: Enter the full command to run the server:
        ```bash
        uv run --with mcp[cli] mcp run /full/path/to/your/main.py
        ```
5. Click `Add`
6. You may need to press the refresh button to populate the tool list

### Project-Specific Setup

Alternatively, set up for your specific project:

1. Create a `.cursor/mcp.json` file in your project directory with:
   ```json
   {
     "mcpServers": {
       "ai-sticky-notes": {
         "command": "uv",
         "command": "uv",
         "args": [
           "run",
           "--with",
           "mcp[cli]",
           "mcp",
           "run",
           "/full/path/to/your/main.py"
         ]
       }
     }
   }
   ```

### Important Notes

- **Resources Limitation**: Cursor currently only supports MCP tools but not resources. This means the `notes://latest` resource will not be available in Cursor.
- **Tool Approval**: By default, Cursor will ask for your approval before running any MCP tools. You can enable "Yolo mode" in settings to allow automatic execution.
- **Tool Usage**: The Agent will automatically use MCP tools when relevant. You can also prompt specific tool usage by mentioning the tool by name or description.

## Features

### Tools

- `add_note` - Append a new note to the notes file
- `read_notes` - Read and return all notes from the notes file

### Resources

- `notes://latest` - Get the latest note from the notes file

### Prompts

- `note_summary_prompt` - Generate a summary of the current notes

## Example Usage

Once connected to Claude or Cursor's AI assistant, you can interact with the note system using natural language:

```
User: Add a reminder to buy groceries tomorrow
AI: I'll add that note for you.
    [Uses add_note tool]
    Note added successfully!

User: What notes do I currently have?

AI: Let me check your notes:
    [Uses read_notes tool]
    - Buy groceries: milk, eggs, bread
    - Call dentist to reschedule appointment
    - Meeting with team at 3pm tomorrow

User: What was the most recent note I added?

AI: Your most recent note is:
    [Uses notes://latest resource]
    Meeting with team at 3pm tomorrow

User: Can you summarize all my notes?

AI: [Uses note_summary_prompt]
    Your notes contain reminders about shopping for basic groceries (milk, eggs, bread), 
    calling the dentist to change your appointment time, and an upcoming team meeting 
    scheduled for tomorrow at 3pm.
```

## Project Structure

- `main.py` - Main MCP server implementation with tool definitions
- `notes.txt` - File where notes are stored

## Customization

You can modify the `NOTES_FILE` path in `main.py` to change where notes are stored.

## Debugging

Since MCP servers communicate over stdio, debugging can be challenging. The MCP dev mode provides helpful debugging information:

```bash
uv run mcp dev main.py
```

