FROM postgres:13.1-alpine
LABEL mainteiner="André Luzardo Porto <andreportol@gmail.com>"
ENV POSTGRES_USER=controle_user
ENV POSTGRES_PASSWORD=controle_pass
ENV POSTGRES_DB=controle_app
EXPOSE 5432

