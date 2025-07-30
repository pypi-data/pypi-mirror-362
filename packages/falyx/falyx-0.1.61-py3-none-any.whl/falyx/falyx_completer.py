from collections import Counter
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from typing import Iterable, Set, Optional
import shlex

from falyx.command import Command
from falyx.parser.command_argument_parser import CommandArgumentParser
from falyx.parser.argument import Argument
from falyx.parser.argument_action import ArgumentAction

class FalyxCompleter(Completer):
    """Completer for Falyx commands and their arguments."""
    def __init__(self, falyx: "Falyx"):
        self.falyx = falyx
        self._used_args: Set[str] = set()
        self._used_args_counter: Counter = Counter()

    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        text = document.text_before_cursor
        try:
            tokens = shlex.split(text)
            cursor_at_end_of_token = document.text_before_cursor.endswith((' ', '\t'))
        except ValueError:
            return

        if not tokens or (len(tokens) == 1 and not cursor_at_end_of_token):
            # Suggest command keys and aliases
            yield from self._suggest_commands(tokens[0] if tokens else "")
            return

        command = self._match_command(tokens[0])
        if not command:
            return

        if command.arg_parser is None:
            return

        self._set_used_args(tokens, command)

        next_arg = self._next_expected_argument(tokens, command.arg_parser)

        if next_arg:
            # Positional arguments or required flagged arguments
            yield from self._suggest_argument(next_arg, document)
        else:
            # Optional arguments
            for arg in command.arg_parser._keyword.values():
                if not self._arg_already_used(arg.dest):
                    yield from self._suggest_argument(arg, document)

    def _set_used_args(self, tokens: list[str], command: Command) -> None:
        """Extracts used argument flags from the provided tokens."""
        if not command.arg_parser:
            return
        self._used_args.clear()
        self._used_args_counter.clear()
        for token in tokens[1:]:
            if token.startswith('-'):
                if keyword_argument := command.arg_parser._keyword.get(token):
                    self._used_args_counter[keyword_argument.dest] += 1
                    if isinstance(keyword_argument.nargs, int) and self._used_args_counter[keyword_argument.dest] > keyword_argument.nargs:
                        continue
                    elif isinstance(keyword_argument.nargs, str) and keyword_argument.nargs in ("?"):
                        self._used_args.add(keyword_argument.dest)
                    else:
                        self._used_args.add(keyword_argument.dest)
            else:
                # Handle positional arguments
                if command.arg_parser._positional:
                    for arg in command.arg_parser._positional.values():
                        if arg.dest not in self._used_args:
                            self._used_args.add(arg.dest)
                            break
        print(f"Used args: {self._used_args}, Counter: {self._used_args_counter}")

    def _suggest_commands(self, prefix: str) -> Iterable[Completion]:
        prefix = prefix.upper()
        seen = set()
        for cmd in self.falyx.commands.values():
            for key in [cmd.key] + cmd.aliases:
                if key.upper().startswith(prefix) and key not in seen:
                    yield Completion(key, start_position=-len(prefix))
                    seen.add(key)

    def _match_command(self, token: str) -> Optional[Command]:
        token = token.lstrip("?").upper()
        return self.falyx._name_map.get(token)

    def _next_expected_argument(
        self, tokens: list[str], parser: CommandArgumentParser
    ) -> Optional[Argument]:
        """Determine the next expected argument based on the current tokens."""
        # Positional arguments first
        for arg in parser._positional.values():
            if arg.dest not in self._used_args:
                return arg

        # Then required keyword arguments
        for arg in parser._keyword_list:
            if arg.required and not self._arg_already_used(arg.dest):
                return arg

        return None

    def _arg_already_used(self, dest: str) -> bool:
        print(f"Checking if argument '{dest}' is already used: {dest in self._used_args} - Used args: {self._used_args}")
        return dest in self._used_args

    def _suggest_argument(self, arg: Argument, document: Document) -> Iterable[Completion]:
        if not arg.positional:
            for flag in arg.flags:
                yield Completion(flag, start_position=0)

        if arg.choices:
            for choice in arg.choices:
                yield Completion(
                    choice,
                    start_position=0,
                    display=f"{arg.dest}={choice}"
                )

        if arg.default is not None and arg.action == ArgumentAction.STORE:
            yield Completion(
                str(arg.default),
                start_position=0,
                display=f"{arg.dest} (default: {arg.default})"
            )
