output "bucket_name" {
  description = "The name of the S3 bucket"
  value       = data.aws_s3_bucket.stock_scraper_bucket.bucket
}

output "instance_id" {
  description = "The ID of the instance"
  value       = aws_instance.stock_scraper_instance.id
}
