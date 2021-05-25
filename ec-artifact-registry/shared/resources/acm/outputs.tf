output "regional_zone_id" {
  value = aws_api_gateway_domain_name.domain.regional_zone_id
}

output "regional_domain_name" {
  value = aws_api_gateway_domain_name.domain.regional_domain_name
}

output "certificate_arn" {
  value = module.acm.certificate_arn
}
