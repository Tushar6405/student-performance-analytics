"""Reusable functions for the Student Performance Analytics System."""
import numpy as np
import pandas as pd

SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer_Science"]
PASS_MARK = 35            # minimum marks needed in EACH subject
MIN_ATTENDANCE = 75       # attendance % below this is flagged
GRADE_RULES = [           # (minimum average, grade) - checked top to bottom
    (90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (40, "E"),
]


def load_data(path):
    """Read the student CSV into a Pandas DataFrame."""
    return pd.read_csv(path)


def add_total_and_average(df, subjects=SUBJECTS):
    """Add Total and Average columns using NumPy row-wise calculations."""
    marks = df[subjects].to_numpy()
    df["Total"] = np.sum(marks, axis=1)
    df["Average"] = np.round(np.mean(marks, axis=1), 2)
    return df


def assign_grade(average):
    """Return a grade for an average using GRADE_RULES (F if below all)."""
    for minimum, grade in GRADE_RULES:
        if average >= minimum:
            return grade
    return "F"


def add_grades(df):
    """Add a Grade column by looping over every student's average."""
    grades = []
    for avg in df["Average"]:
        grades.append(assign_grade(avg))
    df["Grade"] = grades
    return df


def add_result(df, subjects=SUBJECTS):
    """Pass only if the student scored >= PASS_MARK in every subject."""
    passed_all = np.all(df[subjects].to_numpy() >= PASS_MARK, axis=1)
    df["Result"] = np.where(passed_all, "Pass", "Fail")
    return df


def subject_analysis(df, subjects=SUBJECTS):
    """Highest, lowest, average and pass count for every subject."""
    rows = []
    for subject in subjects:
        scores = df[subject].to_numpy()
        rows.append({
            "Subject": subject,
            "Highest": int(np.max(scores)),
            "Lowest": int(np.min(scores)),
            "Average": round(float(np.mean(scores)), 2),
            "Pass_Count": int(np.sum(scores >= PASS_MARK)),
        })
    return pd.DataFrame(rows)


def top_performers(df, n=5):
    """Return the top n students ranked by average marks."""
    return df.sort_values("Average", ascending=False).head(n)[
        ["Student_ID", "Name", "Department", "Total", "Average", "Grade"]
    ]


def department_analysis(df):
    """Average marks, attendance and pass count per department."""
    return df.groupby("Department").agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average", "mean"),
        Avg_Attendance=("Attendance", "mean"),
        Passed=("Result", lambda r: (r == "Pass").sum()),
    ).round(2).reset_index()
