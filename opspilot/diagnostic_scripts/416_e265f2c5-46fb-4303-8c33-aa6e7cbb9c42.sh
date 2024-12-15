# Storage Diagnostic Script for MySQL Memory Usage High on db-server-1

# This script collects diagnostic information related to storage usage on the server.

# Display the hostname of the server
sudo echo "Fetching hostname..."
sudo hostname

# Display disk space usage
sudo echo "Fetching disk space usage..."
sudo df -h

# Display block device information
sudo echo "Fetching block device information..."
sudo lsblk

# Display detailed disk usage for each directory
sudo echo "Fetching detailed disk usage for each directory..."
sudo du -sh /*

# Display file system disk space usage
sudo echo "Fetching file system disk space usage..."
sudo df -i

# Display the current memory usage
sudo echo "Fetching current memory usage..."
sudo free -h

# Display the top 10 largest files and directories
sudo echo "Fetching the top 10 largest files and directories..."
sudo du -ah / | sort -rh | head -n 10
