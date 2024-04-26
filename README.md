# VehiclePricePrediction

```bash
curl --request POST \
  --url https://localhost:3000/inference \
  --header 'content-type: application/json' \
  --data '{
        "data": {
                "Year": 2014,
                "Mileage": 31909,
                "State": " MD",
                "Make": "Nissan",
                "Model": "MuranoAWD"
        }
    }'
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