# %%
import re
from dataclasses import dataclass

import polars as pl

# %%
df = pl.read_csv("./data/results-survey2023.csv")


# %%
@dataclass
class Question:
    column: str
    question_id: str
    question_text: str
    answer_id: str | None
    answer_text: str | None


def column_to_question(column_name: str) -> Question:
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


# parse each column
questions: list[Question] = [
    question
    for column in df.columns
    if (question := column_to_question(column)).question_id
    not in ["id", "submitdate", "lastpage", "startlanguage", "seed"]
]

# group by question id
questions_by_id = {
    question_id: [
        question for question in questions if question.question_id == question_id
    ]
    for question_id in list(
        dict.fromkeys(question.question_id for question in questions)
    )
}

# %%
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
    # NOTE assume a categorical question has less than 15 answers
    and len(set(df[questions_of_id[0].column])) < 15
}

other_questions = {
    question_id: questions_by_id[question_id]
    for question_id in questions_by_id
    if question_id not in multiple_choice_questions
    and question_id not in categorical_questions
}

assert sum(
    map(len, [multiple_choice_questions, categorical_questions, other_questions])
) == len(questions_by_id)
assert sum(
    map(
        lambda qs_by_id: sum(len(qs) for qs in qs_by_id.values()),
        [multiple_choice_questions, categorical_questions, other_questions],
    )
) == len(questions)

# %%
count_answers_categorical_question_by_id = {
    question_id: sum(len(set(df[q.column])) for q in questions)
    for question_id, questions in categorical_questions.items()
}

count_answers_multiple_choice_question_by_id = {
    question_id: sum(len(set(df[q.column])) for q in questions)
    for question_id, questions in multiple_choice_questions.items()
}

count_answers_other_question_by_id = {
    question_id: sum(len(set(df[q.column])) for q in questions)
    for question_id, questions in other_questions.items()
}

# %%
answers_other_question_by_id = {
    question_id: [answer for q in questions for answer in set(df[q.column])]
    for question_id, questions in other_questions.items()
}
# %%
