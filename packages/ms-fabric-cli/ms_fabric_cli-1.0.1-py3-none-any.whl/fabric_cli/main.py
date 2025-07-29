# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import argparse
import html
import re
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

from fabric_cli import __version__
from fabric_cli.commands.auth import fab_auth as login
from fabric_cli.core import fab_constant, fab_logger, fab_state_config
from fabric_cli.core.fab_commands import Command
from fabric_cli.core.fab_context import Context
from fabric_cli.parsers import fab_acls_parser as acls_parser
from fabric_cli.parsers import fab_api_parser as api_parser
from fabric_cli.parsers import fab_auth_parser as auth_parser
from fabric_cli.parsers import fab_config_parser as config_parser
from fabric_cli.parsers import fab_describe_parser as describe_parser
from fabric_cli.parsers import fab_extension_parser as extension_parser
from fabric_cli.parsers import fab_fs_parser as fs_parser
from fabric_cli.parsers import fab_jobs_parser as jobs_parser
from fabric_cli.parsers import fab_labels_parser as labels_parser
from fabric_cli.parsers import fab_tables_parser as tables_parser
from fabric_cli.utils import fab_error_parser as utils_error_parser
from fabric_cli.utils import fab_ui as utils_ui

commands = {
    "Core Commands": {
        "assign": "Assign a resource to a workspace.",
        "cd": "Change to the specified directory.",
        utils_ui.get_os_specific_command(
            "cp"
        ): "Copy an item or file to a destination.",
        "export": "Export an item.",
        "exists": "Check if a workspace, item, or file exists.",
        "get": "Get a workspace or item property.",
        "import": "Import an item to create or modify it.",
        utils_ui.get_os_specific_command("ls"): "List workspaces, items, and files.",
        utils_ui.get_os_specific_command("ln"): "Create a shortcut.",
        "mkdir": "Create a new workspace, item, or directory.",
        utils_ui.get_os_specific_command("mv"): "Move an item or file.",
        "open": "Open a workspace or item in the browser.",
        "pwd": "Print the current working directory.",
        utils_ui.get_os_specific_command(
            "rm"
        ): "Delete a workspace, item, or file. Use with caution.",
        "set": "Set a workspace or item property.",
        "start": "Start a resource.",
        "stop": "Stop a resource.",
        "unassign": "Unassign a resource from a workspace.",
    },
    "Resource Commands": {
        "acl": fab_constant.COMMAND_ACLS_DESCRIPTION,
        "label": fab_constant.COMMAND_LABELS_DESCRIPTION,
        "job": fab_constant.COMMAND_JOBS_DESCRIPTION,
        "table": fab_constant.COMMAND_TABLES_DESCRIPTION,
    },
    "Util Commands": {
        "api": fab_constant.COMMAND_API_DESCRIPTION,
        "auth": fab_constant.COMMAND_AUTH_DESCRIPTION,
        "config": fab_constant.COMMAND_CONFIG_DESCRIPTION,
        "desc": fab_constant.COMMAND_DESCRIBE_DESCRIPTION,
        # "extension": fab_constant.COMMAND_EXTENSIONS_DESCRIPTION,
    },
    "Flags": {
        "--help": "Show help for command.",
        "--version": "Show version.",
    },
}


