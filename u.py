import re

log_data = """
2026-03-06 192.168.1.15 INFO User logged in
2026-03-06 10.0.0.5 ERROR Database connection failed
2026-03-06 172.16.254.1 WARNING Disk space low
2026-03-06 192.168.1.22 ERROR Unauthorized access attempt
"""

def parse_logs(data):
    pattern = r"(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(?P<level>INFO|WARNING|ERROR)\s+(?P<message>.*)"
    results = []

    for match in re.finditer(pattern, data):
        log_entry = match.groupdict()
        log_entry["ip"] = re.sub(r'\.\d+$', '.x', log_entry['ip'])
        results.append(log_entry)
    return results

parsed_logs = parse_logs(log_data)

print("--- ERROR Report ---")

for entry in parsed_logs:
    if entry["level"] == "ERROR":
        print(f"[{entry['date']}] | IP: {entry['ip']} | Error: {entry['message']}")