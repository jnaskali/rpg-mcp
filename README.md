# RPG MCP Server

This is a simple MCP (Machine Control Protocol) server designed to assist in playing RPGs with Large Language Models (LLMs). It includes simple tools for LLM tool calling that allow true randomness, without which LLMs tend to always let you succeed and generate clichéd stories.

---

![Example screenshot of RPG MCP in use](https://github.com/user-attachments/assets/4bbb2ffb-e097-41a8-83a6-eefaa4d49a4a)

---

The simplest way to utilize the MCP server is to set it up as an stdio MCP server in your chat app of choice (e.g. [Witsy](https://github.com/nbonamy/witsy)) with **python** as the command and **app.py** as the argument (use full paths).

Include instructions in your prompt to, for example,
`"Call check_success, whenever a player character attempts something with a chance of failure, and generate_event to generate a random event at the start of a new scene or when moving to a new location. Incorporate the results into the story without explicitly stating what the generated results was."`

The defaults should work OK, and allow the LLM to customize probabilities based on the story.

The event generation system was loosely inspired by [Mythic Game Master Emulator](https://www.wordmillgames.com/page/mythic-gme.html), a great solo-roleplaying system.


## Features

Tools that can be invoked by an LLM:

*   **`list_tools()`**:
    *   **Description**: Lists all available tools in the MCP server.
    *   **Returns**: A JSON string containing tool names and their descriptions.
    *   **Use Case**: Allows the LLM to discover the capabilities of this server.

*   **`check_success(probability: int = 80, critical_rate: int = 5)`**:
    *   **Description**: Checks for success based on a given probability and critical rate.
    *   **Arguments**:
        *   `probability`: The chance of success (integer between 0-100, defaults to 80).
        *   `critical_rate`: The percentage for critical success/failure (integer between 0-50, defaults to 5). A roll within the bottom `critical_rate` percent is a critical failure, and a roll within the top `critical_rate` percent is a critical success.
    *   **Returns**: A string indicating 'Critical Success!', 'Success!', 'Failure!', or 'Critical Failure!', along with the rolled number.
    *   **Use Case**: Determining the outcome of actions in an RPG where success is probabilistic.

*   **`roll_dice(expr: str)`**:
    *   **Description**: Rolls dice using standard RPG notation (e.g., '1d6', '2d8+3').
    *   **Arguments**:
        *   `expr`: A dice expression string in the format 'NdM[+/-]K' (e.g., '2d6', '1d20+4').
    *   **Returns**: A string detailing the rolls, any modifier, and the total sum.
    *   **Use Case**: Simulating dice rolls for attacks, damage, skill checks, etc.

*   **`generate_event()`**:
    *   **Description**: Generates a random RPG event based on predefined subjects, actions, and objects. It's intended to be interpreted loosely to inspire narrative developments.
    *   **Returns**: A string describing the generated event.
    *   **Use Case**: Introducing unexpected plot twists, environmental changes, or NPC actions to enrich the game.


## Running the Server

The server can be run using different transport protocols, though I've only tested stdio, which is the default.


### Prerequisites

*   Python 3
*   The `FastMCP` library


### Command-Line Arguments

*   `--transport`: Choose the transport protocol.
    *   `stdio` (default): Uses standard input/output for communication.
    *   `http`: Runs an HTTP server.
*   `--host`: Host address for HTTP transport (default: `127.0.0.1`).
*   `--port`: Port number for HTTP transport (default: `8080`).


## Usage with LLMs

### How it works

This MCP server acts as a backend tool provider for an LLM. When the LLM needs to perform an action like rolling dice or determining the success of an action, it can make a request to this server by calling the appropriate tool with the required parameters. You can run it locally, even if you use a remote API for the LLM, as long as the chat application supports local MCPs. After enabling the server, its use is automatic.

For example, if an LLM is narrating a scene where a player attempts to pick a lock, it might:
1.  Decide on a `probability` of success (e.g., 60%) and a `critical_rate` (e.g., 10%).
2.  Call the `check_success(probability=60, critical_rate=10)` tool on this server.
3.  Receive the result (e.g., "Rolled 45: Success!").
4.  Incorporate this result into its narrative.

Similarly, for combat within a rule-set that includes dice throws, the LLM could call `roll_dice(expr='1d20+5')` for an attack roll or `roll_dice(expr='2d6+3')` for damage.

The `generate_event()` tool can be used by the LLM to introduce spontaneous elements into the story when appropriate, either automatically in the prompt or by asking for it.

This separation allows the LLM to focus on creative storytelling and role-playing, while the MCP server handles the randomness and mechanical aspects of the RPG.


> [!IMPORTANT]  
> Tool calling currently works best with Mistral, Llama or Qwen, as well as most paid APIs.

### Integrating with an LLM via STDIO

The simplest way to use this server with an app that supports MCP via standard input/output (stdio) is to download app.py and configure the LLM to run this script directly:

*   **Command**: `/usr/bin/python` (the full path to your Python interpreter)
*   **Arguments**: `app.py` (the full path to `app.py`)

![Screenshot of RPG MCP in Witsy](https://github.com/user-attachments/assets/bf5261bb-9fe9-44d8-af25-de7f67c5e1c1)


The LLM will then communicate with the server by writing MCP requests to its standard input and reading MCP responses from its standard output. Make sure that the `app.py` script is in the working directory of the LLM process, or provide the full path to `app.py`.

You can test the functionality by using the default prompt and querying for a random event:

![Screenshot of a working test](https://github.com/user-attachments/assets/8b280c0d-aedf-4177-b833-872c93ba6c85)

The format should be unique enough to recognize whether the LLM is hallucinating or returning a functioning random event. Most models complain that they don't have information on or the correct context for generate_event, if it's not working.


## TODO

- [ ] Include complete example prompts
