#!/bin/bash
# Compute Diagnostic Script for MySQL Memory Usage High on db-server-1 with IP 3.229.119.20. Current memory usage is 15925248.

# Display the hostname of the server
sudo echo "Getting the hostname..."
sudo hostname

# Check disk space usage
sudo echo "Checking disk space usage..."
sudo df -h

# List block devices and their mount points
sudo echo "Listing block devices..."
sudo lsblk

# Check memory usage
sudo echo "Checking memory usage..."
sudo free -h

# Check running processes and their memory usage
sudo echo "Checking running processes and their memory usage..."
sudo ps aux --sort=-%mem | head -n 10

# Check MySQL status
sudo echo "Checking MySQL status..."
sudo systemctl status mysql

# Check MySQL memory usage
sudo echo "Checking MySQL memory usage..."
sudo mysqladmin status

# Check system logs for any memory-related issues
sudo echo "Checking system logs for memory-related issues..."
sudo dmesg | grep -i memory

# Check for swap usage
sudo echo "Checking swap usage..."
sudo swapon --show
