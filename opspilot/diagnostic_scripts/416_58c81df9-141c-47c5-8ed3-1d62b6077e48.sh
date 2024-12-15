# Compute Diagnostic Script for MySQL Memory Usage High on db-server-1

# Display the hostname of the server
sudo echo "Getting the hostname..."
sudo hostname

# Check the disk usage to see if there is enough space available
sudo echo "Checking disk usage..."
sudo df -h

# List block devices to understand the storage configuration
sudo echo "Listing block devices..."
sudo lsblk

# Check memory usage to see how much memory is being utilized
sudo echo "Checking memory usage..."
sudo free -h

# Display the current running processes to identify any high memory usage processes
sudo echo "Listing current running processes..."
sudo ps aux --sort=-%mem | head -n 10

# Check MySQL process status to see if it is running and its resource usage
sudo echo "Checking MySQL process status..."
sudo systemctl status mysql

# Check MySQL memory usage specifically
sudo echo "Checking MySQL memory usage..."
sudo cat /proc/meminfo | grep -i mysql

# Check system logs for any related errors or warnings
sudo echo "Checking system logs for errors..."
sudo journalctl -xe | grep mysql
