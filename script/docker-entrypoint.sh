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

python3 create_data.py
count=0
while :
do
  echo "Loop"
  python3 transactions.py || echo "Transactions fail"
  echo "Transactions done" 
  if ((count % 2 == 0)); then
    python3 extract.py || echo "Extract fail"
    echo "Extract done"
  fi

  ((++count)) || echo "Count fail"
  sleep 10 || echo "Sleep fail"
  echo "End loop"
done 
