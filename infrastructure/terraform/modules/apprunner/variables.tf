variable "environment" {
  description = "Environment name (dev/prod)"
  type        = string
}

variable "branch_name" {
  description = "Git branch to deploy"
  type        = string
}

variable "cpu" {
  description = "CPU allocation"
  type        = string
  default     = "1 vCPU"
}

variable "memory" {
  description = "Memory allocation"
  type        = string
  default     = "2 GB"
}

variable "github_connection_arn" {
  description = "ARN of GitHub connection"
  type        = string
}

variable "repository_url" {
  description = "GitHub repository URL"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "fpl-notifier"
}
