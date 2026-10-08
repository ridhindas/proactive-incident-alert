import time
import requests
import csv
import os

# 'app' is the service name defined in docker-compose.yml
APP_METRICS_URL = "http://app:8000/metrics"
CSV_FILE = "/app/metrics.csv" # Path inside the shared Docker volume

def get_app_memory():
    try:
        response = requests.get(APP_METRICS_URL, timeout=2)
        if response.status_code == 200:
            return response.json().get("memory_usage_mb")
    except requests.exceptions.RequestException:
        pass
    return None

def main():
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'memory_usage_mb'])
        
        print("🔍 Starting telemetry collection...")
        while True:
            mem = get_app_memory()
            if mem is not None:
                timestamp = time.time()
                writer.writerow([timestamp, round(mem, 2)])
                f.flush()
                print(f"[Telemetry] Recorded Memory: {round(mem, 2)} MB")
            else:
                print("[Telemetry] Waiting for FastAPI app to be ready...")
            time.sleep(2)

if __name__ == '__main__':
    main()
