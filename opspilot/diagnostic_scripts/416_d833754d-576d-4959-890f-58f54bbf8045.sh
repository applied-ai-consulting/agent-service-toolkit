#!/bin/bash
# Network Diagnostic Script for The MySQL Memory Usage on the server mysql-db-server (IP: 3.229.119.20) is reported as high, with a current value of 15925248. The trigger for this issue indicates a high severity problem.

# Display the hostname of the server
sudo echo "Fetching the hostname of the server..."
sudo hostname

# Display disk usage to check for available space
sudo echo "Checking disk usage..."
sudo df -h

# List block devices to see mounted filesystems
sudo echo "Listing block devices..."
sudo lsblk

# Display current memory usage to understand memory allocation
sudo echo "Checking current memory usage..."
sudo free -h

# Display network interfaces and their statuses
sudo echo "Listing network interfaces and their statuses..."
sudo ip a

# Display routing table to check network routes
sudo echo "Displaying the routing table..."
sudo route -n

# Display current TCP connections to see active connections
sudo echo "Checking current TCP connections..."
sudo netstat -tuln

# Display system logs for any relevant error messages
sudo echo "Fetching system logs for errors..."
sudo dmesg | tail -n 50

# Display MySQL process status to check for any issues
sudo echo "Checking MySQL process status..."
sudo ps aux | grep mysql
