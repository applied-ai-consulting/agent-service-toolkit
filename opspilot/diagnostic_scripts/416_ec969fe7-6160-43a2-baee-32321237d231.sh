#!/bin/bash
# Storage Diagnostic Script for The MySQL Memory Usage on the server mysql-db-server (IP: 3.229.119.20) is reported as high, with a current value of 15925248. The trigger for this issue indicates a high severity problem.

# Display the hostname of the server
sudo echo "Getting the hostname of the server..."
sudo hostname

# Display disk space usage
sudo echo "Checking disk space usage..."
sudo df -h

# List block devices
sudo echo "Listing block devices..."
sudo lsblk

# Check for disk I/O statistics
sudo echo "Checking disk I/O statistics..."
sudo iostat -x 1 3

# Check for mounted filesystems
sudo echo "Checking mounted filesystems..."
sudo mount

# Check for memory usage
sudo echo "Checking memory usage..."
sudo free -h

# Check for running processes related to MySQL
sudo echo "Checking running MySQL processes..."
sudo ps aux | grep mysql

# Check MySQL status
sudo echo "Checking MySQL service status..."
sudo systemctl status mysql
