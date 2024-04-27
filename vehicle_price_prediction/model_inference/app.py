import json
import joblib
import pandas as pd
from inspect import cleandoc


# import requests
def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format
        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """


    # read model (pipeline)
    path = '/opt/ml/model/'
    model = joblib.load(path+'price_xgboost3477.pkl')

    # read data
    try:
        # Obtener los datos del cuerpo de la solicitud
        if event['httpMethod'] == 'GET':
            # Obtener los parámetros de la cadena de consulta de la URL
            parameters = event['queryStringParameters']
            # Resto del código para procesar los parámetros
            data = {
                'Year': int(parameters.get('Year', 0)),
                'Mileage': int(parameters.get('Mileage', 0)),
                'State': f" {parameters.get('State', '').strip()}",
                'Make': parameters.get('Make', ''),
                'Model': parameters.get('Model', '')
            }
            
        else:
            # Obtener los datos del cuerpo de la solicitud
            if 'body' in event:
                data = json.loads(event['body'])
            else:
                data = event

    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

    # predict
    X_request = pd.DataFrame({col:{'0':val} for col, val in data.items()})
    enc_pred = model.predict(X_request)[0]
    
    # show predict
    return {
        "statusCode": 200,
        "body": json.dumps({
            "prediction": float(enc_pred)
        }),
    }
