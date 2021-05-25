locals {
  account_id          = data.aws_caller_identity.current.account_id
  aws_org_id          = "o-sbfm45508y"
  formatted_workspace = lower(replace(terraform.workspace, "/\\./", "-"))
  hosted_zone_name = trimspace(<<EOS
%{if var.git_branch == "main"~}${lower(var.base_hosted_zone_name)}%{else}${lower("${var.git_branch}.${var.base_hosted_zone_name}")}%{endif~}
EOS
  )
  domain_name = "${local.formatted_workspace}.api.${local.hosted_zone_name}"
  cert_cn     = "*.api.${local.hosted_zone_name}"
  stage_name  = local.formatted_workspace
}

resource "random_string" "entropy_id" {
  length  = 8
  special = false
}

module "acm" {
  source                        = "git::https://stash1-tools.swacorp.com/scm/ec/ec-terraform-modules.git//acm?ref=refs/tags/v0.5.2"
  region                        = var.region
  ssl_certificate_common_name   = local.cert_cn
  display_name                  = "new_account_artifact_registry_api_cert_${terraform.workspace}"
  certificate_authority_arn     = var.ca_arn
  swa_cs_manager_cert_role      = var.ca_role
  private_key_secret_name       = "/swa/ec/artifact_registry/${terraform.workspace}/certs/private_key_${random_string.entropy_id.result}"
  certificate_secret_name       = "/swa/ec/artifact_registry/${terraform.workspace}/certs/certificate_${random_string.entropy_id.result}"
  certificate_chain_secret_name = "/swa/ec/artifact_registry/${terraform.workspace}/certs/certificate_chain_${random_string.entropy_id.result}"
  subject_alt_names = [
    local.cert_cn
  ]
  tags = {
    TF_WORKSPACE = terraform.workspace
  }
}



resource "aws_api_gateway_domain_name" "domain" {
  domain_name              = local.domain_name
  regional_certificate_arn = module.acm.certificate_arn
  security_policy          = "TLS_1_2"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

data "aws_ssm_parameter" "artifact_registry_api" {
  name = "${var.ssm_namespace}/ec-artifact-registry-service/api_gateway"
}

data "aws_ssm_parameter" "artifact_deployment_api" {
  name = "${var.ssm_namespace}/ec-artifact-deployment-service/api_gateway"
}

data "aws_api_gateway_rest_api" "artifact_registry_api" {
  name = data.aws_ssm_parameter.artifact_registry_api.value
}

data "aws_api_gateway_rest_api" "artifact_deployment_api" {
  name = data.aws_ssm_parameter.artifact_deployment_api.value
}

resource "aws_api_gateway_base_path_mapping" "artifact_registry_api" {
  api_id      = data.aws_api_gateway_rest_api.artifact_registry_api.id
  stage_name  = terraform.workspace
  domain_name = aws_api_gateway_domain_name.domain.domain_name
  base_path   = "artifacts"
}

resource "aws_api_gateway_base_path_mapping" "artifact_deployment_api" {
  api_id      = data.aws_api_gateway_rest_api.artifact_deployment_api.id
  stage_name  = terraform.workspace
  domain_name = aws_api_gateway_domain_name.domain.domain_name
  base_path   = "deployments"
}
