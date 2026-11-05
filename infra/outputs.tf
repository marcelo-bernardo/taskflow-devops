output "instance_public_ip" {
  description = "IP publico do servidor da aplicacao"
  value       = aws_instance.app.public_ip
}

output "api_url" {
  description = "URL de health check da API"
  value       = "http://${aws_instance.app.public_ip}:5000/health"
}

output "artifacts_bucket" {
  description = "Nome do bucket S3 de artefatos"
  value       = aws_s3_bucket.artifacts.bucket
}
