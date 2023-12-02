FROM python:3.11.4-alpine3.18

WORKDIR /code

RUN python -m pip install poetry
COPY . .
RUN poetry install

CMD ["sh", "-c", "poetry run uvicorn propinvest_ai.__main__:app --reload --host 0.0.0.0"]
