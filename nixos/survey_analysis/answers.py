from dataclasses import dataclass
from typing import cast

from polars import DataFrame

from nixos.survey_analysis.questions import Choice


@dataclass
class QuestionWithAnswer:
    question: Choice
    answer: str


def get_categorical_question_answers(
    choices: list[Choice],
    df: DataFrame,
) -> list[str]:
    """
    Used for categorical questions.
    """
    questions_not_other = [choice for choice in choices if choice.choice_id != "other"]
    assert len(questions_not_other) == 1
    question = questions_not_other[0]
    return [
        "Not answered" if answer == "" else answer for answer in df[question.column]
    ]


def get_answers_by_choice_id(
    choices: list[Choice],
    df: DataFrame,
) -> dict[str, list[str]]:
    """
    Used for multiple choices questions.
    """
    assert all(choice.choice_id is not None for choice in choices)
    return {cast(str, choice.choice_id): list(df[choice.column]) for choice in choices}
