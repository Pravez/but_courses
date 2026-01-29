from pathlib import Path
from typing import Annotated
import json
import polars as pl
import rich
from rich.table import Table
import typer
from langchain_mistralai import ChatMistralAI

from assessments.processing import (
    load_markdown_answers,
    process_zip_answers,
    create_parquet_from_answers,
)
from assessments.rating import AnswerRater

app = typer.Typer()

@app.command()
def convert_answers(
    input_directory: Annotated[Path, typer.Argument(help="Path to the input file")],
    output_file: Annotated[Path, typer.Argument(help="Path to the output file")],
):
    answers = load_markdown_answers(input_directory)
    create_parquet_from_answers(answers, output_file, num_answers=2)

@app.command(name="prepare_answers")
def prepare_answers(
    input_directory: Annotated[Path, typer.Argument(help="Path to the input directory")],
    output_file: Annotated[Path, typer.Argument(help="Path to the output file")],
):
    answers = process_zip_answers(input_directory)
    create_parquet_from_answers(answers, output_file, num_answers=14)

@app.command(name="rate_answers")
def rate_answers(
    input_file: Annotated[Path, typer.Argument(help="Path to the input parquet file")],
    mistral_api_key: Annotated[str, typer.Option(help="Mistral API key", envvar="MISTRAL_API_KEY")],
    output_file: Annotated[Path, typer.Argument(help="Path to the output parquet file")] = "ratings.parquet",
    only_student: Annotated[str | None, typer.Option(help="Only rate answers for a specific student")] = None,
    llm_model: Annotated[str, typer.Option(help="LLM model name", envvar="MISTRAL_MODEL")] = "mistral-small-latest",
):
    rich.print(f"Loading input parquet from {input_file} ...")
    df = pl.read_parquet(input_file)

    llm = ChatMistralAI(model=llm_model, api_key=mistral_api_key)
    rater = AnswerRater(llm=llm)

    if only_student:
        df = df.filter(pl.col("username") == only_student)
        if df.is_empty():
            raise ValueError(f"No rows found for student {only_student}")
    results = [rater.rate_student_answers(row) for row in df.to_dicts()]

    rich.print(f"Generating parquet output to {output_file} ...")
    output_df = pl.DataFrame(results)
    
    # Reorder columns to ensure consistency
    columns = ["username"] + [f"answer_correction_{i}" for i in range(14)]
    output_df = output_df.select(columns)
    output_df.write_parquet(output_file)
    rich.print("Done.")

@app.command(name="compute_grades")
def compute_grades(
    input_file: Annotated[Path, typer.Argument(help="Path to the ratings parquet file")],
    answers_file: Annotated[Path, typer.Option(help="Path to the answers.json file")] = Path(__file__).parent.parent.parent / "resources" / "answers.json",
):
    rich.print(f"Loading ratings from {input_file} ...")
    df = pl.read_parquet(input_file)

    rich.print(f"Loading answers from {answers_file} ...")
    with open(answers_file, "r") as f:
        answers_data = json.load(f)

    # Extract coefficients for questions "1" to "14"
    coeffs = {}
    for i in range(1, 15):
        q_id = str(i)
        q_info = answers_data.get(q_id, {})
        coeffs[i] = q_info.get("coefficient", 1)

    total_coeffs = sum(coeffs.values())
    
    results = []
    for row in df.to_dicts():
        username = row["username"]
        weighted_sum = 0.0
        for i in range(14):
            col_name = f"answer_correction_{i}"
            correction_json = row.get(col_name)
            if correction_json:
                correction = json.loads(correction_json)
                note = correction.get("note", 0.0)
                coeff = coeffs.get(i + 1, 1)
                weighted_sum += note * coeff
        
        # Calculate grade on 20
        grade_on_20 = (weighted_sum / total_coeffs) * 20 if total_coeffs > 0 else 0.0
        results.append({
            "username": username,
            "score": weighted_sum,
            "grade_20": grade_on_20
        })

    table = Table(title="Tableau des notes")
    table.add_column("Étudiant", style="cyan")
    table.add_column("Score pondéré", justify="right")
    table.add_column("Note / 20", style="green", justify="right")

    # Sort by username
    results.sort(key=lambda x: x["username"])

    for res in results:
        table.add_row(
            res["username"],
            f"{res['score']:.2f}",
            f"{res['grade_20']:.2f}"
        )

    rich.print(table)

if __name__ == "__main__":
    app()

