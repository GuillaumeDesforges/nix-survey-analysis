from dataclasses import dataclass

from polars import DataFrame

from nixos.survey_analysis.questions import Question


@dataclass
class QuestionWithAnswer:
    question: Question
    answer: str


def _answer_rows(
    questions_by_id: dict[str, list[Question]],
    question_id: str,
    df: DataFrame,
):
    return [
        [
            QuestionWithAnswer(
                question=q,
                answer=answer,
            )
            for q, answer in zip(questions_by_id[question_id], answer_row)
        ]
        for answer_row in zip(
            *(df[q.column].to_list() for q in questions_by_id[question_id])
        )
    ]


def unfold_answers(
    questions_by_id: dict[str, list[Question]],
    question_id: str,
    df: DataFrame,
):
    answers = []
    answer_rows = _answer_rows(
        questions_by_id=questions_by_id,
        question_id=question_id,
        df=df,
    )
    for answer_row in answer_rows:
        if all(
            question_with_answer.answer == "" for question_with_answer in answer_row
        ):
            answers.append("Not answered")
            continue

        for question_with_answer in answer_row:
            if question_with_answer.answer != "":
                answers.append(question_with_answer.answer)

    return answers


def get_categorical_answers(
    questions: list[Question],
    df: DataFrame,
):
    questions_not_other = [
        question for question in questions if question.answer_id != "other"
    ]
    assert len(questions_not_other) == 1
    question = questions_not_other[0]
    return [
        "Not answered" if answer == "" else answer for answer in df[question.column]
    ]
