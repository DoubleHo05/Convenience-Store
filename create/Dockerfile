FROM ubuntu:20.04

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary things
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y netcat && \
    rm -rf /var/lib/apt/lists/*

# Install fake and mysql-connector 
RUN pip3 install faker mysql-connector-python

RUN mkdir -p /app/ft

# Custom entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Working folder
WORKDIR /app
COPY . .

ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]