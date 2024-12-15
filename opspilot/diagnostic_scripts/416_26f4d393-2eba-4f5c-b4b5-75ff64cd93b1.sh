#!/bin/bash
# Security Diagnostic Script for MySQL Memory Usage High on db-server-1 (IP: 3.229.119.20) with current memory usage at 15925248.

# Display the hostname of the server
sudo echo "Fetching the hostname of the server..."
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
sudo echo "Listing MySQL related processes..."
sudo ps aux | grep mysql

# Display MySQL configuration file location
sudo echo "Finding MySQL configuration file..."
sudo find / -name my.cnf 2>/dev/null

# Display MySQL status
sudo echo "Checking MySQL service status..."
sudo systemctl status mysql

# Display MySQL performance schema
sudo echo "Fetching MySQL performance schema..."
sudo mysql -e 'SHOW GLOBAL STATUS;'
