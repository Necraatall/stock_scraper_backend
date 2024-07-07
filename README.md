# Stock Scraper Project

![Coverage](./coverage.svg)

### Description

This project is a web scraper for stock values, set up using Docker, Poetry, Taskfile, and PostgreSQL. It efficiently scrapes and stores stock data, providing a structured environment for developing and deploying a Python application.

## Prerequisites

- Docker
- Docker Compose
- Poetry

## Installation

### Clone the repository

To clone the repository from GitHub, use the following command:
```sh
git clone git@github.com:Necraatall/stock_scraper_backend.git .
```
This will clone the repository into the current directory.

### Setup for devops/Python Newbies

On terminal at project dir install Taskfile:

#### Linux

1. Download the latest version of Task:
```sh
sh -c "$(curl -fsSL https://taskfile.dev/install.sh)"
```
2. Move the binary to a directory in your PATH:
```sh
sudo mv ./bin/task /usr/local/bin/
```

#### macOS

1. Using Homebrew:
```sh
brew install go-task/tap/go-task
```

#### Windows

1. Download the latest release from [Taskfile Releases](https://github.com/go-task/task/releases).
2. Extract the task.exe file to a directory in your PATH.

##### Set up dependencies

Here is info only for linux guys:
```sh
task setup-install
```

### Set up the environment

1. Create a .env file in the root directory based on the provided .env.example file.
2. Install Poetry dependencies:
```sh
poetry install
```
3. Set up the virtual environment:
```sh
poetry shell
```

### Running the Application

1. Build and start the Docker containers:
```sh
docker-compose up --build -d
```
2. Run database migrations:
```sh
poetry run alembic upgrade head
```

### Running Tests

To run the tests, use the following command:
```sh
poetry run pytest
```

## Additional Scripts

- cleanup_docker.sh: Script to clean up Docker containers and images.
- wait-for-it.sh: Script to wait for a service to be available.

## Project Structure

```scss
.
├── alembic
│   ├── env.py
│   ├── __pycache__
│   │   └── env.cpython-310.pyc
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── __pycache__
├── alembic.ini
├── bin
│   └── task
├── cleanup_docker.sh
├── cloudformation
│   ├── combined.yaml
│   ├── ec2_instance.yaml
│   └── s3_bucket.yaml
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── README.md
├── requirements.txt
├── src
│   ├── initialize_db.py
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── main.cpython-310.pyc
│   │   ├── models.cpython-310.pyc
│   │   └── scraper.cpython-310.pyc
│   ├── README.md
│   └── scraper.py
├── Taskfile.yaml
├── terraform
│   ├── backend-config.tfvars
│   ├── backend.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── tfplan
│   └── variables.tf
├── tests
│   ├── db_healthcheck.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── test_database.py
│   ├── test_db
│   └── test_scraper.py
├── update_readme_tree.sh
├── wait-for-it.sh
└── ZALOHA
    ├── poznamky.txt
    └── prune_docker.sh

13 directories, 41 files
```

## License

This project is licensed under the [Beerware License](https://en.wikipedia.org/wiki/Beerware).


## Note:

### This project is still under development

#### How the Script Works: update_readme_tree.sh

The script generates the directory structure using tree, and then replaces the content between two ```scss tags with the newly generated structure using awk. Once the process is complete, the result is saved back to README.md.
Setting Up GitHub Actions

If you want to automate this process on every push to the repository, you can add a GitHub Actions workflow as described earlier to run the update_readme_tree.sh script automatically. This will ensure that the README.md file always contains the current directory structure of the project.
