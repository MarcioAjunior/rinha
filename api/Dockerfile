FROM python:3.10.13-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY . .

ENV DBHOST=127.0.0.1
ENV DBNAME=DB
ENV PASS=PASS
ENV USER=USER

ENV HOST=127.0.0.1
ENV PORT_HTTP=8080

EXPOSE 8080

RUN pip install -r requirements.txt

CMD ["python", "./index.py"]
