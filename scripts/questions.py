import polars as pl

from nixos.survey_analysis.questions import (
    group_by_question_id,
    group_by_question_type,
    parse_questions,
)

df = pl.read_csv("./data/results-survey2023.csv")
questions_by_id = group_by_question_id(parse_questions(df))
questions_by_id_by_type = group_by_question_type(
    questions_by_id=questions_by_id,
    df=df,
)

for question_type, questions_by_id in questions_by_id_by_type.__dict__.items():
    print(f"question_type={question_type}")
    for question_id, questions in questions_by_id.items():
        print(f"question_id={question_id}")
        for question in questions:
            print(question)
    print()
