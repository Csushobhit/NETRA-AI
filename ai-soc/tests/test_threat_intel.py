import csv
import re

from threat_intel.services.checker import classify

FILE_PATH = "tests/MRGKONFR.csv"

def extract_ip(text):
    if not text:
        return None

    pattern = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
    match = re.search(pattern, text)

    if match:
        ip = match.group()
        parts = ip.split(".")
        if all(0 <= int(p) <= 255 for p in parts):
            return ip

    return None


def run():
    processed = 0
    skipped = 0

    with open(FILE_PATH, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)

        if "Message" not in reader.fieldnames:
            print("Column 'Message' not found")
            return

        for row in reader:
            raw = row.get("Message")
            ip = extract_ip(raw)

            if not ip:
                skipped += 1
                continue

            result = classify(ip)

            if isinstance(result, tuple):
                label, source = result
                reasoning = ""
                confidence = ""
            else:
                label = result.get("label", "unknown")
                source = "api"
                reasoning = result.get("reasoning", "")
                confidence = result.get("confidence", "")

            print(f"{ip} → {label} ({source}) {confidence} {reasoning}")

            processed += 1

    print("\n--- SUMMARY ---")
    print("Processed:", processed)
    print("Skipped:", skipped)


if __name__ == "__main__":
    run()