from pathlib import Path
import re
from typing import TypedDict

ANSWERS_PARSING_REGEX = r"## Question \d+\s*\n\n(.*?)(?=\n\n## Question|\Z)"


class Answers(TypedDict):
    username: str
    answers: list[str]


def convert_markdown_to_answers(input_file: Path) -> Answers:
    if input_file.suffix != ".md":
        raise ValueError("Input file must be a Markdown file")

    with open(input_file, "r") as f:
        content = f.readlines()

    _, _, _, username = content[0].replace("#", "").replace(" ", "").split("-")
    answers = re.findall(ANSWERS_PARSING_REGEX, "".join(content[2:]), re.DOTALL)
    return {"username": username.strip(), "answers": answers}
