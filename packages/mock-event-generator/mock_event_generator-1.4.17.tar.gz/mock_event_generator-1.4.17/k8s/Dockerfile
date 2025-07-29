# syntax = docker/dockerfile:1.3
ARG BUILD_ENV

FROM python:3.11-slim as python-base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN adduser --disabled-password --gecos '' meguser
WORKDIR /home/meguser

RUN apt-get update \
 && apt install --yes gcc libkrb5-dev swig libssl-dev \
 && apt-get clean
RUN pip install --upgrade pip

# Install MEG from PyPI
FROM python-base as python-release
ARG PACKAGE_VERSION
RUN pip install \
  --no-cache-dir \
  --root-user-action=ignore \
  mock-event-generator==${PACKAGE_VERSION}

# Install MEG from GitLab Package Registry
FROM python-base as python-test
ARG PACKAGE_VERSION
RUN --mount=type=secret,id=netrc,dst=/root/.netrc \
  pip install \
  --no-cache-dir \
  --root-user-action=ignore \
  --extra-index-url=https://git.ligo.org/api/v4/projects/11815/packages/pypi/simple \
  mock-event-generator==${PACKAGE_VERSION}

# Install MEG from host repository
FROM python-base as python-local
COPY pyproject.toml ./
COPY mock_event_generator mock_event_generator/
RUN pip install \
  --root-user-action=ignore \
  .  igwn-robot-auth

FROM python-${BUILD_ENV} as python-build

RUN chmod 666 $(python -c "import certifi; print(certifi.where())")

USER meguser

## RUN --mount=type=secret,id=x509,dst=/tmp/x509up_u1000,uid=1000 \
##   meg fetch S220609hl --source playground

COPY _static/cache_test_events.tgz cache_test_events.tgz
RUN tar xvzf cache_test_events.tgz
RUN ls -lta
RUN ls -lta .cache
