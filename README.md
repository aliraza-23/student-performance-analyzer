# 🎓 Student Performance Analyzer

A Python-based **Student Performance Analyzer** that processes student marks and attendance data, calculates academic performance metrics, identifies performance and risk levels, generates visual reports, and provides an interactive **Streamlit web dashboard**.

The project is designed to work with different CSV datasets by automatically detecting student information, attendance, and numeric subject columns instead of relying on fixed subject names.

---

## ✨ Features

### 📊 Data Analysis

- Load student data from CSV files using Pandas
- Inspect dataset shape, columns, statistics, missing values, and duplicates
- Automatically detect:
  - Student Name
  - Student ID / Roll Number / Registration Number
  - Attendance column
  - Numeric subject columns
- Support datasets with different subject names and different numbers of subjects
- Calculate:
  - Total marks
  - Average marks
  - Highest and lowest averages
  - Subject-wise averages
  - Subject-wise highest and lowest marks
  - Standard deviation
  - Strongest and weakest subjects

### 🎓 Academic Performance

- Automatic grade calculation
- Pass / Fail classification
- Performance categories:
  - Excellent
  - Good
  - Needs Improvement
- Top-performing students
- Student consistency analysis

### 📅 Attendance Analysis

When an attendance column is available, the analyzer can calculate:

- Average attendance
- Attendance vs. performance correlation
- Students with low attendance
- Attendance-based risk classification

If attendance is not present, attendance-specific analysis is skipped automatically.

### ⚠️ Risk Analysis

Students are classified into:

- 🟢 Low Risk
- 🟡 Medium Risk
- 🔴 High Risk

Risk analysis considers academic performance and, when available, attendance.

### 📈 Visualizations

The project generates charts for:

- Student average performance
- Subject-wise average performance
- Grade distribution
- Performance category distribution
- Attendance vs. performance
- Student risk distribution
- Risk percentage distribution
- Top-performing students

### 🌐 Streamlit Web Application

The project also includes an interactive web interface with:

- CSV upload
- Automatic column detection
- Automatic subject detection
- Dashboard metrics
- Student performance table
- Student search
- Grade filtering
- Risk filtering
- Individual student analysis
- Subject statistics
- Attendance correlation
- Risk analysis
- Downloadable analyzed CSV
- Downloadable text report

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data loading, cleaning, transformation, and analysis |
| NumPy | Numerical calculations and statistics |
| Matplotlib | Data visualization |
| Streamlit | Interactive web application |

---

## 📁 Project Structure

```text
Student Performance Analyzer/
│
├── data/
│   └── students-sample-dataset.csv
│
├── src/
│   ├── main.py
│   └── app.py
│
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
│   │
│   ├── complete_analysis_report.csv
│   ├── final_student_report.csv
│   ├── risk_analysis_report.csv
│   ├── student_performance_analyzed.csv
│   ├── student_performance_dashboard.png
│   └── subject_statistics.csv
│
├── .gitignore
└── README.md
```

> **Note:** A local `.venv/` virtual environment may exist in the development folder. It should not be committed to GitHub. Use `.gitignore` to exclude it.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/student-performance-analyzer.git
```

Move into the project directory:

```bash
cd student-performance-analyzer
```

---

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

If PowerShell blocks script execution, you can allow locally created scripts for your current user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.venv\Scripts\activate
```

---

### 3. Install Dependencies

Install the required packages:

```bash
pip install pandas numpy matplotlib streamlit
```

If the repository contains a `requirements.txt` file, you can instead use:

```bash
pip install -r requirements.txt
```

---

# 💻 Running the Python Analyzer

The command-line/data-analysis version is located at:

```text
src/main.py
```

Run it from the project root:

```bash
python src/main.py
```

The analyzer reads the sample dataset from:

```text
data/students-sample-dataset.csv
```

and generates analysis files and charts in:

```text
output/
```

---

# 🌐 Running the Web Application

The Streamlit application is located at:

```text
src/app.py
```

Start the application with:

