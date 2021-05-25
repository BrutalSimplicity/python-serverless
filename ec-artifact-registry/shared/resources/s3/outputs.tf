output "arn" {
  description = "The ARN of the EC Artifact Registry Bucket"
  value       = module.artifact_registry.arn
}

output "id" {
  description = "The name of the EC Artifact Registry Bucket"
  value       = module.artifact_registry.id
}

resource "aws_ssm_parameter" "arn" {
  name  = "${var.ssm_namespace}/registry_bucket/arn"
  value = module.artifact_registry.arn
  type  = "String"
}

resource "aws_ssm_parameter" "name" {
  name  = "${var.ssm_namespace}/registry_bucket/name"
  value = module.artifact_registry.id
  type  = "String"
}
