# Slot Machine on the Web (Flask + Jinja2)

## Overview
A simple web-based slot machine that simulates the mechanics of a traditional slot machine, operating randomly. This project was created **without using JavaScript** to add complexity and make it more challenging.

### Features:
- Integration with a database using SQLAlchemy.
- User authentication (sign up, log in, log out).
- Deposit simulation.
- Betting on winning lines.
- Automatic detection and display of winnings.

### Demonstration
**[Watch the project demonstration on YouTube](https://youtu.be/7TvXGQN-oVA)**

---

## How to Run the Project

### Prerequisites:
- Python 3.8+
- pip (Python package installer)
- A virtual environment (optional but recommended)

### Steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rmnp1/flask-slot-machine.git
   cd slot_machine
   ```

2. **Initialize the project and install dependencies**
   ```bash
   uv init
   uv add flask flask-sqlalchemy flask-migrate
   ```



3. **Initialize and migrate the database:**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```
   The port can be modified in the `run.py` file.

---

## Notes
- Ensure the database configurations are correctly set up in `app.py`.

