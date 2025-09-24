#!/bin/bash
set -e
host=$MYSQL_HOST
user=$MYSQL_USER
password=$MYSQL_PASSWORD
port=$PORT

echo "Waiting for MySQL at $host with user $user..."

until nc -z "$host" "$port"; do
  echo "Waiting for $host:$port..."
  sleep 1
done

echo "MySQL is up - executing command"

python3 extract.py || echo "Cannot extract"
echo "Finish extracting data at $(date)"