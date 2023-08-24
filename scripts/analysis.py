"""
This script is run the analysis of survey results.
"""
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl
import yaml

from nixos.survey_analysis.config import Config
from nixos.survey_analysis.plot import (
    NotMultileChoicesQuestion,
    plot_categorical_question,
    plot_multiple_choices_question,
)
from nixos.survey_analysis.questions import (
    ChoicesByQuestionIdByType,
    group_by_question_type,
    group_choices_by_question_id,
    ungrouped_choices_from_columns,
)

with open("./configs/2023.yml") as f:
    config = Config.model_validate(yaml.safe_load(f))


def plot_categorical_questions(
    questions_by_id_by_type: ChoicesByQuestionIdByType,
    df: pl.DataFrame,
    output_folder: Path,
):
    plot_folder = output_folder / "categorical"

    categorical_questions_by_id = questions_by_id_by_type.categorical

    for question_id in categorical_questions_by_id:
        plt.subplots(figsize=(10, 5))
        plot_categorical_question(
            questions=categorical_questions_by_id[question_id],
            answer_order=(
                config.questions[question_id].order
                if question_id in config.questions
                else None
            ),
            df=df,
        )
        plot_folder.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(plot_folder / f"{question_id}.png"))
        plt.show(block=False)
        plt.close()


def plot_multiple_choices_questions(
    choices_by_question_id_by_type: ChoicesByQuestionIdByType,
    df: pl.DataFrame,
    output_folder: Path,
):
    plot_folder = output_folder / "multiple_choices"

    multiple_choices_questions_by_id = questions_by_id_by_type.multiple_choices

    for question_id in multiple_choices_questions_by_id:
        plt.subplots(figsize=(10, 8))
        try:
            plot_multiple_choices_question(
                choices=choices_by_question_id_by_type.multiple_choices[question_id],
                df=df,
            )
        except NotMultileChoicesQuestion as e:
            print(f"{question_id} is not a multiple choices question: {e}")
            continue

        plot_folder.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(plot_folder / f"{question_id}.png"))
        plt.show(block=False)
        plt.close()


OUT_FOLDER = Path(f"./plots/{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}")

df = pl.read_csv("./data/results-survey2023.csv")
questions_by_id = group_choices_by_question_id(
    ungrouped_choices_from_columns(
        columns=df.columns,
    ),
)
# remove choices that are excluded in the config
for question_id, choices in questions_by_id.items():
    if question_id not in config.questions:
        continue
    choices_to_exclude = config.questions[question_id].exclude
    if choices_to_exclude is None:
        continue
    questions_by_id[question_id] = [
        choice for choice in choices if choice.choice_id not in choices_to_exclude
    ]
questions_by_id_by_type = group_by_question_type(
    choices_by_question_id=questions_by_id,
    df=df,
)
plot_categorical_questions(
    questions_by_id_by_type=questions_by_id_by_type,
    df=df,
    output_folder=OUT_FOLDER,
)
plot_multiple_choices_questions(
    choices_by_question_id_by_type=questions_by_id_by_type,
    df=df,
    output_folder=OUT_FOLDER,
)
