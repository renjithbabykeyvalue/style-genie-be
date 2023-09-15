FROM python:3.11.4

RUN apt-get update

WORKDIR /pencil-model-server
COPY . /pencil-model-server

RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD ["python", "worker.py"]
