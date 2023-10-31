FROM python:3.8.12

WORKDIR /app

COPY ./request_handler.py /app/
COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python", "request_handler.py"]