import re
from dataclasses import dataclass

from polars import DataFrame


@dataclass
class Choice:
    column: str
    question_id: str
    question_text: str
    choice_id: str | None
    choice_text: str | None


def column_to_choice(
    column_name: str,
) -> Choice:
    # NOTE assumes "{question_id} [{choice_id}]|{question_text} [{choice_text}]"
    match = re.match(
        r"(?P<question_id>[^\[]+)"
        r"(\[(?P<choice_id>.+)\])?"
        r"\|(?P<question_text>[^\[+]+)"
        r"(\[(?P<choice_text>.+)\])?",
        column_name,
    )
    if match is None:
        raise ValueError(f"Invalid column name: {column_name}")
    groups = match.groupdict()
    return Choice(
        column=column_name,
        question_id=groups["question_id"],
        choice_id=groups["choice_id"],
        question_text=groups["question_text"].rstrip(),
        choice_text=groups["choice_text"],
    )


def ungrouped_choices_from_columns(
    columns: list[str],
) -> list[Choice]:
    return [
        choice
        for column in columns
        if (choice := column_to_choice(column)).question_id
        not in ["id", "submitdate", "lastpage", "startlanguage", "seed"]
    ]


# group by question id
def group_choices_by_question_id(
    ungrouped_choices: list[Choice],
) -> dict[str, list[Choice]]:
    return {
        question_id: [
            choice for choice in ungrouped_choices if choice.question_id == question_id
        ]
        for question_id in list(
            dict.fromkeys(choice.question_id for choice in ungrouped_choices)
        )
    }


@dataclass
class ChoicesByQuestionIdByType:
    ranking: dict[str, list[Choice]]
    categorical: dict[str, list[Choice]]
    multiple_choices: dict[str, list[Choice]]
    other: dict[str, list[Choice]]


def group_by_question_type(
    choices_by_question_id: dict[str, list[Choice]],
    df: DataFrame,
) -> ChoicesByQuestionIdByType:
    ranking_questions = {
        question_id: choices
        for question_id, choices in choices_by_question_id.items()
        if all(
            (
                choice.choice_text is not None
                and f"Rank {choice.choice_id}" == choice.choice_text
            )
            for choice in choices
        )
    }

    multiple_choice_questions = {
        question_id: choices
        for question_id, choices in choices_by_question_id.items()
        if (
            question_id not in ranking_questions
            and (
                (len(choices) > 1 and "other" not in [q.choice_id for q in choices])
                or len(choices) > 2
            )
        )
    }

    categorical_questions = {
        question_id: choices
        for question_id in choices_by_question_id
        if (
            question_id not in ranking_questions
            and question_id not in multiple_choice_questions
            and (
                (len(choices := choices_by_question_id[question_id]) == 1)
                or (len(choices) == 2 and "other" in [q.choice_id for q in choices])
            )
        )
        # this condition helps separate categorical from free text questions
        # NOTE in 2023 categorical questions had a max of 9 choices
        and len(set(df[choices[0].column])) <= 9
    }

    # group up the rest
    other_questions = {
        question_id: choices_by_question_id[question_id]
        for question_id in choices_by_question_id
        if (
            question_id not in ranking_questions
            and question_id not in multiple_choice_questions
            and question_id not in categorical_questions
        )
    }

    # make sure that all questions are accounted for
    assert sum(
        map(
            len,
            [
                ranking_questions,
                multiple_choice_questions,
                categorical_questions,
                other_questions,
            ],
        )
    ) == len(choices_by_question_id)

    return ChoicesByQuestionIdByType(
        ranking=ranking_questions,
        categorical=categorical_questions,
        multiple_choices=multiple_choice_questions,
        other=other_questions,
    )
