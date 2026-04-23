def normalize(feature):
    return [
        min(feature["request_freq"] / 200, 1.0),
        feature["failed_ratio"],
        min(feature["unique_ports"] / 50, 1.0),
        feature["off_hour"]
    ]