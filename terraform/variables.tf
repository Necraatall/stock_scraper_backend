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

variable "ecr_repo_name" {
  description = "The name of the ECR repository"
  default     = "public.ecr.aws/d8o8x6c7/stock_scraper_backend"
}

variable "ci_cd_user_name" {
  description = "The name of the CI/CD IAM user"
  default     = "technical_user"
}

variable "bucket" {
  description = "The name of the S3 bucket for Terraform state"
  default     = "terraform-stock-scraper-state-bucket"
}

variable "key" {
  description = "The key for the Terraform state file"
  default     = "terraform/state/terraform.tfstate"
}
