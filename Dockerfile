﻿FROM python:3

RUN apt-get update
RUN apt-get  install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade pipenv
RUN pip install --upgrade pylint
RUN pip install --upgrade pytest
RUN pip install --upgrade autopep8

ENV PYTHONPATH "${PYTHONPATH}:/work"
# ENV PIPENV_VENV_IN_PROJECT 1