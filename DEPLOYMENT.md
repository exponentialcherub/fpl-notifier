# AWS App Runner Deployment Guide

## Prerequisites

1. **AWS Account** with App Runner access
2. **GitHub Repository** connected to AWS
3. **AWS CLI** installed and configured
4. **Terraform** (optional, for IaC deployment)

## Quick Start

### Option 1: AWS Console (Easiest)

1. **Create GitHub Connection**
   - Go to AWS App Runner → Connections
   - Click "Create connection"
   - Choose "GitHub"
   - Authorize AWS to access your repository

2. **Deploy Service**
   - Go to App Runner → Services → Create service
   - Source: Repository
   - Connect to GitHub and select `exponentialcherub/fpl-notifier`
   - Branch: `develop` (for dev) or `main` (for prod)
   - Build settings:
     - Configuration source: Use configuration file
     - Configuration file: `apprunner.yaml`
   - Service name: `fpl-notifier-dev` or `fpl-notifier-prod`
   - Click "Create & Deploy"

### Option 2: CloudFormation

1. **Create GitHub Connection** (one-time setup)
   ```bash
   # Go to AWS Console → App Runner → Connections
   # Create connection and note the ARN
   ```

2. **Deploy Dev Environment**
   ```bash
   aws cloudformation create-stack \
     --stack-name fpl-notifier-dev \
     --template-body file://infrastructure/cloudformation/apprunner-dev.yaml \
     --parameters \
       ParameterKey=GitHubConnectionArn,ParameterValue=YOUR_CONNECTION_ARN \
       ParameterKey=RepositoryUrl,ParameterValue=https://github.com/exponentialcherub/fpl-notifier \
       ParameterKey=BranchName,ParameterValue=develop \
     --capabilities CAPABILITY_NAMED_IAM \
     --region us-east-1
   ```

3. **Deploy Prod Environment**
   ```bash
   aws cloudformation create-stack \
     --stack-name fpl-notifier-prod \
     --template-body file://infrastructure/cloudformation/apprunner-prod.yaml \
     --parameters \
       ParameterKey=GitHubConnectionArn,ParameterValue=YOUR_CONNECTION_ARN \
       ParameterKey=RepositoryUrl,ParameterValue=https://github.com/exponentialcherub/fpl-notifier \
       ParameterKey=BranchName,ParameterValue=main \
     --capabilities CAPABILITY_NAMED_IAM \
     --region us-east-1
   ```

### Option 3: Terraform

1. **Initialize Terraform**
   ```bash
   cd infrastructure/terraform
   terraform init
   ```

2. **Create variables file**
   ```bash
   cat > terraform.tfvars <<EOF
   aws_region = "us-east-1"
   github_connection_arn = "YOUR_CONNECTION_ARN"
   repository_url = "https://github.com/exponentialcherub/fpl-notifier"
   EOF
   ```

3. **Deploy infrastructure**
   ```bash
   terraform plan
   terraform apply
   ```

4. **Get service URLs**
   ```bash
   terraform output service_urls
   ```

## CI/CD Setup

### GitHub Actions

1. **Add GitHub Secrets**
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`
     - `APP_RUNNER_SERVICE_ARN_DEV` (from CloudFormation/Terraform output)
     - `APP_RUNNER_SERVICE_ARN_PROD` (from CloudFormation/Terraform output)

2. **Automatic Deployments**
   - Push to `develop` branch → Deploys to dev
   - Push to `main` branch → Deploys to prod

## Environment Configuration

### Dev Environment
- **Branch**: `develop`
- **URL**: `https://fpl-notifier-dev.REGION.awsapprunner.com`
- **Resources**: 1 vCPU, 2 GB RAM
- **Auto-deploy**: Enabled

### Prod Environment
- **Branch**: `main`
- **URL**: `https://fpl-notifier-prod.REGION.awsapprunner.com`
- **Resources**: 1 vCPU, 3 GB RAM
- **Auto-deploy**: Enabled

## File Structure

```
.
├── requirements.txt              # Python dependencies
├── apprunner.yaml               # App Runner configuration
├── Dockerfile                   # Docker configuration (optional)
├── .streamlit/
│   └── config.toml             # Streamlit config
├── infrastructure/
│   ├── cloudformation/
│   │   ├── apprunner-dev.yaml  # Dev CloudFormation template
│   │   └── apprunner-prod.yaml # Prod CloudFormation template
│   └── terraform/
│       └── main.tf             # Terraform configuration
└── .github/
    └── workflows/
        ├── deploy-dev.yml      # Dev deployment workflow
        └── deploy-prod.yml     # Prod deployment workflow
```

## Cost Estimates

### Dev Environment
- Compute: ~$7/month (1 vCPU, 2GB RAM, ~730 hours)
- Data transfer: ~$1-2/month
- **Total**: ~$8-9/month

### Prod Environment
- Compute: ~$12/month (1 vCPU, 3GB RAM, ~730 hours)
- Data transfer: ~$2-3/month
- **Total**: ~$14-15/month

### Both Environments
- **Total**: ~$22-24/month

## Monitoring

View logs in AWS Console:
- App Runner → Services → Select service → Logs

Or use AWS CLI:
```bash
aws logs tail /aws/apprunner/fpl-notifier-dev/service --follow
```

## Troubleshooting

### Build Failures
1. Check `requirements.txt` is present
2. Verify Python version compatibility
3. Check App Runner logs

### Deployment Failures
1. Verify GitHub connection is active
2. Check IAM permissions
3. Review CloudFormation/Terraform errors

### Health Check Failures
1. Ensure app runs on port 8080
2. Verify `/_stcore/health` endpoint is accessible
3. Check application logs

## Cleanup

### CloudFormation
```bash
aws cloudformation delete-stack --stack-name fpl-notifier-dev
aws cloudformation delete-stack --stack-name fpl-notifier-prod
```

### Terraform
```bash
cd infrastructure/terraform
terraform destroy
```

## Next Steps

1. Set up custom domain (Route 53)
2. Configure SSL certificate (ACM)
3. Set up monitoring/alerting (CloudWatch)
4. Configure secrets management (Secrets Manager)
5. Add database (RDS) if needed
