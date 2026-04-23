import random
from datetime import datetime

COMMON_PORTS = [80, 443, 22]

def random_ip():
    return f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def normal_log():
    return {
        "ip": random_ip(),
        "timestamp": now(),
        "event_type": random.choice(["request", "login"]),
        "status": random.choices(["success", "failed"], weights=[0.9, 0.1])[0],
        "port": random.choice(COMMON_PORTS)
    }

def brute_force(ip):
    return {
        "ip": ip,
        "timestamp": now(),
        "event_type": "login",
        "status": random.choices(["failed", "success"], weights=[0.9, 0.1])[0],
        "port": 22
    }

def traffic_spike(ip):
    return {
        "ip": ip,
        "timestamp": now(),
        "event_type": "request",
        "status": "success",
        "port": random.choice(COMMON_PORTS)
    }

def port_scan(ip):
    return {
        "ip": ip,
        "timestamp": now(),
        "event_type": "request",
        "status": "success",
        "port": random.randint(1, 65535)
    }