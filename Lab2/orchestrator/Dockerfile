FROM python:3.8.12

WORKDIR /app

COPY ./request_handler.py /app/
COPY ./requirements.txt /app/
COPY ../data/worker_status.json /app/

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python request_handler.py > output.log 2>&1"]