# VehiclePricePrediction

```bash
curl -G \
  -d 'Year=2014' \
  -d 'Mileage=31909' \
  -d 'State=MD' \
  -d 'Make=Nissan' \
  -d 'Model=MuranoAWD' \
  "https://56wgw6okv8.execute-api.us-east-1.amazonaws.com/Prod/inference"
```

Check region y accountID
```bash
aws configure list
aws sts get-caller-identity --query Account --output text
```

```bash
aws --region <region> ecr get-login-password | docker login --username AWS --password-stdin <accountID>.dkr.ecr.<region>.amazonaws.com
```

```bash
aws ecr create-repository \
--repository-name "vehicle-price-prediction" \
--image-tag-mutability MUTABLE \
--image-scanning-configuration scanOnPush=true
```

se obtiene el "repositoryUri"
<region>.dkr.ecr.us-east-1.amazonaws.com/vehicle-price-prediction

```bash
aws ecr delete-repository --registry-id <account-id> --repository-name vehicle-price-prediction --force
```