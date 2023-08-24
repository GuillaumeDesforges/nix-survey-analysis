"""
Print a table of all questions in the survey, grouped by question type.
"""
import polars as pl

from nixos.survey_analysis.questions import (
    group_by_question_id,
    group_by_question_type,
    parse_questions,
)

df = pl.read_csv("./data/results-survey2023.csv")
questions_by_id_by_type = group_by_question_type(
    questions_by_id=group_by_question_id(parse_questions(df)),
    df=df,
)

df_questions = pl.DataFrame(
    [
        {
            "question_type": question_type,
            "question_id": question_id,
            "question_text": questions[0].question_text,
            "count_unique_answers": len(
                set(
                    answer
                    for question in questions
                    for answer in df[question.column].drop_nulls().to_list()
                )
            ),
        }
        for question_type, questions_by_id in questions_by_id_by_type.__dict__.items()
        for question_id, questions in questions_by_id.items()
    ]
)

print(df_questions.to_pandas().to_markdown())
