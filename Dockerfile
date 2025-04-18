FROM python:3.13 AS requirements-stage

WORKDIR /tmp

# Poetry >= 1.7.1 includes export by default
RUN pip install poetry==1.7.1

COPY ./pyproject.toml ./poetry.lock* /tmp/

# This works now because export is built-in
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.13

WORKDIR /code
EXPOSE 8443

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
    postgresql-client

RUN pip install --no-cache-dir --default-timeout=600 --upgrade -r /code/requirements.txt

COPY ./src /code
COPY ./.env /code
COPY ./alembic.ini /code/alembic.ini
COPY ./alembic /code/alembic


COPY ./start.sh /code/start.sh
RUN chmod +x /code/start.sh


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8443"]
