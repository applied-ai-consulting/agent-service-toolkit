# Storage Diagnostic Script for MySQL Memory Usage High on db-server-1 with IP 3.229.119.20

# This script collects storage diagnostics to help analyze high memory usage in MySQL.

# Display the hostname of the server
sudo echo "Fetching hostname..."
sudo hostname

# Display disk space usage in a human-readable format
sudo echo "Collecting disk space usage..."
sudo df -h

# List all block devices
sudo echo "Listing block devices..."
sudo lsblk

# Display detailed disk usage for each directory
sudo echo "Collecting detailed disk usage..."
sudo du -sh /*

# Check for any mounted filesystems
sudo echo "Checking mounted filesystems..."
sudo mount

# Display memory usage statistics
sudo echo "Fetching memory usage statistics..."
sudo free -h

# Display the current I/O statistics
sudo echo "Collecting I/O statistics..."
sudo iostat -x 1 5

# Display the current disk usage by MySQL
sudo echo "Checking MySQL disk usage..."
sudo du -sh /var/lib/mysql/*

# Display the MySQL process status
sudo echo "Fetching MySQL process status..."
sudo ps aux | grep mysql
