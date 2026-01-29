import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import rich
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage
from assessments.models import AnswerCorrection

resources_path = Path(__file__).parent.parent.parent / "resources"


class AnswerRater:
    answers_data: Dict[str, Any]
    system_prompt: str
    user_prompt_template: str
    llm: BaseChatModel
    structured_llm: Runnable

    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.structured_llm = self.llm.with_structured_output(AnswerCorrection)
        self._load_resources()

    def _load_resources(self):
        self.answers_data = json.loads((resources_path / "answers.json").read_text())
        self.system_prompt = (resources_path / "questions_system_prompt.txt").read_text()
        self.user_prompt_template = (
            resources_path / "questions_answer_correction_prompt.txt"
        ).read_text()

    def rate_student_answers(self, student_row: Dict[str, Any], num_questions: int = 14) -> Dict[str, Any]:
        username = student_row["username"]
        rich.print(f"Rating answers for student: [blue]{username}[/blue]")
        correction_row = {"username": username}

        for i in range(num_questions):
            answer_key = f"answer_{i}"
            question_id = str(i + 1)
            student_answer = student_row.get(answer_key, "")

            q_info = self.answers_data.get(question_id)
            if not q_info:
                rich.print(f"[yellow]Warning: No info for question {question_id}[/yellow]")
                correction_row[f"answer_correction_{i}"] = None
                continue

            try:
                correction = self.rate_single_answer(q_info, student_answer)
                correction_row[f"answer_correction_{i}"] = json.dumps(correction.model_dump())
                rich.print(f"Answer_{i}: {correction.model_dump()}")
            except Exception as e:
                rich.print(f"[red]Error rating answer_{i} for {username}: {e}[/red]")
                correction_row[f"answer_correction_{i}"] = json.dumps(
                    {
                        "note": 0.0,
                        "justification": "Error during correction",
                        "commentaire": str(e),
                    }
                )
        return correction_row

    def rate_single_answer(self, question_info: Dict[str, Any], student_answer: str) -> AnswerCorrection:
        # Prepare prompts
        prompt_content = self.user_prompt_template.replace(
            "{{student_answer}}", "{student_answer}"
        )
        user_message_content = prompt_content.format(
            context=question_info["context"],
            question=question_info["question"],
            answer=question_info["answer"],
            student_answer=student_answer,
        )

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_message_content),
        ]

        return self.structured_llm.invoke(messages)
