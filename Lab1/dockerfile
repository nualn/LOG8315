FROM python:3.8.12

WORKDIR /app

COPY ./app/ /app/

RUN pip install -r requirements.txt

COPY ./.aws /root/.aws

VOLUME ./data:/app/data

ENTRYPOINT [ "python" ]