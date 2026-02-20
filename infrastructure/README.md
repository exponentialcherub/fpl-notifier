# Infrastructure Overview

## What Each File Does

### **Essential for Web App** ✅

1. **`requirements.txt`** (Root directory)
   - Lists Python packages your web app needs
   - Used by AWS to install dependencies when deploying
   
2. **`apprunner.yaml`** (Root directory)
   - Tells AWS App Runner how to build and run your web app
   - Specifies port, build commands, runtime settings
   
3. **`.streamlit/config.toml`** (Root directory)
   - Configures Streamlit web app settings
   - Sets theme, ports, browser behavior

### **Infrastructure as Code (Choose ONE)** 📋

#### **Option A: Terraform** (Recommended for version control)
- `terraform/main.tf` - Main configuration file
- `terraform/modules/apprunner/` - Reusable module for App Runner
  - `main.tf` - Creates the App Runner service
  - `variables.tf` - Input parameters
  - `outputs.tf` - Returns service URLs and ARNs

**Purpose**: Automates creation of AWS resources using code
**When to use**: You want infrastructure versioned in git

#### **Option B: CloudFormation**
- `cloudformation/apprunner-dev.yaml` - Dev environment template
- `cloudformation/apprunner-prod.yaml` - Prod environment template

**Purpose**: Same as Terraform but AWS-native
**When to use**: You prefer AWS-native tools

### **CI/CD (Optional but Recommended)** 🔄

- `.github/workflows/deploy-dev.yml` - Auto-deploys on push to `develop`
- `.github/workflows/deploy-prod.yml` - Auto-deploys on push to `main`

**Purpose**: Automatically deploys your app when you push code
**When to use**: You want automatic deployments

### **Optional**

- **`Dockerfile`** - Container configuration (not needed if using `apprunner.yaml`)

## Resource Purpose

### What is App Runner?
**App Runner** is AWS's simplest way to run a web application. It:
- Builds your code from GitHub
- Runs your Streamlit web app
- Provides a public URL (e.g., `https://xxx.eu-west-2.awsapprunner.com`)
- Auto-scales based on traffic
- Handles SSL/HTTPS certificates
- Monitors health and restarts if needed

### What Resources Does Terraform/CloudFormation Create?

1. **IAM Role** - Gives App Runner permission to write logs to CloudWatch
2. **App Runner Service** - The actual web application running your code

That's it! Just 2 AWS resources per environment.

## Terraform Module Structure

```
infrastructure/terraform/
├── main.tf                      # Main entry point
│   ├── Defines AWS provider (London region)
│   ├── Calls apprunner module for dev
│   └── Calls apprunner module for prod
│
└── modules/apprunner/           # Reusable module
    ├── main.tf                  # Creates IAM role + App Runner service
    ├── variables.tf             # Input parameters (env, branch, cpu, etc.)
    └── outputs.tf               # Returns service URL and ARN
```

## Why Modules?

**Before (monolithic):**
```
main.tf (200 lines)
├── All dev resources
└── All prod resources
```

**After (modular):**
```
main.tf (50 lines) - just calls modules
modules/apprunner/ (80 lines) - reusable logic
```

**Benefits:**
- ✅ **DRY** - Write once, use for dev AND prod
- ✅ **Testable** - Can test module independently
- ✅ **Reusable** - Can add staging/qa environments easily
- ✅ **Maintainable** - Changes in one place apply everywhere

## Region Configuration

All resources are now configured for **London, UK**:
- AWS Region: `eu-west-2`
- This ensures data stays in UK for compliance/latency

## Minimal Setup (Just Web App)

If you only want the web app, you need:

```
fpl-notifier/
├── requirements.txt              ✅ Essential
├── apprunner.yaml               ✅ Essential
├── .streamlit/config.toml       ✅ Essential
├── webapp/app.py                ✅ Your app code
└── infrastructure/
    └── terraform/               ✅ Choose Terraform OR CloudFormation
        ├── main.tf
        └── modules/apprunner/
```

**Optional but helpful:**
- `.github/workflows/` - For auto-deployment
- `Dockerfile` - If you prefer Docker over apprunner.yaml
- CloudFormation templates - Alternative to Terraform

## Quick Start

1. **Choose your IaC tool**: Terraform or CloudFormation
2. **Create GitHub connection** in AWS Console (one-time)
3. **Deploy**:
   ```bash
   # Terraform
   cd infrastructure/terraform
   terraform init
   terraform apply
   
   # OR CloudFormation
   aws cloudformation create-stack ...
   ```
4. **Access your web app** at the URL provided

## Cost Breakdown

Per environment (dev or prod):
- **App Runner compute**: ~$7-15/month depending on CPU/RAM
- **Data transfer**: ~$1-3/month
- **CloudWatch logs**: ~$0.50/month
- **Total**: ~$8-20/month per environment

Both dev + prod: **~$16-40/month**
