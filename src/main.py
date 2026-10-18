import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("data/students-sample-dataset.csv")

print(df)

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(list(df.columns))

print("\nDataset information:")
df.info()

print("\nStatistical summary:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())


# ============================================================
# 2. AUTOMATICALLY DETECT IMPORTANT COLUMNS
# ============================================================

def find_column(columns, possible_names):
    """Find a column using common column-name variations."""
    normalized = {
        str(column).strip().lower().replace("_", " ").replace("-", " "): column
        for column in columns
    }

    for name in possible_names:
        key = name.strip().lower().replace("_", " ").replace("-", " ")
        if key in normalized:
            return normalized[key]

    return None


name_column = find_column(
    df.columns,
    [
        "name",
        "student name",
        "student_name",
        "full name",
        "full_name",
        "student",
        "learner name",
        "learner_name"
    ]
)

id_column = find_column(
    df.columns,
    [
        "student id",
        "student_id",
        "id",
        "roll no",
        "roll_no",
        "roll number",
        "roll_number",
        "registration no",
        "registration_no",
        "registration number",
        "registration_number"
    ]
)

attendance_column = None

for column in df.columns:
    if "attendance" in str(column).lower():
        attendance_column = column
        break


# If a Name column does not exist, use the row number.
if name_column is None:
    df["Student_Name"] = "Student " + (df.index + 1).astype(str)
    name_column = "Student_Name"

# If an ID column does not exist, use the row number.
if id_column is None:
    df["Student_ID_Auto"] = df.index + 1
    id_column = "Student_ID_Auto"


print("\nDetected Name Column:")
print(name_column)

print("\nDetected ID Column:")
print(id_column)

print("\nDetected Attendance Column:")
print(attendance_column)


# ============================================================
# 3. AUTOMATICALLY DETECT SUBJECT COLUMNS
# ============================================================

numeric_columns = df.select_dtypes(include=np.number).columns

excluded_columns = {
    id_column
}

if attendance_column is not None:
    excluded_columns.add(attendance_column)

subjects = [
    column
    for column in numeric_columns
    if column not in excluded_columns
]

if len(subjects) == 0:
    raise ValueError(
        "No numeric subject columns were detected. "
        "Make sure your subject marks are numeric."
    )

print("\nDetected Subjects:")
print(list(subjects))


# ============================================================
# 4. STUDENT AVERAGE
# ============================================================

df["Average"] = df[subjects].mean(axis=1)

print("\nStudent averages:")
print(df[[name_column, "Average"]])


# ============================================================
# 5. GRADES
# ============================================================

def assign_grade(average):
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


df["Grade"] = df["Average"].apply(assign_grade)

print("\nStudent grades:")
print(df[[name_column, "Average", "Grade"]])


# ============================================================
# 6. PASS / FAIL
# ============================================================

def check_status(average):
    if average >= 50:
        return "Pass"
    else:
        return "Fail"


df["Status"] = df["Average"].apply(check_status)

print("\nStudent performance:")
print(df[[name_column, "Average", "Grade", "Status"]])


# ============================================================
# 7. OVERALL STATISTICS
# ============================================================

average_marks = np.mean(df["Average"])
highest_marks = np.max(df["Average"])
lowest_marks = np.min(df["Average"])

print("\nOverall Statistics:")
print("Average marks:", average_marks)
print("Highest marks:", highest_marks)
print("Lowest marks:", lowest_marks)


# ============================================================
# 8. TOP 5 STUDENTS
# ============================================================

top_5 = df.sort_values(by="Average", ascending=False).head(5)

print("\nTop 5 Students:")
print(top_5[[name_column, "Average", "Grade", "Status"]])


highest_student = df.loc[df["Average"].idxmax()]
lowest_student = df.loc[df["Average"].idxmin()]

print("\nHighest Performing Student:")
print(highest_student[[name_column, "Average", "Grade", "Status"]])

print("\nLowest Performing Student:")
print(lowest_student[[name_column, "Average", "Grade", "Status"]])


# ============================================================
# 9. SUBJECT-WISE STATISTICS
# ============================================================

print("\nSubject-wise Statistics:")

for subject in subjects:
    marks = df[subject].to_numpy()

    average = np.mean(marks)
    highest = np.max(marks)
    lowest = np.min(marks)
    std_dev = np.std(marks)

    print(f"\n{subject}")
    print("Average:", average)
    print("Highest:", highest)
    print("Lowest:", lowest)
    print("Standard Deviation:", std_dev)


# ============================================================
# 10. STRONGEST / WEAKEST SUBJECT
# ============================================================

subject_averages = {}

for subject in subjects:
    marks = df[subject].to_numpy()
    subject_averages[subject] = np.mean(marks)

strongest_subject = max(subject_averages, key=subject_averages.get)
weakest_subject = min(subject_averages, key=subject_averages.get)

print("\nSubject Performance:")
print("Strongest Subject:", strongest_subject)
print("Average:", subject_averages[strongest_subject])

print("Weakest Subject:", weakest_subject)
print("Average:", subject_averages[weakest_subject])


# ============================================================
# 11. ATTENDANCE ANALYSIS (OPTIONAL)
# ============================================================

if attendance_column is not None:

    attendance = pd.to_numeric(
        df[attendance_column],
        errors="coerce"
    ).to_numpy()

    average_marks_array = df["Average"].to_numpy()

    valid = ~np.isnan(attendance) & ~np.isnan(average_marks_array)

    if valid.sum() >= 2:
        correlation = np.corrcoef(
            attendance[valid],
            average_marks_array[valid]
        )[0, 1]
    else:
        correlation = np.nan

    print("\nAttendance vs Performance:")
    print("Correlation:", correlation)

else:
    print("\nAttendance column not found.")
    print("Attendance analysis will be skipped.")


# ============================================================
# 12. CHART - STUDENT AVERAGES
# ============================================================

plt.figure(figsize=(12, 6))

plt.bar(df[name_column].astype(str), df["Average"])

plt.xlabel("Students")
plt.ylabel("Average Marks")
plt.title("Student Average Performance")

plt.xticks(rotation=90)

plt.tight_layout()
plt.savefig("output/charts/student_averages_chart.png", dpi=300)
plt.show()


# ============================================================
# 13. CHART - SUBJECT AVERAGES
# ============================================================

subject_names = list(subject_averages.keys())
subject_means = list(subject_averages.values())

plt.figure(figsize=(8, 5))

plt.bar(subject_names, subject_means)

plt.xlabel("Subjects")
plt.ylabel("Average Marks")
plt.title("Subject-Wise Average Performance")

plt.tight_layout()
plt.savefig("output/charts/subject_averages_chart.png", dpi=300)
plt.show()


# ============================================================
# 14. ATTENDANCE SCATTER PLOT (OPTIONAL)
# ============================================================

if attendance_column is not None:

    x = pd.to_numeric(
        df[attendance_column],
        errors="coerce"
    )
    y = df["Average"]

    valid = x.notna() & y.notna()

    plt.figure(figsize=(8, 5))

    plt.scatter(x[valid], y[valid])

    plt.xlabel(str(attendance_column))
    plt.ylabel("Average Marks")
    plt.title("Attendance vs Average Marks")

    plt.tight_layout()
    plt.savefig("output/charts/attendance_vs_performance.png", dpi=300)
    plt.show()


# ============================================================
# 15. GRADE DISTRIBUTION
# ============================================================

grade_counts = df["Grade"].value_counts().sort_index()

print("\nGrade Distribution:")
print(grade_counts)

plt.figure(figsize=(8, 5))

plt.bar(grade_counts.index, grade_counts.values)

plt.xlabel("Grade")
plt.ylabel("Number of Students")
plt.title("Grade Distribution")

plt.tight_layout()
plt.savefig("output/charts/grade_distribution.png", dpi=300)
plt.show()


# ============================================================
# 16. SAVE ANALYZED DATA
# ============================================================

output_file = "output/student_performance_analyzed.csv"

df.to_csv(output_file, index=False)

print("\nAnalyzed data saved successfully!")
print("File:", output_file)


# ============================================================
# 17. STUDENT PERFORMANCE SUMMARY
# ============================================================

print("\n" + "=" * 40)
print("STUDENT PERFORMANCE SUMMARY")
print("=" * 40)

print("Total Students:", len(df))
print("Overall Average:", round(np.mean(df["Average"]), 2))
print("Highest Average:", round(np.max(df["Average"]), 2))
print("Lowest Average:", round(np.min(df["Average"]), 2))

print("\nPass:", (df["Status"] == "Pass").sum())
print("Fail:", (df["Status"] == "Fail").sum())

print("Strongest Subject:", strongest_subject)
print("Weakest Subject:", weakest_subject)

print("=" * 40)


# ============================================================
# 18. PERFORMANCE CATEGORY
# ============================================================

def performance_category(average):
    if average >= 80:
        return "Excellent"
    elif average >= 70:
        return "Good"
    else:
        return "Needs Improvement"


df["Performance"] = df["Average"].apply(performance_category)

print("\nPerformance Categories:")
print(df[[name_column, "Average", "Performance"]])

performance_counts = df["Performance"].value_counts()

print("\nPerformance Category Distribution:")
print(performance_counts)

plt.figure(figsize=(8, 5))

plt.bar(performance_counts.index, performance_counts.values)

plt.xlabel("Performance Category")
plt.ylabel("Number of Students")
plt.title("Performance Category Distribution")

plt.tight_layout()
plt.savefig("output/charts/performance_category_distribution.png", dpi=300)
plt.show()


# ============================================================
# 19. PASS PERCENTAGE
# ============================================================

total_students = len(df)
passed_students = (df["Status"] == "Pass").sum()

pass_percentage = (passed_students / total_students) * 100

print("Pass:", passed_students)
print("Fail:", (df["Status"] == "Fail").sum())
print("\nPass Percentage:", round(pass_percentage, 2), "%")


# ============================================================
# 20. TOP 3 STUDENTS
# ============================================================

top_3 = df.sort_values(by="Average", ascending=False).head(3).copy()
top_3.index = range(1, len(top_3) + 1)

print("\nTop 3 Students:")
print(top_3[[name_column, "Average", "Grade", "Performance"]])

plt.figure(figsize=(8, 5))

plt.bar(top_3[name_column].astype(str), top_3["Average"])

plt.xlabel("Students")
plt.ylabel("Average Marks")
plt.title("Top 3 Students")

plt.tight_layout()
plt.savefig("output/charts/top_3_students.png", dpi=300)
plt.show()


# ============================================================
# 21. SUBJECT CONSISTENCY
# ============================================================

subject_std = {}

for subject in subjects:
    marks = df[subject].to_numpy()
    subject_std[subject] = np.std(marks)

most_consistent_subject = min(
    subject_std,
    key=subject_std.get
)

print("\nMost Consistent Subject:", most_consistent_subject)
print(
    "Standard Deviation:",
    subject_std[most_consistent_subject]
)

plt.figure(figsize=(8, 5))

plt.bar(subject_names, subject_means)

plt.xlabel("Subjects")
plt.ylabel("Average Marks")
plt.title("Subject Performance Comparison")

plt.tight_layout()
plt.savefig("output/charts/subject_averages_chart.png", dpi=300)
plt.show()


# ============================================================
# 22. ATTENDANCE TREND LINE (OPTIONAL)
# ============================================================

if attendance_column is not None:

    x = pd.to_numeric(
        df[attendance_column],
        errors="coerce"
    )
    y = df["Average"]

    valid = x.notna() & y.notna()

    if valid.sum() >= 2:
        coefficients = np.polyfit(
            x[valid],
            y[valid],
            1
        )

        trend_line = np.poly1d(coefficients)

        plt.figure(figsize=(8, 5))

        plt.scatter(x[valid], y[valid])
        plt.plot(x[valid], trend_line(x[valid]))

        plt.xlabel(str(attendance_column))
        plt.ylabel("Average Marks")
        plt.title("Attendance vs Average with Trend Line")

        plt.tight_layout()
        plt.savefig("output/charts/attendance_vs_performance.png", dpi=300)
        plt.show()


# ============================================================
# 23. TOTAL MARKS
# ============================================================

df["Total Marks"] = df[subjects].sum(axis=1)

print("\nStudent Total Marks:")
print(df[[name_column, "Total Marks", "Average"]])

df.to_csv(output_file, index=False)

print("\nUpdated analyzed report saved successfully!")


highest_total_student = df.loc[df["Total Marks"].idxmax()]

print("\nHighest Total Marks:")
print(
    highest_total_student[
        [name_column, "Total Marks", "Average", "Grade", "Performance"]
    ]
)

lowest_total_student = df.loc[df["Total Marks"].idxmin()]

print("\nLowest Total Marks:")
print(
    lowest_total_student[
        [name_column, "Total Marks", "Average", "Grade", "Performance"]
    ]
)


# ============================================================
# 24. FINAL STUDENT REPORT
# ============================================================

final_report_columns = [
    id_column,
    name_column,
    "Total Marks",
    "Average",
    "Grade",
    "Status",
    "Performance"
]

final_report = df[final_report_columns]

print("\nFinal Student Report:")
print(final_report)

final_report_file = "output/final_student_report.csv"

final_report.to_csv(final_report_file, index=False)

print("\nFinal student report saved successfully!")
print("File:", final_report_file)


# ============================================================
# 25. GRADE PERCENTAGES
# ============================================================

grade_percentage = (grade_counts / len(df)) * 100

print("\nGrade Percentages:")
print(grade_percentage.round(2))

plt.figure(figsize=(7, 7))

plt.pie(
    grade_percentage.values,
    labels=grade_percentage.index,
    autopct="%1.1f%%"
)

plt.title("Grade Percentage Distribution")

plt.tight_layout()
plt.savefig("output/charts/grade_distribution.png", dpi=300)
plt.show()


# ============================================================
# 26. ATTENDANCE STATISTICS (OPTIONAL)
# ============================================================

if attendance_column is not None:

    attendance_series = pd.to_numeric(
        df[attendance_column],
        errors="coerce"
    )

    average_attendance = attendance_series.mean()
    highest_attendance = attendance_series.max()
    lowest_attendance = attendance_series.min()

    print("\nAttendance Statistics:")
    print(
        "Average Attendance:",
        round(average_attendance, 2),
        "%"
    )
    print(
        "Highest Attendance:",
        round(highest_attendance, 2),
        "%"
    )
    print(
        "Lowest Attendance:",
        round(lowest_attendance, 2),
        "%"
    )

    low_attendance = df[
        attendance_series < 75
    ]

    print("\nStudents with Low Attendance:")
    print(
        low_attendance[
            [name_column, attendance_column, "Average", "Status"]
        ]
    )

else:
    print("\nAttendance statistics skipped.")


# ============================================================
# 27. STUDENTS NEEDING IMPROVEMENT
# ============================================================

students_needing_improvement = df[
    df["Performance"] == "Needs Improvement"
]

improvement_columns = [
    name_column,
    "Average",
    "Grade"
]

if attendance_column is not None:
    improvement_columns.append(attendance_column)

print("\nStudents Needing Improvement:")
print(
    students_needing_improvement[improvement_columns]
)


# ============================================================
# 28. RISK ANALYSIS
# ============================================================

def check_risk(row):
    if attendance_column is not None:
        attendance_value = pd.to_numeric(
            row[attendance_column],
            errors="coerce"
        )

        if (
            row["Average"] < 60
            or (
                pd.notna(attendance_value)
                and attendance_value < 75
            )
        ):
            return "At Risk"

    else:
        if row["Average"] < 60:
            return "At Risk"

    return "Low Risk"


df["Risk"] = df.apply(check_risk, axis=1)

risk_columns = [
    name_column,
    "Average"
]

if attendance_column is not None:
    risk_columns.append(attendance_column)

risk_columns += [
    "Performance",
    "Risk"
]

print("\nStudent Risk Analysis:")
print(df[risk_columns])

risk_counts = df["Risk"].value_counts()

print("\nRisk Distribution:")
print(risk_counts)

plt.figure(figsize=(7, 5))

plt.bar(risk_counts.index, risk_counts.values)

plt.xlabel("Risk Category")
plt.ylabel("Number of Students")
plt.title("Student Risk Distribution")

plt.tight_layout()
plt.savefig("output/charts/student_risk_distribution.png", dpi=300)
plt.show()


# ============================================================
# 29. UPDATED FINAL REPORT WITH RISK
# ============================================================

final_report_columns = [
    id_column,
    name_column,
    "Total Marks",
    "Average",
    "Grade",
    "Status",
    "Performance",
    "Risk"
]

final_report = df[final_report_columns]

final_report.to_csv(
    final_report_file,
    index=False
)

print("\nFinal report updated successfully!")


# ============================================================
# 30. RISK PERCENTAGES
# ============================================================

risk_percentage = (risk_counts / len(df)) * 100

print("\nRisk Percentages:")
print(risk_percentage.round(2))

plt.figure(figsize=(7, 7)) 

plt.pie(
    risk_percentage.values,
    labels=risk_percentage.index,
    autopct="%1.1f%%"
)

plt.title("Risk Percentage Distribution")

plt.tight_layout()
plt.savefig("output/charts/risk_percentage_distribution.png", dpi=300)
plt.show()


# ============================================================
# 31. AT-RISK STUDENTS
# ============================================================

at_risk_students = df[
    df["Risk"] == "At Risk"
]

at_risk_columns = [
    name_column,
    "Average"
]

if attendance_column is not None:
    at_risk_columns.append(attendance_column)

at_risk_columns += [
    "Grade",
    "Risk"
]

print("\nAt Risk Students:")
print(
    at_risk_students[at_risk_columns]
)

at_risk_count = (
    df["Risk"] == "At Risk"
).sum()

at_risk_percentage = (
    at_risk_count / len(df)
) * 100

print(
    "\nAt Risk Percentage:",
    round(at_risk_percentage, 2),
    "%"
)


# ============================================================
# 32. SPECIAL CASE ANALYSIS
# ============================================================

low_performance_good_attendance = pd.DataFrame()

low_attendance_good_performance = pd.DataFrame()

if attendance_column is not None:

    attendance_series = pd.to_numeric(
        df[attendance_column],
        errors="coerce"
    )

    low_performance_good_attendance = df[
        (df["Average"] < 70)
        & (attendance_series >= 75)
    ]

    print("\nLow Performance but Good Attendance:")
    print(
        low_performance_good_attendance[
            [name_column, "Average", attendance_column, "Grade", "Performance"]
        ]
    )

    low_attendance_good_performance = df[
        (attendance_series < 75)
        & (df["Average"] >= 70)
    ]

    print("\nLow Attendance but Good Performance:")
    print(
        low_attendance_good_performance[
            [name_column, "Average", attendance_column, "Grade", "Performance"]
        ]
    )

else:
    print(
        "\nSpecial attendance-based analysis skipped "
        "because no attendance column was found."
    )


# ============================================================
# 33. BEST STUDENT IN EACH SUBJECT
# ============================================================

print("\nBest Student in Each Subject:")

for subject in subjects:
    best_student = df.loc[df[subject].idxmax()]

    print(
        subject + ":",
        best_student[name_column],
        "-",
        best_student[subject]
    )


# ============================================================
# 34. WEAKEST STUDENT IN EACH SUBJECT
# ============================================================

print("\nWeakest Student in Each Subject:")

for subject in subjects:
    weakest_student = df.loc[df[subject].idxmin()]

    print(
        subject + ":",
        weakest_student[name_column],
        "-",
        weakest_student[subject]
    )


# ============================================================
# 35. COMPLETE ANALYSIS REPORT
# ============================================================

analysis_report_columns = [
    id_column,
    name_column
]

analysis_report_columns += subjects

if attendance_column is not None:
    analysis_report_columns.append(attendance_column)

analysis_report_columns += [
    "Total Marks",
    "Average",
    "Grade",
    "Status",
    "Performance",
    "Risk"
]

analysis_report = df[analysis_report_columns]

analysis_report_file = "output/complete_analysis_report.csv"

analysis_report.to_csv(
    analysis_report_file,
    index=False
)

print("\nComplete analysis report saved successfully!")
print("File:", analysis_report_file)


# ============================================================
# 36. SUBJECT STATISTICS REPORT
# ============================================================

subject_report = []

for subject in subjects:
    marks = df[subject].to_numpy()

    subject_report.append({
        "Subject": subject,
        "Average": np.mean(marks),
        "Highest": np.max(marks),
        "Lowest": np.min(marks),
        "Standard Deviation": np.std(marks)
    })

subject_report = pd.DataFrame(subject_report)

subject_report_file = "output/subject_statistics.csv"

subject_report.to_csv(
    subject_report_file,
    index=False
)

print("\nSubject statistics saved successfully!")
print("File:", subject_report_file)


# ============================================================
# 37. RISK ANALYSIS REPORT
# ============================================================

risk_report_columns = [
    id_column,
    name_column,
    "Average"
]

if attendance_column is not None:
    risk_report_columns.append(attendance_column)

risk_report_columns += [
    "Grade",
    "Performance",
    "Risk"
]

risk_report = df[risk_report_columns]

risk_report_file = "output/risk_analysis_report.csv"

risk_report.to_csv(
    risk_report_file,
    index=False
)

print("\nRisk analysis report saved successfully!")
print("File:", risk_report_file)


# ============================================================
# 38. DASHBOARD
# ============================================================

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)

