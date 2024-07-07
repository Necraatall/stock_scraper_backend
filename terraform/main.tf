provider "aws" {
  region = var.region
}

data "aws_s3_bucket" "stock_scraper_bucket" {
  bucket = var.bucket_name
}

data "aws_iam_user" "existing_user" {
  user_name = var.ci_cd_user_name
}

resource "aws_instance" "stock_scraper_instance" {
  ami           = var.ami
  instance_type = var.instance_type

  tags = {
    Name = "StockScraperInstance"
  }
}

resource "aws_ecr_repository" "public_repo" {
  name                 = var.ecr_repo_name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_iam_user" "ci_cd_user" {
  count = data.aws_iam_user.existing_user.id == "" ? 1 : 0
  name  = var.ci_cd_user_name
}

resource "aws_iam_access_key" "ci_cd_access_key" {
  count = data.aws_iam_user.existing_user.id == "" ? 1 : 0
  user  = var.ci_cd_user_name
}

resource "aws_iam_user_policy" "ecr_access_policy" {
  name = "ecr-access-policy"
  user = var.ci_cd_user_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ecr:*"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}
