
FROM python:3.11-slim

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy

RUN pipenv sync --system

WORKDIR /app
COPY ./ ./

CMD ["python", "bot.py"]