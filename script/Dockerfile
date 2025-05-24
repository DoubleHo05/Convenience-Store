FROM ubuntu:20.04

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary things
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y default-mysql-client && \
    apt-get install -y netcat && \
    rm -rf /var/lib/apt/lists/*

# Install fake and mysql-connector 
RUN pip3 install faker mysql-connector-python

# Custom entrypoint
COPY wait_for_mysql.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait_for_mysql.sh

# Working folder
WORKDIR /app
COPY . .

ENTRYPOINT [ "/usr/local/bin/wait_for_mysql.sh" ]