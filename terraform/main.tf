terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "inventory_state" {
    bucket = "connor-inventory-api-tf-state"

    tags = {
        Name            = "inventory-api-tf-state"
        Environment    = "dev" 
        Project         = "inventory-api"
    }
}
output "s3_bucket_name" {
  value       = aws_s3_bucket.inventory_state.bucket
  description = "The name of the S3 bucket"
}