class CustomHelpFormatter(argparse.HelpFormatter):

    def __init__(
        self,
        prog,
        fab_examples=None,
        fab_aliases=None,
        fab_learnmore=None,
        *args,
        **kwargs,
    ):
        super().__init__(prog, *args, **kwargs)
        self.fab_examples = fab_examples or []
        self.fab_aliases = fab_aliases or []
        self.fab_learnmore = fab_learnmore or []

    def _format_args(self, action, default_metavar):
        # For nargs='*' or '+', show only the metavar without '[...]'
        if action.nargs in ("*", "+"):
            if action.option_strings:
                return ""
            else:
                # Ensure metavar is lowercase for positional arguments
                return f"<{action.dest}>"
        return super()._format_args(action, default_metavar)

    def _format_action_invocation(self, action):
        if not action.metavar and action.nargs in (None, "?"):
            # For no metavar and simple arguments
            return ", ".join(action.option_strings)
        elif action.nargs in ("*", "+"):
            # For nargs='*' or '+', ensure metavar or default formatting
            metavar = self._format_args(action, action.dest)
            return ", ".join(action.option_strings) + metavar
        else:
            return super()._format_action_invocation(action)

    def format_help(self):
        help_message = super().format_help()

        # Custom output
        help_message = help_message.replace("usage:", "Usage:")
        help_message = help_message.replace("positional arguments:", "Arg(s):")
        help_message = help_message.replace("options:", "Flags:")

        help_message = re.sub(
            r"\s*-h, --help\s*(Show help for command|show this help message and exit)?",
            "",
            help_message,
        )
        help_message = help_message.replace("  -help\n", "")
        help_message = help_message.replace("[-h] ", "")
        help_message = help_message.replace("[-help] ", "")
        help_message = help_message.replace("[-help]", "")

        # Check if there are any flags (options) and omit if none
        if "Flags:" in help_message:
            flags_section = help_message.split("Flags:")[1].strip()
            if not flags_section:  # If no flags follow the "Flags:" line, remove it
                help_message = help_message.replace("\nFlags:\n", "")

        # Add aliases
        if self.fab_aliases:
            help_message += "\nAliases:\n"
            for alias in self.fab_aliases:
                help_message += f"  {alias}\n"

        # Add examples
        if self.fab_examples:
            help_message += "\nExamples:\n"
            for example in self.fab_examples:
                if "#" in example:
                    # Grey color
                    help_message += f"  \033[38;5;243m{example}\033[0m\n"
                else:
                    help_message += f"  {example}\n"

        # Add learn more
        if self.fab_learnmore:
            help_message += "\nLearn more:\n"
            if self.fab_learnmore != ["_"]:
                for learn_more in self.fab_learnmore:
                    help_message += f"  {learn_more}\n"
            help_message += "  For more usage examples, see https://aka.ms/fabric-cli\n"

        return help_message + "\n"


class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(
        self, *args, fab_examples=None, fab_aliases=None, fab_learnmore=None, **kwargs
    ):
        kwargs["formatter_class"] = lambda prog: CustomHelpFormatter(
            prog,
            fab_examples=fab_examples,
            fab_aliases=fab_aliases,
            fab_learnmore=fab_learnmore,
        )
        super().__init__(*args, **kwargs)
        # Add custom help flags
        self.add_argument("-help", action="help")
        self.fab_mode = fab_constant.FAB_MODE_COMMANDLINE
        self.fab_examples = fab_examples or []
        self.fab_aliases = fab_aliases or []

    def print_help(self, file=None):
        command_name = self.prog.split()[-1]

        help_functions = {
            "acl": lambda: acls_parser.show_help(None),
            "job": lambda: jobs_parser.show_help(None),
            "label": lambda: labels_parser.show_help(None),
            "table": lambda: tables_parser.show_help(None),
            "auth": lambda: auth_parser.show_help(None),
            "config": lambda: config_parser.show_help(None),
            "fab": lambda: utils_ui.display_help(commands),
        }

        if command_name in help_functions:
            help_functions[command_name]()
        else:
            super().print_help(file)

    def set_mode(self, mode):
        self.fab_mode = mode

    def get_mode(self):
        return self.fab_mode

    def error(self, message):
        if "invalid choice" in message:
            utils_error_parser.invalid_choice(self, message)
        elif "unrecognized arguments" in message:
            utils_error_parser.unrecognized_arguments(message)
        elif "the following arguments are required" in message:
            utils_error_parser.missing_required_arguments(message)
        else:
            # Add more custom error parsers here
            fab_logger.log_warning(message)

        if self.fab_mode == fab_constant.FAB_MODE_COMMANDLINE:
            sys.exit(2)


