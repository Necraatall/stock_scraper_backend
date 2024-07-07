output "bucket_name" {
  description = "The name of the S3 bucket"
  value       = data.aws_s3_bucket.stock_scraper_bucket.bucket
}

output "instance_id" {
  description = "The ID of the instance"
  value       = aws_instance.stock_scraper_instance.id
}

output "repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.public_repo.repository_url
}

output "ci_cd_access_key_id" {
  description = "The access key ID for the CI/CD user"
  value       = length(aws_iam_access_key.ci_cd_access_key) > 0 ? aws_iam_access_key.ci_cd_access_key[0].id : ""
}

output "ci_cd_secret_access_key" {
  description = "The secret access key for the CI/CD user"
  value       = length(aws_iam_access_key.ci_cd_access_key) > 0 ? aws_iam_access_key.ci_cd_access_key[0].secret : ""
  sensitive   = true
}
