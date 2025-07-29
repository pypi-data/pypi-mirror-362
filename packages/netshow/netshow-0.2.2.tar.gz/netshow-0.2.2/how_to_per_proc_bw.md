# The Definitive Guide to Per-Process Bandwidth Monitoring with Python

## Overview

Per-process bandwidth monitoring tracks network usage by individual processes, enabling you to identify which applications consume the most bandwidth. This guide covers cross-platform solutions that work on both macOS and Linux.

## Core Approaches

### 1. **System-Level Tools with Python Wrappers**

The most reliable approach leverages existing system monitoring tools through Python subprocess calls.

#### **Linux: nethogs**
```python
import subprocess
import re
import json

class NethogsBandwidthMonitor:
    def __init__(self):
        self.process = None
    
    def start_monitoring(self, interface='eth0'):
        """Start nethogs in JSON mode for easy parsing"""
        cmd = ['sudo', 'nethogs', '-t', '-d', '1', interface]
        self.process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
    
    def parse_output(self):
        """Parse nethogs output and return bandwidth data"""
        bandwidth_data = {}
        
        for line in self.process.stdout:
            # Format: program/pid/uid  sent_kb/s  recv_kb/s
            match = re.match(r'(\S+)/(\d+)/(\d+)\s+([\d.]+)\s+([\d.]+)', line)
            if match:
                program, pid, uid, sent, recv = match.groups()
                bandwidth_data[pid] = {
                    'program': program,
                    'sent_kbps': float(sent),
                    'recv_kbps': float(recv),
                    'total_kbps': float(sent) + float(recv)
                }
        
        return bandwidth_data
```

#### **macOS: nettop**
```python
import subprocess
import re

class NettopBandwidthMonitor:
    def __init__(self):
        self.last_values = {}
    
    def get_bandwidth(self):
        """Get current bandwidth usage per process"""
        cmd = ['nettop', '-P', '-L', '1', '-J', 'bytes_in,bytes_out']
        
        try:
            output = subprocess.check_output(cmd, text=True)
            return self._parse_nettop_output(output)
        except subprocess.CalledProcessError as e:
            print(f"Error running nettop: {e}")
            return {}
    
    def _parse_nettop_output(self, output):
        """Parse nettop output"""
        bandwidth_data = {}
        
        for line in output.split('\n'):
            if '.' in line and 'bytes' not in line.lower():
                parts = line.split(',')
                if len(parts) >= 3:
                    process_info = parts[0].strip()
                    bytes_in = int(parts[1].strip())
                    bytes_out = int(parts[2].strip())
                    
                    # Extract PID from process info
                    pid_match = re.search(r'\.(\d+)', process_info)
                    if pid_match:
                        pid = pid_match.group(1)
                        bandwidth_data[pid] = {
                            'process': process_info.split('.')[0],
                            'bytes_in': bytes_in,
                            'bytes_out': bytes_out,
                            'total_bytes': bytes_in + bytes_out
                        }
        
        return bandwidth_data
```

### 2. **psutil-based Solution**

A more portable but less accurate approach uses psutil to track network connections per process.

```python
import psutil
import time
from collections import defaultdict

class PsutilBandwidthMonitor:
    def __init__(self):
        self.last_io_counters = {}
        self.connection_map = defaultdict(set)
    
    def update_connections(self):
        """Map network connections to processes"""
        self.connection_map.clear()
        
        for conn in psutil.net_connections(kind='inet'):
            if conn.pid:
                self.connection_map[conn.pid].add(
                    (conn.laddr, conn.raddr, conn.status)
                )
    
    def estimate_bandwidth(self, interval=1.0):
        """Estimate bandwidth by monitoring system-wide changes"""
        # Get initial network stats
        net_io_1 = psutil.net_io_counters()
        proc_io_1 = {}
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_io_1[proc.pid] = proc.io_counters()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        time.sleep(interval)
        
        # Get final network stats
        net_io_2 = psutil.net_io_counters()
        bandwidth_data = {}
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.pid in proc_io_1:
                    io_2 = proc.io_counters()
                    io_1 = proc_io_1[proc.pid]
                    
                    # Calculate I/O delta (approximation)
                    read_delta = io_2.read_bytes - io_1.read_bytes
                    write_delta = io_2.write_bytes - io_1.write_bytes
                    
                    # Only include if process has network connections
                    if proc.pid in self.connection_map:
                        bandwidth_data[proc.pid] = {
                            'name': proc.name(),
                            'connections': len(self.connection_map[proc.pid]),
                            'read_bytes_sec': read_delta / interval,
                            'write_bytes_sec': write_delta / interval
                        }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return bandwidth_data
```

### 3. **eBPF-based Solution (Linux only)**

For the most accurate Linux monitoring, use eBPF with Python bindings.

