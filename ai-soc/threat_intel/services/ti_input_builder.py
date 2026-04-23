def build_ti_input(ip, maltrail_hit, cache_result, abuse, otx, vt):
    return {
        "ip": ip,
        "maltrail": maltrail_hit,
        "cache": cache_result,
        "abuse_score": abuse,
        "otx_score": otx,
        "vt_score": vt
    }