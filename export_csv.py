import argparse
import csv
import json
from pathlib import Path

p = argparse.ArgumentParser(description="Export completed journal results to a new CSV, without API calls.")
p.add_argument("journal", type=Path)
p.add_argument("output", type=Path)
a = p.parse_args()
latest = {}
for line in a.journal.read_text(encoding="utf-8").splitlines():
    event = json.loads(line)
    if event.get("status") != "manifest": latest[event["id"]] = event
with a.output.open("x", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=["source_row", "result", "valid_label", "request_id"])
    writer.writeheader()
    for row_id, item in latest.items():
        if item["status"] == "completed":
            text = item["result"]
            # Prevent AI output from becoming a spreadsheet formula on open.
            if text.lstrip().startswith(("=", "+", "-", "@", "\t", "\r")): text = "'" + text
            writer.writerow({"source_row": row_id, "result": text, "valid_label": item.get("valid_label", True), "request_id": item.get("request_id")})
