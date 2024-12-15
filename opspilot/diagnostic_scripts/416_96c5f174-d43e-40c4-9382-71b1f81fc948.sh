#!/bin/bash
# Compute Diagnostic Script for MySQL Memory Usage High on mysql-db-server with IP 3.229.119.20. Current memory usage is 15925248.

# Display the hostname of the server
sudo echo "Getting the hostname of the server..."
sudo hostname

# Check the disk space usage
sudo echo "Checking disk space usage..."
sudo df -h

# List block devices and their mount points
sudo echo "Listing block devices..."
sudo lsblk

# Check memory usage
sudo echo "Checking memory usage..."
sudo free -h

# Display MySQL process status
sudo echo "Checking MySQL process status..."
sudo systemctl status mysql

# Check MySQL configuration for memory settings
sudo echo "Checking MySQL configuration for memory settings..."
sudo cat /etc/mysql/my.cnf | grep -i 'innodb_buffer_pool_size'

# Check for running MySQL queries
sudo echo "Checking for running MySQL queries..."
sudo mysql -e 'SHOW PROCESSLIST;' 