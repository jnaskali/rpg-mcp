# RPG MCP Server

A simple MCP (Model Context Protocol) server for playing RPGs with Large Language Models. It provides tools for dice rolling, success checks, and random event generation.

---

![Example screenshot of RPG MCP in use](https://github.com/user-attachments/assets/4bbb2ffb-e097-41a8-83a6-eefaa4d49a4a)

---

## Features

- **`check_success(probability, critical_rate)`** - Determines success/failure with optional critical results
- **`roll_dice(expr)`** - Rolls dice using standard RPG notation (e.g., '1d6', '2d8+3')
- **`generate_event()`** - Generates random RPG events for plot twists and surprises
- **`list_tools()`** - Lists all available tools

## Installation

### Prerequisites

- Python 3
- [uv](https://docs.astral.sh/uv/) - A fast Python package installer

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jnaskali/rpg-mcp.git
cd rpg-mcp
```

2. Install dependencies with uv:
```bash
uv sync
```

### Configuration

Add the following to your MCP client's configuration file (e.g., `mcp.json` in Claude Desktop or other MCP-compatible clients):

```json
{
  "mcpServers": {
    "rpg-mcp": {
      "command": "/usr/bin/uv",
      "args": [
        "run",
        "python",
        "app.py"
      ],
      "cwd": "/PATH_TO/rpg-mcp/"
    }
  }
}
```

Replace `/PATH_TO/rpg-mcp/` with the actual path to your rpg-mcp directory.

## Usage

Once configured, the LLM can call the tools to:

- Roll dice for attacks, damage, or skill checks
- Determine action outcomes with customizable success probabilities
- Generate random events to drive the narrative forward

### Example Prompt

Include instructions in your prompt like:

> "Call check_success whenever a player character attempts something with a chance of failure, and generate_event to generate a random event at the start of a new scene or when moving to a new location."

The event generation system is inspired by [Mythic Game Master Emulator](https://www.wordmillgames.com/page/mythic-gme.html).

> [!IMPORTANT]  
> Tool calling works best with models that support function calling, such as Claude, GPT-4, Mistral, Llama, or Qwen.

## Examples

Test the server by asking the LLM to generate a random event. The unique format should make it clear whether the tool is working or if the LLM is hallucinating results.

![Screenshot of a working test](https://github.com/user-attachments/assets/8b280c0d-aedf-4177-b833-872c93ba6c85)