class InteractiveCLI:
    def __init__(self, parser, subparsers):
        self.parser = parser
        self.parser.set_mode(fab_constant.FAB_MODE_INTERACTIVE)
        self.subparsers = subparsers
        self.history = InMemoryHistory()
        self.session = PromptSession(history=self.history)
        self.custom_style = Style(
            [
                ("prompt", "fg:#49C5B1"),  # Prompt color, original #49C5B1
                ("context", "fg:#017864"),  # Context color, original #017864
                ("detail", "fg:grey"),
                ("input", "fg:white"),  # Input color
            ]
        )

    def handle_command(self, command):
        """Process the user command."""
        _print_log_file_path()

        command_parts = command.strip().split()  # Split the command into parts

        # Handle special commands first
        if command in ["quit", "q", "exit"]:
            utils_ui.print("Exiting interactive mode. Goodbye!")
            return True
        elif command in ["help", "h", "fab", "-h", "--help"]:
            utils_ui.display_help(commands, "Usage: <command> <subcommand> [flags]")
            return False  # Do not exit
        elif command in ["version", "v", "-v", "--version"]:
            _print_version()
            return False

        # Interactive mode
        self.parser.set_mode(fab_constant.FAB_MODE_INTERACTIVE)

        # Now check for subcommands
        if command_parts:  # Only if there's something to process
            subcommand_name = command_parts[0]
            if subcommand_name in self.subparsers.choices:
                subparser = self.subparsers.choices[subcommand_name]

                try:
                    subparser_args = subparser.parse_args(command_parts[1:])
                    subparser_args.command = subcommand_name
                    subparser_args.fab_mode = fab_constant.FAB_MODE_INTERACTIVE
                    subparser_args.command_path = Command.get_command_path(
                        subparser_args
                    )

                    if not command_parts[1:]:
                        subparser_args.func(subparser_args)
                    elif hasattr(subparser_args, "func"):
                        subparser_args.func(subparser_args)
                    else:
                        utils_ui.print(
                            f"No function associated with the command: {command.strip()}"
                        )
                except SystemExit as e:
                    # Catch SystemExit raised by ArgumentParser and prevent exiting
                    # print(f"Error: {e}\n")  # Optionally show the error message
                    # subparser.print_help()  # Print the help for the subparser
                    return
            else:
                self.parser.error(f"invalid choice: '{command.strip()}'")

        return False

    def start_interactive(self):
        """Start the interactive mode using prompt_toolkit for input."""
        utils_ui.print("\nWelcome to the Fabric CLI ⚡")
        utils_ui.print("Type 'help' for help. \n")

        while True:
            try:
                context = Context().context
                pwd_context = f"/{context.path.strip('/')}"

                prompt_text = HTML(
                    f"<prompt>fab</prompt><detail>:</detail><context>{html.escape(pwd_context)}</context><detail>$</detail> "
                )

                user_input = self.session.prompt(
                    prompt_text,
                    style=self.custom_style,
                    cursor=CursorShape.BLINKING_BEAM,
                    enable_history_search=True,
                )
                # TODO review history fab > help > quit > fab
                # self.history.append_string(user_input)  # Explicitly add the command to history
                should_exit = self.handle_command(user_input)
                if should_exit:  # Check if the command was to exit
                    break

            except (EOFError, KeyboardInterrupt):
                utils_ui.print("\nExiting interactive mode. Goodbye!")
                break


