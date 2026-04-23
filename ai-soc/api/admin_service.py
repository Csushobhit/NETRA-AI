import os
from threat_intel.init.update_maltrail import update

def update_env(data):
    path = ".env"

    env = {}

    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    env[k] = v

    for k, v in data.items():
        env[k] = v

    with open(path, "w") as f:
        for k, v in env.items():
            f.write(f"{k}={v}\n")

    return True

def refresh_maltrail():
    update()
    return True