from pydantic import BaseModel


class QuestionConfig(BaseModel):
    order: list[str] | None


class Config(BaseModel):
    questions: dict[str, QuestionConfig]
