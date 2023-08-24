from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from polars import DataFrame

from nixos.survey_analysis.answers import (
    get_answers_by_choice_id,
    get_categorical_question_answers,
)
from nixos.survey_analysis.questions import Choice


def plot_categorical_question(
    questions: list[Choice],
    answer_order: list[str] | None,
    df: DataFrame,
):
    answers = get_categorical_question_answers(
        choices=questions,
        df=df,
    )
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

    question_text = questions[0].question_text
    plt.title(question_text)
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


class NotMultileChoicesQuestion(Exception):
    pass


def plot_multiple_choices_question(
    choices: list[Choice],
    df: DataFrame,
):
    for choice in choices:
        if choice.choice_id is None:
            raise NotMultileChoicesQuestion(f"Choice without an id: {choice}")
        if choice.choice_text is None:
            raise NotMultileChoicesQuestion(f"Choice without a text: {choice}")

    answers_by_choice_id = get_answers_by_choice_id(
        choices=choices,
        df=df,
    )

    # format answers in "Other"
    other_choice = next(
        (choice for choice in choices if choice.choice_id == "other"),
        None,
    )
    if other_choice is not None:
        assert other_choice.choice_id is not None
        answers_by_choice_id[other_choice.choice_id] = [
            "Yes" if answer != "" else "No"
            for answer in answers_by_choice_id[other_choice.choice_id]
        ]

    # make sure it's just "Yes", "No" or "N/A"
    unique_answers = list(
        set(answer for answers in answers_by_choice_id.values() for answer in answers)
    )
    if len(unique_answers) > 3:
        raise NotMultileChoicesQuestion("Too many answers")

    expected_answers = ["Yes", "No", "N/A"]
    for answer in unique_answers:
        if answer not in expected_answers:
            raise NotMultileChoicesQuestion(f"Unexpected answer: {answer}")

    unique_answers = expected_answers
    color_by_answer = {
        "Yes": "green",
        "No": "gray",
        "N/A": "lightgray",
    }

    # count answers per choice
    count_by_choice_by_answer = {
        answer: {
            cast(str, choice.choice_id): answers_by_choice_id[
                cast(str, choice.choice_id)
            ].count(answer)
            for choice in choices
        }
        for answer in unique_answers
    }

    # sort choices by count of yes
    # but leave other at the end
    if other_choice is not None:
        choices.remove(other_choice)
    choices = sorted(
        choices,
        key=lambda choice: count_by_choice_by_answer["Yes"][
            cast(str, choice.choice_id)
        ],
        reverse=True,
    )
    if other_choice is not None:
        choices.append(other_choice)

    question_text = choices[0].question_text
    plt.title(question_text)
    # vertical grid
    plt.grid(axis="x")

    # order choices per count of yes answers
    # plot horizontal stacked bar chart
    ax = plt.gca()
    left = np.zeros(len(choices))
    choice_texts = [cast(str, choice.choice_text) for choice in choices]
    for answer, count_by_choice in count_by_choice_by_answer.items():
        answer_counts = [
            count_by_choice[cast(str, choice.choice_id)] for choice in choices
        ]
        ax.barh(
            y=choice_texts,
            width=answer_counts,
            height=0.8,
            label=answer,
            left=left,
            color=color_by_answer[answer],
        )
        left += answer_counts
    # plot first on top
    plt.gca().invert_yaxis()
    # plot bar labels
    plt.legend(loc="upper right")
    # make sure that labels are not cut off
    plt.tight_layout()

    # plot % of Yes answers per choice
    total_count = len(df)
    for i, choice in enumerate(choices):
        choice_yes_count = count_by_choice_by_answer["Yes"][cast(str, choice.choice_id)]
        plt.text(
            x=choice_yes_count,
            y=i,
            s=f"{choice_yes_count / total_count * 100:.1f}%",
            ha="left",
            va="center",
            color="white",
        )
