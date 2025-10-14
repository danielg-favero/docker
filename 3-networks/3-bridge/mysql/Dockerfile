FROM mysql:8.0.43

# Essa pasta serve para rodar script de banco de dados
COPY schema.sql /docker-entrypoint-initdb.d/

# Padrão do MySQL
EXPOSE 3306

# Backup posterior
VOLUME ["/backup"]

