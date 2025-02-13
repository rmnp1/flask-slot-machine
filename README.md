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
- can find in [pyproject.toml](https://github.com/rmnp1/flask-slot-machine/blob/2d03e9ac65e6b849da6a5352df3cf7641cdf18c1/pyproject.toml)

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
    flask run -h 0.0.0.0 -p 5001 
   ```
   The port can be modified.

---

## Notes
- Ensure the database configurations are correctly set up in `app.py`.


---

## Running the Project with Docker

This project uses Docker for containerization. Before starting, make sure you have Docker installed.

### Requirements

- [Docker](https://docs.docker.com/get-docker/)

### Setup and Run Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/rmnp1/flask-slot-machine.git
   cd slot_machine
   ```

2. Start the container:
   ```sh
   docker-compose up --build
   ```

This command will build the images (if they do not exist) and start the containers as defined in the `docker-compose.yml` file.

### Stopping the Containers

To stop the containers, press `Ctrl+C` or use the command:
```sh
docker-compose down
```

If necessary, you can remove the stored container data with:
```sh
docker-compose down -v