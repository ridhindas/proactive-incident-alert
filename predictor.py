import time
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os
import requests

# Securely load from environment variable, fallback for local testing
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/YOUR/WEBHOOK/URL")
CSV_FILE = "/app/metrics.csv"

def send_slack_alert(message):
    payload = {"text": f"🚨 *PREDICTIVE INCIDENT MANAGEMENT ALERT* 🚨\n{message}"}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print("✅ Alert successfully sent to Slack!")
        else:
            print(f"Failed to send Slack alert: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error connecting to Slack webhook: {e}")

def evaluate_risk():
    if not os.path.exists(CSV_FILE):
        return False

    df = pd.read_csv(CSV_FILE)
    if len(df) < 5:
        print("📊 Collecting baseline data points...")
        return False

    X = np.array(range(len(df))).reshape(-1, 1)
    y = df['memory_usage_mb'].values

    model = LinearRegression()
    model.fit(X, y)

    future_steps = 10
    future_X = np.array([[len(df) + future_steps]])
    predicted_memory = model.predict(future_X)[0]

    CRITICAL_LIMIT_MB = 80.0
    current_mem = y[-1]
    
    print(f"📈 Current: {current_mem:.2f}MB | Predicted in {future_steps*2}s: {predicted_memory:.2f}MB | Limit: {CRITICAL_LIMIT_MB}MB")

    if predicted_memory >= CRITICAL_LIMIT_MB:
        alert_msg = (
            f"Service: *FastAPI App (Containerized)*\n"
            f"Issue: *Memory exhaustion predicted soon!*\n"
            f"• Current Memory: `{current_mem:.2f} MB`\n"
            f"• Projected Memory: `{predicted_memory:.2f} MB` in {future_steps*2}s\n"
            f"• Action: *Triggering automated scaling / pod restart.*"
        )
        print("\n🚨 [PROACTIVE INCIDENT ALERT] Sending payload to Slack...")
        send_slack_alert(alert_msg)
        return True
    return False

if __name__ == '__main__':
    print("🤖 Starting Predictive Incident Monitor...")
    while True:
        is_critical = evaluate_risk()
        if is_critical:
            time.sleep(30) # Prevent spamming Slack
        else:
            time.sleep(2)
