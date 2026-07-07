# Contributing to Mosque Management System

Thank you for your interest in contributing! We welcome contributions to improve the user experience, translate content, fix bugs, or add features.

Please read through the guidelines below to ensure a smooth contribution process.

---

## 1. How to Report Bugs

If you find a bug or experience unexpected behavior:
1. Search the **Issues** tab on GitHub to see if it has already been reported.
2. If it is new, open a new Issue using the following format:
   - **Clear Title**: Summarize the issue (e.g., *Urdu text alignment off on employees screen*).
   - **Steps to Reproduce**: Detailed list of steps to trigger the bug.
   - **Expected vs. Actual Behavior**: Explain what should have happened versus what did.
   - **Environment Details**: Python version, CustomTkinter version, and OS.
   - **Screenshots / Logs**: Attach screenshots if applicable.

---

## 2. Feature Suggestion Process

We want to keep the system lightweight and stable. If you have an idea for a feature:
1. Open an Issue under the **Feature Request** category.
2. Explain the **Why**: What problem does this solve for mosque admins?
3. Describe the **How**: Outline the user interface flow or database changes you suggest.
4. Wait for feedback or approval from the maintainers before starting work.

---

## 3. Contribution Workflow

We follow a standard fork-and-pull-request workflow:

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/salmanasmat/mosque-management.git
   cd mosque-management
   ```
3. Create a descriptive **feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your code changes and document them.
5. **Commit** your changes with clear, semantic commit messages:
   ```bash
   git commit -m "Fix auto-lock inactivity timer reset on click"
   ```
6. **Push** your branch to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Open a **Pull Request (PR)** against the `main` branch of the original repository.

---

## 4. Local Development Setup

To run and modify the project locally:

1. Ensure **Python 3.7+** is installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install customtkinter Pillow
   ```
4. Run the application:
   ```bash
   python mosque_app.py
   ```

---

## 5. Pre-Submission Checklist

Before submitting a Pull Request, please verify:
- [ ] The code is clean and compiles without syntax errors (`python -m py_compile mosque_app.py`).
- [ ] No regressions have been introduced (run the app manually and check core screens: Dashboard, Donations, Expenses, HR, Settings).
- [ ] Clean code format has been maintained.
- [ ] No secrets, database files (`mosque.db`), or personal backup directories are tracked by git (run `git status` to verify).
- [ ] Documentation (`CODE_DOCUMENTATION.md`, `README.md`) has been updated if database tables or columns were changed.
