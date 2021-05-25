resource "aws_ssm_parameter" "arn" {
  name      = "${var.ssm_namespace}/registry_table/arn"
  value     = aws_dynamodb_table.artifact_registry.arn
  overwrite = true
  type      = "String"
}

resource "aws_ssm_parameter" "stream_arn" {
  name      = "${var.ssm_namespace}/registry_table/stream_arn"
  value     = aws_dynamodb_table.artifact_registry.stream_arn
  overwrite = true
  type      = "String"
}

resource "aws_ssm_parameter" "name" {
  name      = "${var.ssm_namespace}/registry_table/name"
  value     = aws_dynamodb_table.artifact_registry.id
  overwrite = true
  type      = "String"
}
