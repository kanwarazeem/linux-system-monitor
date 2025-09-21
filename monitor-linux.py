#!/usr/bin/env python3
import psutil
import os
import time
import logging
from datetime import datetime
from colorama import Fore, Style, init
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import argparse
import socket
from collections import deque

# Initialize colorama
init(autoreset=True)

# Configuration setup
CONFIG_FILE = '/etc/system_monitor.conf'
DEFAULT_CONFIG = f"""[Thresholds]
# CPU usage threshold (%)
cpu = 85

# Memory usage threshold (%)
memory = 80

# Disk usage threshold (%)
disk = 90

# Network send threshold (MB/s)
net_sent = 10

# Network receive threshold (MB/s)
net_recv = 10

[Email]
# Sender email address
sender = your_email@gmail.com

# Recipient email address
receiver = recipient@example.com

# Email subject
subject = Linux System Monitor Alert

# SMTP server
smtp_server = smtp.gmail.com

# SMTP port
smtp_port = 587

# Email username
username = your_email@gmail.com

[Logging]
# Log file path
log_file = /var/log/system_monitor.log

# Max log size in MB
max_size = 10

# Number of backup logs
backup_count = 5

[General]
# Check interval in seconds
interval = 5

# System hostname
hostname = {socket.gethostname()}
"""

# Network history for rate calculation
net_history = {
    'sent': deque(maxlen=10),
    'recv': deque(maxlen=10),
    'timestamp': deque(maxlen=10)
}

def load_config():
    """Load configuration from file with fallback to defaults"""
    config = configparser.ConfigParser()
    
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            f.write(DEFAULT_CONFIG)
        print(f"Created default config file: {CONFIG_FILE}")
    
    config.read(CONFIG_FILE)
    
    # Get password from environment variable
    email_password = os.getenv('EMAIL_PASSWORD')
    
    # Set up log rotation if specified
    log_file = config.get('Logging', 'log_file', fallback='/var/log/system_monitor.log')
    max_size = config.getint('Logging', 'max_size', fallback=10) * 1024 * 1024  # Convert to bytes
    backup_count = config.getint('Logging', 'backup_count', fallback=5)
    
    return {
        'cpu_threshold': config.getfloat('Thresholds', 'cpu', fallback=85),
        'mem_threshold': config.getfloat('Thresholds', 'memory', fallback=80),
        'disk_threshold': config.getfloat('Thresholds', 'disk', fallback=90),
        'net_sent_threshold': config.getfloat('Thresholds', 'net_sent', fallback=10),
        'net_recv_threshold': config.getfloat('Thresholds', 'net_recv', fallback=10),
        'email_sender': config.get('Email', 'sender', fallback=''),
        'email_receiver': config.get('Email', 'receiver', fallback=''),
        'email_subject': config.get('Email', 'subject', fallback='System Alert'),
        'smtp_server': config.get('Email', 'smtp_server', fallback=''),
        'smtp_port': config.getint('Email', 'smtp_port', fallback=587),
        'email_username': config.get('Email', 'username', fallback=''),
        'email_password': email_password,
        'log_file': log_file,
        'max_log_size': max_size,
        'log_backup_count': backup_count,
        'interval': config.getint('General', 'interval', fallback=5),
        'hostname': config.get('General', 'hostname', fallback=socket.gethostname())
    }

