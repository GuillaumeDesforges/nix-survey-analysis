from polars import DataFrame
from nixos.survey_analysis.answers import get_categorical_answers
from nixos.survey_analysis.questions import Question
import matplotlib.pyplot as plt


def plot_categorical_question(
    questions: list[Question],
    answer_order: list[str] | None,
    df: DataFrame,
):
    answers = get_categorical_answers(
        questions=questions,
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
