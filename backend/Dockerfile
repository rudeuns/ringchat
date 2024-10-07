FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /workdir/backend

# RUN pip install -U pip && pip install -U poetry

# RUN poetry config virtualenvs.create false \
#     && poetry config virtualenvs.in-project false

# COPY pyproject.toml ./

# RUN poetry install --no-root --no-interaction

RUN pip install -U pip

COPY requirements.txt ./

RUN pip install -r requirements.txt --default-timeout=600

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]