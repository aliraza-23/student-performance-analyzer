# 🎓 Student Performance Analyzer

A Python-based **Student Performance Analyzer** that analyzes student marks and attendance, calculates academic performance metrics, identifies at-risk students, generates visual reports, and provides an interactive **Streamlit dashboard**.

The project supports different CSV datasets by automatically detecting student information, attendance, and numeric subject columns instead of relying on fixed subject names.

## ✨ Features

### 📊 Data Analysis
- Load and analyze student data from CSV files using Pandas.
- Inspect dataset dimensions, columns, statistics, missing values, and duplicates.
- Automatically detect student names, IDs/roll numbers, attendance, and numeric subject columns.
- Support different subject names and different numbers of subjects.
- Calculate total marks, average marks, subject averages, highest/lowest marks, and standard deviation.

### 🎓 Academic Performance
- Calculate grades automatically.
- Classify students as Pass or Fail.
- Categorize performance as Excellent, Good, or Needs Improvement.
- Identify top-performing students.
- Analyze student consistency.

### 📅 Attendance Analysis
When an attendance column is available, the analyzer can calculate:
- Average attendance.
- Attendance-versus-performance correlation.
- Students with low attendance.
- Attendance-based risk classifications.

If attendance data is unavailable, attendance-specific analysis is skipped.

### ⚠️ Risk Analysis
Students are classified into:
- 🟢 Low Risk
- 🟡 Medium Risk
- 🔴 High Risk

Risk classification considers academic performance and, when available, attendance.

### 📈 Visualizations
The project can generate charts for:
- Student average performance.
- Subject-wise average performance.
- Grade and performance-category distributions.
- Attendance versus performance.
- Student risk distribution and risk percentages.
- Top-performing students.

### 🌐 Streamlit Dashboard
- Upload a CSV dataset.
- Detect student and subject columns automatically.
- View dashboard metrics and student performance tables.
- Search students and filter by grade or risk.
- Explore individual student analysis and subject statistics.
- Review attendance correlation and risk analysis.
- Download analyzed CSV data and a text report.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data loading, cleaning, and analysis |
| NumPy | Numerical calculations and statistics |
| Matplotlib | Data visualization |
| Streamlit | Interactive web dashboard |

## 📁 Project Structure

```text
student-performance-analyzer/
├── data/
│   └── students-sample-dataset.csv
├── src/
│   ├── main.py
│   └── app.py
├── output/
│   ├── charts/
│   │   ├── attendance_vs_performance.png
│   │   ├── grade_distribution.png
│   │   ├── performance_category_distribution.png
│   │   ├── risk_percentage_distribution.png
│   │   ├── student_averages_chart.png
│   │   ├── student_risk_distribution.png
│   │   ├── subject_averages_chart.png
│   │   └── top_3_students.png
│   ├── complete_analysis_report.csv
│   ├── final_student_report.csv
│   ├── risk_analysis_report.csv
│   ├── student_performance_analyzed.csv
│   ├── student_performance_dashboard.png
│   └── subject_statistics.csv
├── .gitignore
├── README.md
└── requirements.txt
```

> **Note:** This is an example structure based on the project description. Keep only files and folders that actually exist in your repository. Do not commit your local `.venv/` virtual environment.

## 🚀 Getting Started

### 1. Clone the Repository

Replace `YOUR-USERNAME` with your GitHub username:

```bash
git clone https://github.com/YOUR-USERNAME/student-performance-analyzer.git
cd student-performance-analyzer
```

If the project is already on your computer, open its folder in VS Code and skip this step.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can either configure the execution policy for your current user or run the commands without activating the environment by using `.venv\Scripts\python`.

### 3. Install Dependencies

