# S3 Website Health Check

A small Python automation project that checks the availability of an Amazon S3 static website endpoint and selected website assets.

## What it does

- Checks whether an S3 static website endpoint is reachable
- Validates selected assets such as `index.html` and `style.css`
- Prints pass/fail results with HTTP status codes
- Logs check results to a CSV file
- Supports basic monitoring and troubleshooting for static website hosting

## Why I built this

I created this project after completing an AWS S3 static website hosting lab. The original lab involved configuring S3 static hosting, bucket policies, public access settings and object permissions. I then extended the lab by writing a Python health-check script to practise automation, monitoring and troubleshooting.

## Tech used

- Python
- Requests
- CSV logging
- Amazon S3 static website hosting

## How to run

Install dependencies:

```bash
pip install -r requirements.txt
