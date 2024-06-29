from pydantic import BaseModel
from typing import List


class OpenAIRequest(BaseModel):
    samples: int
    fields: List[str]
    message: str
