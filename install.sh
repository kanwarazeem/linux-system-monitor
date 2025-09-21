#!/bin/bash
# Linux System Monitor Installation Script

set -e

echo "📦 Installing Linux System Monitor Service"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root"
    exit 1
fi

# Install dependencies
echo "🔧 Installing dependencies..."
apt update
apt install -y python3 python3-pip
pip3 install psutil colorama

# Copy files
echo "📁 Copying files..."
cp monitor-linux.py /usr/local/bin/
chmod +x /usr/local/bin/monitor-linux.py

cp system_monitor.conf /etc/
chmod 644 /etc/system_monitor.conf

cp system-monitor.service /etc/systemd/system/
chmod 644 /etc/systemd/system/system-monitor.service

# Create log file
echo "📝 Setting up logging..."
touch /var/log/system_monitor.log
chown root:root /var/log/system_monitor.log
chmod 644 /var/log/system_monitor.log

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit /etc/system_monitor.conf with your settings"
echo "2. Set EMAIL_PASSWORD environment variable:"
echo "   sudo systemctl edit system-monitor"
echo "3. Enable and start the service:"
echo "   sudo systemctl enable system-monitor"
echo "   sudo systemctl start system-monitor"
echo "4. Check status: sudo systemctl status system-monitor"
