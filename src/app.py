import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
}

.subtitle {
    font-size: 18px;
    opacity: 0.75;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_column(column):
    return (
        str(column)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def find_column(columns, variants):

    normalized_columns = {
        normalize_column(column): column
        for column in columns
    }

    for variant in variants:

        key = normalize_column(variant)

        if key in normalized_columns:
            return normalized_columns[key]

    return None


def detect_columns(df):

    # -----------------------------
    # Name
    # -----------------------------

    name_variants = [
        "Name",
        "Student_Name",
        "Full_Name",
        "Student",
        "Learner_Name"
    ]

    name_column = find_column(
        df.columns,
        name_variants
    )


    # -----------------------------
    # ID
    # -----------------------------

    id_variants = [
        "Student_ID",
        "ID",
        "Roll_No",
        "Roll_Number",
        "Registration_No",
        "Registration_Number",
        "Roll",
        "Student_Number"
    ]

    id_column = find_column(
        df.columns,
        id_variants
    )


    # -----------------------------
    # Attendance
    # -----------------------------

    attendance_column = None

    for column in df.columns:

        if "attendance" in str(column).lower():

            attendance_column = column
            break


    # -----------------------------
    # Numeric columns
    # -----------------------------

    numeric_columns = list(
        df.select_dtypes(include=np.number).columns
    )


    # -----------------------------
    # Exclude ID + Attendance
    # -----------------------------

    excluded_columns = set()

    if id_column is not None:
        excluded_columns.add(id_column)

    if attendance_column is not None:
        excluded_columns.add(attendance_column)


    # -----------------------------
    # Subjects
    # -----------------------------

    subjects = [
        column
        for column in numeric_columns
        if column not in excluded_columns
    ]


    return (
        name_column,
        id_column,
        attendance_column,
        subjects
    )


def calculate_grade(average):

    if average >= 90:
        return "A+"

    elif average >= 80:
        return "A"

    elif average >= 70:
        return "B"

    elif average >= 60:
        return "C"

    elif average >= 50:
        return "D"

    else:
        return "F"


def calculate_status(average):

    if average >= 50:
        return "Pass"

    return "Fail"


def calculate_risk(row, attendance_column):

    average = row["Average"]


    # If attendance exists
    if attendance_column is not None:

        attendance = row[attendance_column]

        if average < 50 or attendance < 60:
            return "High"

        elif average < 60 or attendance < 75:
            return "Medium"

        else:
            return "Low"


    # If attendance doesn't exist
    if average < 50:
        return "High"

    elif average < 60:
        return "Medium"

    else:
        return "Low"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🎓 Student Performance Analyzer'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload any student CSV and automatically analyze performance.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Analyzer")

    uploaded_file = st.file_uploader(
        "📁 Upload Student CSV",
        type=["csv"]
    )

    st.divider()

    st.write("### Supported Features")

    st.write("✅ Automatic subject detection")
    st.write("✅ Average & total marks")
    st.write("✅ Grade calculation")
    st.write("✅ Pass / Fail")
    st.write("✅ Attendance analysis")
    st.write("✅ Risk analysis")
    st.write("✅ Interactive dashboard")


# ============================================================
# NO FILE
# ============================================================

if uploaded_file is None:

    st.info(
        "👈 Upload a CSV file from the sidebar to begin."
    )

    st.subheader("📌 Example CSV")

    st.code("""
Student_ID,Name,Programming,Mathematics,Attendance
STU001,Ali,85,78,90
STU002,Sara,92,88,95
STU003,Ahmed,65,72,80
""")

    st.stop()


# ============================================================
# READ CSV
# ============================================================

try:

    df = pd.read_csv(uploaded_file)

except Exception as error:

    st.error(
        f"❌ Error reading CSV: {error}"
    )

    st.stop()


if df.empty:

    st.error("❌ The uploaded CSV is empty.")

    st.stop()


# ============================================================
# DETECT COLUMNS
# ============================================================

(
    name_column,
    id_column,
    attendance_column,
    subjects
) = detect_columns(df)


# ============================================================
# CREATE FALLBACK NAME
# ============================================================

if name_column is None:

    df["Student_Name_Auto"] = [
        f"Student {i + 1}"
        for i in range(len(df))
    ]

    name_column = "Student_Name_Auto"


# ============================================================
# CREATE FALLBACK ID
# ============================================================

if id_column is None:

    df["Student_ID_Auto"] = [
        f"STU{i + 1:03d}"
        for i in range(len(df))
    ]

    id_column = "Student_ID_Auto"


# ============================================================
# CHECK SUBJECTS
# ============================================================

if len(subjects) == 0:

    st.error(
        "❌ No numeric subject columns were detected."
    )

    st.write("Detected columns:")

    st.write(list(df.columns))

    st.stop()


# ============================================================
# CONVERT SUBJECTS TO NUMERIC
# ============================================================

for subject in subjects:

    df[subject] = pd.to_numeric(
        df[subject],
        errors="coerce"
    )


# ============================================================
# HANDLE MISSING SUBJECT VALUES
# ============================================================

for subject in subjects:

    if df[subject].isna().any():

        mean_value = df[subject].mean()

        df[subject] = df[subject].fillna(
            mean_value
        )


# ============================================================
# ATTENDANCE
# ============================================================

if attendance_column is not None:

    df[attendance_column] = pd.to_numeric(
        df[attendance_column],
        errors="coerce"
    )

    attendance_mean = df[attendance_column].mean()

    df[attendance_column] = (
        df[attendance_column]
        .fillna(attendance_mean)
    )


# ============================================================
# CALCULATIONS
# ============================================================

# Average
df["Average"] = df[subjects].mean(axis=1)


# Total
df["Total Marks"] = df[subjects].sum(axis=1)


# Grade
df["Grade"] = df["Average"].apply(
    calculate_grade
)


# Pass / Fail
df["Status"] = df["Average"].apply(
    calculate_status
)


# Risk
df["Risk"] = df.apply(
    lambda row: calculate_risk(
        row,
        attendance_column
    ),
    axis=1
)


# ============================================================
# SUCCESS
# ============================================================

st.success(
    f"✅ {uploaded_file.name} loaded successfully!"
)


# ============================================================
# AUTOMATIC DETECTION
# ============================================================

with st.expander(
    "🔍 View Automatic Column Detection",
    expanded=False
):

    col1, col2, col3 = st.columns(3)


    with col1:

        st.write("🆔 **Student ID**")

        st.info(id_column)


    with col2:

        st.write("👤 **Student Name**")

        st.info(name_column)


    with col3:

        st.write("📅 **Attendance**")

        if attendance_column:

            st.info(attendance_column)

        else:

            st.info("Not available")


    st.write("📚 **Detected Subjects**")

    st.success(
        f"{len(subjects)} subjects detected"
    )

    st.write(subjects)


# ============================================================
# TABS
# ============================================================

dashboard_tab, students_tab, analytics_tab, risk_tab, report_tab = st.tabs(
    [
        "📊 Dashboard",
        "👨‍🎓 Students",
        "📈 Analytics",
        "⚠️ Risk Analysis",
        "📋 Reports"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

with dashboard_tab:

    st.header("📊 Performance Dashboard")


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    total_students = len(df)

    overall_average = df["Average"].mean()

    pass_percentage = (
        df["Status"].eq("Pass").mean() * 100
    )

    at_risk = df[
        df["Risk"].isin(
            ["Medium", "High"]
        )
    ].shape[0]


    col1, col2, col3, col4, col5 = st.columns(5)


    col1.metric(
        "👨‍🎓 Students",
        total_students
    )


    col2.metric(
        "📊 Average",
        f"{overall_average:.2f}%"
    )


    col3.metric(
        "✅ Pass %",
        f"{pass_percentage:.1f}%"
    )


    col4.metric(
        "⚠️ At Risk",
        at_risk
    )


    if attendance_column:

        average_attendance = (
            df[attendance_column].mean()
        )

        col5.metric(
            "📅 Attendance",
            f"{average_attendance:.1f}%"
        )

    else:

        col5.metric(
            "📚 Subjects",
            len(subjects)
        )


    st.divider()


    # --------------------------------------------------------
    # SUBJECT AVERAGE
    # --------------------------------------------------------

    chart_col, top_col = st.columns(
        [1.5, 1]
    )


    with chart_col:

        st.subheader(
            "📚 Subject-wise Average"
        )

        subject_average = (
            df[subjects]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        fig, ax = plt.subplots(
            figsize=(9, 5)
        )

        subject_average.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "Subject-wise Average"
        )

        ax.set_ylabel(
            "Average Marks"
        )

        ax.set_xlabel(
            "Subjects"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


    # --------------------------------------------------------
    # TOP STUDENTS
    # --------------------------------------------------------

    with top_col:

        st.subheader(
            "🏆 Top 5 Students"
        )

        top5 = (
            df.sort_values(
                "Average",
                ascending=False
            )
            .head(5)
        )


        st.dataframe(
            top5[
                [
                    name_column,
                    "Average",
                    "Grade"
                ]
            ].reset_index(
                drop=True
            ),
            use_container_width=True,
            hide_index=True
        )


    # --------------------------------------------------------
    # GRADE DISTRIBUTION
    # --------------------------------------------------------

    st.subheader(
        "🎯 Grade Distribution"
    )

    grade_order = [
        "A+",
        "A",
        "B",
        "C",
        "D",
        "F"
    ]

    grade_counts = (
        df["Grade"]
        .value_counts()
        .reindex(
            grade_order,
            fill_value=0
        )
    )


    fig, ax = plt.subplots(
        figsize=(9, 4)
    )

    grade_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Grade Distribution"
    )

    ax.set_xlabel("Grade")

    ax.set_ylabel(
        "Number of Students"
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# STUDENTS
# ============================================================

with students_tab:

    st.header(
        "👨‍🎓 Student Performance"
    )


    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        search = st.text_input(
            "🔍 Search Student",
            placeholder="Name or ID..."
        )


    with col2:

        grades = [
            "All"
        ] + sorted(
            df["Grade"].unique().tolist()
        )

        selected_grade = st.selectbox(
            "🎓 Grade",
            grades
        )


    with col3:

        selected_risk = st.selectbox(
            "⚠️ Risk",
            [
                "All",
                "Low",
                "Medium",
                "High"
            ]
        )


    filtered_df = df.copy()


    # Search
    if search:

        search = search.lower()

        name_match = (
            filtered_df[name_column]
            .astype(str)
            .str.lower()
            .str.contains(
                search,
                na=False
            )
        )

        id_match = (
            filtered_df[id_column]
            .astype(str)
            .str.lower()
            .str.contains(
                search,
                na=False
            )
        )

        filtered_df = filtered_df[
            name_match | id_match
        ]


    # Grade filter
    if selected_grade != "All":

        filtered_df = filtered_df[
            filtered_df["Grade"]
            == selected_grade
        ]


    # Risk filter
    if selected_risk != "All":

        filtered_df = filtered_df[
            filtered_df["Risk"]
            == selected_risk
        ]


    # --------------------------------------------------------
    # DISPLAY TABLE
    # --------------------------------------------------------

    display_columns = [
        id_column,
        name_column,
        *subjects,
        "Total Marks",
        "Average",
        "Grade",
        "Status"
    ]


    if attendance_column:

        display_columns.append(
            attendance_column
        )


    display_columns.append(
        "Risk"
    )


    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True
    )


    st.caption(
        f"Showing {len(filtered_df)} "
        f"of {len(df)} students."
    )


    st.divider()


    # --------------------------------------------------------
    # INDIVIDUAL STUDENT
    # --------------------------------------------------------

    st.subheader(
        "🔎 Individual Student Analysis"
    )


    student_names = (
        df[name_column]
        .astype(str)
        .tolist()
    )


    selected_student = st.selectbox(
        "Select Student",
        student_names
    )


    student = df[
        df[name_column].astype(str)
        == selected_student
    ].iloc[0]


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "📊 Average",
        f"{student['Average']:.2f}%"
    )


    c2.metric(
        "🎓 Grade",
        student["Grade"]
    )


    c3.metric(
        "📌 Status",
        student["Status"]
    )


    c4.metric(
        "⚠️ Risk",
        student["Risk"]
    )


    if attendance_column:

        st.metric(
            "📅 Attendance",
            f"{student[attendance_column]:.2f}%"
        )


    st.subheader(
        "📚 Subject Performance"
    )


    subject_data = pd.DataFrame({

        "Subject": subjects,

        "Marks": [
            student[subject]
            for subject in subjects
        ]

    })


    st.dataframe(
        subject_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ANALYTICS
# ============================================================

with analytics_tab:

    st.header(
        "📈 Detailed Analytics"
    )


    # --------------------------------------------------------
    # SUBJECT STATISTICS
    # --------------------------------------------------------

    st.subheader(
        "📚 Subject Statistics"
    )


    statistics = []


    for subject in subjects:

        marks = df[subject].to_numpy()


        statistics.append({

            "Subject": subject,

            "Average": np.mean(marks),

            "Highest": np.max(marks),

            "Lowest": np.min(marks),

            "Std Dev": np.std(marks)

        })


    statistics_df = pd.DataFrame(
        statistics
    )


    st.dataframe(
        statistics_df.round(2),
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # STRONGEST / WEAKEST
    # --------------------------------------------------------

    subject_averages = {
        subject: df[subject].mean()
        for subject in subjects
    }


    strongest = max(
        subject_averages,
        key=subject_averages.get
    )


    weakest = min(
        subject_averages,
        key=subject_averages.get
    )


    c1, c2 = st.columns(2)


    c1.success(
        f"🏆 Strongest Subject: "
        f"**{strongest}** "
        f"({subject_averages[strongest]:.2f})"
    )


    c2.warning(
        f"📉 Weakest Subject: "
        f"**{weakest}** "
        f"({subject_averages[weakest]:.2f})"
    )


    # --------------------------------------------------------
    # CONSISTENCY
    # --------------------------------------------------------

    st.subheader(
        "📏 Student Consistency"
    )


    consistency = df[
        [name_column]
    ].copy()


    consistency["Average"] = df[
        "Average"
    ]


    consistency["Std Dev"] = df[
        subjects
    ].std(axis=1)


    consistency["Consistency"] = np.where(

        consistency["Std Dev"] <= 5,

        "Very Consistent",

        np.where(

            consistency["Std Dev"] <= 10,

            "Moderately Consistent",

            "Less Consistent"
        )
    )


    st.dataframe(
        consistency.sort_values(
            "Std Dev"
        ),
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # ATTENDANCE CORRELATION
    # --------------------------------------------------------

    if attendance_column:

        st.subheader(
            "📅 Attendance vs Performance"
        )


        correlation = np.corrcoef(

            df[attendance_column],

            df["Average"]

        )[0, 1]


        st.metric(
            "Correlation",
            f"{correlation:.3f}"
        )


        fig, ax = plt.subplots(
            figsize=(9, 5)
        )


        ax.scatter(
            df[attendance_column],
            df["Average"]
        )


        ax.set_xlabel(
            "Attendance (%)"
        )

        ax.set_ylabel(
            "Average Marks"
        )

        ax.set_title(
            "Attendance vs Performance"
        )


        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# RISK ANALYSIS
# ============================================================

with risk_tab:

    st.header(
        "⚠️ Risk Analysis"
    )


    risk_counts = (
        df["Risk"]
        .value_counts()
        .reindex(
            [
                "Low",
                "Medium",
                "High"
            ],
            fill_value=0
        )
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "🟢 Low Risk",
        int(risk_counts["Low"])
    )


    c2.metric(
        "🟡 Medium Risk",
        int(risk_counts["Medium"])
    )


    c3.metric(
        "🔴 High Risk",
        int(risk_counts["High"])
    )


    # --------------------------------------------------------
    # RISK CHART
    # --------------------------------------------------------

    st.subheader(
        "📊 Risk Distribution"
    )


    fig, ax = plt.subplots(
        figsize=(8, 5)
    )


    risk_counts.plot(
        kind="bar",
        ax=ax
    )


    ax.set_title(
        "Student Risk Distribution"
    )

    ax.set_xlabel(
        "Risk Level"
    )

    ax.set_ylabel(
        "Number of Students"
    )


    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


    # --------------------------------------------------------
    # AT-RISK STUDENTS
    # --------------------------------------------------------

    st.subheader(
        "🚨 Students Needing Attention"
    )


    at_risk_df = df[
        df["Risk"].isin(
            ["Medium", "High"]
        )
    ]


    risk_columns = [
        id_column,
        name_column,
        "Average",
        "Grade",
        "Status"
    ]


    if attendance_column:

        risk_columns.append(
            attendance_column
        )


    risk_columns.append(
        "Risk"
    )


    if at_risk_df.empty:

        st.success(
            "🎉 No students are currently at risk!"
        )

    else:

        st.dataframe(
            at_risk_df[
                risk_columns
            ].sort_values(
                "Average"
            ),
            use_container_width=True,
            hide_index=True
        )


    # --------------------------------------------------------
    # LOW ATTENDANCE
    # --------------------------------------------------------

    if attendance_column:

        st.subheader(
            "📅 Students with Low Attendance"
        )


        low_attendance = df[
            df[attendance_column] < 75
        ]


        if low_attendance.empty:

            st.success(
                "✅ No student has attendance below 75%."
            )

        else:

            st.dataframe(

                low_attendance[
                    [
                        id_column,
                        name_column,
                        attendance_column,
                        "Average",
                        "Grade",
                        "Risk"
                    ]
                ].sort_values(
                    attendance_column
                ),

                use_container_width=True,

                hide_index=True
            )


# ============================================================
# REPORTS
# ============================================================

with report_tab:

    st.header(
        "📋 Reports & Downloads"
    )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "📌 Final Summary"
    )


    st.write(
        f"👨‍🎓 **Total Students:** {len(df)}"
    )


    st.write(
        f"📚 **Total Subjects:** {len(subjects)}"
    )


    st.write(
        f"📊 **Overall Average:** "
        f"{df['Average'].mean():.2f}%"
    )


    st.write(
        f"✅ **Pass Percentage:** "
        f"{(df['Status'] == 'Pass').mean() * 100:.2f}%"
    )


    if attendance_column:

        st.write(
            f"📅 **Average Attendance:** "
            f"{df[attendance_column].mean():.2f}%"
        )


    st.write(
        f"🏆 **Strongest Subject:** {strongest}"
    )


    st.write(
        f"📉 **Weakest Subject:** {weakest}"
    )


    st.write(
        f"⚠️ **At-Risk Students:** {at_risk}"
    )


    st.divider()


    # --------------------------------------------------------
    # DOWNLOAD CSV
    # --------------------------------------------------------

    st.subheader(
        "⬇️ Download Analyzed CSV"
    )


    analyzed_csv = df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(

        label="⬇️ Download Analysis CSV",

        data=analyzed_csv,

        file_name="student_performance_analysis.csv",

        mime="text/csv"

    )


    # --------------------------------------------------------
    # TEXT REPORT
    # --------------------------------------------------------

    report = []

    report.append(
        "STUDENT PERFORMANCE ANALYZER"
    )

    report.append(
        "=" * 50
    )

    report.append(
        f"Total Students: {len(df)}"
    )

    report.append(
        f"Total Subjects: {len(subjects)}"
    )

    report.append(
        f"Overall Average: {df['Average'].mean():.2f}%"
    )

    report.append(
        f"Pass Percentage: "
        f"{(df['Status'] == 'Pass').mean() * 100:.2f}%"
    )


    if attendance_column:

        report.append(
            f"Average Attendance: "
            f"{df[attendance_column].mean():.2f}%"
        )


    report.append("")

    report.append(
        "SUBJECT AVERAGES"
    )

    report.append(
        "-" * 50
    )


    for subject in subjects:

        report.append(
            f"{subject}: "
            f"{df[subject].mean():.2f}"
        )


    report.append("")

    report.append(
        "TOP 5 STUDENTS"
    )

    report.append(
        "-" * 50
    )


    top5 = (
        df.sort_values(
            "Average",
            ascending=False
        )
        .head(5)
    )


    for i, (_, row) in enumerate(
        top5.iterrows(),
        start=1
    ):

        report.append(
            f"{i}. {row[name_column]} - "
            f"{row['Average']:.2f}% - "
            f"Grade {row['Grade']}"
        )


    report.append("")

    report.append(
        "RISK SUMMARY"
    )

    report.append(
        "-" * 50
    )


    for risk in [
        "Low",
        "Medium",
        "High"
    ]:

        report.append(
            f"{risk}: "
            f"{risk_counts.get(risk, 0)}"
        )


    report_text = "\n".join(
        report
    )


    st.download_button(

        label="📄 Download Text Report",

        data=report_text,

        file_name="student_performance_report.txt",

        mime="text/plain"

    )


    # --------------------------------------------------------
    # REPORT PREVIEW
    # --------------------------------------------------------

    st.subheader(
        "👁️ Report Preview"
    )


    st.text(
        report_text
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎓 Student Performance Analyzer | "
    "Python + Pandas + NumPy + Matplotlib + Streamlit"
)