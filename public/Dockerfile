FROM python:3.10

WORKDIR /app

RUN mkdir "temp"

COPY requirements.txt requirements.txt

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY .. .