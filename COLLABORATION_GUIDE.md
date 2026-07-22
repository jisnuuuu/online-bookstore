# 📖 NovelNest: Local Setup & Git Guide

Welcome to your Python internship group project! Here is how to set up the code on your machines and start collaborating.

---

## 💻 Local Setup Instructions

Follow these steps on both of your computers:

### 1. Set Up a Virtual Environment
A virtual environment keeps your project's dependencies separate from your global Python installation.

Open your terminal in the `online_book` directory and run:
```bash
# Create the virtual environment (named 'venv')
python -m venv venv

# Activate it
# On Windows (Command Prompt):
venv\Scripts\activate
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Project Dependencies
With the virtual environment activated, install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Seed the Database
Run the database seed script to populate your local database file (`instance/database.db` or `database.db`) with test books:
```bash
python seed_db.py
```

### 4. Run the Development Server
Start the Flask local development server:
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000/`**

---

## 🐙 Git Collaboration Guide

Since this is your first group project, follow this exact workflow to make collaboration smooth and conflict-free!

### Step 1: Initialize Git & Push the Skeleton (Only Person A does this once)
1. Initialize git locally:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: project skeleton"
   ```
2. Create a new **private or public repository** on [GitHub](https://github.com).
3. Connect your local directory to GitHub:
   ```bash
   git remote add origin <your-github-repo-url>
   git branch -M main
   git push -u origin main
   ```
4. On GitHub, go to **Settings > Collaborators** and invite **Person B** by their email/GitHub username.

### Step 2: Clone the Repo (Only Person B does this once)
Once Person B accepts the invite, Person B runs:
```bash
git clone <your-github-repo-url>
```

### Step 3: Daily Development Routine (Both Person A & Person B)

To avoid conflicts, you will work on separate **branches** instead of `main`.

#### 1. Create your own working branch
- **Person A (Backend)**: `git checkout -b feature/backend`
- **Person B (Frontend)**: `git checkout -b feature/frontend`

#### 2. Write your code & save progress (Commit early, commit often!)
```bash
git add .
git commit -m "Added login form validation logic"
```

#### 3. Push your branch to GitHub
```bash
# Push your branch (e.g., feature/backend)
git push origin feature/backend
```

#### 4. Merge changes into `main` via GitHub Pull Requests
1. Go to GitHub and click **Compare & pull request**.
2. Select your branch to merge into `main`.
3. Approve the request.

#### 5. Get the latest changes daily
Before starting new work, pull the latest merged code from `main`:
```bash
# Switch back to main
git checkout main
# Pull the latest updates
git pull origin main
# Go back to your feature branch
git checkout feature/backend (or feature/frontend)
# Merge the latest main into your branch
git merge main
```

---

## 💡 Pro-Tips for Success

1. **Keep communication open**: Tell each other before changing database models or starting a new page.
2. **Never commit `database.db`**: Create a file named `.gitignore` and add `instance/`, `database.db`, and `venv/` to it, so you don't overwrite each other's test data! (A `.gitignore` file has been added for you).
