import json
import boto3
import joblib
from io import BytesIO 
import pandas as pd
from inspect import cleandoc

s3_client = boto3.client('s3')


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
    model = load_model(
        s3_bucket='hr-s3-itec', 
        key='price_xgboost3477.pkl'
    )

    # read data
    if 'body' in event.keys():
        data = json.loads(event['body'])['data']
    else:
        data = event['data']

    # predict
    data['State'] = f" {data.get('State').strip()}"
    X_request = pd.DataFrame({col:{'0':val} for col, val in data.items()})
    enc_pred = model.predict(X_request)[0]
    
    # show predict
    return {
        "statusCode": 200,
        "body": json.dumps({
            "prediction": enc_pred
        }),
    }


def load_model(s3_bucket, key):
    try:
        with BytesIO() as file_pkl:
            s3_client.download_fileobj(s3_bucket, key, file_pkl)
            file_pkl.seek(0)
            model = joblib.load(file_pkl)

    except Exception as error:
        print(error)
        print(
            cleandoc(f'''
                Error getting object {key} from bucket {s3_bucket}. 
                Make sure they exist and your bucket 
                is in the same region as this function.
            ''')
        )
        raise error
    
    return model
