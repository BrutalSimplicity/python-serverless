
variable "region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "artifact_registry_table" {
  type        = string
  description = "Table that stores information about New Account Artifacts.  This is not the same as the DDE Artifact Registry."
  default     = "deployment-artifact-registry-table"
}

variable "ssm_namespace" {
  type    = string
  default = "/swacorp/ec/artifact_registry"
}

provider "aws" {
  region  = var.region
  version = "~> 3.34.0"
}

data "aws_caller_identity" "current" {}

data "aws_kms_key" "swa_kms_key" {
  key_id = "alias/swa_${data.aws_caller_identity.current.account_id}_kms"
}

terraform {
  backend "s3" {
    key     = "artifact_registry_dynamodb"
    encrypt = true
  }
}
