FROM python:3.10

WORKDIR /files

RUN mkdir "temp"

COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt \
    && rm -rf /root/.cache/pip

COPY .. .