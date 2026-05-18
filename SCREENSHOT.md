# Linux System Monitor - Output Examples

## Basic System Overview

```
╔════════════════════════════════════════════════════════════╗
║          Linux System Monitor - 2026-05-18 14:32          ║
╠════════════════════════════════════════════════════════════╣
║ CPU Usage:        45.3% (Load: 2.1, 1.8, 1.5)            ║
║ Memory Usage:     12.4 GB / 32 GB (38.7%)                ║
║ Disk Usage:       250 GB / 500 GB (50%)                  ║
║ Network (eth0):   ↓ 2.5 Mbps ↑ 1.2 Mbps                  ║
║ Temperature:      62°C                                   ║
╠════════════════════════════════════════════════════════════╣
║ Top Processes by CPU                                      ║
║ 1. Chrome         - 18.5%                                ║
║ 2. Firefox        - 12.3%                                ║
║ 3. Python         - 8.7%                                 ║
║ 4. VS Code        - 6.2%                                 ║
║ 5. System Monitor - 1.2%                                 ║
╚════════════════════════════════════════════════════════════╝
```

## Detailed CPU Monitoring

```
═══════════════════════════════════════════════════════════════════
                    CPU ANALYSIS - Core Details
═══════════════════════════════════════════════════════════════════

Overall CPU Usage: 45.3%
├─ CPU 0: 52.1% [████████████████░░░░░░░]
├─ CPU 1: 48.5% [███████████████░░░░░░░░░]
├─ CPU 2: 42.0% [████████████░░░░░░░░░░░░]
├─ CPU 3: 38.7% [███████████░░░░░░░░░░░░░]
├─ CPU 4: 45.2% [████████████░░░░░░░░░░░░]
├─ CPU 5: 43.1% [█████████████░░░░░░░░░░░]
├─ CPU 6: 44.8% [████████████░░░░░░░░░░░░]
└─ CPU 7: 46.3% [██████████████░░░░░░░░░░]

Load Average: 2.1 (1 min) | 1.8 (5 min) | 1.5 (15 min)
Context Switches: 125,432
Interrupts: 542,108
```

## Memory Detailed View

```
═══════════════════════════════════════════════════════════════════
                      MEMORY ANALYSIS
═══════════════════════════════════════════════════════════════════

Physical Memory:
  Total:      32.0 GB
  Used:       12.4 GB ████████████░░░░░░░░░░░░░░░░░░░░░░░░
  Available:  19.6 GB
  Free:        8.2 GB
  Usage:      38.7%

Swap Memory:
  Total:       8.0 GB
  Used:        0.5 GB ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  Free:        7.5 GB
  Usage:       6.2%

Memory Distribution:
  ├─ Buffers:  2.1 GB
  ├─ Cached:   4.5 GB
  ├─ Used:     5.8 GB
  └─ Free:     19.6 GB
```

## Disk Usage

```
═══════════════════════════════════════════════════════════════════
                        DISK USAGE
═══════════════════════════════════════════════════════════════════

Mount Point          Total    Used     Free    Usage%   Type
─────────────────────────────────────────────────────────────────
/                   500 GB   250 GB   250 GB   50%     ext4
├─ Home Files       200 GB   145 GB    55 GB   72%     ▓▓▓▓▓▓░░░░
├─ Applications      80 GB    70 GB    10 GB   87%     ▓▓▓▓▓▓▓▓░░
├─ Media            120 GB    90 GB    30 GB   75%     ▓▓▓▓▓▓░░░░
└─ Documents         80 GB    35 GB    45 GB   43%     ▓▓▓░░░░░░░

/boot               500 MB   245 MB   255 MB   49%     ext4
/dev                  8 GB      0 GB     8 GB    0%     devtmpfs
```

## Network Interface Statistics

```
═══════════════════════════════════════════════════════════════════
                     NETWORK INTERFACES
═══════════════════════════════════════════════════════════════════

Interface: eth0 (Active)
  Status:         Connected
  IP Address:     192.168.1.100
  MAC Address:    00:1a:2b:3c:4d:5e
  
  Bytes Received:    2.5 GB
  Bytes Sent:        1.2 GB
  Download Speed:    2.5 Mbps ↓
  Upload Speed:      1.2 Mbps ↑
  Packets In:        125,432
  Packets Out:       98,567
  Errors In:         0
  Errors Out:        0

Interface: wlan0 (Active)
  Status:         Connected
  IP Address:     192.168.1.101
  MAC Address:    00:1a:2b:3c:4d:5f
  
  Bytes Received:    1.8 GB
  Bytes Sent:        0.9 GB
  Download Speed:    1.8 Mbps ↓
  Upload Speed:      0.9 Mbps ↑
```

