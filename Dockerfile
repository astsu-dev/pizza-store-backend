FROM python:3.9

WORKDIR /app

COPY poetry.lock pyproject.toml ./

# Convert pyproject.toml and poetry.lock to requirements.txt, then install dependencies with pip
RUN pip install poetry==1.1.6 && \
    poetry export -f requirements.txt --output requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

COPY pizza_store ./pizza_store
COPY .env gunicorn.conf.py ./

EXPOSE 8000

CMD [ "gunicorn" ]
