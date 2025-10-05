import re


def extract_command(command: str) -> tuple[str, tuple[str, ...]]:
    """
    Extract the function name and arguments from a command string.

    Example:
        >>> extract_command("upload [source] [dest]")
        ('upload', ('source', 'dest'))
    """

    func = command.split(" ")[0]
    args: tuple[str] = tuple(re.findall(r"\[(.*?)\]", command))

    return func, args
