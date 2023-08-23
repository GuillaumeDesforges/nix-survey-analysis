# %%
from collections import defaultdict, namedtuple
from datetime import datetime
from pathlib import Path
import re
from dataclasses import dataclass

import polars as pl
import matplotlib.pyplot as plt


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
    df: pl.DataFrame,
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
    df: pl.DataFrame,
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


# %%
def plot_categorical_question(
    questions_by_id: dict[str, list[Question]],
    question_id: str,
    answer_order: list[str] | None,
    df: pl.DataFrame,
):
    answers = get_categorical_answers(questions_by_id, question_id, df)
    unique_answers = list(set(answers))

    if answer_order is None:
        answer_order = unique_answers

        # sort by count, but keep "Other", "Not answered" and "N/A" at the end
        has_not_answered = "Not answered" in answer_order
        has_other = "Other" in answer_order
        has_na = "N/A" in answer_order
        if has_not_answered:
            answer_order.remove("Not answered")
        if has_other:
            answer_order.remove("Other")
        if has_na:
            answer_order.remove("N/A")
        answer_order.sort(
            key=lambda x: answers.count(x),
            reverse=True,
        )
        if has_other:
            answer_order.append("Other")
        if has_not_answered:
            answer_order.append("Not answered")
        if has_na:
            answer_order.append("N/A")

    assert all(answer in unique_answers for answer in answer_order)

    plt.title(questions_by_id[question_id][0].question_text)
    # vertical grid
    plt.grid(axis="x")
    # plot horizontal bar chart
    plt.barh(
        answer_order,
        [answers.count(answer) for answer in answer_order],
    )
    # plot first on top
    plt.gca().invert_yaxis()
    # make sure that labels are not cut off
    plt.tight_layout()
    # add percentage on top of bar
    for i, v in enumerate([answers.count(answer) for answer in answer_order]):
        plt.text(v, i, f"{v/len(answers):.1%}", va="center")


answer_order_by_question_id: dict[str, list[str] | None] = defaultdict(lambda: None)
answer_order_by_question_id["age"] = [
    "5-14 years",
    "15-24 years",
    "25-34 years",
    "35-44 years",
    "45-54 years",
    "55-64 years",
    "65+ years",
    "Not answered",
]
answer_order_by_question_id["durationNix"] = [
    "less than a month",
    "1-6 months",
    "6 months - 1 year",
    "1-3 years",
    "3-10 years",
    "10+ years",
    "Not answered",
]
answer_order_by_question_id["durationNixOS"] = [
    "Less than 6 months",
    "6 months - 1 year",
    "1 year - 3 years",
    "3-6 years",
    "6-10 years",
    "10+ years",
    "Not answered",
]

save_figs = True


def plot_categorical_questions(
    questions_by_id_by_type: QuestionsByIdByType,
    df: pl.DataFrame,
):
    _now = datetime.now()
    _plot_folder = Path(f"./plots/{_now.strftime('%Y-%m-%dT%H-%M-%S')}")
    categorical_questions_by_id = questions_by_id_by_type.categorical
    for question_id in categorical_questions_by_id:
        plt.subplots(figsize=(10, 5))
        plot_categorical_question(
            questions_by_id=categorical_questions_by_id,
            question_id=question_id,
            answer_order=answer_order_by_question_id[question_id],
            df=df,
        )
        if save_figs:
            _plot_folder.mkdir(parents=True, exist_ok=True)
            plt.savefig(str(_plot_folder / f"{question_id}.png"))
        plt.show(block=False)
        plt.close()


df = pl.read_csv("./data/results-survey2023.csv")
questions_by_id = group_by_question_id(parse_questions(df))
questions_by_id_by_type = group_by_question_type(questions_by_id)
plot_categorical_questions(
    questions_by_id_by_type=questions_by_id_by_type,
    df=df,
)

# %%

# might me useful to take "other" into account
QuestionWithAnswer = namedtuple("QuestionWithAnswer", ["question", "answer"])


def _answer_rows(
    questions_by_id: dict[str, list[Question]],
    question_id: str,
    df: pl.DataFrame,
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
    df: pl.DataFrame,
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
