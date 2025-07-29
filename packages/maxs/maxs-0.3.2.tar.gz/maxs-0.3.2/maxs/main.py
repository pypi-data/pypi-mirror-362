#!/usr/bin/env python3
"""
maxs - main application module.

a minimalist strands agent.
"""

import argparse
import base64
import os
import sys
import datetime
import json
from typing import Any
import uuid
from pathlib import Path

from strands import Agent
from strands.telemetry import StrandsTelemetry
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

from maxs.models.models import create_model
from maxs.handlers.callback_handler import callback_handler


def read_prompt_file():
    """Read system prompt text from .prompt file if it exists (repo or /tmp/.maxs/.prompt)."""
    prompt_paths = [
        Path(".prompt"),
        Path("/tmp/.maxs/.prompt"),
        Path("README.md"),
    ]
    for path in prompt_paths:
        if path.is_file():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read(), str(path)
            except Exception:
                continue
    return "", None


def get_shell_history_file():
    """Get the maxs-specific history file path."""
    # Use /tmp/.maxs_history as requested
    maxs_history = Path("/tmp/.maxs_history")
    return str(maxs_history)


def get_shell_history_files():
    """Get available shell history file paths."""
    history_files = []

    # Maxs history (primary)
    maxs_history = Path("/tmp/.maxs_history")
    if maxs_history.exists():
        history_files.append(("maxs", str(maxs_history)))

    # Bash history
    bash_history = Path.home() / ".bash_history"
    if bash_history.exists():
        history_files.append(("bash", str(bash_history)))

    # Zsh history
    zsh_history = Path.home() / ".zsh_history"
    if zsh_history.exists():
        history_files.append(("zsh", str(zsh_history)))

    return history_files


def parse_history_line(line, history_type):
    """Parse a history line based on the shell type."""
    line = line.strip()
    if not line:
        return None

    if history_type == "maxs":
        # Maxs format: ": timestamp:0;# maxs: query" or ": timestamp:0;# maxs_result: result"
        if "# maxs:" in line:
            try:
                timestamp_str = line.split(":")[1]
                timestamp = int(timestamp_str)
                readable_time = datetime.datetime.fromtimestamp(timestamp).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                query = line.split("# maxs:")[-1].strip()
                return ("you", readable_time, query)
            except (ValueError, IndexError):
                return None
        elif "# maxs_result:" in line:
            try:
                timestamp_str = line.split(":")[1]
                timestamp = int(timestamp_str)
                readable_time = datetime.datetime.fromtimestamp(timestamp).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                result = line.split("# maxs_result:")[-1].strip()
                return ("me", readable_time, result)
            except (ValueError, IndexError):
                return None

    elif history_type == "zsh":
        # Zsh format: ": timestamp:0;command"
        if line.startswith(": ") and ":0;" in line:
            try:
                parts = line.split(":0;", 1)
                if len(parts) == 2:
                    timestamp_str = parts[0].split(":")[1]
                    timestamp = int(timestamp_str)
                    readable_time = datetime.datetime.fromtimestamp(timestamp).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    command = parts[1].strip()
                    # Skip maxs commands to avoid duplication
                    if not command.startswith("maxs "):
                        return ("shell", readable_time, f"$ {command}")
            except (ValueError, IndexError):
                return None

    elif history_type == "bash":
        # Bash format: simple command per line (no timestamps usually)
        # We'll use a generic timestamp and only include recent ones
        readable_time = "recent"
        # Skip maxs commands to avoid duplication
        if not line.startswith("maxs "):
            return ("shell", readable_time, f"$ {line}")

    return None


def get_distributed_events(agent):
    """Get recent distributed events using the event_bridge tool."""
    try:
        # Check if event_bridge tool is available
        if not hasattr(agent.tool, 'event_bridge'):
            return
            
        # Get distributed event count from environment variable, default to 25
        event_count = int(os.getenv("MAXS_DISTRIBUTED_EVENT_COUNT", "25"))

        # Subscribe to distributed events using the event_bridge tool
        agent.tool.event_bridge(action="subscribe", limit=event_count)

    except Exception as e:
        # Silently fail if distributed events can't be fetched
        return


def publish_conversation_turn(agent, query, response, event_type="conversation_turn"):
    """Publish a conversation turn to the distributed event bridge."""
    try:
        # Check if event_bridge tool is available
        if not hasattr(agent.tool, 'event_bridge'):
            return
            
        # Create a summary of the conversation turn
        response_summary = (
            str(response).replace("\n", " ")[:500] + "..."
            if len(str(response)) > 500
            else str(response)
        )

        message = f"Q: {query}\nA: {response_summary}"

        # Publish the event using the event_bridge tool
        agent.tool.event_bridge(
            action="publish",
            message=message,
            event_type=event_type,
            record_direct_tool_call=False,
        )

    except Exception as e:
        # Silently fail if event publishing fails
        pass


