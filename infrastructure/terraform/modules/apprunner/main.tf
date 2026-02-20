# IAM Role for App Runner Instance
resource "aws_iam_role" "apprunner_instance_role" {
  name = "${var.project_name}-${var.environment}-instance-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "tasks.apprunner.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Attach CloudWatch Logs policy
resource "aws_iam_role_policy_attachment" "apprunner_logs" {
  role       = aws_iam_role.apprunner_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

# App Runner Service
resource "aws_apprunner_service" "webapp" {
  service_name = "${var.project_name}-${var.environment}"
  
  source_configuration {
    authentication_configuration {
      connection_arn = var.github_connection_arn
    }
    
    auto_deployments_enabled = true
    
    code_repository {
      repository_url = var.repository_url
      
      source_code_version {
        type  = "BRANCH"
        value = var.branch_name
      }
      
      code_configuration {
        configuration_source = "API"
        
        code_configuration_values {
          runtime        = "PYTHON_3"
          build_command  = "pip install -r requirements.txt"
          start_command  = "streamlit run webapp/app.py --server.port 8080 --server.address 0.0.0.0 --server.headless true"
          port           = "8080"
          
          runtime_environment_variables = {
            STREAMLIT_SERVER_HEADLESS            = "true"
            STREAMLIT_BROWSER_GATHER_USAGE_STATS = "false"
            ENVIRONMENT                          = var.environment
          }
        }
      }
    }
  }
  
  instance_configuration {
    cpu               = var.cpu
    memory            = var.memory
    instance_role_arn = aws_iam_role.apprunner_instance_role.arn
  }
  
  health_check_configuration {
    protocol            = "HTTP"
    path                = "/_stcore/health"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 1
    unhealthy_threshold = 5
  }
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}
