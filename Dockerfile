# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install build dependencies
RUN apt update && apt install -y gcc python3-dev libpq-dev

# install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt

# copy docker-entrypoint.sh
COPY ./scripts/docker-entrypoint.sh ./docker-entrypoint.sh

# install netcat required in entrypoint
RUN apt install -y netcat

# copy project
COPY . .

# make entrypoint executable
RUN chmod +x ./docker-entrypoint.sh

# run docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]