# Storage Diagnostic Script for High Disk Usage on mysql-db-server (IP: 3.229.119.20)

# Display the hostname of the server
sudo echo "Getting the hostname..."
sudo hostname

# Check the disk space usage on all mounted filesystems
sudo echo "Checking disk space usage..."
sudo df -h

# List all block devices and their mount points
sudo echo "Listing block devices..."
sudo lsblk

# Display detailed information about disk usage in the root directory
sudo echo "Getting detailed disk usage in the root directory..."
sudo du -sh /*

# Check for large files in the /var directory, which is commonly used for logs
sudo echo "Finding large files in /var directory..."
sudo find /var -type f -exec du -h {} + | sort -rh | head -n 10

# Check for disk I/O statistics
sudo echo "Checking disk I/O statistics..."
sudo iostat -x 1 5

# Check the system logs for any disk-related errors
sudo echo "Checking system logs for disk-related errors..."
sudo dmesg | grep -i error

# Check the current disk usage by inodes
sudo echo "Checking inode usage..."
sudo df -i
