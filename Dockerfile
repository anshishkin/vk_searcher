FROM python:3.11-slim-bullseye
RUN python -m pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
ENV PYTHONPATH=/app