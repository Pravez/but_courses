from pydantic import BaseModel

class AnswerCorrection(BaseModel):
    note: float
    justification: str
    commentaire: str
