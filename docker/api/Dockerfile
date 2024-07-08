# syntax = docker/dockerfile:1.5
FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN  --mount=type=cache,target=/root/.cache \
     pip install poetry==1.5.1

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11 as builder

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN apt-get update && \
    apt-get install -y wget tar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

FROM python:3.11-slim-bookworm

RUN useradd --create-home docker_user

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

USER docker_user
RUN mkdir /home/docker_user/app
WORKDIR /home/docker_user/app

ENV PYTHONUNBUFFERED=1
ENV ENV=production
ENV PYTHONPATH=/home/docker_user/app

COPY --chown=docker_user /docker /home/docker_user/docker
RUN chmod +x /home/docker_user/docker/api/startup.sh
COPY /src /home/docker_user/app

ENTRYPOINT ["/home/docker_user/docker/api/startup.sh"]
