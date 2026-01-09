variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "alert_email" {
  description = "Email address for SNS alerts"
  type        = string
}

variable "urls_to_monitor" {
  description = "List of URLs to monitor"
  type        = list(string)
}
