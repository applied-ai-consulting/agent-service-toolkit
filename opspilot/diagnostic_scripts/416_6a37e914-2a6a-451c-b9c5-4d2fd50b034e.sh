#!/bin/bash
# Compute Diagnostic Script for The MySQL Memory Usage on the server mysql-db-server (IP: 3.229.119.20) is reported as high, with a current value of 15925248. The trigger for this issue indicates a high severity problem.

# Display the hostname of the server
sudo echo "Fetching the hostname of the server..."
sudo hostname

# Display disk usage in a human-readable format
sudo echo "Checking disk usage..."
sudo df -h

# List block devices
sudo echo "Listing block devices..."
sudo lsblk

# Check memory usage
sudo echo "Checking memory usage..."
sudo free -h

# Display MySQL process status
sudo echo "Checking MySQL process status..."
sudo systemctl status mysql

# Display MySQL memory usage
sudo echo "Fetching MySQL memory usage..."
sudo ps aux | grep mysql

# Display system logs for any errors related to MySQL
sudo echo "Checking system logs for MySQL errors..."
sudo journalctl -u mysql --since "1 hour ago"