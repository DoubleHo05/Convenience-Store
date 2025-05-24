#!/bin/bash
set -e

host="mysql"
user="giabao"
password="giabao"
port=3306

echo "Waiting for MySQL at $host with user $user..."

until nc -z "$host" "$port"; do
  echo "Waiting for $host:$port..."
  sleep 1
done

echo "MySQL is up - executing command"
exec python3 create_data.py