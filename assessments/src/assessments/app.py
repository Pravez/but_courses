from pathlib import Path
from typing import Annotated
import polars as pl

import rich
import typer

from assessments.files import convert_markdown_to_answers

app = typer.Typer()


@app.command()
def convert_answers(
    input_directory: Annotated[Path, typer.Argument(help="Path to the input file")],
    output_file: Annotated[Path, typer.Argument(help="Path to the output file")],
):
    rich.print(f"Looking for answer files in {input_directory}...")
    files = [f for f in input_directory.glob("ANSWERS.md", case_sensitive=True)]
    rich.print(f"Found {len(files)} answer files.")

    rich.print("Loading files ...")
    answers = [convert_markdown_to_answers(f) for f in files]

    rich.print(f"Generating CSV output to {output_file} ...")
    output = (
        pl.DataFrame(answers)
        .with_columns(
            pl.col("answers").list.to_struct(
                fields=lambda i: f"answer_{i}", upper_bound=2
            )
        )
        .unnest("answers")
    )
    output.write_csv(output_file)
    rich.print("Done.")


@app.command()
def rate_answers(
    year: Annotated[int, typer.Argument(help="Year of the exam")],
    group: Annotated[str, typer.Argument(help="Group of the exam")],
):
    pass
