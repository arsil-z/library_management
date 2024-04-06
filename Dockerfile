FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get install ghostscript -y
RUN apt-get install git -y

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

CMD exec gunicorn -t 600 -b :10000 main:app --reload