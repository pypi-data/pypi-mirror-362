#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Robust input module for command-line applications.

This module provides a highly configurable and robust input routine for
command-line applications. It supports cursor movement, input validation,
type casting, password masking, and styling.

This module only uses the Python standard library and is intended for Linux usage.
"""

import re
import select
import sys
import termios
import tty
from typing import Any, Callable, Optional, Type, List

# Terminal control constants
CTRL_C = 3
ENTER = 13
ESCAPE = 27
BACKSPACE = 127
PRINTABLE_ASCII_START = 32
PRINTABLE_ASCII_END = 126

# Timeout constants
SELECT_TIMEOUT = 0.1  # Timeout for select operations in seconds


class InputStyle:
    """Comprehensive ANSI styling options for input prompts and text."""

    # === RESET ===
    RESET = "\033[0m"

    # === TEXT ATTRIBUTES ===
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    SLOW_BLINK = "\033[5m"
    RAPID_BLINK = "\033[6m"
    INVERTED = "\033[7m"
    CONCEAL = "\033[8m"
    STRIKETHROUGH = "\033[9m"

    # === RESET SPECIFIC ATTRIBUTES ===
    RESET_BOLD = "\033[22m"
    RESET_DIM = "\033[22m"
    RESET_ITALIC = "\033[23m"
    RESET_UNDERLINE = "\033[24m"
    RESET_BLINK = "\033[25m"
    RESET_REVERSE = "\033[27m"
    RESET_CONCEAL = "\033[28m"
    RESET_STRIKETHROUGH = "\033[29m"

    # === STANDARD FOREGROUND COLORS (30-37) ===
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    DEFAULT_FG = "\033[39m"

    # === STANDARD BACKGROUND COLORS (40-47) ===
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    DEFAULT_BG = "\033[49m"

    # === BRIGHT FOREGROUND COLORS (90-97) ===
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # === BRIGHT BACKGROUND COLORS (100-107) ===
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"

    # === LESS COMMON FONT STYLES ===
    PRIMARY_FONT = "\033[10m"
    ALT_FONT_1 = "\033[11m"
    ALT_FONT_2 = "\033[12m"
    ALT_FONT_3 = "\033[13m"
    ALT_FONT_4 = "\033[14m"
    ALT_FONT_5 = "\033[15m"
    ALT_FONT_6 = "\033[16m"
    ALT_FONT_7 = "\033[17m"
    ALT_FONT_8 = "\033[18m"
    ALT_FONT_9 = "\033[19m"
    FRAKTUR = "\033[20m"
    DOUBLE_UNDERLINE = "\033[21m"
    FRAMED = "\033[51m"
    ENCIRCLED = "\033[52m"
    OVERLINED = "\033[53m"
    NOT_FRAMED = "\033[54m"
    NOT_OVERLINED = "\033[55m"

    @staticmethod
    def apply_style(text: str, *styles: str) -> str:
        """Apply one or more styles to the given text.

        Args:
            text: The text to style.
            *styles: One or more style constants to apply.

        Returns:
            The styled text.
        """
        if not styles:
            return text

        # Use list join for more efficient string building
        parts = list(styles)
        parts.append(text)
        parts.append(InputStyle.RESET)
        return "".join(parts)

    @staticmethod
    def color_256(n: int) -> str:
        """Generate 256-color foreground color code.

        Args:
            n: Color number (0-255)

        Returns:
            ANSI escape sequence for 256-color foreground
        """
        return f"\033[38;5;{n}m"

    @staticmethod
    def bg_color_256(n: int) -> str:
        """Generate 256-color background color code.

        Args:
            n: Color number (0-255)

        Returns:
            ANSI escape sequence for 256-color background
        """
        return f"\033[48;5;{n}m"

    @staticmethod
    def rgb_color(r: int, g: int, b: int) -> str:
        """Generate RGB true color foreground code.

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            ANSI escape sequence for RGB foreground color
        """
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def rgb_bg_color(r: int, g: int, b: int) -> str:
        """Generate RGB true color background code.

        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)

        Returns:
            ANSI escape sequence for RGB background color
        """
        return f"\033[48;2;{r};{g};{b}m"


class InputValidator:
    """Validator for input values based on various constraints."""

    # Cache for compiled regex patterns to improve performance
    _pattern_cache = {}
    _MAX_CACHE_SIZE = 100

    @staticmethod
    def validate_length(
        value: str, min_length: Optional[int] = None, max_length: Optional[int] = None
    ) -> bool:
        """Validate the length of the input string.

        Args:
            value: The input string to validate.
            min_length: The minimum allowed length (inclusive).
            max_length: The maximum allowed length (inclusive).

        Returns:
            True if the length is valid, False otherwise.
        """
        if min_length is not None and len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        return True

    @staticmethod
    def validate_type(value: str, target_type: Type) -> bool:
        """Validate if the input string can be cast to the target type.

        Args:
            value: The input string to validate.
            target_type: The target type to cast to.

        Returns:
            True if the value can be cast to the target type, False otherwise.
        """
        # Check for empty string specifically, not falsy values like "0"
        if value == "" and target_type != str:
            return False

        try:
            if target_type == bool:
                # Special handling for boolean values - only validate truthy values
                # since cast_value only accepts truthy values for consistency
                return value.lower() in (
                    "true",
                    "yes",
                    "t",
                    "y",
                    "1",
                    "false",
                    "no",
                    "f",
                    "n",
                    "0",
                )
            elif target_type == int:
                int(value)
            elif target_type == float:
                float(value)
            elif target_type == str:
                # String is always valid
                pass
            else:
                # For other types, try to initialize with the string value
                target_type(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_pattern(value: str, pattern: str) -> bool:
        """Validate if the input string matches the given regex pattern.

        Args:
            value: The input string to validate.
            pattern: The regex pattern to match against.

        Returns:
            True if the value matches the pattern, False otherwise.
        """
        # Use cached compiled patterns for better performance
        if pattern not in InputValidator._pattern_cache:
            try:
                # Check cache size limit and clear oldest entries if needed
                if len(InputValidator._pattern_cache) >= InputValidator._MAX_CACHE_SIZE:
                    # Remove the oldest entries (simple FIFO strategy)
                    oldest_keys = list(InputValidator._pattern_cache.keys())[:10]
                    for key in oldest_keys:
                        del InputValidator._pattern_cache[key]

                InputValidator._pattern_cache[pattern] = re.compile(pattern)
            except re.error:
                # Invalid regex pattern
                return False

        compiled_pattern = InputValidator._pattern_cache[pattern]
        return bool(compiled_pattern.match(value))

    @staticmethod
    def validate_ip_address(value: str) -> bool:
        """Validate if the input string is a valid IP address.

        Args:
            value: The input string to validate.

        Returns:
            True if the value is a valid IP address, False otherwise.
        """
        pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        if not re.match(pattern, value):
            return False

        # Check each octet is in range 0-255 and has no leading zeros
        octets = value.split(".")
        for octet in octets:
            # Reject leading zeros (except for "0" itself)
            if len(octet) > 1 and octet[0] == "0":
                return False

            try:
                num = int(octet)
                if num < 0 or num > 255:
                    return False
            except ValueError:
                return False

        return True

    @staticmethod
    def validate_in_choices(value: str, choices: List[str]) -> bool:
        """Validate if the input string is one of the allowed choices.

        Args:
            value: The input string to validate.
            choices: List of allowed choices.

        Returns:
            True if the value is in choices, False otherwise.
        """
        return value in choices


def cast_value(value: str, target_type: Type) -> Any:
    """Cast the input string to the target type.

    Args:
        value: The input string to cast.
        target_type: The target type to cast to.

    Returns:
        The cast value.

    Raises:
        ValueError: If the value cannot be cast to the target type.
    """
    if target_type == bool:
        # Match the same values accepted by validate_type for consistency
        lower_val = value.lower()
        if lower_val in ("true", "yes", "t", "y", "1"):
            return True
        elif lower_val in ("false", "no", "f", "n", "0"):
            return False
        else:
            raise ValueError(f"Cannot convert '{value}' to boolean")
    elif target_type == int:
        return int(value)
    elif target_type == float:
        return float(value)
    elif target_type == str:
        return value
    else:
        return target_type(value)


class InputHandler:
    """Handles terminal input with cursor movement and validation."""

    def __init__(self, config: "InputConfig"):
        self.config = config
        self.buffer = []
        self.cursor_pos = 0
        self.old_settings = None

        # Pre-compile validation chain for better performance
        self._validators = self._build_validator_chain()

    def _build_validator_chain(self):
        """Build an optimized validation chain without lambda overhead."""
        validators = []

        # Add a length validator if needed
        if self.config.min_length is not None or self.config.max_length is not None:
            validators.append(
                ("length", self.config.min_length, self.config.max_length)
            )

        # Add type validator
        validators.append(("type", self.config.target_type))

        # Add pattern validator if specified
        if self.config.pattern is not None:
            validators.append(("pattern", self.config.pattern))

        # Add choice validator if specified
        if self.config.choices is not None:
            validators.append(("choices", self.config.choices))

        # Add custom validator if specified
        if self.config.custom_validator is not None:
            validators.append(("custom", self.config.custom_validator))

        return validators

    def get_input(self) -> Any:
        """Main input loop with validation."""
        # Check if we're in a proper terminal
        if not sys.stdin.isatty():
            # Fallback to simple input for non-terminal environments
            # Uses default max_attempts of 10 for non-terminal mode
            return self._simple_input(max_attempts=10)

        self.old_settings = termios.tcgetattr(sys.stdin)

        try:
            self._display_prompt()

            while True:
                char = self._read_char()

                # Skip empty chars from timeout
                if not char:
                    continue

                if ord(char) == CTRL_C:
                    raise KeyboardInterrupt
                elif ord(char) == ENTER:
                    result = self._process_enter()
                    if result is not None:
                        return result
                elif ord(char) == BACKSPACE:
                    self._process_backspace()
                elif ord(char) == ESCAPE:
                    self._process_arrow_keys()
                elif PRINTABLE_ASCII_START <= ord(char) <= PRINTABLE_ASCII_END:
                    self._process_printable_char(char)

        finally:
            if self.old_settings:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def _simple_input(self, max_attempts: Optional[int] = None) -> Any:
        """Fallback input for non-terminal environments.

        Args:
            max_attempts: Maximum number of validation attempts. None for unlimited.
        """
        attempt_count = 0
        while True:
            try:
                if max_attempts is not None:
                    attempt_count += 1
                    if attempt_count > max_attempts:
                        raise ValueError(
                            f"Maximum validation attempts ({max_attempts}) exceeded"
                        )

                raw_input = self._collect_simple_input()
                result = self._handle_simple_input_result(raw_input)
                if result is not None:
                    return result
            except (KeyboardInterrupt, EOFError) as e:
                return self._handle_simple_input_error(e)

    def _collect_simple_input(self) -> str:
        """Collect raw input based on configuration."""
        if self.config.is_password:
            import getpass

            return getpass.getpass(self.config.prompt + ": ")
        else:
            return input(self.config.styled_prompt)

    def _handle_simple_input_result(self, raw_input: str) -> Optional[Any]:
        """Process and validate the input result."""
        if not raw_input and self.config.default is not None:
            raw_input = self.config.default

        if self._validate_input(raw_input):
            return cast_value(raw_input, self.config.target_type)
        else:
            self._display_simple_error()
            return None

    def _display_simple_error(self):
        """Display an error message below input and reposition cursor."""
        # Clear any existing error text on next line and display new error
        sys.stdout.write("\033[K")  # Clear the current line first
        sys.stdout.write(
            InputStyle.apply_style(self.config.error_message, *self.config.error_style)
        )
        sys.stdout.write("\n")
        sys.stdout.flush()

        # Move the cursor up to the input line and clear the input line only
        sys.stdout.write("\033[A\033[K")  # Move up and clear the input line
        sys.stdout.flush()

    def _handle_simple_input_error(self, error: Exception) -> Any:
        """Handle input errors and exceptions."""
        if isinstance(error, KeyboardInterrupt):
            raise
        elif isinstance(error, EOFError):
            if self.config.default is not None:
                # Validate the default value before using it
                if self._validate_input(self.config.default):
                    return cast_value(self.config.default, self.config.target_type)
                else:
                    raise ValueError(
                        f"Default value '{self.config.default}' failed validation"
                    )
            raise
        else:
            raise error

    def _read_char(self) -> str:
        """Read a single character in raw mode with timeout protection."""
        try:
            tty.setraw(sys.stdin.fileno())
            # Use select with timeout to prevent indefinite blocking
            ready, _, _ = select.select([sys.stdin], [], [], SELECT_TIMEOUT)
            if ready:
                char = sys.stdin.read(1)
            else:
                char = ""
        finally:
            if self.old_settings:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

        return char

    def _display_prompt(self):
        """Display the styled prompt."""
        sys.stdout.write(self.config.styled_prompt)
        sys.stdout.flush()

    def _process_enter(self) -> Optional[Any]:
        """Process the Enter key and validate input."""
        current_input = "".join(self.buffer)

        if not current_input and self.config.default is not None:
            current_input = self.config.default

        if self._validate_input(current_input):
            # Clear any error text below before proceeding
            sys.stdout.write("\n\033[K")  # Move to the next line and clear any error
            sys.stdout.flush()
            return cast_value(current_input, self.config.target_type)
        else:
            self._display_error_and_reset()
            return None

    def _validate_input(self, input_str: str) -> bool:
        """Validate input against all constraints using pre-compiled validators."""
        if not self.config.allow_empty and not input_str:
            return False

        # Use pre-compiled validators for better performance
        for validator_spec in self._validators:
            if not InputHandler._execute_validator(input_str, validator_spec):
                return False

        return True

    @staticmethod
    def _execute_validator(input_str: str, validator_spec: tuple) -> bool:
        """Execute a single validator specification."""
        validator_type = validator_spec[0]

        if validator_type == "length":
            return InputHandler._validate_length_spec(
                input_str, validator_spec[1], validator_spec[2]
            )
        elif validator_type == "type":
            return InputValidator.validate_type(input_str, validator_spec[1])
        elif validator_type == "pattern":
            return InputValidator.validate_pattern(input_str, validator_spec[1])
        elif validator_type == "choices":
            return InputValidator.validate_in_choices(input_str, validator_spec[1])
        elif validator_type == "custom":
            return validator_spec[1](input_str)

        return True

    @staticmethod
    def _validate_length_spec(
        input_str: str, min_len: Optional[int], max_len: Optional[int]
    ) -> bool:
        """Validate length constraint for the input string."""
        return InputValidator.validate_length(input_str, min_len, max_len)

    def _display_error_and_reset(self):
        """Display an error message below input and reposition cursor."""
        # Move to the next line and clear any existing error text
        sys.stdout.write("\n\033[K")  # Move down and clear the line

        # Display error message
        sys.stdout.write(
            InputStyle.apply_style(self.config.error_message, *self.config.error_style)
        )
        sys.stdout.flush()

        # Move the cursor back up to input line and clear input line only
        sys.stdout.write("\033[A")  # Move up one line
        sys.stdout.write("\r\033[K")  # Clear input line

        # Redisplay the prompt at the same position
        sys.stdout.write(self.config.styled_prompt)

        self.buffer = []
        self.cursor_pos = 0
        sys.stdout.flush()

    def _process_backspace(self):
        """Process backspace key."""
        if self.cursor_pos > 0:
            self.buffer.pop(self.cursor_pos - 1)
            self.cursor_pos -= 1

            sys.stdout.write("\b \b")

            if self.cursor_pos < len(self.buffer):
                self._redraw_from_cursor()

            sys.stdout.flush()

    def _process_arrow_keys(self):
        """Process arrow key sequences with timeout protection."""
        try:
            # Read an escape sequence with timeout protection
            ready, _, _ = select.select([sys.stdin], [], [], SELECT_TIMEOUT)
            if not ready:
                return
            next1 = sys.stdin.read(1)

            ready, _, _ = select.select([sys.stdin], [], [], SELECT_TIMEOUT)
            if not ready:
                return
            next2 = sys.stdin.read(1)

            if next1 == "[":
                if next2 == "D" and self.cursor_pos > 0:  # Left arrow
                    self.cursor_pos -= 1
                    sys.stdout.write("\033[D")
                    sys.stdout.flush()
                elif next2 == "C" and self.cursor_pos < len(self.buffer):  # Right arrow
                    self.cursor_pos += 1
                    sys.stdout.write("\033[C")
                    sys.stdout.flush()
                elif next2 == "H":  # Home key
                    self._move_to_start()
                elif next2 == "F":  # End key
                    self._move_to_end()
                elif next2.isdigit():  # Handle multi-character sequences like 1~ or 4~
                    self._handle_extended_keys(next2)
        except (OSError, IOError):
            # Ignore malformed escape sequences
            pass

    def _move_to_start(self):
        """Move the cursor to the beginning of the input."""
        if self.cursor_pos > 0:
            # Move cursor to start of input
            sys.stdout.write(f"\033[{self.cursor_pos}D")
            self.cursor_pos = 0
            sys.stdout.flush()

    def _move_to_end(self):
        """Move the cursor to the end of the input."""
        if self.cursor_pos < len(self.buffer):
            # Move the cursor to the end of the input
            moves_needed = len(self.buffer) - self.cursor_pos
            sys.stdout.write(f"\033[{moves_needed}C")
            self.cursor_pos = len(self.buffer)
            sys.stdout.flush()

    def _handle_extended_keys(self, digit: str):
        """Handle extended key sequences like 1~ (Home) and 4~ (End)."""
        try:
            # Read the final character of the sequence
            ready, _, _ = select.select([sys.stdin], [], [], SELECT_TIMEOUT)
            if not ready:
                return
            final_char = sys.stdin.read(1)

            if final_char == "~":
                if digit == "1":  # Home key (\033[1~)
                    self._move_to_start()
                elif digit == "4":  # End key (\033[4~)
                    self._move_to_end()
                # Other extended keys like 2~ (Insert), 3~ (Delete), etc. can be added here
        except (OSError, IOError):
            # Ignore malformed sequences
            pass

    def _process_printable_char(self, char: str):
        """Process printable character input with optimized redrawing."""
        if (
            self.config.max_length is not None
            and len(self.buffer) >= self.config.max_length
        ):
            return

        # Insert character into the buffer
        self.buffer.insert(self.cursor_pos, char)

        # Check if we're inserting at the end (the most common case)
        is_append = self.cursor_pos == len(self.buffer) - 1
        self.cursor_pos += 1

        if is_append:
            # Optimize for appending - just display the character
            self._display_char(char)
        else:
            # Insert in the middle-need to redraw efficiently
            self._display_char(char)
            self._redraw_from_cursor_optimized()

        sys.stdout.flush()

    def _display_char(self, char: str):
        """Display a single character with appropriate styling."""
        if self.config.is_password:
            sys.stdout.write("*")
        else:
            sys.stdout.write(InputStyle.apply_style(char, *self.config.input_style))

    def _redraw_from_cursor(self):
        """Redraw buffer content from the cursor position."""
        sys.stdout.write("\033[K")  # Clear line from the cursor

        remaining_chars = "".join(self.buffer[self.cursor_pos :])
        if self.config.is_password:
            sys.stdout.write("*" * len(remaining_chars))
        else:
            sys.stdout.write(
                InputStyle.apply_style(remaining_chars, *self.config.input_style)
            )

        if remaining_chars:
            sys.stdout.write(f"\033[{len(remaining_chars)}D")  # Move cursor back

    def _redraw_from_cursor_optimized(self):
        """Optimized redraw that minimizes string operations."""
        # Only redraw if there are characters after the cursor
        remaining_count = len(self.buffer) - self.cursor_pos
        if remaining_count <= 0:
            return

        # Clear line from the cursor and redraw remaining characters
        sys.stdout.write("\033[K")

        if self.config.is_password:
            # For passwords, just write asterisks - no styling needed
            sys.stdout.write("*" * remaining_count)
        else:
            # Build styled output more efficiently
            if self.config.input_style:
                style_prefix = "".join(self.config.input_style)
                # Write each character with minimal styling overhead
                for i in range(self.cursor_pos, len(self.buffer)):
                    sys.stdout.write(style_prefix + self.buffer[i] + InputStyle.RESET)
            else:
                # No styling - direct write
                for char in self.buffer[self.cursor_pos :]:
                    sys.stdout.write(char)

        # Move cursor back to correct position
        if remaining_count > 0:
            sys.stdout.write(f"\033[{remaining_count}D")


class InputConfig:
    """Configuration for input handling."""

    def __init__(
        self,
        prompt: str,
        default: Optional[str] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        allow_empty: bool = True,
        target_type: Type = str,
        pattern: Optional[str] = None,
        choices: Optional[List[str]] = None,
        is_password: bool = False,
        prompt_style: Optional[List[str]] = None,
        input_style: Optional[List[str]] = None,
        error_message: Optional[str] = None,
        error_style: Optional[List[str]] = None,
        custom_validator: Optional[Callable[[str], bool]] = None,
    ):
        self.prompt = prompt
        self.default = default
        self.min_length = min_length
        self.max_length = max_length
        self.allow_empty = allow_empty
        self.target_type = target_type
        self.pattern = pattern
        self.choices = choices
        self.is_password = is_password
        self.custom_validator = custom_validator

        # Set default styles
        self.prompt_style = prompt_style or [InputStyle.GREEN]
        self.input_style = input_style or [InputStyle.CYAN]
        self.error_style = error_style or [InputStyle.RED]

        # Validate configuration parameters after styles are set
        self._validate_config()

        # Set default error message
        self.error_message = error_message or "Invalid input. Please try again."

        # Generate styled prompt
        display_prompt = prompt
        if default is not None:
            display_prompt += f" [{default}]"
        display_prompt += ": "
        self.styled_prompt = InputStyle.apply_style(display_prompt, *self.prompt_style)

    def _validate_config(self):
        """Validate configuration parameters for consistency and safety."""
        self._validate_length_constraints()
        self._validate_choices()
        self._validate_regex_pattern()
        self._validate_target_type()
        self._validate_prompt()
        self._validate_custom_validator()
        self._validate_style_lists()

    def _validate_length_constraints(self):
        """Validate length constraint parameters."""
        if self.min_length is not None and self.min_length < 0:
            raise ValueError("min_length cannot be negative")
        if self.max_length is not None and self.max_length < 0:
            raise ValueError("max_length cannot be negative")
        if (
            self.min_length is not None
            and self.max_length is not None
            and self.min_length > self.max_length
        ):
            raise ValueError("min_length cannot be greater than max_length")

    def _validate_choices(self):
        """Validate choices list parameter."""
        if self.choices is not None:
            if not isinstance(self.choices, list) or len(self.choices) == 0:
                raise ValueError("choices must be a non-empty list")
            if not all(isinstance(choice, str) for choice in self.choices):
                raise ValueError("all choices must be strings")

    def _validate_regex_pattern(self):
        """Validate regex pattern parameter."""
        if self.pattern is not None:
            try:
                re.compile(self.pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}")

    def _validate_target_type(self):
        """Validate target type parameter."""
        if not isinstance(self.target_type, type):
            raise ValueError("target_type must be a valid type")

    def _validate_prompt(self):
        """Validate prompt parameter."""
        if not self.prompt or not isinstance(self.prompt, str):
            raise ValueError("prompt must be a non-empty string")

    def _validate_custom_validator(self):
        """Validate custom validator parameter."""
        if self.custom_validator is not None and not callable(self.custom_validator):
            raise ValueError("custom_validator must be callable")

    def _validate_style_lists(self):
        """Validate style list parameters."""
        for style_name, style_list in [
            ("prompt_style", self.prompt_style),
            ("input_style", self.input_style),
            ("error_style", self.error_style),
        ]:
            if style_list and not all(isinstance(s, str) for s in style_list):
                raise ValueError(f"{style_name} must contain only strings")


def get_input(
    prompt: str,
    default: Optional[str] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_empty: bool = True,
    target_type: Type = str,
    pattern: Optional[str] = None,
    choices: Optional[List[str]] = None,
    is_password: bool = False,
    prompt_style: Optional[List[str]] = None,
    input_style: Optional[List[str]] = None,
    error_message: Optional[str] = None,
    error_style: Optional[List[str]] = None,
    custom_validator: Optional[Callable[[str], bool]] = None,
) -> Any:
    """Get user input with robust validation and formatting.

    This function provides a comprehensive input routine that supports cursor
    movement, input validation, type casting, password masking, and styling.

    Args:
        prompt: The prompt to display to the user.
        default: The default value to use if the user presses Enter without an input.
        min_length: The minimum allowed length for the input.
        max_length: The maximum allowed length for the input.
        allow_empty: Whether to allow empty input. If False and the default is None,
                    the user must enter a value.
        target_type: The type to cast the input to.
        pattern: A regex pattern that the input must match.
        choices: A list of allowed values for the input.
        is_password: Whether to mask the input (display asterisks).
        prompt_style: A list of style constants to apply to the prompt.
        input_style: A list of style constants to apply to the input.
        error_message: Custom error message to display for invalid input.
        error_style: A list of style constants to apply to the error message.
        custom_validator: A custom validation function that takes the input
                        string and returns a boolean indicating validity.

    Returns:
        The validated and cast input value.
    """
    config = InputConfig(
        prompt=prompt,
        default=default,
        min_length=min_length,
        max_length=max_length,
        allow_empty=allow_empty,
        target_type=target_type,
        pattern=pattern,
        choices=choices,
        is_password=is_password,
        prompt_style=prompt_style,
        input_style=input_style,
        error_message=error_message,
        error_style=error_style,
        custom_validator=custom_validator,
    )

    handler = InputHandler(config)
    return handler.get_input()


def get_password(
    prompt: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_empty: bool = False,
    pattern: Optional[str] = None,
    prompt_style: Optional[List[str]] = None,
    error_message: Optional[str] = None,
    custom_validator: Optional[Callable[[str], bool]] = None,
) -> str:
    """Get a password from the user with masking.

    This is a convenience wrapper around get_input for password input.

    Args:
        prompt: The prompt to display to the user.
        min_length: The minimum allowed length for the password.
        max_length: The maximum allowed length for the password.
        allow_empty: Whether to allow empty password.
        pattern: A regex pattern that the password must match.
        prompt_style: A list of style constants to apply to the prompt.
        error_message: Custom error message to display for invalid input.
        custom_validator: A custom validation function that takes the input
            string and returns a boolean indicating validity.

    Returns:
        The validated password string.
    """
    if error_message is None:
        error_message = "Invalid password. Please try again."

    return get_input(
        prompt=prompt,
        min_length=min_length,
        max_length=max_length,
        allow_empty=allow_empty,
        target_type=str,
        pattern=pattern,
        is_password=True,
        prompt_style=prompt_style,
        error_message=error_message,
        custom_validator=custom_validator,
    )


def get_integer(
    prompt: str,
    default: Optional[int] = None,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    allow_empty: bool = False,
    prompt_style: Optional[List[str]] = None,
    input_style: Optional[List[str]] = None,
    error_message: Optional[str] = None,
) -> int:
    """Get an integer from the user.

    This is a convenience wrapper around get_input for integer input.

    Args:
        prompt: The prompt to display to the user.
        default: The default value to use if the user presses Enter without an input.
        min_value: The minimum allowed value (inclusive).
        max_value: The maximum allowed value (inclusive).
        allow_empty: Whether to allow empty input.
        prompt_style: A list of style constants to apply to the prompt.
        input_style: A list of style constants to apply to the input.
        error_message: Custom error message to display for invalid input.

    Returns:
        The validated integer value.
    """
    if error_message is None:
        constraints = []
        if min_value is not None:
            constraints.append(f"minimum: {min_value}")
        if max_value is not None:
            constraints.append(f"maximum: {max_value}")

        if constraints:
            error_message = f"Please enter a valid integer ({', '.join(constraints)})."
        else:
            error_message = "Please enter a valid integer."

    # Custom validator for min/max constraints
    def validate_range(value: str) -> bool:
        try:
            num = int(value)
            if min_value is not None and num < min_value:
                return False
            if max_value is not None and num > max_value:
                return False
            return True
        except ValueError:
            return False

    return get_input(
        prompt=prompt,
        default=str(default) if default is not None else None,
        allow_empty=allow_empty,
        target_type=int,
        prompt_style=prompt_style,
        input_style=input_style,
        error_message=error_message,
        custom_validator=validate_range,
    )


def get_choice(
    prompt: str,
    choices: List[str],
    default: Optional[str] = None,
    allow_empty: bool = False,
    prompt_style: Optional[List[str]] = None,
    input_style: Optional[List[str]] = None,
    error_message: Optional[str] = None,
) -> str:
    """Get a choice from a list of options.

    This is a convenience wrapper around get_input for choice selection.

    Args:
        prompt: The prompt to display to the user.
        choices: A list of allowed values for the input.
        default: The default value to use if the user presses Enter without an input.
        allow_empty: Whether to allow empty input.
        prompt_style: A list of style constants to apply to the prompt.
        input_style: A list of style constants to apply to the input.
        error_message: Custom error message to display for invalid input.

    Returns:
        The selected choice.
    """
    if error_message is None:
        error_message = f"Please enter one of: {', '.join(choices)}."

    return get_input(
        prompt=prompt,
        default=default,
        allow_empty=allow_empty,
        target_type=str,
        choices=choices,
        prompt_style=prompt_style,
        input_style=input_style,
        error_message=error_message,
    )


def get_ip_address(
    prompt: str,
    default: Optional[str] = None,
    allow_empty: bool = False,
    prompt_style: Optional[List[str]] = None,
    input_style: Optional[List[str]] = None,
    error_message: Optional[str] = None,
) -> str:
    """Get a valid IP address from the user.

    This is a convenience wrapper around get_input for IP address input.

    Args:
        prompt: The prompt to display to the user.
        default: The default value to use if the user presses Enter without an input.
        allow_empty: Whether to allow empty input.
        prompt_style: A list of style constants to apply to the prompt.
        input_style: A list of style constants to apply to the input.
        error_message: Custom error message to display for invalid input.

    Returns:
        The validated IP address.
    """
    if error_message is None:
        error_message = "Please enter a valid IP address (e.g., 192.168.1.1)."

    return get_input(
        prompt=prompt,
        default=default,
        allow_empty=allow_empty,
        target_type=str,
        prompt_style=prompt_style,
        input_style=input_style,
        error_message=error_message,
        custom_validator=InputValidator.validate_ip_address,
    )
