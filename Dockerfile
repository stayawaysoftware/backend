FROM python:3.11 as builder

COPY ./configs/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt