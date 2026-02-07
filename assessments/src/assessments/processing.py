import tempfile
import zipfile
from pathlib import Path
from typing import List
import py7zr
import tarfile
import polars as pl
import rich

from assessments.files import convert_markdown_to_answers

def process_archive_answers(input_directory: Path) -> List[dict]:
    rich.print(f"Searching for archive files in {input_directory}...")

    # Collect all supported archive types
    zip_files = list(input_directory.rglob("*.zip"))
    tar_gz_files = list(input_directory.rglob("*.tar.gz"))
    sevenz_files = list(input_directory.rglob("*.7z"))

    all_archives = zip_files + tar_gz_files + sevenz_files
    rich.print(
        f"Found {len(all_archives)} archive files ({len(zip_files)} zip, {len(tar_gz_files)} tar.gz, {len(sevenz_files)} 7z).")

    answers = []

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        for archive_file in all_archives:
            extract_to = temp_path / archive_file.stem
            try:
                if archive_file.suffix == ".zip":
                    with zipfile.ZipFile(archive_file, "r") as zip_ref:
                        zip_ref.extractall(extract_to)
                elif archive_file.suffix == ".gz" and archive_file.suffixes[-2:] == [".tar", ".gz"]:
                    with tarfile.open(archive_file, "r:gz") as tar_ref:
                        tar_ref.extractall(extract_to)
                elif archive_file.suffix == ".7z":
                    with py7zr.SevenZipFile(archive_file, mode="r") as sevenz_ref:
                        sevenz_ref.extractall(path=extract_to)

            except Exception as e:
                rich.print(f"[red]Error extracting {archive_file}: {e}[/red]")
                continue

            terraform_content = _extract_terraform_content(extract_to)

            answer_files = list(extract_to.rglob("ANSWERS.md"))
            if not answer_files:
                rich.print(f"[red]Error: ANSWERS.md not found in {archive_file}[/red]")
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
        if "__MACOSX" in tf_f.parts:
            rich.print(f"[orange]Skipping {tf_f}[/orange]")
            continue
        terraform_content += f"--- {tf_f.relative_to(extract_to)} ---\n"
        try:
            terraform_content += tf_f.read_text()
        except UnicodeDecodeError:
            rich.print(f"[red]Error reading {tf_f}[/red]")
            terraform_content += "Error reading file"
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
