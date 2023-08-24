"""
Print a table of all questions in the survey, grouped by question type.
"""
import polars as pl

from nixos.survey_analysis.questions import (
    group_choices_by_question_id,
    group_by_question_type,
    ungrouped_choices_from_columns,
)

df = pl.read_csv("./data/results-survey2023.csv")
choices_by_question_id_by_type = group_by_question_type(
    choices_by_question_id=group_choices_by_question_id(
        ungrouped_choices_from_columns(
            columns=df.columns,
        ),
    ),
    df=df,
)

df_questions = pl.DataFrame(
    [
        {
            "i": df.columns.index(choices[0].column),
            "question_type": question_type,
            "question_id": question_id,
            "question_text": choices[0].question_text,
            "count_choices": len(choices),
            "count_unique_answers": len(
                set(
                    answer
                    for question in choices
                    for answer in df[question.column].drop_nulls().to_list()
                )
            ),
        }
        for question_type, questions_by_id in choices_by_question_id_by_type.__dict__.items()
        for question_id, choices in questions_by_id.items()
    ]
)

print(df_questions.sort(by="i").to_pandas().to_markdown(index=False))
