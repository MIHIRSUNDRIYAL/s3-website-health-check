import csv
import re
import sys
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests


LOG_FILE = "health_check_log.csv"


def check_url(url):
    try:
        response = requests.get(url, timeout=10)

        return {
            "url": url,
            "status_code": response.status_code,
            "success": 200 <= response.status_code < 400,
            "error": "",
            "content": response.text if "text/html" in response.headers.get("Content-Type", "") else ""
        }

    except requests.RequestException as error:
        return {
            "url": url,
            "status_code": "N/A",
            "success": False,
            "error": str(error),
            "content": ""
        }


def extract_assets(html_content, base_url):
    patterns = [
        r'href=["\']([^"\']+)["\']',
        r'src=["\']([^"\']+)["\']'
    ]

    found_assets = []

    for pattern in patterns:
        matches = re.findall(pattern, html_content)

        for match in matches:
            if match.startswith(("mailto:", "tel:", "#", "javascript:")):
                continue

            full_url = urljoin(base_url, match)
            found_assets.append(full_url)

    return sorted(set(found_assets))


def is_same_site(url, website_url):
    return urlparse(url).netloc == urlparse(website_url).netloc


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
    website_url = input("Enter your S3 static website endpoint: ").strip()

    if not website_url:
        print("No website URL entered.")
        sys.exit(1)

    if not website_url.startswith(("http://", "https://")):
        website_url = "http://" + website_url

    print("\nRunning S3 static website health check...\n")

    results = []

    homepage_result = check_url(website_url)
    results.append(homepage_result)

    homepage_status = "PASS" if homepage_result["success"] else "FAIL"
    print(f"{homepage_status} | {homepage_result['status_code']} | {website_url}")

    if not homepage_result["success"]:
        write_log(results)
        print(f"\nResults logged to {LOG_FILE}")
        print("Homepage failed. Fix the S3 website endpoint or permissions first.")
        sys.exit(1)

    assets = extract_assets(homepage_result["content"], website_url)

    same_site_assets = [
        asset for asset in assets
        if is_same_site(asset, website_url)
    ]

    if not same_site_assets:
        print("\nNo same-site assets found in homepage HTML.")

    for asset_url in same_site_assets:
        result = check_url(asset_url)
        results.append(result)

        status = "PASS" if result["success"] else "FAIL"
        print(f"{status} | {result['status_code']} | {asset_url}")

        if result["error"]:
            print(f"Error: {result['error']}")

    write_log(results)

    failed_checks = [result for result in results if not result["success"]]

    print(f"\nResults logged to {LOG_FILE}")

    if failed_checks:
        print(f"Health check failed: {len(failed_checks)} issue(s) found.")
        sys.exit(1)

    print("Health check passed: homepage and discovered assets loaded successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()