provider "aws" {
  region  = "eu-central-1"
}

terraform {
  backend "s3" {}
}

terraform {
  required_providers {
    time = {
      source = "hashicorp/time"
      version = "~> 0.7"
    }
  }
}