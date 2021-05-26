FROM postgres:13.2-alpine
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD 12345678
ENV POSTGRES_DB buns_n_cakes
COPY buns_n_cakes.sql ./docker-entrypoint-initdb.d/buns_n_cakes.sql