from pathlib import Path
from typing import Annotated, Optional
import json
import polars as pl
import rich
from langchain_google_genai import ChatGoogleGenerativeAI
from rich.table import Table
import typer
from langchain_mistralai import ChatMistralAI
from .tui.app import AssessmentsReviewerApp

from assessments.processing import (
    load_markdown_answers,
    process_archive_answers,
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
    answers = process_archive_answers(input_directory)
    create_parquet_from_answers(answers, output_file, num_answers=14)

@app.command(name="rate_answers")
def rate_answers(
    input_file: Annotated[Path, typer.Argument(help="Path to the input parquet file")],
    llm_model: Annotated[str, typer.Option(help="LLM model name", envvar="LLM_MODEL")],
    mistral_api_key: Annotated[Optional[str], typer.Option(help="Mistral API key", envvar="MISTRAL_API_KEY")] = None,
    google_api_key: Annotated[Optional[str], typer.Option(help="Vertex AI API key", envvar="GOOGLE_API_KEY")] = None,
    output_file: Annotated[Path, typer.Argument(help="Path to the output parquet file")] = "ratings.parquet",
    only_student: Annotated[str | None, typer.Option(help="Only rate answers for a specific student")] = None,
):
    rich.print(f"Loading input parquet from {input_file} ...")
    df = pl.read_parquet(input_file)

    if mistral_api_key:
        llm = ChatMistralAI(model=llm_model, api_key=mistral_api_key)
    elif google_api_key:
        llm = ChatGoogleGenerativeAI(model=llm_model, api_key=google_api_key)
    else:
        rich.print("[red]Error:[/red] Please provide either Mistral API key or Google API key")
        raise typer.Exit(1)

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

@app.command(name="rate_terraform")
def rate_terraform(
    input_file: Annotated[Path, typer.Argument(help="Path to the input parquet file")],
    llm_model: Annotated[str, typer.Option(help="LLM model name", envvar="LLM_MODEL")],
    mistral_api_key: Annotated[Optional[str], typer.Option(help="Mistral API key", envvar="MISTRAL_API_KEY")] = None,
    google_api_key: Annotated[Optional[str], typer.Option(help="Vertex AI API key", envvar="GOOGLE_API_KEY")] = None,
    output_file: Annotated[Path, typer.Argument(help="Path to the output parquet file")] = "terraform_ratings.parquet",
    only_student: Annotated[str | None, typer.Option(help="Only rate answers for a specific student")] = None,
):
    rich.print(f"Loading input parquet from {input_file} ...")
    df = pl.read_parquet(input_file)

    if mistral_api_key:
        llm = ChatMistralAI(model=llm_model, api_key=mistral_api_key)
    elif google_api_key:
        llm = ChatGoogleGenerativeAI(model=llm_model, api_key=google_api_key)
    else:
        rich.print("[red]Error:[/red] Please provide either Mistral API key or Google API key")
        raise typer.Exit(1)

    rater = AnswerRater(llm=llm)

    # Extract criteria from answers.json
    terraform_criterias = rater.answers_data.get("terraform_criterias", [])

    if only_student:
        df = df.filter(pl.col("username") == only_student)
        if df.is_empty():
            raise ValueError(f"No rows found for student {only_student}")

    results = []
    for row in df.to_dicts():
        username = row["username"]
        rich.print(f"Rating Terraform for student: [blue]{username}[/blue]")
        student_code = row.get("terraform", "")
        try:
            rating = rater.rate_terraform(student_code, terraform_criterias)
            result_row = {"username": username}
            for criteria in terraform_criterias:
                name = criteria["name"]
                correction = rating.criterias.get(name)
                result_row[name] = (
                    json.dumps(correction.model_dump(), ensure_ascii=False)
                    if correction
                    else None
                )
            results.append(result_row)
            rich.print(f"Terraform correction for {username} done.")
        except Exception as e:
            rich.print(f"[red]Error rating Terraform for {username}: {e}[/red]")
            result_row = {"username": username}
            for criteria in terraform_criterias:
                name = criteria["name"]
                result_row[name] = json.dumps(
                    {
                        "note": 0.0,
                        "justification": "Error during correction",
                        "commentaire": str(e),
                    },
                    ensure_ascii=False,
                )
            results.append(result_row)

    rich.print(f"Generating parquet output to {output_file} ...")
    output_df = pl.DataFrame(results)

    # Reorder columns to ensure consistency
    columns = ["username"] + [c["name"] for c in terraform_criterias]
    output_df = output_df.select(columns)

    output_df.write_parquet(output_file)
    rich.print("Done.")

@app.command(name="compute_grades")
def compute_grades(
    input_file: Annotated[Path, typer.Argument(help="Path to the ratings parquet file")],
    terraform_input_file: Annotated[Path, typer.Argument(help="Path to the terraform ratings parquet file")],
    answers_file: Annotated[Path, typer.Option(help="Path to the answers.json file")] = Path(__file__).parent.parent.parent / "resources" / "answers.json",
):
    rich.print(f"Loading ratings from {input_file} ...")
    df_answers = pl.read_parquet(input_file)

    rich.print(f"Loading terraform ratings from {terraform_input_file} ...")
    df_terraform = pl.read_parquet(terraform_input_file)

    rich.print(f"Loading answers from {answers_file} ...")
    with open(answers_file, "r") as f:
        answers_data = json.load(f)

    # Extract coefficients for questions "1" to "14"
    coeffs = {}
    bonus_questions = []
    for i in range(1, 15):
        q_id = str(i)
        q_info = answers_data.get(q_id, {})
        coeffs[i] = q_info.get("coefficient", 1)
        if q_info.get("bonus"):
            bonus_questions.append(i)

    total_normal_coeffs = sum(coeff for i, coeff in coeffs.items() if i not in bonus_questions)

    # Extract coefficients for terraform criterias
    terraform_criterias = answers_data.get("terraform_criterias", [])
    tf_coeffs = {i: c.get("coefficient", 1) for i, c in enumerate(terraform_criterias)}
    total_tf_coeffs = sum(tf_coeffs.values())

    # Join both dataframes on username
    df = df_answers.join(df_terraform, on="username", how="inner")
    
    results = []
    for row in df.to_dicts():
        username = row["username"]
        
        # Calculate answers grade
        answers_weighted_sum = 0.0
        bonus_points = 0.0
        for i in range(14):
            q_num = i + 1
            col_name = f"answer_correction_{i}"
            correction_json = row.get(col_name)
            if correction_json:
                correction = json.loads(correction_json)
                note = correction.get("note", 0.0)
                coeff = coeffs.get(q_num, 1)
                if q_num in bonus_questions:
                    bonus_points += (note / 20.0) * coeff
                else:
                    answers_weighted_sum += note * coeff
        
        answers_grade_20 = (answers_weighted_sum / total_normal_coeffs) * 20 if total_normal_coeffs > 0 else 0.0
        answers_grade_20 = min(20.0, answers_grade_20 + bonus_points)

        # Calculate terraform grade
        tf_weighted_sum = 0.0
        for i, criteria in enumerate(terraform_criterias):
            col_name = criteria['name']
            correction_json = row.get(col_name)
            if correction_json:
                correction = json.loads(correction_json)
                note = correction.get("note", 0.0)
                coeff = tf_coeffs.get(i, 1)
                tf_weighted_sum += note * coeff
        
        tf_grade_20 = (tf_weighted_sum / total_tf_coeffs) * 20 if total_tf_coeffs > 0 else 0.0
        
        # Final composite grade: 60% answers, 40% terraform
        final_grade = (answers_grade_20 * 0.6) + (tf_grade_20 * 0.4)

        results.append({
            "username": username,
            "answers_grade": answers_grade_20,
            "terraform_grade": tf_grade_20,
            "final_grade": final_grade
        })

    table = Table(title="Tableau des notes")
    table.add_column("Étudiant", style="cyan")
    table.add_column("Réponses / 20", justify="right")
    table.add_column("Terraform / 20", justify="right")
    table.add_column("Note Finale / 20", style="green", justify="right")

    # Sort by username
    results.sort(key=lambda x: x["username"])

    for res in results:
        table.add_row(
            res["username"],
            f"{res['answers_grade']:.2f}",
            f"{res['terraform_grade']:.2f}",
            f"{res['final_grade']:.2f}"
        )

    rich.print(table)

@app.command()
def review_grades(
        answers_file: Annotated[Path, typer.Option("--answers", "-a")],
        ratings_file: Annotated[Path, typer.Option("--ratings", "-r")],
        terraform_ratings_file: Annotated[Path, typer.Option("--terraform-ratings", "-t")],
):
    df_answers = pl.read_parquet(answers_file)
    df_ratings = pl.read_parquet(ratings_file)
    df_tf_ratings = pl.read_parquet(terraform_ratings_file)

    df = df_answers.join(df_ratings, on="username").join(df_tf_ratings, on="username")

    answers_json_path = Path(__file__).parent.parent.parent / "resources" / "answers.json"
    with open(answers_json_path, "r") as f:
        answers_data = json.load(f)

    _app = AssessmentsReviewerApp(df=df, answers_data=answers_data)
    _app.run()

if __name__ == "__main__":
    app()

