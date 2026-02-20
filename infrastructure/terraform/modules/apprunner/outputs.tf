output "service_url" {
  description = "URL of the App Runner service"
  value       = aws_apprunner_service.webapp.service_url
}

output "service_arn" {
  description = "ARN of the App Runner service"
  value       = aws_apprunner_service.webapp.arn
}

output "service_id" {
  description = "ID of the App Runner service"
  value       = aws_apprunner_service.webapp.service_id
}

output "service_status" {
  description = "Status of the App Runner service"
  value       = aws_apprunner_service.webapp.status
}
