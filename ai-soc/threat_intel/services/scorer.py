from threat_intel.services.external_apis import (
    check_abuseipdb,
    check_otx,
    check_virustotal
)

def normalize(val):
    if val is None:
        return 0.0
    return float(val)

def amplify(a, o, v):
    if a > 0:
        a = max(a, 40.0)
    if o > 0:
        o = max(o, 40.0)
    if v > 0:
        v = max(v, 70.0)
    return a, o, v

def get_scores(ip):
    a = normalize(check_abuseipdb(ip))
    o = normalize(check_otx(ip))
    v = normalize(check_virustotal(ip))

    a, o, v = amplify(a, o, v)

    return a, o, v