import re
from dataclasses import dataclass

from polars import DataFrame


@dataclass
class Question:
    column: str
    question_id: str
    question_text: str
    answer_id: str | None
    answer_text: str | None


def column_to_question(
    column_name: str,
) -> Question:
    # NOTE assume "|" splits id and text
    match = re.match(
        r"(?P<question_id>[^\[]+)"
        r"(\[(?P<answer_id>.+)\])?"
        r"\|(?P<question_text>[^\[+]+)"
        r"(\[(?P<answer_text>.+)\])?",
        column_name,
    )
    if match is None:
        raise ValueError(f"Invalid column name: {column_name}")
    groups = match.groupdict()
    return Question(
        column=column_name,
        question_id=groups["question_id"],
        answer_id=groups["answer_id"],
        question_text=groups["question_text"].rstrip(),
        answer_text=groups["answer_text"],
    )


def parse_questions(
    df: DataFrame,
) -> list[Question]:
    return [
        question
        for column in df.columns
        if (question := column_to_question(column)).question_id
        not in ["id", "submitdate", "lastpage", "startlanguage", "seed"]
    ]


# group by question id
def group_by_question_id(
    questions: list[Question],
) -> dict[str, list[Question]]:
    return {
        question_id: [
            question for question in questions if question.question_id == question_id
        ]
        for question_id in list(
            dict.fromkeys(question.question_id for question in questions)
        )
    }


@dataclass
class QuestionsByIdByType:
    categorical: dict[str, list[Question]]
    multiple_choices: dict[str, list[Question]]
    other: dict[str, list[Question]]


def group_by_question_type(
    questions_by_id: dict[str, list[Question]],
    df: DataFrame,
) -> QuestionsByIdByType:
    # split into multiple choice and categorical questions
    multiple_choice_questions = {
        question_id: questions_of_id
        for question_id in questions_by_id
        if (
            (
                len(questions_of_id := questions_by_id[question_id]) > 1
                and "other" not in [q.answer_id for q in questions_of_id]
            )
            or len(questions_of_id) > 2
        )
    }
    categorical_questions = {
        question_id: questions_of_id
        for question_id in questions_by_id
        if (
            (len(questions_of_id := questions_by_id[question_id]) == 1)
            or (
                len(questions_of_id) == 2
                and "other" in [q.answer_id for q in questions_of_id]
            )
        )
        # this condition helps separate categorical from free text questions
        # NOTE in 2023 categorical questions had a max of 9 choices
        and len(set(df[questions_of_id[0].column])) <= 9
    }

    # group up the rest
    other_questions = {
        question_id: questions_by_id[question_id]
        for question_id in questions_by_id
        if question_id not in multiple_choice_questions
        and question_id not in categorical_questions
    }

    # make sure that all questions are accounted for
    assert sum(
        map(len, [multiple_choice_questions, categorical_questions, other_questions])
    ) == len(questions_by_id)

    return QuestionsByIdByType(
        categorical=categorical_questions,
        multiple_choices=multiple_choice_questions,
        other=other_questions,
    )


def get_categorical_answers(
    questions_by_id: dict[str, list[Question]],
    question_id: str,
    df: DataFrame,
):
    questions_not_other = [
        question
        for question in questions_by_id[question_id]
        if question.answer_id != "other"
    ]
    assert len(questions_not_other) == 1
    question = questions_not_other[0]
    return [
        "Not answered" if answer == "" else answer for answer in df[question.column]
    ]
