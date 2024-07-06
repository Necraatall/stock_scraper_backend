# terraform/backend.tf
terraform {
  backend "s3" {
    bucket = "terraform-stock-scraper-state-bucket"
    key    = "terraform/state/terraform.tfstate"
    region = "us-east-1"
  }
}
