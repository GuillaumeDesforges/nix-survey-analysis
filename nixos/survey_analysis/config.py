from pydantic import BaseModel


class QuestionConfig(BaseModel):
    order: list[str] | None = None
    exclude: list[str] | None = None


class Config(BaseModel):
    questions: dict[str, QuestionConfig]
