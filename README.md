# Serverless URL Monitoring System (AWS + Terraform)

## Overview
This project is a lightweight, cost‑efficient, serverless URL monitoring system built on AWS.  
It checks the health of one or more URLs every 5 minutes and sends an email alert if any endpoint becomes unreachable or returns an unexpected response.

The entire infrastructure is deployed using **Terraform**, making it reproducible and easy to maintain.

---

## Architecture

### Components
- **Amazon EventBridge**  
  Schedules the Lambda function to run every 5 minutes.

- **AWS Lambda (Python)**  
  Performs HTTP(S) health checks against the configured URLs.  
  Detects:
  - Non‑200 responses  
  - Timeouts  
  - SSL certificate issues  
  - Connection failures  

- **Amazon SNS**  
  Sends email alerts when a URL check fails.

- **Amazon CloudWatch Logs**  
  Stores Lambda execution logs for debugging and monitoring.

- **Terraform**  
  Deploys and manages all AWS resources.

---

## How It Works

1. EventBridge triggers the Lambda function on a 5‑minute schedule.
2. Lambda checks each URL defined in the environment variables.
3. If a URL fails (status code, timeout, SSL error, etc.), Lambda publishes a message to SNS.
4. SNS sends an email alert to the configured recipient.
5. CloudWatch Logs capture execution details for troubleshooting.

---

## Prerequisites
### Terraform installed (recommended: latest version)

### Access to the target cloud provider (AWS)

### Credentials configured locally
```bash
aws configure
```
### optional, configure HCP remote backend and save AWS credentials as a secret on HCP.

## Update Environment variables
``` bash
cd terraform
vim terrform.tfvars
```
### update the values as per requirments
``` bash
alert_email = "youremail@gmail.com"

urls_to_monitor = [
  "https://google.com",
  "https://example.com",
  "https://your-api.com/health"
]
```

## Initialize Terraform
```bash
terraform init
```
## validate Terraform
``` bash
terraform validate
```
## Plan terraform
``` bash
terraform plan
```
## Apply terraform
``` bash
terraform apply --auto-approve
```
## Destroy Terraform Infra if doing demo
``` bash
terraform destroy --auto-approve
```


