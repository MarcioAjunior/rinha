FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

EXPOSE 8080

ENV PORT=5432
ENV HOST='db'

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]





