# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import builtins
import html
import json
import platform
import unicodedata
from typing import Any, Optional, Sequence

import questionary
from prompt_toolkit import HTML, print_formatted_text
from questionary import Style

from fabric_cli.core import fab_constant, fab_state_config
from fabric_cli.core.fab_exceptions import FabricCLIError

custom_style = Style(
    [
        ("qmark", "fg:#49C5B1"),
        ("question", ""),
        ("answer", "fg:#6c6c6c"),
        ("pointer", "fg:#49C5B1"),
        ("highlighted", "fg:#49C5B1"),
        ("selected", "fg:#49C5B1"),
        ("separator", "fg:#6c6c6c"),
        ("instruction", "fg:#49C5B1"),
        ("text", ""),
        ("disabled", "fg:#858585 italic"),
    ]
)

# Prompts - Questionary


def prompt_ask(text: str = "Question") -> Any:
    return questionary.text(text, style=custom_style).ask()


def prompt_password(text: str = "password") -> Any:
    return questionary.password(text, style=custom_style).ask()


def prompt_confirm(text: str = "Are you sure?") -> Any:
    return questionary.confirm(text, style=custom_style).ask()


def prompt_select_items(question: str, choices: Sequence) -> Any:
    # Prompt the user to select multiple items from a checkbox
    selected_items = questionary.checkbox(
        question, choices=choices, pointer=">", style=custom_style
    ).ask()

    return selected_items


def prompt_select_item(question: str, choices: Sequence) -> Any:
    # Prompt the user to select a single item from a list of choices
    selected_item = questionary.select(
        question, choices=choices, pointer=">", style=custom_style
    ).ask()

    return selected_item


# Prints - Questionary


def print(text: str) -> None:
    _safe_print(text)


def print_fabric(text: str) -> None:
    _safe_print(text, style="fg:#49C5B1")


def print_grey(text: str) -> None:
    _safe_print(text, style="fg:grey")


def print_progress(text, progress: Optional[str] = None) -> None:
    if progress:
        print_grey(f"∟ {text}: {progress}%")
    else:
        print_grey(f"∟ {text}")


def print_api_response(payload: Any) -> None:
    # Print the JSON payload in a readable format
    try:
        pretty_json = json.dumps(payload, indent=2)
        print_grey(pretty_json)
    except (TypeError, json.JSONDecodeError):
        # If the payload is not JSON, print it as plain text
        print_grey(str(payload))


# Prints - prompt_toolkit


def print_done(text: str) -> None:
    # Escape the text to avoid HTML injection and parsing issues
    escaped_text = html.escape(text)
    _safe_print_formatted_text(f"<ansigreen>*</ansigreen> {escaped_text}", escaped_text)


def print_warning(text: str, command: Optional[str] = None) -> None:
    # Escape the text to avoid HTML injection and parsing issues
    text = text.rstrip(".")
    escaped_text = html.escape(text)
    if command:
        _safe_print_formatted_text(
            f"<ansiyellow>!</ansiyellow> {command}: {escaped_text}", escaped_text
        )
    else:
        _safe_print_formatted_text(
            f"<ansiyellow>!</ansiyellow> {escaped_text}", escaped_text
        )


def print_error(text_or_exception, command: Optional[str] = None) -> None:
    escaped_text = ""
    if isinstance(text_or_exception, FabricCLIError):
        debug = fab_state_config.get_config(fab_constant.FAB_DEBUG_ENABLED) == "true"
        escaped_text = text_or_exception.formatted_message(debug)
    else:
        # Escape the text to avoid HTML injection and parsing issues
        text_or_exception = text_or_exception.rstrip(".")
        escaped_text = html.escape(text_or_exception)

    if command:
        _safe_print_formatted_text(
            f"<ansired>x</ansired> {command}: {escaped_text}", escaped_text
        )
    else:
        _safe_print_formatted_text(f"<ansired>x</ansired> {escaped_text}", escaped_text)


def print_info(text, command: Optional[str] = None) -> None:
    # Escape the text to avoid HTML injection and parsing issues
    escaped_text = html.escape(text.rstrip("."))
    if command:
        _safe_print_formatted_text(
            f"<ansiblue>*</ansiblue> {command}: {escaped_text}", escaped_text
        )
    else:
        _safe_print_formatted_text(
            f"<ansiblue>*</ansiblue> {escaped_text}", escaped_text
        )


# Display


