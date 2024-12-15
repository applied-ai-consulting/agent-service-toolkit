# Compute Diagnostic Script for MySQL Memory Usage High on mysql-db-server (IP: 3.229.119.20)

# Display the hostname of the server
sudo echo "Fetching the hostname..."
sudo hostname

# Display disk space usage
sudo echo "Checking disk space usage..."
sudo df -h

# Display block devices
sudo echo "Listing block devices..."
sudo lsblk

# Display memory usage
sudo echo "Checking memory usage..."
sudo free -h

# Display running processes related to MySQL
sudo echo "Listing MySQL processes..."
sudo ps aux | grep mysql

# Display MySQL configuration file location
sudo echo "Finding MySQL configuration file..."
sudo find / -name my.cnf 2>/dev/null

# Display MySQL status
sudo echo "Checking MySQL service status..."
sudo systemctl status mysql

# Display system logs for MySQL
sudo echo "Fetching MySQL logs..."
sudo tail -n 50 /var/log/mysql/error.log

# Display current system load
sudo echo "Checking system load..."
sudo uptime

# Display network connections
sudo echo "Checking network connections..."
sudo netstat -tuln