def get_messages_dir():
    """Get the maxs messages directory path."""
    messages_dir = Path("/tmp/.maxs")
    messages_dir.mkdir(exist_ok=True)
    return messages_dir


def get_session_file():
    """Get or create session file path."""
    messages_dir = get_messages_dir()

    # Generate session ID based on date and UUID
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    session_id = str(uuid.uuid4())[:8]  # Short UUID

    session_file = messages_dir / f"{today}-{session_id}.json"
    return str(session_file)


def save_agent_messages(agent, session_file):
    """Save agent.messages to JSON file."""
    try:
        # Convert messages to serializable format
        messages_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "messages": [],
        }

        # Handle different message formats
        for msg in agent.messages:
            if hasattr(msg, "to_dict"):
                # If message has to_dict method
                messages_data["messages"].append(msg.to_dict())
            elif hasattr(msg, "__dict__"):
                # If message is an object with attributes
                msg_dict = {}
                for key, value in msg.__dict__.items():
                    try:
                        # Try to serialize the value
                        json.dumps(value)
                        msg_dict[key] = value
                    except (TypeError, ValueError):
                        # If not serializable, convert to string
                        msg_dict[key] = str(value)
                messages_data["messages"].append(msg_dict)
            else:
                # Fallback: convert to string
                messages_data["messages"].append(str(msg))

        # Write to file
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(messages_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        # Silently fail if we can't save messages
        print(f"⚠️  Warning: Could not save messages: {e}")


def get_last_messages(agent=None):
    """Get the last N messages from multiple shell histories and distributed events for context."""
    try:
        # Get message count from environment variable, default to 100
        message_count = int(os.getenv("MAXS_LAST_MESSAGE_COUNT", "100"))

        all_entries = []

        # Get all history files (local shell history)
        history_files = get_shell_history_files()

        for history_type, history_file in history_files:
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # For bash history, only take recent lines since there are no timestamps
                if history_type == "bash":
                    lines = lines[-message_count:]  # Only last N bash commands

                # Parse lines based on history type
                for line in lines:
                    parsed = parse_history_line(line, history_type)
                    if parsed:
                        all_entries.append(parsed)
            except Exception as e:
                # Skip files that can't be read
                continue

        # Get distributed events if agent is available
        if agent:
            try:
                get_distributed_events(agent)
            except Exception as e:
                # Skip distributed events if they can't be fetched
                pass

        # Take the last N entries
        recent_entries = (
            all_entries[-message_count:]
            if len(all_entries) >= message_count
            else all_entries
        )

        if not recent_entries:
            return ""

        # Format for context
        context = (
            f"\n\nRecent conversation context (last {len(recent_entries)} messages):\n"
        )
        for speaker, timestamp, content in recent_entries:
            context += f"[{timestamp}] {speaker}: {content}\n"
        # print(context)
        return context

    except Exception:
        return ""


def append_to_shell_history(query, response):
    """Append the interaction to maxs shell history."""
    try:
        history_file = get_shell_history_file()

        # Format the entry for shell history
        # Use a comment format that's shell-compatible
        timestamp = os.popen("date +%s").read().strip()

        with open(history_file, "a", encoding="utf-8") as f:
            # Add the query
            f.write(f": {timestamp}:0;# maxs: {query}\n")
            # Add a compressed version of the response
            response_summary = (
                str(response).replace("\n", " ")[
                    : int(os.getenv("MAXS_RESPONSE_SUMMARY_LENGTH", "500"))
                ]
                + "..."
            )
            f.write(f": {timestamp}:0;# maxs_result: {response_summary}\n")

    except Exception as e:
        # Silently fail if we can't write to history
        pass


def setup_otel() -> None:
    """Setup OpenTelemetry if configured."""
    otel_host = os.environ.get("LANGFUSE_HOST")

    if otel_host:
        public_key = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        secret_key = os.environ.get("LANGFUSE_SECRET_KEY", "")

        if public_key and secret_key:
            auth_token = base64.b64encode(
                f"{public_key}:{secret_key}".encode()
            ).decode()
            otel_endpoint = f"{otel_host}/api/public/otel/v1/traces"

            os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_endpoint
            os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = (
                f"Authorization=Basic {auth_token}"
            )
            # strands_telemetry = StrandsTelemetry()
            # strands_telemetry.setup_otlp_exporter()


def get_tools() -> dict[str, Any]:
    """Returns the filtered collection of available agent tools for strands.

    This function first gets all available tools, then filters them based on
    the STRANDS_TOOLS environment variable if it exists.

    Returns:
        Dict[str, Any]: Dictionary mapping tool names to tool functions
    """
    # First get all tools
    tools = _get_all_tools()

    # Then apply filtering based on environment variable
    return _filter_tools(tools)


def _get_all_tools() -> dict[str, Any]:
    """Returns all available tools without filtering.

    Returns:
        Dict[str, Any]: Dictionary mapping tool names to tool functions
    """
    tools = {}

    try:
        # Strands tools
        from maxs.tools import (
            event_bridge,
            bash,
            tcp,
            use_agent,
            scraper,
            tasks,
            use_computer,
            environment,
            dialog,
        )

        tools = {
            "event_bridge": event_bridge,
            "bash": bash,
            "tcp": tcp,
            "use_agent": use_agent,
            "scraper": scraper,
            "tasks": tasks,
            "use_computer": use_computer,
            "environment": environment,
            "dialog": dialog,
        }

    except ImportError as e:
        print(f"Warning: Could not import all tools: {e!s}")

    return tools


def _filter_tools(all_tools: dict[str, Any]) -> dict[str, Any]:
    """Filter tools based on STRANDS_TOOLS environment variable.

    Supports both comma-separated strings and JSON arrays for flexibility.

    Args:
        all_tools: Dictionary of all available tools

    Returns:
        Dict[str, Any]: Filtered dictionary of tools
    """
    # Get tool filter from environment variable
    tool_filter_str = os.getenv("STRANDS_TOOLS", "bash,environment,tcp,scraper,use_agent,tasks")

    # If env var not set or set to 'ALL', return all tools
    if not tool_filter_str or tool_filter_str == "ALL":
        return all_tools

    tool_filter = None

    # First try to parse as JSON array
    try:
        tool_filter = json.loads(tool_filter_str)
        if not isinstance(tool_filter, list):
            tool_filter = None
    except json.JSONDecodeError:
        # If JSON parsing fails, try comma-separated string
        pass

    # If JSON parsing failed or didn't produce a list, try comma-separated
    if tool_filter is None:
        # Handle comma-separated string format
        tool_filter = [
            tool.strip() for tool in tool_filter_str.split(",") if tool.strip()
        ]

        # If we still don't have a valid list, return all tools
        if not tool_filter:
            print(
                "Warning: STRANDS_TOOLS env var is not a valid JSON array or comma-separated string. Using all tools."
            )
            return all_tools

    # Filter the tools
    filtered_tools = {}
    for tool_name in tool_filter:
        if tool_name in all_tools:
            filtered_tools[tool_name] = all_tools[tool_name]
        else:
            print(
                f"Warning: Tool '{tool_name}' specified in STRANDS_TOOLS env var not found."
            )

    return filtered_tools


def create_agent(model_provider="ollama"):
    """
    Create a Strands Agent with Ollama model.

    Args:
        model_provider: Model provider, default ollama (default: qwen3:4b)
        host: Ollama host URL (default: http://localhost:11434)

    Returns:
        Agent: Configured Strands agent
    """
    setup_otel()

    model = create_model(provider=os.getenv("MODEL_PROVIDER", model_provider))

    tools = get_tools()

    # Create the agent
    agent = Agent(
        model=model,
        tools=list(tools.values()),
        callback_handler=callback_handler,
        load_tools_from_directory=True,
    )

    return agent


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="maxs",
        description="minimalist strands agent with ollama integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  maxs                              # Interactive mode
  maxs hello world                  # Single query mode
  maxs "what can you do"            # Single query with quotes
  maxs "hello world" --interactive  # Query then stay interactive
        """,
    )

    parser.add_argument(
        "query",
        nargs="*",
        help="Query to ask the agent (if provided, runs once and exits unless --interactive is used)",
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Keep the conversation active after processing the initial query (useful in tmux)",
    )

    return parser.parse_args()


def main():
    """Main entry point for the maxs agent."""
    # Parse command line arguments
    args = parse_args()

    # Show configuration
    model_provider = os.getenv("MODEL_PROVIDER", "ollama")

    # Create agent first (needed for distributed events)
    agent = create_agent(model_provider)

    # Get recent conversation context (including distributed events)
    recent_context = get_last_messages(agent)

    # Enhanced system prompt with history context and self-modification instructions
    base_prompt = "i'm maxs. minimalist agent. welcome to chat."
    # Read .prompt or /tmp/.maxs/.prompt if present
    prompt_file_content, prompt_file_path = read_prompt_file()
    if prompt_file_content and prompt_file_path:
        prompt_file_note = f"\n\n[Loaded system prompt from: {prompt_file_path}]\n{prompt_file_content}\n"
    else:
        prompt_file_note = ""

    self_modify_note = (
        "\n\nNote: The system prompt for maxs is built from your base instructions, "
        "conversation history, and the .prompt file (in this directory or /tmp/.maxs/.prompt). "
        "You (or the agent) can modify the .prompt file directly to change my personality and instructions. "
        "You can also override with the environment tool: environment(action='set', name='SYSTEM_PROMPT', value='new prompt')."
    )

    system_prompt = (
        base_prompt
        + recent_context
        + prompt_file_note
        + self_modify_note
        + os.getenv("SYSTEM_PROMPT", ".")
    )

    # Set system prompt
    agent.system_prompt = system_prompt

    # Get session file for storing messages
    session_file = get_session_file()
    print(f"📝 Session messages will be saved to: {session_file}")

    # Check if query provided as arguments
    if args.query:
        # Single query mode - join all arguments as the query
        query = " ".join(args.query)
        print(f"\n# {query}")

        try:
            result = agent(query)
            append_to_shell_history(query, result)
            save_agent_messages(agent, session_file)
            # Publish conversation turn to distributed event bridge
            publish_conversation_turn(agent, query, result)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
        
        # If --interactive flag is set, continue to interactive mode
        if not args.interactive:
            return

    print("💡 Type 'exit', 'quit', or 'bye' to quit, or Ctrl+C")

    # Set up prompt_toolkit with history
    history_file = get_shell_history_file()
    history = FileHistory(history_file)

    # Create completions from common commands and shell history
    common_commands = ["exit", "quit", "bye", "help", "clear", "ls", "pwd", "cd"]
    completer = WordCompleter(common_commands, ignore_case=True)

    while True:
        try:
            # Use prompt_toolkit for enhanced input
            q = prompt(
                "\n# ",
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
                completer=completer,
                complete_while_typing=True,
            )

            if q.startswith("!"):
                shell_command = q[1:]  # Remove the ! prefix
                print(f"$ {shell_command}")

                try:
                    # Execute shell command directly using the shell tool
                    result = agent.tool.bash(
                        command=shell_command, timeout=900, shell=True
                    )
                    print(result["content"][0]["text"])
                    append_to_shell_history(q, result["content"][0]["text"])
                    save_agent_messages(agent, session_file)
                    # Publish shell command to distributed event bridge
                    publish_conversation_turn(
                        agent, q, result["content"][0]["text"], "shell_command"
                    )
                except Exception as e:
                    print(f"Shell command execution error: {str(e)}")
                continue

            if q.lower() in ["exit", "quit", "bye"]:
                print("\n👋 Goodbye!")
                break

            if not q.strip():
                continue

            # Get recent conversation context (including distributed events)
            recent_context = get_last_messages(agent)

            # Enhanced system prompt with history context and self-modification instructions
            base_prompt = "i'm maxs. minimalist agent. welcome to chat."
            # Read .prompt or /tmp/.maxs/.prompt if present
            prompt_file_content, prompt_file_path = read_prompt_file()
            if prompt_file_content and prompt_file_path:
                prompt_file_note = f"\n\n[Loaded system prompt from: {prompt_file_path}]\n{prompt_file_content}\n"
            else:
                prompt_file_note = ""

            self_modify_note = (
                "\n\nNote: The system prompt for maxs is built from your base instructions, "
                "conversation history, and the .prompt file (in this directory or /tmp/.maxs/.prompt). "
                "You (or the agent) can modify the .prompt file directly to change my personality and instructions. "
                "You can also override with the environment tool: environment(action='set', name='SYSTEM_PROMPT', value='new prompt')."
            )

            system_prompt = (
                base_prompt
                + recent_context
                + prompt_file_note
                + self_modify_note
                + os.getenv("SYSTEM_PROMPT", ".")
            )
            agent.system_prompt = system_prompt

            result = agent(q)
            append_to_shell_history(q, result)
            save_agent_messages(agent, session_file)
            # Publish conversation turn to distributed event bridge
            publish_conversation_turn(agent, q, result)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue


if __name__ == "__main__":
    main()
