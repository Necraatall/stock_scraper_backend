# Stock Scraper Project


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
git clone git@github.com:Necraatall/lection2.git .
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
├── alembic/
├── bin/
├── src/
├── tests/
├── .dockerignore
├── .env
├── .git/
├── .github/
├── .python-version
├── .venv/
├── alembic.ini
├── cleanup_docker.sh
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── prestart.sh
├── pyproject.toml
├── README.md
├── requirements.txt
├── Taskfile.yaml
├── wait-for-it.sh
└── ZALOHA
```

## License

This project is licensed under the [Beerware License](https://en.wikipedia.org/wiki/Beerware).


## Note:

### This project is still under development
