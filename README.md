# Online Examination System

This is a comprehensive online examination system built with Django. It provides a platform for professors to create and manage exams, and for students to take them in a secure and user-friendly environment. The user interface has been designed to be fun and engaging, especially for younger users.

## ✨ Features

- **Separate Student and Professor Portals:** Distinct interfaces for students and faculty.
- **Kid-Friendly User Interface:** A fun, colorful, and intuitive theme across the entire application.
- **Course Management:** Professors can create courses and enroll students.
- **Exam Creation:**
    - Create question papers by selecting from a question bank.
    - Set exam start and end times.
    - Associate exams with specific courses.
- **Exam Experience:**
    - One-question-at-a-time view to reduce overwhelm.
    - Progress bar to track completion.
    - Countdown timer.
- **Automated Grading:** Scores are calculated automatically upon submission.
- **Result Viewing:** Students can view their results immediately after completing an exam.
- **Cross-Window Communication:** The exam window automatically closes upon submission, and the main window redirects to the results page.

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

It's highly recommended to use a virtual environment to keep project dependencies isolated.

```bash
# For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```
*(Note: If a `requirements.txt` file is not present, you may need to install Django manually: `pip install django`)*

### 4. Set Up the Database

This project uses SQLite, which is configured by default. Run the following commands to create the database and apply the necessary structure.

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Create an Administrator Account

You'll need a superuser account to access the Django admin panel, where you can manage users and groups.

```bash
python3 manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

Once everything is set up, you can start the development server.

```bash
python3 manage.py runserver
```
The application will be available at `http://127.0.0.1:8000`.

## 📝 How to Use the System

### Step 1: Create User Groups

For the course management system to work, you first need to create two essential user groups.

1.  Navigate to the admin panel: `http://127.0.0.1:8000/admin/`
2.  Log in with your superuser credentials.
3.  Go to **Groups** and click **"Add Group"**.
4.  Create a group named `Professor`.
5.  Create another group named `Student`.

### Step 2: Create Users (Professors and Students)

1.  In the admin panel, go to **Users** and click **"Add User"**.
2.  Create users for your professors and students.
3.  **Crucially**, assign each user to the appropriate group (`Professor` or `Student`) in the "Groups" section of the user creation page.

### Step 3: Manage Courses (as a Professor)

1.  Log out of the admin account and log in as a professor.
2.  On the sidebar, click **"📚 Courses"**.
3.  Here you can create new courses and click **"Manage"** to add students to them.

### Step 4: Create and Assign Exams (as a Professor)

1.  Follow the three-step exam creation process from the faculty dashboard.
2.  When creating a **"New Main Exam"**, you will now see a **Course** dropdown menu.
3.  Select the course to which this exam belongs.

### Step 5: Take an Exam (as a Student)

1.  Log in as a student who has been enrolled in a course.
2.  The student will now see the exams that are available for their enrolled courses.
3.  Click **"Appear Now!"** to start an exam.
4.  Upon submission, the exam window will close, and the main window will display the results.
