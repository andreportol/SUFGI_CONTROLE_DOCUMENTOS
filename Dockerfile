FROM python:3.10.12-alpine
LABEL mainteiner="André Luzardo Porto <andreportol@gmail.com>"
COPY . /var/www
WORKDIR /var/www
RUN apk update && \
    apk add zlib-dev jpeg-dev gcc musl-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \ 
    python manage.py migrate
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
