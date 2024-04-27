[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/es/)
[![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)](https://peps.python.org/pep-0596/#schedule-first-bugfix-release)
[![XGBoost-CI](https://github.com/dmlc/xgboost/workflows/XGBoost-CI/badge.svg?branch=master)](https://github.com/dmlc/xgboost/actions)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/r/amazon/aws-lambda-python)
[![Json](https://img.shields.io/badge/json-5E5C5C?style=flat-square&logo=json&logoColor=white)](vehicle_price_prediction/events/event.json)
[![Hoppscotch](https://img.shields.io/badge/Hoppscotch-31C48D?style=flat-square&logo=hoppscotch&logoColor=white)](https://hoppscotch.io/)
![GitHub last commit](https://img.shields.io/github/last-commit/HubertRonald/VehiclePricePrediction?style=flat-square)

# VehiclePricePrediction

## Infraestructura - IaC
El respositorio actual permite desplegar la siguiente arquitectura para disponibilizar un modelo que predice los precios de un vehículo, previamente calibrado con optuna y entrenado con xgboost.

![](./src/aws_apiRest_serverless_model_xgboost_optuna.png)

## Modelo Predictivo

El pipeline que se [serializó](./vehicle_price_prediction/model_inference/model/) fue el que se muestra a continuación

<div style="text-align:center"><img width="60%" src="./src/Pipeline.png" /></div>

En el pipeline-1 se hace un tratamiento para las variables predictoras numéricas, mientras que en el pipeline-2 se hace lo propio pero con las variables predictoras categorias.

Finalmente estas variables predictioras y de test que ya están separadas en muestras de entrenamiento y test son empleadas en un modelo xgboostRegressor con hiperparametros ya calibrados previamente con Optuna.

## Desplegando el Servicio

Se efectuan los siguientes pasos:

1. Al ingresar a AWS se levanta el servicio cloud9, con una instancia EC2 de por lo menos t3.medium y se clona este respositorio
   ```bash
   $ git clone https://github.com/HubertRonald/VehiclePricePrediction.git
   ```
2. Ingresar al directorio y ejecutar el compilar el servicio con sam, más informacio [aquí](./vehicle_price_prediction/README.md)
   ```bash 
   $ cd VehiclePricePrediction/vehicle_price_prediction
   $ sam init
   ```
3. Luego se requiere levantar el servicio ECR para ello es necesario saber cuál es nuestro **accountID** (`$ aws configure list`) y la **region** que se emplea habitualmente para la cuenta antes encontrada (`$ aws sts get-caller-identity --query Account --output text`)
    ```bash
    $ aws --region <region> ecr get-login-password | docker login \
        --username AWS \
        --password-stdin <accountID>.dkr.ecr.<region>.amazonaws.com
    ```
4. Para el respositorio a crea se le da el nombre de `vehicle-price-prediction`
    ```bash
    $ aws ecr create-repository \
      --repository-name "vehicle-price-prediction" \
      --image-tag-mutability MUTABLE \
      --image-scanning-configuration scanOnPush=true
    ```

se obtiene el "repositoryUri"
<region>.dkr.ecr.us-east-1.amazonaws.com/vehicle-price-prediction

```bash
aws ecr delete-repository --registry-id <account-id> --repository-name vehicle-price-prediction --force
```

## Consumiendo API

Para obtener la prediccion del precio de un vehículo a partir del modelo previamente industrializado se tienen las siguientes opciones

1. En una terminal con alguna distribución Linux, Unix (macOS) o PowerShell de Windows (También puede emularse un [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) en Windows)

```bash
curl -G \
  -d 'Year=2014' \
  -d 'Mileage=31909' \
  -d 'State=MD' \
  -d 'Make=Nissan' \
  -d 'Model=MuranoAWD' \
  "https://56wgw6okv8.execute-api.us-east-1.amazonaws.com/Prod/inference"
```
2. En la barra del navegador de tu preferencia

```bash

```
