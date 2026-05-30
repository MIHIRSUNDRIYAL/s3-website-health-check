# S3 Website Health Check

A Python automation script that checks an Amazon S3 static website endpoint, discovers linked assets and logs pass/fail results for troubleshooting.

## Why I built this

I built this after completing an AWS S3 static website hosting lab.

The original lab involved configuring:

- S3 static website hosting
- Bucket policies
- Public access settings
- Object permissions

After deploying the website, I wanted a simple way to check whether the homepage and linked assets were actually loading correctly.

## What it does

The script:

- Accepts a website endpoint as input
- Checks whether the homepage is reachable
- Scans the homepage HTML
- Discovers linked assets such as images, CSS, JavaScript and SVG files
- Checks each asset using HTTP status codes
- Prints pass/fail results in the terminal
- Logs results to a CSV file

## Tech used

- Python
- Requests
- CSV logging
- Amazon S3 static website hosting

## How to run

Install dependencies:

```bash
pip install -r requirements.txt