subcommands_options: dict[str, dict[str, type]] = {
    "choose": {
        "ordered": bool,  # False
        "height": int,  # 10
        "cursor": str,  # "> "
        "no_show_help": bool,
        "show_help": bool,
        "timeout": str,  # "0s"
        "header": str,  # "Choose:"
        "cursor_prefix": str,  # "• "
        "selected_prefix": str,  # "✓ "
        "unselected_prefix": str,  # "• "
        "selected": str,  # ",..."
        "input_delimiter": str,  # "\\n"
        "output_delimiter": str,  # "\\n"
        "label_delimiter": str,  # ""
        "no_strip_ansi": bool,  # False
        "strip_ansi": bool,  # False
        "limit": int,  # 1
        "no_limit": bool,  # False
        "select_if_one": bool,  # False
        "cursor_foreground": str,  # "212"
        "cursor_background": str,  # ""
        "header_foreground": str,  # "99"
        "header_background": str,  # ""
        "item_foreground": str,  # ""
        "item_background": str,  # ""
        "selected_foreground": str,  # "212"
        "selected_background": str,  # ""
    },
    "confirm": {
        "default": bool,
        "show_output": bool,
        "affirmative": str,
        "negative": str,
        "no_show_help": bool,
        "show_help": bool,
        "timeout": str,
        "prompt_foreground": str,  # "#7571F9"
        "prompt_background": str,  # ""
        "selected_foreground": str,  # "230"
        "selected_background": str,  # "212"
        "unselected_foreground": str,  # "254"
        "unselected_background": str,  # "235"
    },
    "file": {
        "cursor": str,  # ">"
        "all": bool,
        "no_permissions": bool,
        "permissions": bool,
        "no_size": bool,
        "size": bool,
        "file": str,
        "directory": str,
        "no_show_help": bool,
        "show_help": bool,
        "timeout": str,  # "0s"
        "header": str,  # ""
        "height": int,  # 10
        "cursor_foreground": str,  # "212"
        "cursor_background": str,  # ""
        "symlink_foreground": str,  # "36"
        "symlink_background": str,  # ""
        "directory_foreground": str,  # "99"
        "directory_background": str,  # ""
        "file_foreground": str,  # ""
        "file_background": str,  # ""
        "permissions_foreground": str,  # "242"
        "permissions_background": str,  # ""
        "selected_foreground": str,  # "212"
        "selected_background": str,  # ""
        "file_size_foreground": str,  # "240"
        "file_size_background": str,  # ""
        "header_foreground": str,  # 99
        "header_background": str,  # ""
    },
    "filter": {
        # flags
        "indicator": str,
        "selected": str,
        "no_show_help": bool,
        "show_help": bool,
        "selected_prefix": str,
        "unselected_prefix": str,
        "header": str,
        "placeholder": str,
        "prompt": str,
        "width": int,
        "height": int,
        "value": str,
        "reverse": bool,
        "no_fuzzy": bool,
        "fuzzy": bool,
        "no_fuzzy_sort": bool,
        "fuzzy_sort": bool,
        "timeout": str,
        "input_delimiter": str,
        "output_delimiter": str,
        "no_strip_ansi": bool,
        "strip_ansi": bool,
        # Style flags
        "indicator_foreground": str,
        "indicator_background": str,
        "selected_indicator_foreground": str,
        "selected_indicator_background": str,
        "unselected_prefix_foreground": str,
        "unselected_prefix_background": str,
        "header_foreground": str,
        "header_background": str,
        "text_foreground": str,
        "text_background": str,
        "cursor_text_foreground": str,
        "cursor_text_background": str,
        "match_foreground": str,
        "match_background": str,
        "prompt_foreground": str,
        "prompt_background": str,
        "placeholder_foreground": str,
        "placeholder_background": str,
        # Selection
        "limit": int,
        "no_limit": bool,
        "select_if_one": bool,
        "no_strict": bool,
        "strict": bool,
    },
    "format": {
        "theme": str,  # pink
        "language": str,  # ""
        "no_strip_ansi": bool,
        "strip_ansi": bool,
        "type": str,  # "markdown"
    },
    "input": {
        "placeholder": str,  #  "Type something_.."
        "prompt": str,  # "> "
        "cursor_mode": str,  # "blink"
        "value": str,  # ""
        "char_limit": int,  # 400
        "width": int,  # 0
        "password": bool,
        "no_show_help": bool,
        "show_help": bool,
        "header": str,  # ""
        "timeout": str,  # "0s"
        "no_strip_ansi": bool,
        "strip_ansi": bool,
        "prompt_foreground": str,  # ""
        "prompt_background": str,  # ""
        "placeholder_foreground": str,  # "240"
        "placeholder_background": str,  # ""
        "cursor_foreground": str,  # "212"
        "cursor_background": str,  # ""
        "header_foreground": str,  # "240"
        "header_background": str,  # ""
    },
    "join": {
        "align": str,  # "left"
        "horizontal": bool,
        "vertical": bool,
    },
    "pager": {
        "show_line_numbers": bool,
        "no_soft_wrap": bool,
        "soft_wrap": bool,
        "timeout": str,  # "0s"
        "foreground": str,  # ""
        "background": str,  # ""
        "line_number_foreground": str,  # "237"
        "line_number_background": str,  # ""
        "match_foreground": str,  # "212"
        "match_background": str,  # ""
        "match_highlight_foreground": str,  # "235"
        "match_highlight_background": str,  # "225"
        "help_foreground": str,  # "241"
        "help_background": str,
    },
    "spin": {
        "show_output": bool,
        "show_error": bool,
        "show_stdout": bool,
        "show_stderr": bool,
        "spinner": str,  # "dot"
        "title": str,  # "Loading..."
        "align": str,  # "left"
        "timeout": str,  # "0s"
        "spinner_foreground": str,
        "spinner_background": str,
        "title_forground": str,
        "title_background": str,
    },
    "style": {
        "trim": bool,
        "no_strip_ansi": bool,
        "strip_ansi": bool,
        "foreground": str,
        "background": str,
        "border": str,
        "border_background": str,
        "border_foreground": str,
        "align": str,
        "height": int,
        "width": int,
        "margin": str,
        "padding": str,
        "bold": bool,
        "faint": bool,
        "italic": bool,
        "strikethrough": bool,
        "underline": bool,
    },
    "table": {
        "separator": str,  # ","
        "columns": str,
        "widths": str,
        "height": int,  # 0
        "print": bool,
        "file": str,  # ""
        "border": str,  # "rounded"
        "no_show_help": bool,
        "show_help": bool,
        "no_hide_count": bool,
        "hide_count": bool,
        "lazy_quotes": bool,
        "fields_per_record": int,  # 0
        "return_column": int,  # 0
        "timeout": str,  # "0s"
        "border_foreground": str,  # ""
        "border_background": str,  # ""
        "cell_foreground": str,  # ""
        "cell_background": str,  # ""
        "header_foreground": str,  # ""
        "header_background": str,  # ""
        "selected_foreground": str,  # ""
        "selected_background": str,  # ""
    },
    "write": {
        "width": int,  # 0
        "height": int,  # 5
        "header": str,  # ""
        "placeholder": str,  # "Write something_.."
        "prompt": str,  # "|  "
        "show_cursor_line": bool,
        "show_line_numbers": bool,
        "value": str,  # ""
        "char_limit": int,  # 0
        "max_lines": int,  # 0
        "no_show_help": bool,
        "show_help": bool,
        "cursor_mode": str,  # "blink"
        "timeout": str,  # "0s"
        "no_strip_ansi": bool,
        "strip_ansi": bool,
        "base_foreground": str,  # ""
        "base_background": str,  # ""
        "cursor_line_number_foreground": str,  # "7"
        "cursor_line_number_background": str,  # ""
        "cursor_line_foreground": str,  # ""
        "cursor_line_background": str,  # ""
        "cursor_foreground": str,  # "212"
        "cursor_background": str,  # ""
        "end_of_buffer_foreground": str,  # "0"
        "end_of_buffer_background": str,  # ""
        "line_number_foreground": str,  # "7"
        "line_number_background": str,  # ""
        "header_foreground": str,  # "240"
        "header_background": str,  # ""
        "placeholder_foreground": str,  # "240"
        "placeholder_background": str,  # ""
        "prompt_foreground": str,  # "7"
        "prompt_background": str,  # ""
    },
    "log": {
        "file": str,  # ""
        "format": bool,
        "formatter": str,  # "text"
        "level": str,  # "none"
        "prefix": str,  # ""
        "structured": bool,
        "time": str,  # ""
        "min_level": str,  # ""
        "level_foreground": str,  # ""
        "level_background": str,  # ""
        "time_foreground": str,  # ""
        "time_background": str,  # ""
        "prefix_foreground": str,  # ""
        "prefix_background": str,  # ""
        "message_foreground": str,  # ""
        "message_background": str,  # ""
        "key_foreground": str,  # ""
        "key_background": str,  # ""
        "value_foreground": str,  # ""
        "value_background": str,  # ""
        "separator_foreground": str,  # ""
        "separator_background": str,  # ""
    },
    "version_check": {
        "help": bool,
        "version": bool,
    },
}


