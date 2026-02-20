terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "fpl-notifier-terraform-state-uk"
    key    = "apprunner/terraform.tfstate"
    region = "eu-west-2" # London
    # Uncomment and configure for state locking
    # dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "fpl-notifier"
      ManagedBy   = "Terraform"
      Region      = "UK"
    }
  }
}

# Variables
variable "aws_region" {
  description = "AWS region - UK London"
  type        = string
  default     = "eu-west-2"
}

variable "github_connection_arn" {
  description = "ARN of GitHub connection (create this manually in AWS Console first)"
  type        = string
}

variable "repository_url" {
  description = "GitHub repository URL"
  type        = string
  default     = "https://github.com/exponentialcherub/fpl-notifier"
}

# Local variables for environments
locals {
  project_name = "fpl-notifier"
  
  environments = {
    dev = {
      branch = "develop"
      cpu    = "1 vCPU"
      memory = "2 GB"
    }
    prod = {
      branch = "main"
      cpu    = "1 vCPU"
      memory = "3 GB"
    }
  }
}

# Deploy App Runner services for each environment
module "apprunner" {
  source   = "./modules/apprunner"
  for_each = local.environments
  
  project_name           = local.project_name
  environment            = each.key
  branch_name            = each.value.branch
  cpu                    = each.value.cpu
  memory                 = each.value.memory
  github_connection_arn  = var.github_connection_arn
  repository_url         = var.repository_url
}

# Outputs
output "service_urls" {
  description = "URLs of App Runner web apps"
  value = {
    for env, module in module.apprunner :
    env => "https://${module.service_url}"
  }
}

output "service_arns" {
  description = "ARNs of App Runner services"
  value = {
    for env, module in module.apprunner :
    env => module.service_arn
  }
}
