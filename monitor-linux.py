#!/usr/bin/env python3
import psutil
import subprocess
import os
import time
import logging
from datetime import datetime
from colorama import Fore, Style, init
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(filename='system_monitor.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Email alert configuration (replace with your actual info)
EMAIL_SENDER = 'your_email@example.com'
EMAIL_RECEIVER = 'receiver_email@example.com'
EMAIL_SUBJECT = 'Linux System Monitor Alert'
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_USERNAME = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'

# Alert thresholds
CPU_THRESHOLD = 85  # percent
MEMORY_THRESHOLD = 80  # percent
DISK_THRESHOLD = 90  # percent

def colorize(value, threshold):
    if value > threshold:
        return f"{Fore.RED}{value}{Style.RESET_ALL}"
    elif value > threshold - 10:
        return f"{Fore.YELLOW}{value}{Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}{value}{Style.RESET_ALL}"

def send_email_alert(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)

        logging.info(f"Email alert sent: {subject}")

    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

def monitor():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cpu_col = colorize(cpu, CPU_THRESHOLD)
        mem_col = colorize(memory, MEMORY_THRESHOLD)
        disk_col = colorize(disk, DISK_THRESHOLD)

        output = f"[{timestamp}] CPU: {cpu_col}% | Memory: {mem_col}% | Disk: {disk_col}%"
        print(output)
        logging.info(f"CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%")

        # Alerts
        alerts = []
        if cpu > CPU_THRESHOLD:
            alerts.append(f"High CPU usage: {cpu}%")
        if memory > MEMORY_THRESHOLD:
            alerts.append(f"High Memory usage: {memory}%")
        if disk > DISK_THRESHOLD:
            alerts.append(f"High Disk usage: {disk}%")

        if alerts:
            alert_body = "\n".join(alerts)
            logging.warning(alert_body)
            send_email_alert("[ALERT] System Resource Usage Exceeded", alert_body)

        time.sleep(5)  # Adjust interval as needed

if __name__ == '__main__':
    try:
        print(Fore.CYAN + "Starting Linux System Monitor CLI Tool..." + Style.RESET_ALL)
        monitor()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nMonitoring stopped by user." + Style.RESET_ALL)
        logging.info("Monitoring stopped by user.")
