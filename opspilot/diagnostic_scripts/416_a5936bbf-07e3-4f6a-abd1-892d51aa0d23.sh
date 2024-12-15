# Network Diagnostic Script for MySQL Memory Usage High on mysql-db-server (IP: 3.229.119.20)

# Display the hostname of the server
sudo echo "Getting the hostname of the server..."
sudo hostname

# Display disk usage in a human-readable format
sudo echo "Checking disk usage..."
sudo df -h

# List block devices
sudo echo "Listing block devices..."
sudo lsblk

# Display network interfaces and their status
sudo echo "Checking network interfaces..."
sudo ip a

# Display routing table
sudo echo "Displaying the routing table..."
sudo route -n

# Check current network connections
sudo echo "Checking current network connections..."
sudo netstat -tuln

# Display the current memory usage
sudo echo "Checking current memory usage..."
sudo free -h

# Display system logs for any network-related issues
sudo echo "Checking system logs for network-related issues..."
sudo dmesg | grep -i network

# Display the last 100 lines of syslog for any errors
sudo echo "Checking the last 100 lines of syslog for errors..."
sudo tail -n 100 /var/log/syslog | grep -i error
