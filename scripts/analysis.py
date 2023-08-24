"""
This script is run the analysis of survey results.
"""
from datetime import datetime
from pathlib import Path

import polars as pl
import matplotlib.pyplot as plt
from nixos.survey_analysis.config import Config
from nixos.survey_analysis.plot import plot_categorical_question

from nixos.survey_analysis.questions import (
    QuestionsByIdByType,
    group_by_question_id,
    group_by_question_type,
    parse_questions,
)
import yaml

with open("./configs/2023.yml") as f:
    config = Config.model_validate(yaml.safe_load(f))

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
            answer_order=(
                config.questions[question_id].order
                if question_id in config.questions
                else None
            ),
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
