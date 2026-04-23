import time
import random
from generator.modes import normal_log, brute_force, traffic_spike, port_scan, random_ip
from generator.writer import init_file, write_log

MODES = ["normal", "brute", "spike", "scan"]

def run():
    init_file()

    attack_ip = random_ip()
    mode = "normal"
    counter = 0

    while True:
        if counter % 50 == 0:
            mode = random.choice(MODES)

        if mode == "normal":
            log = normal_log()

        elif mode == "brute":
            log = brute_force(attack_ip)

        elif mode == "spike":
            log = traffic_spike(attack_ip)

        elif mode == "scan":
            log = port_scan(attack_ip)

        write_log(log)

        counter += 1
        time.sleep(0.5)

if __name__ == "__main__":
    run()