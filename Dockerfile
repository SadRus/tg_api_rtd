FROM docker.io/python:3.10.12

ARG BASE_DIR=/opt/app

ENV \
    # python
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # poetry
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.1 python3 -
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR ${BASE_DIR}
COPY ./pyproject.toml ./poetry.lock README.md ./
RUN poetry install --no-ansi --with docs --with dev

WORKDIR ${BASE_DIR}/src
ENV PYTHONPATH "$PYTHONPATH:${BASE_DIR}/src/"

COPY tg_api tg_api
COPY tests tests
COPY sphinx_docs sphinx_docs
