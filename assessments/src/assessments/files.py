from pathlib import Path
import re
from typing import TypedDict

ANSWERS_PARSING_REGEX = r"#{2,3} `?Question \d+`?.*?\n(.*?)(?=\n#{2,3} `?Question|\Z)"


class Answers(TypedDict):
    username: str
    answers: list[str]
    terraform: str


def convert_markdown_to_answers(input_file: Path) -> Answers:
    if input_file.suffix != ".md":
        raise ValueError("Input file must be a Markdown file")

    with open(input_file, "r") as f:
        content = f.readlines()

    header_line = content[0]
    for line in content:
        if line.startswith("#"):
            header_line = line
            break

    parts = header_line.replace("#", "").strip().split("-")
    username = parts[-1].strip()

    if username == "[Username]" or not username:
        parent = input_file.parent
        while parent.name.lower() in ["terraform", "stack", "src", "project", "modules"] and parent.parent != parent:
            parent = parent.parent
        username = parent.name

    if username.startswith("[") and username.endswith("]"):
        username = username[1:-1]

    answers = [a.strip() for a in re.findall(ANSWERS_PARSING_REGEX, "".join(content), re.DOTALL)]
    return {"username": username.strip(), "answers": answers, "terraform": ""}
