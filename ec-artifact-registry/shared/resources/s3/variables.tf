
variable "artifact_registry_bucket" {
  type        = string
  description = "S3 Bucket where Registry Artifacts are stored"
}

variable "swa_org_id" {
  type    = string
  default = "o-sbfm45508y"
}

variable "allowed_org_ids_put" {
  type        = list(string)
  default     = ["o-sbfm45508y"]
  description = "AWS Organization Id's that are allowed to call PutObject"
}

variable "region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "ssm_namespace" {
  type    = string
  default = "/swacorp/ec/artifact_registry"
}

data "aws_caller_identity" "current" {}

provider "aws" {
  region  = var.region
  version = "~> 3.34.0"
}

terraform {
  backend "s3" {
    key     = "artifact_registry_s3"
    encrypt = true
  }
}
