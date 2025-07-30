import os
import tempfile
import inspect
from typing import Callable
from typing import Any
from src.flags import validate_subcommand_flags
from src.flags import to_parsable_opt
from src.flags import stringify_value


def choose(items_to_be_chosen: list, **chosen_opts) -> str:
    # checks if `chosen_opts` are valid
    validate_subcommand_flags("choose", **chosen_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in chosen_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    str_items: str = ""
    for item in items_to_be_chosen:
        str_items += stringify_value(item) + " "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum choose {flags} {str_items}"

    return os.popen(cmd).read().strip()


def confirm(prompt: str, **confirm_opts) -> bool:
    # checks if `confirm_opts` are valid
    validate_subcommand_flags("confirm", **confirm_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in confirm_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum confirm '{prompt}' {flags}"

    retval: int = os.system(cmd)
    return True if retval == 0 else False


def file(path: str, **file_opts) -> str:
    # checks if `confirm_opts` are valid
    validate_subcommand_flags("file", **file_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in file_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum file '{path}' {flags}"

    return os.popen(cmd).read().strip()


def filter(items_to_filter: list, **filter_opts) -> str:
    # checks if `confirm_opts` are valid
    validate_subcommand_flags("filter", **filter_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in filter_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    str_items: str = ""
    for item in items_to_filter:
        str_items += stringify_value(item) + " "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum filter {str_items} {flags}"

    return os.popen(cmd).read().strip()


def format(text: str, **format_opts) -> str:
    validate_subcommand_flags("format", **format_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in format_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum format '{text}' {flags}"
    return os.popen(cmd).read().strip()


def input(**input_opts) -> str:
    validate_subcommand_flags("input", **input_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in input_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum input {flags}"
    return os.popen(cmd).read().strip()


def join(*strs, **join_opts) -> str:
    validate_subcommand_flags("join", **join_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in join_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    args: str = ""
    for s in strs:
        args += f'"{s}" '

    cmd: str = f"gum join {args} {flags}"

    return os.popen(cmd).read().strip()


def pager(filepath: str, **pager_opts):
    validate_subcommand_flags("pager", **pager_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in pager_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum pager {flags} < {filepath}"

    os.system(cmd)


def spin(fnc: Callable[..., Any], **spin_opts):
    validate_subcommand_flags("spin", **spin_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in spin_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # make temporary file
    tmpfile = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
    try:
        path = tmpfile.name
        # turn `fnc` declaration into literal string source code
        source_code = inspect.getsource(fnc)

        # the `command` to run for `gum spin`, the function will run as a script for `gum spin`
        code_to_run: str = f"python3 {path}"

        # write `source_code` from `fnc` to `tmpfile`
        with open(tmpfile.name, "w") as tf:
            tf.write(f"""{source_code}\n\n{fnc.__name__}()""")

        # after writing the source code, make `python` execute that code
        cmd: str = f"gum spin {code_to_run} {flags}"

        os.system(cmd)
    finally:
        # clean up
        tmpfile.close()
        os.unlink(tmpfile.name)


def style(text: str, **style_opts) -> str:
    validate_subcommand_flags("style", **style_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in style_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum style '{text}' {flags}"

    return os.popen(cmd).read().strip()


def table(filepath: str, **table_opts) -> str:
    validate_subcommand_flags("table", **table_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in table_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum table {flags} < {filepath}"

    return os.popen(cmd).read().strip()


def write(**write_opts) -> str:
    validate_subcommand_flags("write", **write_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in write_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum write {flags}"
    return os.popen(cmd).read().strip()


def log(text: str, **log_opts):
    validate_subcommand_flags("log", **log_opts)

    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in log_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    # after the flags are parsed accordingly, format them into `gum <subcmd> <flags...> <items...>`
    cmd: str = f"gum log {flags} '{text}'"

    os.system(cmd)


def version_check(**vc_opts):
    validate_subcommand_flags("version_check", **vc_opts)
    # turn valid subcommand options into parsable options that `gum` can parse.
    flags: str = ""
    for opt, value in vc_opts.items():
        parsable_opt: str = to_parsable_opt(opt)
        stringified_value: str = stringify_value(value)
        flags += f"{parsable_opt}={stringified_value} "

    cmd: str = f"gum version-check {flags}"
    os.system(cmd)
