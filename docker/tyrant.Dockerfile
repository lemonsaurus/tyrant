FROM python:3.9-slim-buster

# Set pip&pipenv to have cleaner output and no cache
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV PIPENV_NOSPIN=1
ENV PIPENV_HIDE_EMOJIS=1
ENV PIP_NO_CACHE_DIR=false

RUN apt-get update && apt-get install -y git
RUN pip install pipenv

RUN mkdir -p /tyrant
COPY . /tyrant
WORKDIR /tyrant
RUN pipenv install

CMD ["pipenv", "run", "bot"]
