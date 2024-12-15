# Compute Diagnostic Script for MySQL Memory Usage High on db-server-1 (mysql-db-server) with IP 3.229.119.20. The current memory usage is reported at 15925248.

# Display the hostname of the server
sudo echo "Fetching the hostname of the server..."
sudo hostname

# Check disk space usage
sudo echo "Checking disk space usage..."
sudo df -h

# List block devices and their mount points
sudo echo "Listing block devices and their mount points..."
sudo lsblk

# Check memory usage
sudo echo "Checking memory usage..."
sudo free -h

# Check MySQL process status
sudo echo "Checking MySQL process status..."
sudo systemctl status mysql

# Check MySQL configuration for memory settings
sudo echo "Checking MySQL configuration for memory settings..."
sudo cat /etc/mysql/my.cnf | grep -i 'innodb_buffer_pool_size'

# Check for running MySQL queries
sudo echo "Checking for running MySQL queries..."
sudo mysql -e 'SHOW PROCESSLIST;'