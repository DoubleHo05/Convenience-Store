# Base image
FROM ubuntu:20.04

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install MySQL server and necessary tools
RUN apt-get update && \
    apt-get install -y mysql-server && \
    rm -rf /var/lib/apt/lists/*
    
# Allow remote connection
RUN sed -i 's/^bind-address\s*=.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

# For creating my_store database
RUN mkdir -p /docker-entrypoint-initdb.d
COPY my_store.sql /docker-entrypoint-initdb.d/

# Copy custom entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose MySQL port
EXPOSE 3306

# Set entrypoint and default command
ENTRYPOINT ["docker-entrypoint.sh"]
