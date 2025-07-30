import os
import tomllib
from typing import Dict, List, Callable
from colorama import Fore, Style
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import subprocess

TOOL_FOLDER = ".gai"
RULES_FILE = "gai-rules.md"

def read_gai_rules() -> str:
    """
    Read the rules from the gai-rules.md file.
    """
    rules_path = Path.cwd() / TOOL_FOLDER / RULES_FILE
    if not rules_path.exists():
        return ""
    with rules_path.open('r') as f:
        return f.read()

def attr_is_defined(args, attr: str) -> bool:
    """
    Check if the specified attribute is defined in the given object.
    """
    return hasattr(args, attr) and getattr(args, attr) is not None


def get_attr_or_default(args, attr: str, default) -> any:
    """
    Get the value of the specified attribute from the object, or return a default value.
    """
    value = getattr(args, attr, default)
    return value if value is not None else default


def get_current_branch() -> str:
    """
    Retrieve the name of the current Git branch.
    """
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def push_changes(remote_repo: str) -> None:
    """
    Push changes to the specified remote repository.
    """
    subprocess.run(["git", "push", remote_repo])


def get_package_version(package_name: str) -> str:
    """
    Get the version of the specified package.
    """
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Package not found"


def print_tokens(
    user_message: int,
    max_tokens: int
) -> int:
    """
    Print the number of tokens in the system prompt and user message.
    """
    print("\n" + "="*40)
    print(f"{Fore.CYAN}User tokens: {user_message}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Max tokens: {max_tokens}")
    print(f"={Style.RESET_ALL}"*40 + "\n")


def create_user_message(user_message: str) -> Dict[str, str]:
    """
    Create a user message from the given string.
    """
    return {"role": "user", "content": user_message}


def create_system_message(system_message: str) -> Dict[str, str]:
    """
    Create a system message from the given string.
    """
    return {"role": "system", "content": system_message}


def validate_messages(messages: List[Dict[str, str]]) -> bool:
    """Validate message format."""
    try:
        for message in messages:
            if not isinstance(message, dict):
                raise ValueError("Each message must be a dictionary")
            if "role" not in message and "name" not in message:
                raise ValueError("Each message must have either 'role' or 'name'")
            if "content" not in message:
                raise ValueError("Each message must have 'content'")
        return True
    except Exception as e:
        raise ValueError(f"Message validation failed: {str(e)}")


def get_api_huggingface_key() -> str:
    api_key = os.environ.get("HUGGINGFACE_API_TOKEN")
    if api_key is None:
        raise ValueError(
            "HUGGINGFACE_API_TOKEN is not set, please set it in your environment variables")
    return api_key


def get_ticket_identifier(branch_name: str, ai_client: Callable[[List[Dict[str, str]]], str]) -> str:
    """
    Extract ticket identifier from branch name using AI client.

    Args:
        branch_name: The git branch name to analyze
        ai_client: The AI client function to use for analysis

    Returns:
        The ticket identifier string or None if no ticket found
    """
    from gai_tool.src.prompts import Prompts

    prompt = Prompts().build_ticket_identifier_prompt()

    messages: List[Dict[str, str]] = [
        create_system_message(prompt),
        create_user_message(branch_name)
    ]

    response = ai_client(
        user_message=messages.copy(),
    )
    return None if response == "None" else response