plt.bar(subject_names, subject_means)

plt.xlabel("Subjects")
plt.ylabel("Average Marks")
plt.title("Subject Average")

plt.xticks(rotation=45, ha="right", fontsize=10)
plt.tight_layout()


plt.subplot(2, 2, 2)

plt.bar(grade_counts.index, grade_counts.values)

plt.xlabel("Grade")
plt.ylabel("Students")
plt.title("Grade Distribution")


plt.subplot(2, 2, 3)

if attendance_column is not None:
    attendance_values = pd.to_numeric(
        df[attendance_column],
        errors="coerce"
    )

    valid = attendance_values.notna()

    plt.scatter(
        attendance_values[valid],
        df.loc[valid, "Average"]
    )

    plt.xlabel(str(attendance_column))
    plt.ylabel("Average Marks")
    plt.title("Attendance vs Performance")

else:
    plt.bar(
        performance_counts.index,
        performance_counts.values
    )

    plt.xlabel("Performance")
    plt.ylabel("Students")
    plt.title("Performance Distribution")


plt.subplot(2, 2, 4)

plt.bar(
    risk_counts.index,
    risk_counts.values
)

plt.xlabel("Risk")
plt.ylabel("Students")
plt.title("Risk Distribution")

plt.tight_layout()

dashboard_file = "output/student_performance_dashboard.png"

plt.savefig(
    dashboard_file,
    dpi=300,
    bbox_inches="tight"
)

print("\nDashboard saved successfully!")
print("File:", dashboard_file)

plt.show()


# ============================================================
# 39. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 50)
print("STUDENT PERFORMANCE ANALYZER")
print("=" * 50)

print("Total Students:", len(df))

print(
    "Overall Average:",
    round(np.mean(df["Average"]), 2)
)

print(
    "Highest Average:",
    round(np.max(df["Average"]), 2)
)

print(
    "Lowest Average:",
    round(np.min(df["Average"]), 2)
)

print(
    "Pass Percentage:",
    round(pass_percentage, 2),
    "%"
)

print(
    "At Risk Percentage:",
    round(at_risk_percentage, 2),
    "%"
)

print(
    "Strongest Subject:",
    strongest_subject
)

print(
    "Weakest Subject:",
    weakest_subject
)

print(
    "Most Consistent Subject:",
    most_consistent_subject
)

print("=" * 50)
print("Analysis completed successfully!")
print("=" * 50)
