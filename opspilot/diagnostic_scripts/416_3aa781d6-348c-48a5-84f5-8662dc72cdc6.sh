#!/bin/bash
# Compute Diagnostic Script for MySQL Memory Usage High on db-server-1 (IP: 3.229.119.20) with current memory usage at 15925248.

# Display the hostname of the server
sudo echo "Fetching the hostname of the server..."
sudo hostname

# Check the disk usage to see if there are any issues with available space
sudo echo "Checking disk usage..."
sudo df -h

# List block devices to understand the storage configuration
sudo echo "Listing block devices..."
sudo lsblk

# Check memory usage to see how much memory is being utilized
sudo echo "Checking memory usage..."
sudo free -h

# Display MySQL process status to see if there are any issues with MySQL processes
sudo echo "Checking MySQL process status..."
sudo ps aux | grep mysql

# Check MySQL configuration for memory-related settings
sudo echo "Checking MySQL configuration for memory settings..."
sudo cat /etc/mysql/my.cnf | grep -i 'innodb_buffer_pool_size'

# Check system logs for any errors related to MySQL
sudo echo "Checking system logs for MySQL errors..."
sudo grep mysql /var/log/syslog

# Check for any running MySQL queries that might be consuming resources
sudo echo "Checking for running MySQL queries..."
sudo mysql -e 'SHOW PROCESSLIST;'
