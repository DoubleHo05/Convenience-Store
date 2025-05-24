#!/bin/bash
set -e

echo "Starting MySQL temporarily for setup..."
mysqld_safe --skip-networking &
pid="$!"

# Wait for MySQL to be ready
until mysqladmin ping --silent; do
    sleep 1
done

# Set root password and authentication method
echo "Configuring root password and users..."
mysql <<-EOSQL
    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}';
    FLUSH PRIVILEGES;
EOSQL

# Run .sql files
echo "Running init scripts..."
for f in /docker-entrypoint-initdb.d/*.sql; do
    echo "Executing $f"
    mysql -uroot -p${MYSQL_ROOT_PASSWORD} < "$f"
done

# Create user
if [ -n "$MYSQL_USER" ] && [ -n "$MYSQL_PASSWORD" ]; then
    echo "Creating user: $MYSQL_USER"
    mysql -uroot -p${MYSQL_ROOT_PASSWORD} <<-EOSQL
        CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
        GRANT ALL PRIVILEGES ON \`$MYSQL_DATABASE\`.* TO '$MYSQL_USER'@'%';
        FLUSH PRIVILEGES;
EOSQL
fi

echo "Stopping temporary MySQL..."
mysqladmin -uroot -p${MYSQL_ROOT_PASSWORD} shutdown
wait "$pid"

# Start MySQL normally in foreground
exec mysqld_safe
