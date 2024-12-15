#!/bin/bash
# Compute Diagnostic Script for MySQL Memory Usage High on db-server-1 (IP: 3.229.119.20) with current memory usage at 15925248.

# Display the hostname of the server
sudo echo "Fetching the hostname of the server..."
sudo hostname

# Check disk space usage
sudo echo "Checking disk space usage..."
sudo df -h

# List block devices
sudo echo "Listing block devices..."
sudo lsblk

# Display memory usage
sudo echo "Displaying memory usage..."
sudo free -h

# Check running processes and their memory usage
sudo echo "Checking running processes and their memory usage..."
sudo ps aux --sort=-%mem | head -n 10

# Check MySQL process status
sudo echo "Checking MySQL process status..."
sudo systemctl status mysql

# Check MySQL configuration for memory settings
sudo echo "Checking MySQL configuration for memory settings..."
sudo cat /etc/mysql/my.cnf | grep -i 'innodb_buffer_pool_size'

# Check MySQL slow query log
sudo echo "Checking MySQL slow query log..."
sudo cat /var/log/mysql/mysql-slow.log | tail -n 10
