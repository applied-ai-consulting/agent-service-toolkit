#!/bin/bash
# Storage Diagnostic Script for MySQL Memory Usage High on mysql-db-server with IP 3.229.119.20. Current memory usage is 15925248.

# Display the hostname of the server
sudo echo "Getting the hostname of the server..."
sudo hostname

# Check the disk space usage on all mounted filesystems
sudo echo "Checking disk space usage..."
sudo df -h

# List all block devices and their mount points
sudo echo "Listing all block devices..."
sudo lsblk

# Check the current memory usage
sudo echo "Checking current memory usage..."
sudo free -h

# Display the top 10 processes by memory usage
sudo echo "Displaying top 10 processes by memory usage..."
sudo ps aux --sort=-%mem | head -n 11

# Check for any I/O wait issues
sudo echo "Checking for I/O wait issues..."
sudo iostat -x 1 5

# Check the system logs for any storage-related errors
sudo echo "Checking system logs for storage-related errors..."
sudo dmesg | grep -i error

# Check the status of the file system
sudo echo "Checking file system status..."
sudo fsck -N /dev/sda1

# Check for any active swap usage
sudo echo "Checking active swap usage..."
sudo swapon --show