def validate_subcommand_flags(subcmd: str, **opts):
    # get all allowed flags for a subcommand by indexing a `subcmd` into the `subcommands_options` dictionary.
    allowed_flags: dict[str, type] = subcommands_options[subcmd]

    for opt, value in opts.items():
        # checks if the key named `opt` is valid according to each subcommands `allowed_flags`
        if allowed_flags.get(opt) is None:
            raise KeyError(f"No flag named {opt} in subcommand {subcmd}")

        # checks if the value of `value` is  valid based on the type of `allowed_flags[opt]`
        # the reason why then `type` function is used because it has stricter type requirements
        if type(value) is not allowed_flags[opt]:
            raise TypeError(
                f"expected type {allowed_flags[opt]} instead got {type(value)}"
            )


def is_long_dot_option(flag: str) -> bool:
    last_dash_position: int = flag.rfind("_")
    prefix_indicator: str = flag[:last_dash_position]
    match prefix_indicator:
        case (
            "file_size"
            | "selected_indicator"
            | "unselected_prefix"
            | "cursor_text"
            | "line_number"
            | "match_highlight"
            | "cursor_line_number"
            | "cursor_line"
            | "end_of_buffer"
        ):
            suffix_indicator: str = flag[last_dash_position + 1 :]
            return (
                True
                if suffix_indicator == "foreground" or suffix_indicator == "background"
                else False
            )
        case _:
            return False


