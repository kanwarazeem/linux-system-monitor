1. Create a systemd service file:
   
sudo nano /etc/systemd/system/linux_monitor.service

Paste this (adjust paths if needed):

[Unit]
Description=Linux System Monitor
After=network.target

[Service]
Type=simple
User=linode
WorkingDirectory=/home/linode
ExecStart=/home/linode/venv-monitor/bin/python /home/linode/monitor-linux.py
Restart=on-failure

[Install]
WantedBy=multi-user.target

2. Enable and Start the Service
   
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable linux_monitor.service
sudo systemctl start linux_monitor.service

3. Check Status
   
sudo systemctl status linux_monitor.service
journalctl -u linux_monitor.service -f
