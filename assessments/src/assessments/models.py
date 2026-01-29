from typing import Dict
from pydantic import BaseModel

class AnswerCorrection(BaseModel):
    note: float
    justification: str
    commentaire: str

class TerraformRating(BaseModel):
    criterias: Dict[str, AnswerCorrection]
