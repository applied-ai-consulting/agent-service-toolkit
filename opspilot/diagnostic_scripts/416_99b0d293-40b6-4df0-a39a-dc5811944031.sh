# Compute Diagnostic Script for MySQL Memory Usage High on db-server-1

# Display the hostname of the server
sudo echo "Fetching hostname..."
sudo hostname

# Check disk space usage
sudo echo "Checking disk space usage..."
sudo df -h

# List block devices
sudo echo "Listing block devices..."
sudo lsblk

# Check memory usage
sudo echo "Checking memory usage..."
sudo free -h

# Display running processes related to MySQL
sudo echo "Displaying MySQL related processes..."
sudo ps aux | grep mysql

# Check MySQL configuration file for memory settings
sudo echo "Checking MySQL configuration for memory settings..."
sudo cat /etc/mysql/my.cnf | grep -i 'innodb_buffer_pool_size'

# Check system logs for any MySQL related errors
sudo echo "Checking system logs for MySQL errors..."
sudo grep -i mysql /var/log/syslog

# Check for any active MySQL connections
sudo echo "Checking active MySQL connections..."
sudo netstat -an | grep ':3306'
