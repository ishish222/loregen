variable "terraform_bucket" {
    description = "The name of the S3 bucket to use for Terraform state"
    type        = string
    default     = "srm-terraform.korrino.com"
}

variable "aws_region" {
    description = "The AWS region"
    type        = string
    default     = "eu-central-1"
}

variable "aws_account" {
    description = "The AWS account ID"
    type        = string
    default     = "242532629527"
}

variable "alb_domain_name" {
    description = "The domain name for the ALB"
    type        = string
    default     = "srm.korrino.com"
}

variable "callback_custom_domain" {
    description = "The domain name for the callback API"
    type        = string
    default     = "callback.srm.korrino.com"
}

variable "route53_zone" {
    description = "The name of the Route53 zone"
    type        = string
    default     = "srm.korrino.com."
}

variable "certificate_arn" {
  description = "The ARN of the certificate to use for HTTPS"
  type = string
  default = "arn:aws:acm:eu-central-1:242532629527:certificate/f7b6e317-229d-4eeb-8d1a-b02e28f9a629"
}

variable "certificate_arn_subdomains" {
  description = "The ARN of the certificate to use for subdomains"
  type = string
  default = "arn:aws:acm:eu-central-1:242532629527:certificate/d2c23fe4-60b5-485f-8a58-d1971c6ea1b8"
}

variable "script_name" {
  description = "The name of the script to run"
  type = string
  default = "app.py"
}

variable "environment" {
    description = "The environment to run the script in"
    type        = string
    default     = "dev"
}

variable "app_host" {
    description = "The host to run the app on"
    type        = string
    default     = "0.0.0.0"
}

variable "app_port" {
    description = "The host to run the app on"
    type        = string
    default     = "80"
}

variable "dashboard_image" {
    description = "The Docker image to use for the Loregen's dashboard"
    type        = string
    default     = "242532629527.dkr.ecr.eu-central-1.amazonaws.com/loregen_front/dashboard:latest"
}

variable "cache_bucket" {
    description = "The name of the S3 bucket to use for caching"
    type        = string
    default     = "textract-cache.korrino.com"
}

variable "cache_prefix" {
    description = "The name of the S3 prefix to use for caching"
    type        = string
    default     = "cache"
}

variable "dynamodb_table_name" {
  description = "The name of the table for counting tokens"
  type = string
  default = "token_counter"
}

variable "dynamodb_default_item" {
  description = "The name of the default item for counting tokens"
  type = string
  default = "default"
}

variable "cognito_domain" {
    description = "The domain for the Cognito user pool"
    type        = string
    default     = "https://account.srm.korrino.com"
}

variable "cognito_domain_client_id" {
    description = "The client ID for the Cognito user pool"
    type        = string
    default     = "3stul40m2rgf1rivcq5lc2lfd2"
}

variable "cognito_domain_redirect_uri_login" {
    description = "The redirect URI for the Cognito user pool login"
    type        = string
    default     = "https://srm.korrino.com/login_done"
}

variable "cognito_domain_redirect_uri_logout" {
    description = "The redirect URI for the Cognito user pool logout"
    type        = string
    default     = "https://srm.korrino.com/logout_done"
}

variable "cognito_domain_region" {
    description = "The region for the Cognito user pool"
    type        = string
    default     = "eu-central-1"
}

variable "cognito_domain_user_pool_id" {
    description = "The user pool ID for the Cognito user pool"
    type        = string
    default     = "eu-central-1_SMPYtAEFp"
}

variable "db_name" {
    description = "The name of the database"
    type        = string
    default     = "srm_db"
}

variable "db_username" {
    description = "The username for the database"
    type        = string
    default     = "admin"
}

variable "db_port" {
    description = "The port for the database"
    type        = string
    default     = "3306"
}

variable "layer_bucket_name" {
  description = "Dependencies layer bucket name"
  type        = string
  default    = "srm.dependencies-bucket.sedivio.com"
}

variable "dns_zone_id" {
  description = "The ID of the srm.korrino.com zone"
  type        = string
  default     = "Z0512801208BER8E0TLMZ"
  
}

variable "restore_from_snapshot" {
  description = "The name of the snapshot to restore from"
  type        = bool
  default     = false
}
