import requests
from config.env_config import (
    ABUSEIPDB_API_KEY,
    OTX_API_KEY,
    VIRUSTOTAL_API_KEY
)

def check_abuseipdb(ip):
    if not ABUSEIPDB_API_KEY:
        return None

    try:
        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {
            "Key": ABUSEIPDB_API_KEY,
            "Accept": "application/json"
        }
        params = {
            "ipAddress": ip,
            "maxAgeInDays": 90
        }

        res = requests.get(url, headers=headers, params=params, timeout=5)

        if res.status_code != 200:
            return None

        data = res.json()
        score = data.get("data", {}).get("abuseConfidenceScore")

        if score is None:
            return None

        score = float(score)

        if score > 0:
            return max(score, 30.0)

        return 0.0

    except:
        return None


def check_otx(ip):
    if not OTX_API_KEY:
        return None

    try:
        url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general"
        headers = {
            "X-OTX-API-KEY": OTX_API_KEY
        }

        res = requests.get(url, headers=headers, timeout=5)

        if res.status_code != 200:
            return None

        data = res.json()
        pulses = data.get("pulse_info", {}).get("count")

        if pulses is None:
            return None

        if pulses > 0:
            return 50.0

        return 0.0

    except:
        return None


def check_virustotal(ip):
    if not VIRUSTOTAL_API_KEY:
        return None

    try:
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY
        }

        res = requests.get(url, headers=headers, timeout=5)

        if res.status_code != 200:
            return None

        data = res.json()
        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats")

        if not stats:
            return None

        malicious = stats.get("malicious")

        if malicious is None:
            return None

        if malicious > 0:
            return 80.0

        return 0.0

    except:
        return None