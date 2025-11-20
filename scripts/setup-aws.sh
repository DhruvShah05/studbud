#!/bin/bash

# AWS Deployment Setup Script for StudBud
# This script helps automate the initial AWS setup

set -e  # Exit on error

echo "🚀 StudBud AWS Deployment Setup"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found${NC}"
    echo "Install with: brew install awscli"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo -e "${RED}❌ EB CLI not found${NC}"
    echo "Install with: pip install awsebcli"
    exit 1
fi

echo -e "${GREEN}✅ Required CLIs found${NC}"
echo ""

# Get AWS credentials
echo "📋 AWS Configuration"
echo "===================="
read -p "AWS Region (default: us-east-1): " AWS_REGION
AWS_REGION=${AWS_REGION:-us-east-1}

read -p "Application Name (default: studbud-backend): " APP_NAME
APP_NAME=${APP_NAME:-studbud-backend}

read -p "Environment Name (default: studbud-backend-prod): " ENV_NAME
ENV_NAME=${ENV_NAME:-studbud-backend-prod}

read -p "Instance Type (default: t3.small): " INSTANCE_TYPE
INSTANCE_TYPE=${INSTANCE_TYPE:-t3.small}

echo ""
echo "🔐 Environment Variables Setup"
echo "=============================="

read -p "GEMINI_API_KEY: " GEMINI_API_KEY
read -p "DEEPGRAM_API_KEY: " DEEPGRAM_API_KEY
read -sp "FLASK_SECRET_KEY (will be hidden): " FLASK_SECRET_KEY
echo ""
read -p "DB_HOST (RDS endpoint): " DB_HOST
read -sp "DB_PASSWORD (will be hidden): " DB_PASSWORD
echo ""
read -p "AWS_ACCESS_KEY_ID: " AWS_ACCESS_KEY_ID
read -sp "AWS_SECRET_ACCESS_KEY (will be hidden): " AWS_SECRET_ACCESS_KEY
echo ""
read -p "S3_BUCKET_NAME: " S3_BUCKET_NAME
read -p "Frontend URL (for CORS, e.g., https://app.vercel.app): " FRONTEND_URL

echo ""
echo "📦 Creating S3 Bucket..."
aws s3 mb s3://${S3_BUCKET_NAME} --region ${AWS_REGION} 2>/dev/null || echo "Bucket already exists"

echo ""
echo "🔧 Initializing Elastic Beanstalk..."
cd backend

# Initialize EB
eb init -p python-3.11 ${APP_NAME} --region ${AWS_REGION}

echo ""
echo "🏗️  Creating Elastic Beanstalk Environment..."
echo "This may take 5-10 minutes..."
eb create ${ENV_NAME} --instance-type ${INSTANCE_TYPE} --single

echo ""
echo "⚙️  Setting Environment Variables..."
eb setenv \
  GEMINI_API_KEY=${GEMINI_API_KEY} \
  DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY} \
  FLASK_SECRET_KEY=${FLASK_SECRET_KEY} \
  DB_HOST=${DB_HOST} \
  DB_PORT=5432 \
  DB_NAME=studbud \
  DB_USER=postgres \
  DB_PASSWORD=${DB_PASSWORD} \
  AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  AWS_REGION=${AWS_REGION} \
  S3_BUCKET_NAME=${S3_BUCKET_NAME} \
  FLASK_ENV=production \
  ALLOWED_ORIGINS=${FRONTEND_URL} \
  PORT=8000

echo ""
echo "🚀 Deploying Application..."
eb deploy

echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo "📊 Application Status:"
eb status

echo ""
echo "🌐 Your backend is deployed at:"
eb status | grep CNAME | awk '{print "https://"$2}'

echo ""
echo "📝 Next Steps:"
echo "1. Deploy frontend to Vercel with the backend URL above"
echo "2. Update ALLOWED_ORIGINS with your Vercel URL"
echo "3. Setup GitHub Actions secrets (see DEPLOYMENT.md)"
echo "4. Push to GitHub to enable auto-deployment"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"
