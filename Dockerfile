FROM  postgres:12
COPY rates.sql /docker-entrypoint-initdb.d/
EXPOSE 5433:5432
ENV POSTGRES_PASSWORD=ratestask
