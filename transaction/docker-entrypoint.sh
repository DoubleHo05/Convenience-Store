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

while :
do
  python3 transactions.py || echo "Transaction failed"
  sleep 3
done
