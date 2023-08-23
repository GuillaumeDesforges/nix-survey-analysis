from collections import defaultdict
from datetime import datetime
from pathlib import Path

import polars as pl
import matplotlib.pyplot as plt
from nixos.survey_analysis.plot import plot_categorical_question

from nixos.survey_analysis.questions import (
    QuestionsByIdByType,
    group_by_question_id,
    group_by_question_type,
    parse_questions,
)


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
questions_by_id_by_type = group_by_question_type(
    questions_by_id=questions_by_id,
    df=df,
)
plot_categorical_questions(
    questions_by_id_by_type=questions_by_id_by_type,
    df=df,
)
