locals {
  artifact_registry_bucket = lower(substr(var.artifact_registry_bucket, 0, 59))
}

module "artifact_registry" {
  source              = "git::https://stash1-tools.swacorp.com/scm/ec/ec-terraform-modules.git//s3?ref=refs/tags/v0.5.2"
  bucket_name         = local.artifact_registry_bucket
  force_destroy       = contains(["dev", "qa", "prod"], terraform.workspace) ? false : true
  region              = var.region
  allowed_org_ids_put = var.allowed_org_ids_put
}

resource "aws_s3_bucket_metric" "artifact_registry" {
  bucket = module.artifact_registry.id
  name   = "EC-New-Account-Artifact-Registry-${terraform.workspace}"
}
