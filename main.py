"""Student Performance Analytics System - main program."""
import numpy as np
import pandas as pd
import functions as fn

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)


def heading(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def main():
    # Step 2 - Read the data
    df = fn.load_data("students.csv")
    heading("1. DATASET OVERVIEW")
    print(f"Records: {df.shape[0]}  |  Columns: {df.shape[1]}")
    print("Columns:", ", ".join(df.columns))
    print("Missing values:", int(df.isna().sum().sum()))
    print(df.head())

    # Step 3 - Process the data
    df = fn.add_total_and_average(df)
    df = fn.add_grades(df)
    df = fn.add_result(df)

    heading("2. STUDENT RESULTS (Total, Average, Grade, Result)")
    print(df[["Student_ID", "Name", "Total", "Average", "Grade",
              "Result", "Attendance"]].to_string(index=False))

    # Step 4 - Analysis
    heading("3. CLASS SUMMARY")
    best = df.loc[df["Average"].idxmax()]
    worst = df.loc[df["Average"].idxmin()]
    passed = int((df["Result"] == "Pass").sum())
    failed = len(df) - passed
    print(f"Overall class average : {np.mean(df['Average']):.2f}")
    print(f"Highest average       : {best['Name']} ({best['Average']})")
    print(f"Lowest average        : {worst['Name']} ({worst['Average']})")
    print(f"Passed / Failed       : {passed} / {failed} "
          f"({passed / len(df) * 100:.1f}% pass rate)")
    print(f"Pass rule: >= {fn.PASS_MARK} marks in every subject")

    heading("4. GRADE DISTRIBUTION")
    print(df["Grade"].value_counts().sort_index().to_string())

    heading("5. SUBJECT-WISE ANALYSIS")
    subj = fn.subject_analysis(df)
    print(subj.to_string(index=False))
    top_subj = subj.loc[subj["Average"].idxmax(), "Subject"]
    low_subj = subj.loc[subj["Average"].idxmin(), "Subject"]
    print(f"\nBest subject (highest average)  : {top_subj}")
    print(f"Weakest subject (lowest average): {low_subj}")

    heading("6. TOP 5 PERFORMERS")
    print(fn.top_performers(df).to_string(index=False))

    heading("7. DEPARTMENT-WISE ANALYSIS")
    print(fn.department_analysis(df).to_string(index=False))

    heading("8. STUDENTS NEEDING ATTENTION")
    print("Failed students:")
    for _, row in df[df["Result"] == "Fail"].iterrows():
        print(f"  - {row['Student_ID']} {row['Name']} (Average {row['Average']})")
    print(f"Low attendance (< {fn.MIN_ATTENDANCE}%):")
    for _, row in df[df["Attendance"] < fn.MIN_ATTENDANCE].iterrows():
        print(f"  - {row['Student_ID']} {row['Name']} ({row['Attendance']}%)")

    df.to_csv("results.csv", index=False)
    print("\nFull results saved to results.csv")


if __name__ == "__main__":
    main()
