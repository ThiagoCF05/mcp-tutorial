from enum import StrEnum
from pydantic import BaseModel, Field


class Model(StrEnum):
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_5_MINI = "gpt-5-mini"
    GPT_4_1_NANO = "gpt-4.1-nano"
    GPT_5_NANO = "gpt-5-nano"


class Intensity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ExperimentMetadata(BaseModel):
    name: str
    model: Model = Field(description="Model to be used")
    reasoning: Intensity | None = Field(description="Reasoning intensity")
    verbosity: Intensity | None = Field(description="Verbosity intensity")
    max_turns: int = Field(description="Maximum number of turns")
    planning: bool = Field(description="Use planning")
    structured_output: dict = Field(description="Structured output")
    reflection: bool = Field(description="Use reflection")


class StockInput(BaseModel):
    name: str
    cnpj: str
    stock_id: str
