**🚀 Running the Monitor**

python monitor-linux.py

**🖥️ Linux System Monitor**

A Python-based CLI tool to monitor **CPU**, **Memory**, and **Disk** usage in real-time with:
    • 
    •  Color-coded output
    •  Email alerts for high usage
    •  Logging to file
    •  Systemd service compatibility
      

**📦 Requirements**

    • Python 3.6+
    • Linux system
    • `psutil`, `colorama` installed in a Python environment (recommended: virtualenv)
**Install dependencies:**

#bash

pip install psutil colorama

**Or use a virtual environment:**

python3 -m venv venv-monitor
source venv-monitor/bin/activate
pip install psutil colorama


**⚙️ Email Alerts (Optional)**

EMAIL_SENDER = 'your_email@example.com'

EMAIL_RECEIVER = 'receiver_email@example.com'

SMTP_SERVER = 'smtp.example.com'

SMTP_PORT = 587

EMAIL_USERNAME = 'your_email@example.com'

EMAIL_PASSWORD = 'your_email_password'

**⚠️ Alert Thresholds**

CPU_THRESHOLD = 85

MEMORY_THRESHOLD = 80

DISK_THRESHOLD = 90

