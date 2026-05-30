# S3 Static Website Test Results

This document records the test results from running the S3 Website Health Check script against an Amazon S3 static website endpoint.

## Purpose

The purpose of this test was to check whether my S3 static website and its linked assets were loading correctly after deployment.

The script was used to:

- Check the main S3 static website endpoint
- Scan the homepage HTML
- Discover linked assets such as images, CSS, JavaScript and SVG files
- Check each discovered asset using HTTP status codes
- Log pass/fail results to a CSV file
- Identify access or loading issues for troubleshooting

## Website Tested

http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/

## Result Summary

The homepage returned a successful `200` response, meaning the main S3 static website endpoint was reachable.

Most linked assets also returned `200`, meaning they were publicly accessible and loading correctly.

However, several assets returned `403` responses. In an S3 static website context, a `403` response usually means the asset was requested but access was denied.

This can indicate issues such as:

- The object is not publicly accessible
- The bucket policy does not allow access to that object
- The file path is referenced in the HTML but the object permissions are incorrect
- The object exists but S3 is blocking public read access
- The asset may not display correctly on the website

## Example Successful Checks

200 | http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/

200 | http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/NextWork - You should be in a job you love_files/1.jpg

200 | http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/NextWork - You should be in a job you love_files/analytics.min.js

200 | http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/NextWork - You should be in a job you love_files/index.html

200 | http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/NextWork - You should be in a job you love_files/webflow.e2351bb6c.js

## Example Failed Checks

403 | http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/NextWork - You should be in a job you love_files/13.jpg

403 | http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/NextWork - You should be in a job you love_files/613.jpg.jpg

403 | http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/NextWork - You should be in a job you love_files/analytics(1).min.js

403 | http://nextwork-demo-website.s3-website-ap-southeast-2.amazonaws.com/NextWork - You should be in a job you love_files/global.js

## What I Learned

This test showed that a static website can appear to be working even when some linked assets are failing.

The homepage loaded successfully, but the script still found `403` errors for some assets. This showed me that checking only the homepage is not enough. Images, JavaScript files, CSS files or other linked assets can fail separately and affect how the site displays or behaves.

The `403` results gave me a clear troubleshooting direction. Instead of guessing what was wrong, I could use the script output to identify which specific assets needed to be checked in S3.

Based on these results, the next checks would be:

- Confirm the affected files exist in the bucket
- Check the exact object paths and filenames
- Review object permissions
- Review the bucket policy
- Check public access settings
- Confirm the HTML is referencing the correct file paths

## Real-World Value

This script is useful because it turns manual website checking into a repeatable process.

Instead of opening a website and visually checking whether everything looks right, the script checks the endpoint and discovered assets, records HTTP status codes and highlights which files need attention.

In a real support or platform operations scenario, this could help with:

- Checking whether a static website deployment is reachable
- Validating linked assets after deployment
- Detecting S3 permission or object access issues
- Producing a CSV log for troubleshooting
- Supporting basic monitoring and reliability checks

## Cost Management Note

The S3 static website used for this test was deleted after validation to avoid ongoing AWS costs.

The script, test results and documentation were kept as evidence of the test process and learning outcome.