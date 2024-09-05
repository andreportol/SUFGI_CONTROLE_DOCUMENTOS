FROM postgres:13.1-alpine
LABEL mainteiner="André Luzardo Porto <andreportol@gmail.com>"
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=12345
ENV POSTGRES_DB=controledocumentos
EXPOSE 5432

