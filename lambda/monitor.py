import json
import os
import urllib.request
import time
import boto3
import datetime

sns = boto3.client("sns")

URLS = json.loads(os.environ["URLS"])
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
TIMEOUT = 5  # seconds

def check_url(url):
    start = time.time()
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            status = response.getcode()
            duration = round(time.time() - start, 2)

            if status >= 400:
                return False, f"{url} returned {status} in {duration}s"
            return True, f"{url} OK ({status}) in {duration}s"

    except Exception as e:
        return False, f"{url} failed: {str(e)}"


def lambda_handler(event, context):
    failures = []
    results = []

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    for url in URLS:
        success, message = check_url(url)
        print(message)
        results.append(message)

        if not success:
            failures.append(message)

    if failures:
        # Build plain-text professional alert email
        alert_message = f"""
🚨 URL MONITOR ALERT 🚨
Timestamp: {timestamp}

One or more URLs failed health checks:

"""

        for failure in failures:
            alert_message += f"- {failure}\n"

        alert_message += """
----------------------------------------
All checks are logged in CloudWatch Logs for detailed analysis.
This is an automated message. Do not reply directly.
To stop receiving alerts, unsubscribe from the SNS topic.
"""

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="🚨 URL Monitoring Alert 🚨",
            Message=alert_message
        )

        raise Exception("One or more URLs failed")

    return {
        "statusCode": 200,
        "body": "All URLs healthy"
    }