```python
from bcc import BPF
import time

# eBPF program to track network bytes per PID
bpf_program = """
#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>

BPF_HASH(pid_bytes, u32, u64);

int trace_tcp_sendmsg(struct pt_regs *ctx, struct sock *sk,
                      struct msghdr *msg, size_t size) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    u64 *bytes = pid_bytes.lookup(&pid);
    if (bytes) {
        *bytes += size;
    } else {
        pid_bytes.update(&pid, &size);
    }
    return 0;
}
"""

class EBPFBandwidthMonitor:
    def __init__(self):
        self.bpf = BPF(text=bpf_program)
        self.bpf.attach_kprobe(event="tcp_sendmsg", fn_name="trace_tcp_sendmsg")
        self.last_values = {}
    
    def get_bandwidth_stats(self, interval=1.0):
        """Get bandwidth usage per PID"""
        time.sleep(interval)
        
        bandwidth_data = {}
        pid_bytes = self.bpf["pid_bytes"]
        
        for k, v in pid_bytes.items():
            pid = k.value
            bytes_sent = v.value
            
            if pid in self.last_values:
                bytes_per_sec = (bytes_sent - self.last_values[pid]) / interval
                bandwidth_data[pid] = {
                    'bytes_per_sec': bytes_per_sec,
                    'mbps': (bytes_per_sec * 8) / 1_000_000
                }
            
            self.last_values[pid] = bytes_sent
        
        return bandwidth_data
```

## Unified Cross-Platform Interface

```python
import platform
import os

class BandwidthMonitor:
    def __init__(self):
        self.system = platform.system()
        self.monitor = None
        self._initialize_monitor()
    
    def _initialize_monitor(self):
        """Initialize the appropriate monitor for the current OS"""
        if self.system == 'Linux':
            # Check for available tools
            if os.path.exists('/usr/sbin/nethogs'):
                self.monitor = NethogsBandwidthMonitor()
            else:
                # Fallback to psutil
                self.monitor = PsutilBandwidthMonitor()
        elif self.system == 'Darwin':  # macOS
            self.monitor = NettopBandwidthMonitor()
        else:
            # Default fallback
            self.monitor = PsutilBandwidthMonitor()
    
    def get_process_bandwidth(self, interval=1.0):
        """Get bandwidth data for all processes"""
        if hasattr(self.monitor, 'get_bandwidth'):
            return self.monitor.get_bandwidth()
        elif hasattr(self.monitor, 'estimate_bandwidth'):
            return self.monitor.estimate_bandwidth(interval)
        else:
            raise NotImplementedError("No bandwidth monitoring available")
    
    def format_output(self, bandwidth_data, top_n=10):
        """Format bandwidth data for display"""
        # Sort by total bandwidth
        sorted_procs = sorted(
            bandwidth_data.items(),
            key=lambda x: x[1].get('total_bytes', 0) or 
                         x[1].get('total_kbps', 0) or 0,
            reverse=True
        )[:top_n]
        
        print(f"{'PID':<8} {'Process':<25} {'Download':<15} {'Upload':<15}")
        print("-" * 70)
        
        for pid, data in sorted_procs:
            process_name = data.get('name', data.get('program', 'Unknown'))[:24]
            
            # Handle different data formats
            if 'recv_kbps' in data:
                download = f"{data['recv_kbps']:.2f} KB/s"
                upload = f"{data['sent_kbps']:.2f} KB/s"
            elif 'bytes_in' in data:
                download = f"{data['bytes_in'] / 1024:.2f} KB"
                upload = f"{data['bytes_out'] / 1024:.2f} KB"
            else:
                download = f"{data.get('read_bytes_sec', 0) / 1024:.2f} KB/s"
                upload = f"{data.get('write_bytes_sec', 0) / 1024:.2f} KB/s"
            
            print(f"{pid:<8} {process_name:<25} {download:<15} {upload:<15}")
```

## Usage Example

```python
def main():
    monitor = BandwidthMonitor()
    
    print("Starting bandwidth monitoring...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            bandwidth_data = monitor.get_process_bandwidth(interval=2.0)
            
            # Clear screen (works on most terminals)
            print("\033[2J\033[H")
            
            # Display current bandwidth usage
            monitor.format_output(bandwidth_data, top_n=15)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
```

## Installation Requirements

### **Linux**
```bash
# For nethogs approach
sudo apt-get install nethogs  # Debian/Ubuntu
sudo yum install nethogs      # RHEL/CentOS

# For eBPF approach
pip install bcc

# For psutil approach
pip install psutil
```

### **macOS**
```bash
# nettop comes pre-installed
# For psutil approach
pip install psutil
```

## Important Considerations

1. **Permissions**: Most accurate monitoring requires root/sudo access
2. **Accuracy**: System tools (nethogs, nettop) are most accurate; psutil provides estimates
3. **Performance**: eBPF has minimal overhead; subprocess calls have higher overhead
4. **Portability**: psutil works everywhere but with reduced accuracy

## Advanced Features

### Real-time Graphing
```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

class BandwidthGraph:
    def __init__(self, monitor, max_points=60):
        self.monitor = monitor
        self.max_points = max_points
        self.data = defaultdict(lambda: deque(maxlen=max_points))
        
        self.fig, self.ax = plt.subplots()
        self.lines = {}
    
    def update(self, frame):
        bandwidth_data = self.monitor.get_process_bandwidth()
        
        for pid, data in bandwidth_data.items():
            total_kbps = data.get('total_kbps', 0)
            self.data[pid].append(total_kbps)
            
            if pid not in self.lines:
                line, = self.ax.plot([], [], label=f"PID {pid}")
                self.lines[pid] = line
            
            self.lines[pid].set_data(range(len(self.data[pid])), self.data[pid])
        
        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.legend()
        
    def start(self):
        ani = FuncAnimation(self.fig, self.update, interval=1000)
        plt.show()
```

This guide provides a comprehensive foundation for implementing per-process bandwidth monitoring across platforms, with multiple approaches ranging from simple to advanced, ensuring you can track network usage effectively regardless of your specific requirements or constraints.
