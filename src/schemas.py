from typing import Literal

from pydantic import BaseModel, Field


class YesNoAnswer(BaseModel):
    answer: Literal["yes", "no"] = Field(
        description="The answer must be exactly yes or no."
    )


class NumberAnswer(BaseModel):
    answer: float = Field(
        description="The predicted numerical value."
    )