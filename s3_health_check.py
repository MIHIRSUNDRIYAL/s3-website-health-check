import csv
import sys
from datetime import datetime
from urllib.parse import urljoin

import requests


WEBSITE_URL = "http://your-s3-website-endpoint-here"

ASSETS_TO_CHECK = [
    "",
    "index.html",
    "style.css"
]

LOG_FILE = "health_check_log.csv"


def check_url(url):
    try:
        response = requests.get(url, timeout=10)

        return {
            "url": url,
            "status_code": response.status_code,
            "success": 200 <= response.status_code < 400,
            "error": ""
        }

    except requests.RequestException as error:
        return {
            "url": url,
            "status_code": "N/A",
            "success": False,
            "error": str(error)
        }


def write_log(results):
    try:
        with open(LOG_FILE, "r", newline="") as file:
            file_exists = bool(file.readline())
    except FileNotFoundError:
        file_exists = False

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["timestamp", "url", "status_code", "success", "error"]
        )

        if not file_exists:
            writer.writeheader()

        for result in results:
            writer.writerow({
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "url": result["url"],
                "status_code": result["status_code"],
                "success": result["success"],
                "error": result["error"]
            })


def main():
    print("Running S3 static website health check...\n")

    results = []

    for asset in ASSETS_TO_CHECK:
        full_url = urljoin(WEBSITE_URL.rstrip("/") + "/", asset)
        result = check_url(full_url)
        results.append(result)

        status = "PASS" if result["success"] else "FAIL"
        print(f"{status} | {result['status_code']} | {full_url}")

        if result["error"]:
            print(f"Error: {result['error']}")

    write_log(results)

    failed_checks = [result for result in results if not result["success"]]

    print(f"\nResults logged to {LOG_FILE}")

    if failed_checks:
        print(f"Health check failed: {len(failed_checks)} issue(s) found.")
        sys.exit(1)

    print("Health check passed: all checks successful.")
    sys.exit(0)


if __name__ == "__main__":
    main()
