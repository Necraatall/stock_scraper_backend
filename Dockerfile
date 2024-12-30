FROM python:3.12
LABEL owner="Milan Zlamal"

# Arguments
ARG DEBUG=true

# Set timezone
ENV TIMEZONE=Europe/Prague
ENV PATH="$PATH:./bin"
ENV PATH="/root/.local/bin:$PATH"
ENV PATH="/usr/local/bin:$PATH"
ENV PATH="/usr/local/bin/uvicorn:$PATH"
RUN chmod -R a+x /usr/local/bin

# Add virtual env bin into PATH, use python of virtual env firstly
# Add virtual site-packages into PYTHONPATH, python can find module in it
ENV PATH=/app/.venv/bin:${PATH} \
    PYTHONPATH=.:src:./.venv/lib/python3.12/site-packages:$PYTHONPATH

WORKDIR /app

COPY pyproject.toml poetry.lock Taskfile.yaml requirements.txt ./
COPY wait-for-it.sh ./wait-for-it.sh
RUN chmod +x ./wait-for-it.sh

# Install dependencies and task
RUN apt-get update -y && \
    apt-get install -y curl sudo postgresql-client netcat-openbsd wget apt-transport-https gnupg libpq-dev build-essential && \
    curl -sL https://taskfile.dev/install.sh | sh

RUN pip install six

COPY . .
