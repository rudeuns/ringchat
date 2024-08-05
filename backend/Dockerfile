FROM python:3.10-alpine

RUN pip install -U poetry

WORKDIR /workdir

COPY poetry.lock pyproject.toml /workdir/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction 

COPY . /workdir

ENV PYTHONPATH=/usr/local/bin/python3.10

RUN chmod +x /usr/local/bin/poetry

RUN sed -i '1s|^.*$|#!/usr/local/bin/python3.10|' /usr/local/bin/poetry

RUN ls -l /usr/local/bin/poetry

WORKDIR /workdir/backend

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]