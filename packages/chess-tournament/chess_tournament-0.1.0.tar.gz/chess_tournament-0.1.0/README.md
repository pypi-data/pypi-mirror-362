
# Chess Tournament Software

![Build Dev](https://gitlab.com/thi26/chess-tournament-software/badges/dev/pipeline.svg)

> A standalone, offline Python application to manage chess tournaments and players — using the MVC architecture and a CLI interface.

---

##  Table of Contents

- [Installation](#installation)
- [Execution](#execution)
- [Makefile Commands](#makefile-commands)
- [Tests](#tests)
- [Linting & Formatting](#linting--formatting)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Code Architecture](#code-architecture)
- [Features](#features)
- [Author](#author)

---

## Installation

To configure and run the program, follow the steps below:

1.**Clone the repository**:

If you haven't already cloned the repository, use the following command:

```bash
git clone https://gitlab.com/thi26/chess-tournament-software.git
cd chess-tournament-software
```

2.**Create and activate a virtual environment**:

```bash
python -m venv venv
```

* **On Windows:**

```bash
.\venv\Scripts\activate
```

* **On mac OS/Linux:**

```bash
source venv/bin/activate
```

3.**Install the project and development dependencies:**

```shell
pip install -e ".[dev]"
```

Includes development tools like black, flake8, pytest, and pre-commit.

## Execution

To start the application (after activation of your virtualenv):

```bash
chess
```

Optional flags:

```bash
chess --quiet # Reduces console output
```

## Makefile Commands

This project includes a `Makefile` to simplify your workflow:

```
make install-dev   # Install the app + dev dependencies
make test          # Run all tests
make lint          # Lint code with flake8
make format        # Format code with black
make pre-commit    # Run all pre-commit hooks
make clean         # Remove cache and temporary files
```

## Tests

Tests are located in the tests/ folder and use pytest:

```
make test
```

A test report in HTML is generated automatically in pytest-report/ during GitLab CI.

## Linting & Formatting

To ensure consistent code style:

Lint with Flake8:

```
make lint
```

Auto-format with Black:

```
make format
```

## Pre-commit Hooks

The project uses pre-commit to check code before committing:

```
make pre-commit
```

This runs checks like black, flake8, etc., on staged files before allowing the commit.

## Code Architecture 

[(see details in issue #7)]: https://gitlab.com/Thi26/chess-tournament-software/-/issues/7

The application follows the Model-View-Controller (MVC) pattern to ensure maintainable and testable code.

## Features 

[(see details in issue #6)]: https://gitlab.com/Thi26/chess-tournament-software/-/issues/6

    Player Management: Add, edit, list players
    
    Tournament Management: Create tournaments, pair rounds, record match results
    
    Reports: Generate player and tournament reports

## Author

@Thi26, OpenClassrooms student
Training: Python Application Developer