# Display all available commands organized by category with descriptions
def display_help(
    commands: dict[str, dict[str, str]], custom_header: Optional[str] = None
) -> None:
    if not commands or len(commands) == 0:
        print("No commands available.")
        return
    if custom_header:
        print(f"{custom_header} \n")
    else:
        print("Work seamlessly with Fabric from the command line.\n")
        print("Usage: fab <command> <subcommand> [flags]\n")

    max_command_length = max(
        len(cmd) for cmd_dict in commands.values() for cmd in cmd_dict
    )

    for category, cmd_dict in commands.items():
        print(f"{category}:")
        for command, description in cmd_dict.items():
            padded_command = f"{command:<{max_command_length}}"
            print(f"  {padded_command}: {description}")
        print("")

    # Learn more
    print("Learn More:")
    print(
        "  Use `fab <command> <subcommand> --help` for more information about a command."
    )
    print("  Use `fab config set mode interactive` to enable interactive mode.")
    print("  Read the docs at https://aka.ms/fabric-cli.\n")


# ascii Display


def get_visual_length(entry: Any, field: Any) -> int:
    return _get_visual_length(str(entry.get(field, "")))


# Prints a list of entries in Unix-like format based on specified fields
def print_entries_unix_style(
    entries: Any, fields: Any, header: Optional[bool] = False
) -> None:
    if isinstance(entries, dict):
        _entries = [entries]
    elif isinstance(entries, list):
        if len(entries) == 0:
            # Putting an empty dictionary to avoid errors and print a blank line instead
            # This way in case of headers, the header will be printed
            _entries = [{}]
        else:
            _entries = entries
    else:
        raise FabricCLIError(
            "Invalid entries format provided", fab_constant.ERROR_INVALID_ENTRIES_FORMAT
        )

    if header:
        widths = [
            max(len(field), max(get_visual_length(entry, field) for entry in _entries))
            for field in fields
        ]

    else:
        widths = [
            max(len(str(entry.get(field, ""))) for entry in _entries)
            for field in fields
        ]
    # Add extra space for better alignment
    # Adjust this value for more space if needed
    widths = [w + 2 for w in widths]
    if header:
        print_grey(_format_unix_style_field(fields, widths))
        # Print a separator line, offset of 1 for each field
        print_grey("-" * (sum(widths) + len(widths)))

    for entry in _entries:
        print_grey(_format_unix_style_entry(entry, fields, widths))


# Others


def get_os_specific_command(command: str) -> str:
    if platform.system() == "Windows":
        return fab_constant.OS_COMMANDS.get(command, {}).get("windows", command)
    else:
        return fab_constant.OS_COMMANDS.get(command, {}).get("unix", command)


# Utils


def _safe_print(text: str, style: Optional[str] = None) -> None:
    try:
        if style:
            questionary.print(text, style=style)
        else:
            questionary.print(text)
    except (RuntimeError, AttributeError, Exception) as e:
        _print_fallback(text, e)


def _safe_print_formatted_text(formatted_text: str, escaped_text: str) -> None:
    try:
        print_formatted_text(HTML(formatted_text))
    except (RuntimeError, AttributeError, Exception) as e:
        _print_fallback(escaped_text, e)


def _print_fallback(text: str, e: Exception) -> None:
    # Fallback print
    # https://github.com/prompt-toolkit/python-prompt-toolkit/issues/406
    builtins.print(text)
    if isinstance(e, AttributeError):  # Only re-raise AttributeError (pytest)
        raise


def _format_unix_style_field(fields: list[str], widths: list[int]) -> str:
    formatted = ""
    # Dynamically format based on the fields provided
    for i, field in enumerate(fields):
        # Adjust spacing for better alignment
        formatted += f"{field:<{widths[i]}} "

    return formatted.strip()


def _format_unix_style_entry(
    entry: dict[str, str], fields: list[str], widths: list[int]
) -> str:
    formatted = ""
    # Dynamically format based on the fields provided
    for i, field in enumerate(fields):
        value = str(entry.get(field, ""))
        # Adjust spacing for better alignment
        length = len(value)
        visual_length = _get_visual_length(value)
        if visual_length > length:
            formatted += f"{value:<{widths[i] - (visual_length - length) + 2 }} "
        else:
            formatted += f"{value:<{widths[i]}} "

    return formatted.strip()


def _get_visual_length(string: str) -> int:
    length = 0
    for char in string:
        # Check if the character is wide or normal
        if unicodedata.east_asian_width(char) in [
            "F",
            "W",
        ]:  # Fullwidth or Wide characters
            length += 2
        else:
            length += 1
    return length
