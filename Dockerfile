FROM python:3.11 AS builder

COPY ./configs/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app
COPY ./src/ /app/backend/src/

WORKDIR /app/backend/src
CMD ["python3","-m","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]