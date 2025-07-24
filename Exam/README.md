# Online Examination System

This is a comprehensive online examination system built with Django. It provides a platform for professors to create and manage exams, and for students to take them in a secure and user-friendly environment. The user interface has been designed to be fun and engaging, especially for younger users.

## ✨ Features

- **Course-Centric Management:** Professors can create courses and manage all related content—question banks, question papers, and exams—from a dedicated course dashboard.
- **Separate Student and Professor Portals:** Distinct interfaces for students and faculty.
- **Kid-Friendly User Interface:** A fun, colorful, and intuitive theme across the entire application.
- **Student Dashboards:** Students get an at-a-glance overview of their performance, including stats and charts.
- **Exam Experience:**
    - One-question-at-a-time view to reduce overwhelm.
    - Progress bar to track completion.
    - Countdown timer.
- **Automated Grading & Review:** Scores are calculated automatically, and students can review their answers with explanations.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Online-Examination-System/Exam
```

### 2. Set Up a Virtual Environment

```bash
# For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
*(Note: If a `requirements.txt` file is not present, you may need to install Django manually: `pip install django`)*

### 4. Set Up the Database

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Create an Administrator Account

```bash
python3 manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

```bash
python3 manage.py runserver
```
The application will be available at `http://127.0.0.1:8000`.

## 📝 How to Use the System

### Step 1: Create User Groups

1.  Navigate to the admin panel: `http://127.0.0.1:8000/admin/`
2.  Log in with your superuser credentials.
3.  Go to **Groups** and click **"Add Group"**.
4.  Create a group named `Professor`.
5.  Create another group named `Student`.

### Step 2: Create Users (Professors and Students)

1.  In the admin panel, go to **Users** and click **"Add User"**.
2.  Create users for your professors and students.
3.  Assign each user to the appropriate group (`Professor` or `Student`).

### Step 3: The Professor's Workflow (Course-Centric)

The entire exam creation process is now managed on a per-course basis.

1.  **Log in as a Professor.**
2.  **Create a Course:**
    -   Click on **"📚 Courses"** in the sidebar.
    -   Create a new course.
3.  **Manage the Course:**
    -   From the course list, click **"Manage"** on the course you want to work with. This will take you to the **Course Dashboard**.
4.  **From the Course Dashboard, you can:**
    -   **Manage Questions:** Add, edit, or delete questions for this course's specific question bank.
    -   **Manage Papers:** Create question papers using the questions from the course's bank.
    -   **Manage Exams:** Create exams using the question papers from that course.
    -   **Manage Students:** Enroll students in the course.

### Step 4: The Student's Workflow

1.  **Log in as a Student.**
2.  The student will see their personalized dashboard, including upcoming exams for the courses they are enrolled in.
3.  They can take an exam, and after submitting, they can view their results and review their answers.
