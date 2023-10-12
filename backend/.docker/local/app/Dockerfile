FROM python:3.11

ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/.venv/lib/python3.11/site-packages:$PYTHONPATH"

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./backend/pyproject.toml ./backend/poetry.lock /app/

# プロジェクトのディレクトリ内に仮想環境(.venv)を配置させる
RUN poetry config virtualenvs.in-project true

RUN poetry install
