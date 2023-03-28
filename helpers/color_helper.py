colors = {
    "blue": "\x1b[34m",
    "green": "\x1b[32m",
    "red": "\x1b[31m",
    "cyan": "\x1b[36m",
    "yellow": "\x1b[33m",
    "purple": "\x1b[35m",
    "grey": "\x1b[37m",
    "black": "\x1b[30m",
    "normal": "\x1b[97m",
}


def colored(text: str, color: str) -> str:
    return colors[color] + text
