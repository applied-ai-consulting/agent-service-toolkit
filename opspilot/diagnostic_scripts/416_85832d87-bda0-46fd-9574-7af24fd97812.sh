# Network Diagnostic Script for MySQL Memory Usage High on db-server-1 with IP 3.229.119.20

# Display the hostname of the server
sudo echo "Fetching hostname..."
sudo hostname

# Display disk space usage
sudo echo "Checking disk space usage..."
sudo df -h

# List block devices
sudo echo "Listing block devices..."
sudo lsblk

# Display network interfaces and their status
sudo echo "Checking network interfaces..."
sudo ip a

# Display routing table
sudo echo "Fetching routing table..."
sudo ip route

# Display current network connections
sudo echo "Checking current network connections..."
sudo netstat -tuln

# Display system logs related to networking
sudo echo "Fetching system logs for networking issues..."
sudo journalctl -u NetworkManager --no-pager | tail -n 50

# Display MySQL process status
sudo echo "Checking MySQL process status..."
sudo systemctl status mysql

# Display MySQL memory usage
sudo echo "Checking MySQL memory usage..."
sudo ps aux | grep mysql | awk '{sum += $6} END {print sum/1024 " MB"}'
