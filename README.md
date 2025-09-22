**Linux System Monitor Service 🔍**

A robust, real-time system monitoring service for Linux that tracks CPU, memory, disk, and network usage with configurable thresholds and email alerts.

**🚀 Features**

Real-time Monitoring: Continuous tracking of system resources

Configurable Thresholds: Customizable alert levels for each metric

Email Alerts: Automatic notifications when thresholds are exceeded

Log Rotation: Automated log management with size-based rotation

Colorized Output: Terminal output with color-coded status indicators

Systemd Integration: Runs as a reliable system service

Network Monitoring: Tracks upload/download speeds in MB/s

**📋 Monitored Metrics**

CPU Usage: Percentage of CPU utilization

Memory Usage: RAM consumption percentage

Disk Usage: Storage capacity usage

Network Traffic: Upload and download speeds

Custom Thresholds: Individual limits for each metric

**🛠️ Installation**

     Install required Python packages
     sudo apt update
     sudo apt install python3 python3-pip
     sudo pip3 install psutil colorama

**1. Clone the Repository**

     git clone https://github.com/kanwarazeem/linux-system-monitor.git
     cd linux-system-monitor

**2. Install the Service**

     Copy the monitor script
     sudo cp monitor-linux.py /usr/local/bin/

     Make it executable
     sudo chmod +x /usr/local/bin/monitor-linux.py

     Install configuration file
     sudo cp system_monitor.conf /etc/

     Install systemd service
     sudo cp system-monitor.service /etc/systemd/system/

**3. Configure Email Alerts (Optional)**

Edit the configuration file:

     sudo nano /etc/system_monitor.conf
    
**Update the email section:**

     [Email]
     sender = your_email@gmail.com
     receiver = alert_recipient@example.com
     smtp_server = smtp.gmail.com
     smtp_port = 587
     username = your_email@gmail.com

Set the email password as environment variable:

    sudo systemctl edit system-monitor
Add:

    [Service]
    Environment="EMAIL_PASSWORD=your_app_password"

**4. Enable and Start the Service**

    # Reload systemd configuration
    sudo systemctl daemon-reload

    # Enable service to start on boot
    sudo systemctl enable system-monitor

    # Start the service
    sudo systemctl start system-monitor

    # Check status
    sudo systemctl status system-monitor

**⚙️ Configuration**

The service uses /etc/system_monitor.conf for configuration:

    [Thresholds]
    cpu = 85          # CPU usage percentage
    memory = 80       # Memory usage percentage  
    disk = 90         # Disk usage percentage
    net_sent = 10     # Network upload speed (MB/s)
    net_recv = 10     # Network download speed (MB/s)

**Default Thresholds**
    
    [Thresholds]
    cpu = 85          # CPU usage percentage
    memory = 80       # Memory usage percentage  
    disk = 90         # Disk usage percentage
    net_sent = 10     # Network upload speed (MB/s)
    net_recv = 10     # Network download speed (MB/s)

**Logging Settings**

    [Logging]
    log_file = /var/log/system_monitor.log
    max_size = 10     # MB before rotation
    backup_count = 5  # Number of backup logs

**General Settings**

    [General]
    interval = 5      # Check interval in seconds
    hostname =        # Auto-detected if empty

**📊 Usage
View Real-time Output**

    journalctl -u system-monitor -f

**Check Logs**

    tail -f /var/log/system_monitor.log

**Service Management**

    # Start service
    sudo systemctl start system-monitor

    # Stop service  
    sudo systemctl stop system-monitor

    # Restart service
    sudo systemctl restart system-monitor

    # Check status
    sudo systemctl status system-monitor

    # View logs
    journalctl -u system-monitor

**Test Email Functionality**

    sudo systemctl stop system-monitor
    sudo python3 /usr/local/bin/monitor-linux.py --config /etc/system_monitor.conf --test-email

**📊 Performance Impact**

The service is designed to be lightweight:

CPU Usage: < 1% typically

Memory: ~5-10MB

Disk I/O: Minimal (only log writing)

**🤝 Contributing**

Fork the repository

Create a feature branch

Make your changes

Test thoroughly

Submit a pull request

**📄 License**

MIT License - feel free to use this project for personal or commercial purposes.

**🆘 Support**

If you encounter issues:

Check the troubleshooting section

Review system logs

Open an issue on GitHub with detailed information

**🎯 Use Cases**

Server Monitoring: Keep track of production server health

Development Environments: Monitor resource usage during development

Home Labs: Keep an eye on personal servers and NAS systems

Educational Purposes: Learn about system monitoring and Python programming















