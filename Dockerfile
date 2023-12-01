FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./entrypoint.sh .

COPY . . 

CMD ["/app/entrypoint.sh"]