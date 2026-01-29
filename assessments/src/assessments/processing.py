import tempfile
import zipfile
from pathlib import Path
from typing import List

import polars as pl
import rich

from assessments.files import convert_markdown_to_answers

def process_zip_answers(input_directory: Path) -> List[dict]:
    rich.print(f"Searching for zip files in {input_directory}...")
    zip_files = list(input_directory.rglob("*.zip"))
    rich.print(f"Found {len(zip_files)} zip files.")

    answers = []

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        for zip_file in zip_files:
            extract_to = temp_path / zip_file.stem
            try:
                with zipfile.ZipFile(zip_file, "r") as zip_ref:
                    zip_ref.extractall(extract_to)
            except Exception as e:
                rich.print(f"[red]Error extracting {zip_file}: {e}[/red]")
                continue

            terraform_content = _extract_terraform_content(extract_to)

            answer_files = list(extract_to.rglob("ANSWERS.md"))
            if not answer_files:
                rich.print(f"[red]Error: ANSWERS.md not found in {zip_file}[/red]")
                continue

            for f in answer_files:
                ans = convert_markdown_to_answers(f)
                ans["terraform"] = terraform_content.strip()
                answers.append(ans)
    
    return answers

def _extract_terraform_content(extract_to: Path) -> str:
    tf_files = sorted(extract_to.rglob("*.tf"))
    terraform_content = ""
    for tf_f in tf_files:
        terraform_content += f"--- {tf_f.relative_to(extract_to)} ---\n"
        terraform_content += tf_f.read_text()
        terraform_content += "\n\n"
    return terraform_content

def create_parquet_from_answers(answers: List[dict], output_file: Path, num_answers: int = 14):
    rich.print(f"Generating parquet output to {output_file} ...")
    output = (
        pl.DataFrame(answers)
        .with_columns(
            pl.col("answers").list.to_struct(
                fields=lambda i: f"answer_{i}", upper_bound=num_answers
            )
        )
        .unnest("answers")
    )
    output.write_parquet(output_file)
    rich.print("Done.")

def load_markdown_answers(input_directory: Path) -> List[dict]:
    rich.print(f"Looking for answer files in {input_directory}...")
    files = [f for f in input_directory.glob("ANSWERS.md", case_sensitive=True)]
    rich.print(f"Found {len(files)} answer files.")

    rich.print("Loading files ...")
    return [convert_markdown_to_answers(f) for f in files]