def main():
    parser = CustomArgumentParser(description="Fabric CLI")

    # -c option for command line execution
    parser.add_argument(
        "-c",
        "--command",
        action="append",  # Allow multiple -c options
        help="Run commands in non-interactive mode",
    )

    # -version and --version
    parser.add_argument("-v", "--version", action="store_true")

    subparsers = parser.add_subparsers(dest="command", required=False)

    # Custom parsers
    config_parser.register_parser(subparsers)

    # Single parsers
    fs_parser.register_ls_parser(subparsers)  # ls
    fs_parser.register_mkdir_parser(subparsers)  # mkdir
    fs_parser.register_cd_parser(subparsers)  # cd
    fs_parser.register_rm_parser(subparsers)  # rm
    fs_parser.register_mv_parser(subparsers)  # mv
    fs_parser.register_cp_parser(subparsers)  # cp
    fs_parser.register_exists_parser(subparsers)  # exists
    fs_parser.register_pwd_parser(subparsers)  # pwd
    fs_parser.register_open_parser(subparsers)  # open
    fs_parser.register_export_parser(subparsers)  # export
    fs_parser.register_import_parser(subparsers)  # import
    fs_parser.register_set_parser(subparsers)  # set
    fs_parser.register_get_parser(subparsers)  # get
    fs_parser.register_clear_parser(subparsers)  # clear
    fs_parser.register_ln_parser(subparsers)  # ln
    fs_parser.register_start_parser(subparsers)  # start
    fs_parser.register_stop_parser(subparsers)  # stop
    fs_parser.register_assign_parser(subparsers)  # assign
    fs_parser.register_unassign_parser(subparsers)  # unassign

    jobs_parser.register_parser(subparsers)  # jobs
    tables_parser.register_parser(subparsers)  # tables
    acls_parser.register_parser(subparsers)  # acls
    labels_parser.register_parser(subparsers)  # labels

    api_parser.register_parser(subparsers)  # api
    auth_parser.register_parser(subparsers)  # auth
    describe_parser.register_parser(subparsers)  # desc
    extension_parser.register_parser(subparsers)  # extension

    # version
    version_parser = subparsers.add_parser("version")
    version_parser.set_defaults(func=_print_version)

    args = parser.parse_args()

    try:

        if args.command == "auth" and args.auth_command == None:
            auth_parser.show_help(args)
            return

        if args.command == "auth" and args.auth_command == "login":
            if login.init(args):
                if (
                    fab_state_config.get_config(fab_constant.FAB_MODE)
                    == fab_constant.FAB_MODE_INTERACTIVE
                ):
                    # Initialize InteractiveCLI
                    interactive_cli = InteractiveCLI(parser, subparsers)
                    try:
                        interactive_cli.start_interactive()
                    except (KeyboardInterrupt, EOFError):
                        utils_ui.print(
                            "\nInteractive mode cancelled. Returning to previous menu."
                        )

        if args.command == "auth" and args.auth_command == "logout":
            login.logout(args)
            return

        if args.command == "auth" and args.auth_command == "status":
            login.status(args)
            return

        last_exit_code = fab_constant.EXIT_CODE_SUCCESS
        if args.command:
            if args.command not in ["auth"]:
                _print_log_file_path()
                parser.set_mode(fab_constant.FAB_MODE_COMMANDLINE)

                # Non-intective mode with multi -c option
                if isinstance(args.command, list):
                    commands_execs = 0
                    for index, command in enumerate(args.command):
                        command_parts = command.strip().split()
                        subparser = subparsers.choices[command_parts[0]]
                        subparser_args = subparser.parse_args(command_parts[1:])
                        subparser_args.command = command_parts[0]
                        last_exit_code = _execute_command(
                            subparser_args, subparsers, parser
                        )
                        commands_execs += 1
                        if index != len(args.command) - 1:
                            utils_ui.print_grey("------------------------------")
                    if commands_execs > 1:
                        utils_ui.print("\n")
                        utils_ui.print_done(f"{len(args.command)} commands executed.")

                # Non-interactive mode without -c
                else:
                    last_exit_code = _execute_command(args, subparsers, parser)

                if last_exit_code:
                    sys.exit(last_exit_code)
                else:
                    sys.exit(fab_constant.EXIT_CODE_SUCCESS)

        elif args.version:
            _print_version()
        else:
            # Display help if "fab"
            utils_ui.display_help(commands)

    except KeyboardInterrupt:
        utils_ui.print_error("Operation cancelled")
        sys.exit(fab_constant.EXIT_CODE_CANCELLED_OR_MISUSE_BUILTINS)
    except Exception as e:
        utils_ui.print_error(str(e))
        sys.exit(fab_constant.EXIT_CODE_ERROR)


def _execute_command(args, subparsers, parser):
    if args.command in subparsers.choices:
        subparser_args = args
        subparser_args.command = args.command
        subparser_args.fab_mode = parser.get_mode()
        subparser_args.command_path = Command.get_command_path(subparser_args)

        if hasattr(subparser_args, "func"):
            return subparser_args.func(subparser_args)
        else:
            return None
    else:
        parser.error(f"invalid choice: '{args.command.strip()}'")
        return None


def _print_version(args=None):
    utils_ui.print(f"fab version {__version__} (07-2025)")
    utils_ui.print("https://aka.ms/fabric-cli/release-notes")


def _print_log_file_path():
    if fab_state_config.get_config(fab_constant.FAB_DEBUG_ENABLED) == "true":
        log_file_path = fab_logger.get_log_file_path()
        fab_logger.log_warning(f"'debug_enabled' is on ({log_file_path})\n")


if __name__ == "__main__":
    main()
