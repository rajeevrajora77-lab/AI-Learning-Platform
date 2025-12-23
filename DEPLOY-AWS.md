# AWS Deployment Guide for AI Learning Platform

## Prerequisites

- AWS Account with credentials configured
- Docker installed locally
- AWS CLI installed
- Git installed

## Step-by-Step Deployment

### 1. Build Docker Image

```bash
# Navigate to project root
cd AI-Learning-Platform

# Build Docker image
docker build -t ai-learning-platform:latest .

# Tag for ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker tag ai-learning-platform:latest <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ai-learning-platform:latest
```

### 2. Push to AWS ECR

```bash
# Create ECR repository if not exists
aws ecr create-repository --repository-name ai-learning-platform --region us-east-1

# Push image
docker push <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ai-learning-platform:latest
```

### 3. Set Up RDS Database

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier ai-learning-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password <YOUR_SECURE_PASSWORD> \
  --allocated-storage 20 \
  --region us-east-1

# Get endpoint
aws rds describe-db-instances \
  --db-instance-identifier ai-learning-db \
  --region us-east-1
```

### 4. Create ECS Task Definition

Create `ecs-task-definition.json`:

```json
{
  "family": "ai-learning-platform",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "ai-learning-platform",
      "image": "<YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ai-learning-platform:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        },
        {
          "name": "DATABASE_URL",
          "value": "postgresql://admin:<PASSWORD>@<RDS_ENDPOINT>:5432/ailearning"
        },
        {
          "name": "OPENAI_API_KEY",
          "value": "<YOUR_OPENAI_API_KEY>"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-learning-platform",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### 5. Register Task Definition

```bash
aws ecs register-task-definition \
  --cli-input-json file://ecs-task-definition.json \
  --region us-east-1
```

### 6. Create ECS Cluster

```bash
aws ecs create-cluster \
  --cluster-name ai-learning-cluster \
  --region us-east-1
```

### 7. Create ECS Service

```bash
aws ecs create-service \
  --cluster ai-learning-cluster \
  --service-name ai-learning-service \
  --task-definition ai-learning-platform:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx]}" \
  --region us-east-1
```

### 8. Set Up Load Balancer

```bash
# Create Application Load Balancer
aws elbv2 create-load-balancer \
  --name ai-learning-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx \
  --region us-east-1

# Create target group
aws elbv2 create-target-group \
  --name ai-learning-tg \
  --protocol HTTP \
  --port 5000 \
  --vpc-id vpc-xxxxx \
  --region us-east-1

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:ACCOUNT_ID:loadbalancer/app/ai-learning-alb/xxxxx \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:ACCOUNT_ID:targetgroup/ai-learning-tg/xxxxx \
  --region us-east-1
```

### 9. Set Up S3 for Video Storage

```bash
# Create S3 bucket
aws s3 mb s3://ai-learning-videos-<unique-suffix> \
  --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket ai-learning-videos-<unique-suffix> \
  --versioning-configuration Status=Enabled

# Set up CORS
aws s3api put-bucket-cors \
  --bucket ai-learning-videos-<unique-suffix> \
  --cors-configuration file://cors.json
```

### 10. Set Up CloudFront Distribution

```bash
# Create distribution for CDN
aws cloudfront create-distribution \
  --distribution-config file://cloudfront-config.json \
  --region us-east-1
```

### 11. Set Up CloudWatch Monitoring

```bash
# Create log group
aws logs create-log-group \
  --log-group-name /ecs/ai-learning-platform \
  --region us-east-1

# Create alarm
aws cloudwatch put-metric-alarm \
  --alarm-name ai-learning-cpu-high \
  --alarm-description "Alert when CPU is high" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=ServiceName,Value=ai-learning-service Name=ClusterName,Value=ai-learning-cluster \
  --region us-east-1
```

### 12. Configure Custom Domain

```bash
# Create Route53 record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch file://route53-change.json
```

### 13. Enable HTTPS with ACM

```bash
# Request certificate
aws acm request-certificate \
  --domain-name yourdomain.com \
  --validation-method DNS \
  --region us-east-1

# Update ALB listener with SSL
aws elbv2 modify-listener \
  --listener-arn arn:aws:elasticloadbalancing:us-east-1:ACCOUNT_ID:listener/app/ai-learning-alb/xxxxx/xxxxx \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:us-east-1:ACCOUNT_ID:certificate/xxxxx \
  --region us-east-1
```

## Post-Deployment

### Verify Deployment

```bash
# Check service status
aws ecs describe-services \
  --cluster ai-learning-cluster \
  --services ai-learning-service \
  --region us-east-1

# Check logs
aws logs tail /ecs/ai-learning-platform --follow --region us-east-1
```

### Health Checks

```bash
# Test API endpoint
curl https://yourdomain.com/api/health

# Expected response:
# {"status": "healthy", "timestamp": "2025-12-23T09:00:00.000000"}
```

### Scaling

```bash
# Update desired count
aws ecs update-service \
  --cluster ai-learning-cluster \
  --service ai-learning-service \
  --desired-count 3 \
  --region us-east-1
```

## Cost Estimation

| Service | Free Tier | Price | Monthly Cost |
|---------|-----------|-------|---------------|
| ECS Fargate | 750 hrs/month | $0.04644/hr | $34.83 |
| RDS t3.micro | 750 hrs/month | $0.017/hr | $12.75 |
| S3 Storage | 5GB | $0.023/GB | $2.30 |
| Data Transfer | 1GB free | $0.09/GB | $4.50 |
| CloudFront | 1TB free | $0.085/GB | $8.50 |
| **Total** | | | **~$63/month** |

## Troubleshooting

### Task won't start
- Check CloudWatch logs
- Verify IAM roles have proper permissions
- Check security group rules allow traffic

### Database connection error
- Verify RDS endpoint in environment variables
- Check security group allows 5432 from ECS
- Verify database credentials

### High CPU/Memory
- Increase task CPU/memory in task definition
- Implement caching
- Optimize code

## Rollback

```bash
# Revert to previous task definition version
aws ecs update-service \
  --cluster ai-learning-cluster \
  --service ai-learning-service \
  --task-definition ai-learning-platform:1 \
  --region us-east-1
```

## References

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Docker Documentation](https://docs.docker.com/)
