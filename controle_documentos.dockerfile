FROM python:3.10.12-alpine
LABEL mainteiner="André Luzardo Porto <andreportol@gmail.com>"
COPY . /var/www
WORKDIR /var/www
RUN apk update && \
    apk add --no-cache \
    postgresql-dev \
    py3-pip \
    py3-setuptools && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python manage.py migrate
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
