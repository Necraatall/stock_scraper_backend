variable "region" {
  description = "The AWS region to create resources in"
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "The name of the existing S3 bucket"
  default     = "terraform-stock-scraper-state-bucket"
}

variable "ami" {
  description = "The AMI to use for the instance"
  default     = "ami-029eb80bc237bec6f"
}

variable "instance_type" {
  description = "The instance type to use"
  default     = "t2.micro"
}
