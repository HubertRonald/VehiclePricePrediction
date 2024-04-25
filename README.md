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