provider "aws" {
  region = var.region
}

data "aws_s3_bucket" "stock_scraper_bucket" {
  bucket = var.bucket_name
}

resource "aws_instance" "stock_scraper_instance" {
  ami           = var.ami
  instance_type = var.instance_type

  tags = {
    Name = "StockScraperInstance"
  }
}
