# Storage Diagnostic Script for MySQL Memory Usage High on db-server-1 (mysql-db-server) with IP 3.229.119.20. The current memory usage is reported at 15925248.

# Display the hostname of the server
sudo echo "Getting the hostname of the server..."
sudo hostname

# Check the disk space usage
sudo echo "Checking disk space usage..."
sudo df -h

# List block devices and their mount points
sudo echo "Listing block devices and their mount points..."
sudo lsblk

# Check the current memory usage
sudo echo "Checking current memory usage..."
sudo free -h

# Display MySQL process status
sudo echo "Displaying MySQL process status..."
sudo systemctl status mysql

# Check MySQL error log for any issues
sudo echo "Checking MySQL error log for any issues..."
sudo tail -n 50 /var/log/mysql/error.log

# Check for large files in the MySQL data directory
sudo echo "Checking for large files in the MySQL data directory..."
sudo du -sh /var/lib/mysql/* | sort -hr

# Check for running MySQL queries that may be consuming resources
sudo echo "Checking for running MySQL queries that may be consuming resources..."
sudo mysql -e 'SHOW PROCESSLIST;'