```bash
streamlit run src/app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open that address in your browser.

---

## 📤 Using the Web App

### Step 1 — Start the application

```bash
streamlit run src/app.py
```

### Step 2 — Upload a CSV

Use the **Upload Student CSV** control in the sidebar.

### Step 3 — Automatic Detection

The application detects:

- Student ID
- Student Name
- Attendance
- Numeric subject columns

### Step 4 — Analyze

The dashboard calculates:

- Average
- Total Marks
- Grade
- Pass/Fail
- Performance
- Risk

### Step 5 — Explore

Use the dashboard tabs:

```text
📊 Dashboard
👨‍🎓 Students
📈 Analytics
⚠️ Risk Analysis
📋 Reports
```

### Step 6 — Download

Download:

- Analyzed CSV
- Performance report

---

# 📄 CSV Dataset Format

The application is designed to support different subject names and different numbers of numeric subject columns.

A sample dataset looks like:

```csv
Student_ID,Name,Math,Programming,Database,DSA,Attendance (%)
STU001,Mohammad Ahmed,90,62,51,92,78
STU002,Ayesha Khan,65,69,58,92,73
STU003,Zainab Fatima,93,89,55,82,83
```

The subject names do **not** need to be exactly:

```text
Math
Programming
Database
DSA
```

For example, a dataset can contain:

```csv
Student_ID,Name,Programming Fundamentals,Calculus,Functional English,Islamic Studies,Information & Communication Technology,Applied Physics,Attendance (%)
```

The application detects numeric subject columns automatically.

---

# 🔍 Automatic Column Detection

The analyzer looks for common variations of student information.

### Student Name

Examples:

```text
Name
Student_Name
Full_Name
Student
Learner_Name
```

### Student ID

Examples:

```text
Student_ID
ID
Roll_No
Roll_Number
Registration_No
Registration_Number
Roll
Student_Number
```

### Attendance

Any column containing:

```text
attendance
```

is considered an attendance column.

### Subjects

Numeric columns that are not identified as ID or attendance columns are treated as subject columns.

---

# 🧮 Analysis Logic

## Average

For each student:

```text
Average = mean(all detected subject marks)
```

## Total Marks

```text
Total Marks = sum(all detected subject marks)
```

## Grades

The current grading logic in the application is:

| Average | Grade |
|---:|:---:|
| 90–100 | A+ |
| 80–89.99 | A |
| 70–79.99 | B |
| 60–69.99 | C |
| 50–59.99 | D |
| Below 50 | F |

## Pass / Fail

```text
Average >= 50 → Pass
Average < 50  → Fail
```

## Risk

When attendance is available:

```text
High Risk:
    Average < 50 OR Attendance < 60

Medium Risk:
    Average < 60 OR Attendance < 75

Low Risk:
    Otherwise
```

When attendance is unavailable, risk is based on average performance.

> These thresholds are implemented as project rules and can be modified in `src/app.py` or `src/main.py`.

---

# 📊 Output Files

The analysis version generates CSV reports such as:

### `student_performance_analyzed.csv`

Contains the original student data together with calculated analysis fields.

### `final_student_report.csv`

Contains the final student-level performance summary.

### `complete_analysis_report.csv`

Contains the broader analysis results, including marks, averages, grades, status, performance, and risk.

### `risk_analysis_report.csv`

Contains risk-related student information.

### `subject_statistics.csv`

Contains subject-level statistical information.

### Dashboard and Charts

The `output/charts/` directory contains generated visualizations, while:

```text
output/student_performance_dashboard.png
```

contains the dashboard visualization generated by the analysis workflow.

---

# 🧪 Example Workflow

```text
CSV Dataset
     │
     ▼
Load Data with Pandas
     │
     ▼
Detect Student / ID / Attendance
     │
     ▼
Detect Numeric Subjects
     │
     ▼
Clean & Prepare Data
     │
     ▼
Calculate Total & Average
     │
     ▼
Calculate Grade & Pass/Fail
     │
     ▼
Performance Analysis
     │
     ├── Subject Statistics
     ├── Top Students
     ├── Consistency
     ├── Attendance Analysis
     └── Risk Analysis
     │
     ▼
Charts & Reports
     │
     ▼
Streamlit Dashboard
```

---

# 🎯 Project Goals

This project was developed to practice and demonstrate:

- Python programming
- Pandas data analysis
- NumPy numerical operations
- Matplotlib visualization
- CSV data processing
- Dynamic dataset handling
- Data cleaning
- Statistical analysis
- Conditional logic
- Report generation
- Streamlit web application development

---

# 🔮 Possible Future Improvements

Potential extensions include:

- Interactive Plotly charts
- More flexible grading systems
- Configurable pass marks
- Configurable risk thresholds
- Multiple dataset comparison
- Teacher/admin authentication
- Student profile pages
- Database integration
- PDF report generation
- Excel report export
- More advanced statistical analysis
- Cloud deployment
- Responsive UI improvements
- Persistent storage for uploaded datasets

---

# ⚠️ Important GitHub Note

Do **not** upload the local virtual environment to GitHub.

Add this to `.gitignore`:

```gitignore
# Virtual environment
.venv/
venv/

# Python cache
__pycache__/
*.py[cod]

# Streamlit
.streamlit/secrets.toml

# IDE files
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db
```

The virtual environment can always be recreated using:

```bash
python -m venv .venv
```

and the required packages can be installed again.

---

# 👨‍💻 Author

**Ali**

Student Performance Analyzer — a Python data analysis and Streamlit dashboard project.

---

# 📜 License

This project can be distributed and modified according to the license you choose for your GitHub repository.

For an open-source repository, consider adding an appropriate license such as the **MIT License** in a separate `LICENSE` file.

---

## ⭐ If You Find This Project Useful

Feel free to:

- ⭐ Star the repository
- 🍴 Fork the project
- 🐛 Report issues
- 💡 Suggest improvements
- 🔧 Submit pull requests

---

**Built with Python 🐍, Pandas 🐼, NumPy 🔢, Matplotlib 📊, and Streamlit 🌐**
#   s t u d e n t - p e r f o r m a n c e - a n a l y z e r  
 