If `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

Otherwise, install the listed packages:

```bash
pip install pandas numpy matplotlib streamlit
```

### 4. Run the Command-Line Analyzer

From the project root:

```bash
python src/main.py
```

The analyzer reads the sample dataset from `data/students-sample-dataset.csv` and, according to the project configuration, writes analysis files and charts to `output/`.

### 5. Run the Streamlit Dashboard

```bash
streamlit run src/app.py
```

Open the local URL printed in the terminal, usually:

```text
http://localhost:8501
```

## 📤 Using the Web App

1. Start the app with `streamlit run src/app.py`.
2. Upload a student CSV file using the sidebar.
3. Let the app detect student IDs, names, attendance, and numeric subject columns.
4. Review averages, total marks, grades, pass/fail status, performance, and risk.
5. Explore the Dashboard, Students, Analytics, Risk Analysis, and Reports sections if present in your app.
6. Download the available analysis files.

## 📄 CSV Dataset Format

A CSV file may look like this:

```csv
Student_ID,Name,Math,Programming,Database,DSA,Attendance (%)
STU001,Mohammad Ahmed,90,62,51,92,78
STU002,Ayesha Khan,65,69,58,92,73
STU003,Zainab Fatima,93,89,55,82,83
```

Subject names do not need to be exactly `Math`, `Programming`, `Database`, or `DSA`. The analyzer is designed to detect numeric subject columns dynamically.

For example, another dataset might use subjects such as `Programming Fundamentals`, `Calculus`, `Functional English`, `Islamic Studies`, `Information & Communication Technology`, and `Applied Physics`.

## 🔍 Automatic Column Detection

The analyzer looks for common column-name variations.

| Data type | Examples |
|---|---|
| Student name | `Name`, `Student_Name`, `Full_Name`, `Learner_Name` |
| Student ID | `Student_ID`, `ID`, `Roll_No`, `Roll_Number`, `Registration_No`, `Student_Number` |
| Attendance | Any column containing `attendance` |
| Subject marks | Numeric columns not identified as student IDs or attendance |

Detection depends on the implementation in `src/main.py` and `src/app.py`. Check those files if a column is classified incorrectly.

## 🧮 Analysis Logic

### Average and Total Marks

```text
Average = mean of all detected subject marks
Total Marks = sum of all detected subject marks
```

### Grade Boundaries

The current grading rules described for this project are:

| Average | Grade |
|---:|:---:|
| 90–100 | A+ |
| 80–89.99 | A |
| 70–79.99 | B |
| 60–69.99 | C |
| 50–59.99 | D |
| Below 50 | F |

### Pass / Fail

```text
Average >= 50  → Pass
Average < 50   → Fail
```

### Risk Classification

When attendance is available:

```text
High Risk:   Average < 50 OR Attendance < 60
Medium Risk: Average < 60 OR Attendance < 75
Low Risk:    Otherwise
```

When attendance is unavailable, risk is based on average performance.

> These are project-specific thresholds, not universal academic standards. The rules can be changed in `src/app.py` or `src/main.py`, depending on where they are implemented. Verify the code if you have changed the logic.

## 📊 Output Files

The analysis workflow may generate the following files in `output/`:

| File | Description |
|---|---|
| `student_performance_analyzed.csv` | Original student data plus calculated analysis fields |
| `final_student_report.csv` | Student-level performance summary |
| `complete_analysis_report.csv` | Broader analysis including marks, averages, grades, status, performance, and risk |
| `risk_analysis_report.csv` | Student risk information |
| `subject_statistics.csv` | Subject-level statistical information |
| `student_performance_dashboard.png` | Dashboard visualization |
| `charts/` | Generated chart images |

Actual output files depend on the workflow and configuration in your code.

## 🔄 Project Workflow

```text
CSV Dataset
    ↓
Load Data with Pandas
    ↓
Detect Student / ID / Attendance Columns
    ↓
Detect Numeric Subject Columns
    ↓
Clean and Prepare Data
    ↓
Calculate Total Marks and Average
    ↓
Calculate Grade and Pass/Fail
    ↓
Analyze Performance and Risk
    ↓
Generate Charts and Reports
    ↓
Explore Results in Streamlit Dashboard
```

## 🎯 Learning Objectives

This project demonstrates:
- Python programming.
- Pandas and NumPy data processing.
- Matplotlib visualizations.
- CSV file handling and data cleaning.
- Dynamic column detection.
- Statistical analysis and conditional logic.
- Report generation.
- Streamlit application development.

## 🔮 Future Improvements

Possible extensions include:
- Interactive Plotly charts.
- Configurable grading and pass-mark rules.
- Configurable risk thresholds.
- Comparison of multiple datasets.
- Teacher/admin authentication.
- Student profile pages.
- Database integration.
- PDF report generation and Excel export.
- Cloud deployment and responsive UI improvements.

## 🔐 Git and GitHub Safety

Do not commit your local virtual environment, Python cache files, editor settings, or secrets. A `.gitignore` file can include:

```gitignore
# Virtual environments
.venv/
venv/

# Python cache
__pycache__/
*.py[cod]

# Streamlit secrets
.streamlit/secrets.toml

# Editor settings
.vscode/
.idea/

# Operating system files
.DS_Store
Thumbs.db
```

Keep any real API keys, passwords, or private credentials out of GitHub.

## 👨‍💻 Author

**Ali**

Student Performance Analyzer — a Python data-analysis and Streamlit dashboard project.

## 📜 License

No specific license is stated here. If you want others to reuse and modify the project, choose a license and add its terms in a separate `LICENSE` file.

## ⭐ Support

If you find this project useful, you can:
- Star the repository.
- Fork it.
- Report issues.
- Suggest improvements.
- Submit pull requests.

---

**Built with Python 🐍, Pandas 🐼, NumPy 🔢, Matplotlib 📊, and Streamlit 🌐**
