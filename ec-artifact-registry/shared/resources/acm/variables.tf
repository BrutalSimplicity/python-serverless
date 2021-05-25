variable "region" {
  type = string
}


variable "base_hosted_zone_name" {
  type = string
}

variable "git_branch" {
  type = string
}

variable "ca_arn" {
  type        = string
  description = "ACM PCA Certificate Authority Arn"
}

variable "ca_role" {
  type        = string
  description = "IAM Role that is used to issue a certificate in the ACM-PCA."
}


variable "create_hosted_zone" {
  type        = bool
  description = "create the hosted zone or not?"
}

variable "ssm_namespace" {
  type = string
}

data "aws_caller_identity" "current" {}

data "aws_kms_key" "swa_kms_key" {
  key_id = "alias/swa_${data.aws_caller_identity.current.account_id}_kms"
}

terraform {
  backend "s3" {
    key     = "artifact_registry_acm"
    encrypt = true
  }
}

provider "aws" {
  region  = var.region
  version = "~> 3.34.0"
}
