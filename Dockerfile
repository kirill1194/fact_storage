FROM python:3.7-alpine3.8
RUN apk add --no-cache --virtual .tmp_deps build-base python3-dev libffi-dev openssl-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=fact_storage.dev"]