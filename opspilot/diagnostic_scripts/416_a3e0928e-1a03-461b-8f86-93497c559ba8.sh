# Network Diagnostic Script for MySQL Memory Usage High on db-server-1 (mysql-db-server) with IP 3.229.119.20. The current memory usage is reported at 15925248.

# Display the hostname of the server
sudo echo "Fetching the hostname of the server..."
sudo hostname

# Display disk usage in a human-readable format
sudo echo "Fetching disk usage information..."
sudo df -h

# List block devices
sudo echo "Listing block devices..."
sudo lsblk

# Display network interfaces and their configurations
sudo echo "Fetching network interface configurations..."
sudo ip addr show

# Display routing table
sudo echo "Fetching the routing table..."
sudo route -n

# Display current network connections
sudo echo "Fetching current network connections..."
sudo netstat -tuln

# Display system memory usage
sudo echo "Fetching memory usage information..."
sudo free -h

# Display MySQL process status
sudo echo "Fetching MySQL process status..."
sudo ps aux | grep mysql

# Display MySQL configuration file location
sudo echo "Fetching MySQL configuration file location..."
sudo find / -name my.cnf 2>/dev/null