def setup_logger(config):
    """Configure logging with rotation"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create rotating file handler
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        config['log_file'],
        maxBytes=config['max_log_size'],
        backupCount=config['log_backup_count']
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    logger.addHandler(file_handler)
    
    # Also log to console in development
    if os.getenv('DEBUG'):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        logger.addHandler(console_handler)
    
    return logger

def colorize(value, threshold):
    """Colorize output based on threshold values"""
    if value > threshold:
        return f"{Fore.RED}{value}{Style.RESET_ALL}"
    elif value > threshold - 10:
        return f"{Fore.YELLOW}{value}{Style.RESET_ALL}"
    return f"{Fore.GREEN}{value}{Style.RESET_ALL}"

def get_network_rates():
    """Calculate network transfer rates in MB/s"""
    net_io = psutil.net_io_counters()
    current_time = time.time()
    
    # Initialize history
    if not net_history['timestamp']:
        net_history['sent'].append(net_io.bytes_sent)
        net_history['recv'].append(net_io.bytes_recv)
        net_history['timestamp'].append(current_time)
        return 0.0, 0.0
    
    # Calculate rates
    time_diff = current_time - net_history['timestamp'][0]
    sent_diff = net_io.bytes_sent - net_history['sent'][0]
    recv_diff = net_io.bytes_recv - net_history['recv'][0]
    
    # Convert to MB/s (bytes to MB: / (1024*1024))
    sent_rate = (sent_diff / (1024 * 1024)) / time_diff if time_diff > 0 else 0
    recv_rate = (recv_diff / (1024 * 1024)) / time_diff if time_diff > 0 else 0
    
    # Update history
    net_history['sent'].append(net_io.bytes_sent)
    net_history['recv'].append(net_io.bytes_recv)
    net_history['timestamp'].append(current_time)
    
    return sent_rate, recv_rate

def send_email_alert(config, metrics, alerts):
    """Send detailed HTML email alert"""
    if not all([
        config['email_sender'],
        config['email_receiver'], 
        config['smtp_server'], 
        config['email_password']
    ]):
        logging.error("Email configuration incomplete. Skipping email alert.")
        return

    try:
        # Create HTML email content
        msg = MIMEMultipart('alternative')
        msg['From'] = config['email_sender']
        msg['To'] = config['email_receiver']
        msg['Subject'] = f"{config['email_subject']} - {config['hostname']}"
        
        # System information
        sys_info = f"""
        <p>
            <strong>System:</strong> {config['hostname']} ({socket.gethostbyname(socket.gethostname())})<br>
            <strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
        """
        
        # Build alerts section
        alerts_section = ""
        if alerts:
            alerts_section = "<h3>Active Alerts:</h3><ul>"
            for alert in alerts:
                alerts_section += f"<li style='color: #d9534f;'>{alert}</li>"
            alerts_section += "</ul>"
        
        # Build metrics table
        def status_cell(value, threshold):
            if value > threshold:
                return f"<td style='border: 1px solid #ddd; padding: 8px; color: #d9534f; font-weight: bold;'>CRITICAL</td>"
            elif value > threshold - 10:
                return f"<td style='border: 1px solid #ddd; padding: 8px; color: #f0ad4e; font-weight: bold;'>WARNING</td>"
            return "<td style='border: 1px solid #ddd; padding: 8px;'>Normal</td>"
        
        metrics_table = """
        <h3>Resource Metrics:</h3>
        <table style='border-collapse: collapse; width: 100%;'>
            <tr style='background-color: #4CAF50; color: white;'>
                <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Metric</th>
                <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Value</th>
                <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Threshold</th>
                <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Status</th>
            </tr>
        """
        
        metrics_table += f"""
            <tr>
                <td style='border: 1px solid #ddd; padding: 8px;'>CPU Usage</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{metrics['cpu']:.1f}%</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{config['cpu_threshold']}%</td>
                {status_cell(metrics['cpu'], config['cpu_threshold'])}
            </tr>
            <tr style='background-color: #f2f2f2;'>
                <td style='border: 1px solid #ddd; padding: 8px;'>Memory Usage</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{metrics['memory']:.1f}%</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{config['mem_threshold']}%</td>
                {status_cell(metrics['memory'], config['mem_threshold'])}
            </tr>
            <tr>
                <td style='border: 1px solid #ddd; padding: 8px;'>Disk Usage</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{metrics['disk']:.1f}%</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{config['disk_threshold']}%</td>
                {status_cell(metrics['disk'], config['disk_threshold'])}
            </tr>
            <tr style='background-color: #f2f2f2;'>
                <td style='border: 1px solid #ddd; padding: 8px;'>Network Sent</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{metrics['net_sent']:.2f} MB/s</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{config['net_sent_threshold']} MB/s</td>
                {status_cell(metrics['net_sent'], config['net_sent_threshold'])}
            </tr>
            <tr>
                <td style='border: 1px solid #ddd; padding: 8px;'>Network Received</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{metrics['net_recv']:.2f} MB/s</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{config['net_recv_threshold']} MB/s</td>
                {status_cell(metrics['net_recv'], config['net_recv_threshold'])}
            </tr>
        </table>
        """
        
        # Compose HTML email
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
            <!-- Header -->
            <div style="background-color: #4CAF50; padding: 15px; color: white;">
                <h2 style="margin: 0;">System Resource Alert</h2>
            </div>
            
            <!-- Content Container -->
            <div style="padding: 20px;">
                {sys_info}
                
                <!-- Alerts Section -->
                <div style="margin: 20px 0; padding: 15px; border-left: 4px solid #d9534f; background-color: #f8f8f8;">
                    {alerts_section if alerts else "<p>No active alerts</p>"}
                </div>
                
                <!-- Metrics Table -->
                {metrics_table}
                
                <!-- Footer -->
                <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee; color: #6c757d; font-size: 0.9em;">
                    <p>Generated by Linux System Monitor</p>
                    <p>Next check in {config['interval']} seconds</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version as fallback
        text = f"System Alert on {config['hostname']}\n\n"
        text += "Active Alerts:\n"
        for alert in alerts:
            text += f" - {alert}\n"
        text += "\nResource Metrics:\n"
        text += f"CPU Usage: {metrics['cpu']:.1f}% (Threshold: {config['cpu_threshold']}%)\n"
        text += f"Memory Usage: {metrics['memory']:.1f}% (Threshold: {config['mem_threshold']}%)\n"
        text += f"Disk Usage: {metrics['disk']:.1f}% (Threshold: {config['disk_threshold']}%)\n"
        text += f"Network Sent: {metrics['net_sent']:.2f} MB/s (Threshold: {config['net_sent_threshold']} MB/s)\n"
        text += f"Network Received: {metrics['net_recv']:.2f} MB/s (Threshold: {config['net_recv_threshold']} MB/s)\n"
        text += f"\nGenerated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Attach both versions to the email
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['email_username'], config['email_password'])
            server.send_message(msg)
        
        logging.info("Email alert sent with detailed metrics")

    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

def monitor(config, logger):
    """Main monitoring loop"""
    last_alert_time = 0
    alert_cooldown = 300  # 5 minutes between alerts
    
    # Initialize network history
    get_network_rates()
    
    logger.info(f"Monitoring started on {config['hostname']}")
    logger.info(f"Thresholds - CPU: {config['cpu_threshold']}% | Memory: {config['mem_threshold']}% | "
                f"Disk: {config['disk_threshold']}% | Net Sent: {config['net_sent_threshold']}MB/s | "
                f"Net Recv: {config['net_recv_threshold']}MB/s")

    while True:
        # Collect metrics
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net_sent, net_recv = get_network_rates()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        metrics = {
            'cpu': cpu,
            'memory': memory,
            'disk': disk,
            'net_sent': net_sent,
            'net_recv': net_recv
        }

        # Colorize output
        cpu_col = colorize(cpu, config['cpu_threshold'])
        mem_col = colorize(memory, config['mem_threshold'])
        disk_col = colorize(disk, config['disk_threshold'])
        net_sent_col = colorize(net_sent, config['net_sent_threshold'])
        net_recv_col = colorize(net_recv, config['net_recv_threshold'])

        # Console output
        output = (f"[{timestamp}] CPU: {cpu_col}% | Mem: {mem_col}% | Disk: {disk_col}% | "
                  f"Net: ↑{net_sent_col} MB/s ↓{net_recv_col} MB/s")
        print(output)
        
        # Log entry in requested format
        log_entry = (f"CPU: {cpu}% | Memory: {memory}% | Disk: {disk}% | "
                     f"Net Sent: {net_sent:.2f} MB/s | Net Recv: {net_recv:.2f} MB/s")
        logger.info(log_entry)

        # Check thresholds and send alerts
        current_time = time.time()
        alerts = []
        
        if cpu > config['cpu_threshold']:
            alerts.append(f"High CPU usage: {cpu:.1f}%")
        if memory > config['mem_threshold']:
            alerts.append(f"High Memory usage: {memory:.1f}%")
        if disk > config['disk_threshold']:
            alerts.append(f"High Disk usage: {disk:.1f}%")
        if net_sent > config['net_sent_threshold']:
            alerts.append(f"High Network send rate: {net_sent:.2f} MB/s")
        if net_recv > config['net_recv_threshold']:
            alerts.append(f"High Network receive rate: {net_recv:.2f} MB/s")

        # Send alert if needed
        if alerts and (current_time - last_alert_time) > alert_cooldown:
            logger.warning(f"ALERT: {', '.join(alerts)}")
            send_email_alert(config, metrics, alerts)
            last_alert_time = current_time

        time.sleep(config['interval'])

if __name__ == '__main__':
    # Create a temporary logger first for error handling
    temp_logger = logging.getLogger('TempLogger')
    temp_logger.setLevel(logging.INFO)
    temp_logger.addHandler(logging.StreamHandler())
    
    try:
        parser = argparse.ArgumentParser(description='Linux System Monitor')
        parser.add_argument('--gen-config', action='store_true', help='Generate default config file')
        parser.add_argument('--test-email', action='store_true', help='Send a test email')
        parser.add_argument('--config', default='/etc/system_monitor.conf', help='Path to config file')
        args = parser.parse_args()

        if args.gen_config:
            with open(CONFIG_FILE, 'w') as f:
                f.write(DEFAULT_CONFIG)
            print(f"Generated default configuration at {CONFIG_FILE}")
            print("Please edit this file with your settings")
            exit(0)

        config = load_config()
        logger = setup_logger(config)
        
        if args.test_email:
            print("Sending test email...")
            test_metrics = {
                'cpu': 95.0,
                'memory': 85.0,
                'disk': 92.5,
                'net_sent': 15.3,
                'net_recv': 8.7
            }
            test_alerts = [
                "Test Alert: High CPU usage",
                "Test Alert: High Disk usage",
                "Test Alert: High Network send rate"
            ]
            send_email_alert(config, test_metrics, test_alerts)
            print("Test email sent successfully")
            exit(0)
        
        print(Fore.CYAN + "Starting Linux System Monitor CLI Tool..." + Style.RESET_ALL)
        print(Fore.YELLOW + f"Host: {config['hostname']}")
        print(f"Thresholds - CPU: {config['cpu_threshold']}% | Memory: {config['mem_threshold']}% | "
              f"Disk: {config['disk_threshold']}% | Net Sent: {config['net_sent_threshold']}MB/s | "
              f"Net Recv: {config['net_recv_threshold']}MB/s")
        print(Style.RESET_ALL, end='')
        monitor(config, logger)
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nMonitoring stopped by user." + Style.RESET_ALL)
        if 'logger' in locals():
            logger.info("Monitoring stopped by user.")
        else:
            temp_logger.info("Monitoring stopped by user.")
    
    except Exception as e:
        if 'logger' in locals():
            logger.exception("Critical error occurred")
        else:
            temp_logger.exception("Critical error occurred")
        print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)
        exit(1)