## Top Processes

```
═══════════════════════════════════════════════════════════════════
                    TOP PROCESSES BY CPU
═══════════════════════════════════════════════════════════════════

PID    Name           CPU%    Memory     MEM%    State
──────────────────────────────────────────────────────────────────
1234   chrome         18.5%   1.2 GB     3.8%    running
5678   firefox        12.3%   856 MB     2.7%    running
2341   python         8.7%    245 MB     0.8%    running
6789   vscode         6.2%    512 MB     1.6%    running
3412   systemd-journal 4.1%   128 MB     0.4%    running
7890   docker         3.8%    432 MB     1.3%    running
4123   nginx          2.5%    64 MB      0.2%    running
8901   sshd           1.2%    32 MB      0.1%    running
5234   monitor        1.2%    48 MB      0.1%    running

═══════════════════════════════════════════════════════════════════
                   TOP PROCESSES BY MEMORY
═══════════════════════════════════════════════════════════════════

PID    Name           Memory     MEM%    CPU%    State
──────────────────────────────────────────────────────────────────
1234   chrome         1.2 GB     3.8%    18.5%   running
2341   python         245 MB     0.8%    8.7%    running
6789   vscode         512 MB     1.6%    6.2%    running
7890   docker         432 MB     1.3%    3.8%    running
5678   firefox        856 MB     2.7%    12.3%   running
```

## System Temperature

```
═══════════════════════════════════════════════════════════════════
                    TEMPERATURE SENSORS
═══════════════════════════════════════════════════════════════════

CPU Core 0:     58°C [████░░░░░░░░░░░] Normal
CPU Core 1:     62°C [██████░░░░░░░░░] Normal
CPU Core 2:     55°C [███░░░░░░░░░░░░] Normal
CPU Core 3:     61°C [██████░░░░░░░░░] Normal
CPU Core 4:     63°C [██████░░░░░░░░░] Normal
CPU Core 5:     64°C [███████░░░░░░░░] Normal
CPU Core 6:     59°C [█████░░░░░░░░░░] Normal
CPU Core 7:     62°C [██████░░░░░░░░░] Normal

GPU Temperature: 48°C  [████░░░░░░░░░░░] Normal
Storage:        35°C  [███░░░░░░░░░░░░] Normal

Average CPU Temp: 60.6°C ✓ Healthy
```

## Alerts and Warnings

```
═══════════════════════════════════════════════════════════════════
                     SYSTEM ALERTS
═══════════════════════════════════════════════════════════════════

⚠ WARNING: High Disk Usage
   Mount /home is at 72% capacity
   Available space: 55 GB

⚠ WARNING: Elevated CPU Temperature
   CPU Core 6 reached 74°C

✓ OK: Memory usage normal (38.7%)
✓ OK: Network connectivity stable
✓ OK: CPU usage acceptable (45.3%)
```

## JSON Export Example

```json
{
  "timestamp": "2026-05-18T14:32:45Z",
  "system": {
    "hostname": "workstation",
    "uptime": 45.2,
    "kernel": "5.15.0-56-generic"
  },
  "cpu": {
    "usage_percent": 45.3,
    "count": 8,
    "per_core": [52.1, 48.5, 42.0, 38.7, 45.2, 43.1, 44.8, 46.3],
    "load_average": [2.1, 1.8, 1.5]
  },
  "memory": {
    "total": 34359738368,
    "used": 13353088000,
    "available": 21006650368,
    "percent": 38.7
  },
  "disk": {
    "total": 536870912000,
    "used": 268435456000,
    "free": 268435456000,
    "percent": 50.0
  },
  "network": {
    "eth0": {
      "bytes_sent": 1288490188,
      "bytes_recv": 2576980377
    }
  },
  "top_processes": [
    {"pid": 1234, "name": "chrome", "cpu_percent": 18.5, "memory_mb": 1229.3},
    {"pid": 5678, "name": "firefox", "cpu_percent": 12.3, "memory_mb": 876.4}
  ]
}
```

## CSV Export Example

```
timestamp,hostname,cpu_percent,memory_percent,disk_percent,temp_celsius
2026-05-18T14:32:45Z,workstation,45.3,38.7,50.0,60.6
2026-05-18T14:32:47Z,workstation,46.1,38.9,50.0,61.2
2026-05-18T14:32:49Z,workstation,44.8,38.5,50.0,60.8
2026-05-18T14:32:51Z,workstation,45.5,39.1,50.0,61.5
2026-05-18T14:32:53Z,workstation,44.2,38.4,50.0,60.3
```
