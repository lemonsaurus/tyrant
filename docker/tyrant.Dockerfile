FROM python:3.9-slim-buster

# Set pip&pipenv to have cleaner output and no cache
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1
ENV PIPENV_NOSPIN=1
ENV PIPENV_HIDE_EMOJIS=1
ENV PIP_NO_CACHE_DIR=false

RUN pip install -U pipenv

WORKDIR /tyrant

# Just copy in deps first, so Docker can cache the image upto here
# If there are no dep changes between builds
COPY Pipfile* ./
RUN pipenv install

# Define Git SHA build argument with a default value
ARG git_sha="development"

# Override default value with one from the build stage
# This allows us to override the dev default value with
# thje actual sha in CI.
ENV GIT_SHA=$git_sha

# Copy source code in last
COPY . .

CMD ["pipenv", "run", "bot"]
