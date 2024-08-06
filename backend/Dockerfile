FROM python:3.10-alpine

RUN apk add --no-cache build-base libffi-dev

RUN pip install --upgrade pip
RUN pip install -U poetry

WORKDIR /workdir/backend

COPY pyproject.toml /workdir/backend

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction 

COPY . /workdir/backend

ENV PYTHONPATH=/usr/local/bin/python3.10

RUN chmod +x /usr/local/bin/poetry

RUN sed -i '1s|^.*$|#!/usr/local/bin/python3.10|' /usr/local/bin/poetry

RUN ls -l /usr/local/bin/poetry

WORKDIR /workdir/backend

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]