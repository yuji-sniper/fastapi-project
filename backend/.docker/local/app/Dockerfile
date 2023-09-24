FROM python:3.11

ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./backend/pyproject.toml /app/
COPY ./backend/poetry.lock /app/

RUN poetry install --no-root
