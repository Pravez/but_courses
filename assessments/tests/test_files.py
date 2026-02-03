from pathlib import Path
import pytest
from assessments.files import convert_markdown_to_answers

def test_convert_markdown_to_answers_normal(tmp_path):
    d = tmp_path / "tp_cloud_2025_quentin"
    d.mkdir()
    f = d / "ANSWERS.md"
    f.write_text("# TP - Cloud - 2025 - quentin\n\n## Question 1\n\nAnswer 1")
    
    res = convert_markdown_to_answers(f)
    assert res["username"] == "quentin"

def test_convert_markdown_to_answers_with_brackets(tmp_path):
    d = tmp_path / "tp_cloud_2025_quentin"
    d.mkdir()
    f = d / "ANSWERS.md"
    f.write_text("# TP - Cloud - 2025 - [quentin]\n\n## Question 1\n\nAnswer 1")
    
    res = convert_markdown_to_answers(f)
    # This is expected to fail with current implementation or return "[quentin]"
    assert res["username"] == "quentin"

def test_convert_markdown_to_answers_error_username(tmp_path):
    d = tmp_path / "tp_cloud_2025_quentin"
    d.mkdir()
    f = d / "ANSWERS.md"
    f.write_text("# TP - Cloud - 2025 - [Username]\n\n## Question 1\n\nAnswer 1")
    
    res = convert_markdown_to_answers(f)
    assert res["username"] == "tp_cloud_2025_quentin"

def test_convert_markdown_to_answers_empty_username(tmp_path):
    d = tmp_path / "tp_cloud_2025_quentin"
    d.mkdir()
    f = d / "ANSWERS.md"
    f.write_text("# TP - Cloud - 2025 - \n\n## Question 1\n\nAnswer 1")
    
    res = convert_markdown_to_answers(f)
    assert res["username"] == "tp_cloud_2025_quentin"

def test_convert_markdown_to_answers_terraform_parent(tmp_path):
    d = tmp_path / "tp_cloud_2025_quentin"
    tf = d / "terraform"
    tf.mkdir(parents=True)
    f = tf / "ANSWERS.md"
    f.write_text("# TP - Cloud - 2025 - [Username]\n\n## Question 1\n\nAnswer 1")
    
    res = convert_markdown_to_answers(f)
    assert res["username"] == "tp_cloud_2025_quentin"

def test_convert_markdown_to_answers_nested_generic(tmp_path):
    d = tmp_path / "tp_cloud_2025_quentin"
    nested = d / "terraform" / "stack"
    nested.mkdir(parents=True)
    f = nested / "ANSWERS.md"
    f.write_text("# TP - Cloud - 2025 - [Username]\n\n## Question 1\n\nAnswer 1")
    
    res = convert_markdown_to_answers(f)
    assert res["username"] == "tp_cloud_2025_quentin"

def test_convert_markdown_to_answers_no_empty_lines(tmp_path):
    d = tmp_path / "tp_cloud_2025_quentin"
    d.mkdir()
    f = d / "ANSWERS.md"
    # Question 1: No empty line after title
    # Question 2: No empty line before next title
    f.write_text("# TP - Cloud - 2025 - quentin\n## Question 1\nAnswer 1\n## Question 2\nAnswer 2\n\n## Question 3\nAnswer 3")
    
    res = convert_markdown_to_answers(f)
    assert len(res["answers"]) == 3
    assert res["answers"][0].strip() == "Answer 1"
    assert res["answers"][1].strip() == "Answer 2"
    assert res["answers"][2].strip() == "Answer 3"