def is_short_dot_option(flag: str) -> bool:
    dash_position: int = flag.find("_")
    prefix_indicator: str = flag[:dash_position]
    match prefix_indicator:
        case (
            "border"
            | "base"
            | "case"
            | "cell"
            | "directory"
            | "file"
            | "header"
            | "help"
            | "indicator"
            | "item"
            | "key"
            | "level"
            | "match"
            | "message"
            | "permissions"
            | "placeholder"
            | "prefix"
            | "prompt"
            | "selected"
            | "separator"
            | "spinner"
            | "symlink"
            | "text"
            | "time"
            | "title"
            | "unselected"
            | "value"
        ):
            suffix_indicator: str = flag[dash_position + 1 :]
            return (
                True
                if suffix_indicator == "foreground" or suffix_indicator == "background"
                else False
            )
        case "cursor":
            suffix_indicator: str = flag[dash_position + 1 :]
            return (
                True
                if suffix_indicator == "foreground"
                or suffix_indicator == "background"
                or suffix_indicator == "mode"
                else False
            )
        case _:
            return False


def is_long_dash_option(flag: str) -> bool:
    first_dash: int = flag.find("_")
    prefix_indicator: str = flag[:first_dash]

    match prefix_indicator:
        case "select":
            suffix_indicator: str = flag[first_dash + 1 :]
            return True if suffix_indicator == "if_one" else False
        case "show":
            suffix_indicator: str = flag[first_dash + 1 :]
            return (
                True
                if suffix_indicator == "line_numbers"
                or suffix_indicator == "cursor_line"
                or suffix_indicator == "output"
                else False
            )
        case "fields":
            suffix_indicator: str = flag[first_dash + 1 :]
            return True if suffix_indicator == "per_record" else False
        case _:
            return False


def is_short_dash_option(flag: str) -> bool:
    return flag.find("_") == -1


def to_parsable_opt(flag: str) -> str:
    # e.g `--line-number.background`
    if is_long_dot_option(flag):
        # get the first occurance of `_` in order to be converted into `-`
        first_dash = flag.find("_")
        # get the second occurance of `_` in order to be converted into `.`
        second_dash = flag.find("_", first_dash + 1)

        # make `str` into `list` so that we can index the first and second occurance and replace it into a dash and dot
        to_list = list(flag)
        to_list[first_dash] = "-"
        to_list[second_dash] = "."

        # joined the `list` into a `str`
        joined = "".join(to_list)
        return f"--{joined}"
    # e.g `--item.foreground`
    elif is_short_dot_option(flag):
        parsable_opt = flag.replace("_", ".")
        return f"--{parsable_opt}"
    # e.g `--cursor-prefix`
    elif is_long_dash_option(flag):
        parsable_opt = flag.replace("_", "-")
        return f"--{parsable_opt}"
    # e.g `--limit`
    elif is_short_dash_option(flag):
        return f"--{flag}"
    raise ValueError("Unrecognized type of flag")


def stringify_value(val) -> str:
    if type(val) is str:
        return f'"{val}"'
    elif type(val) is bool:
        return str(val).lower()
    elif type(val) is int:
        return str(val)
    raise ValueError("Unsupported value to stringify...")
