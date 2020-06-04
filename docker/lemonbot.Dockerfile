FROM python:3.8-slim-buster

ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV PIPENV_NOSPIN=1
ENV PIPENV_HIDE_EMOJIS=1

RUN pip install pipenv

RUN mkdir -p /lemonbot
COPY . /lemonbot
WORKDIR /lemonbot
RUN pipenv install

CMD ["pipenv", "run", "bot"]
