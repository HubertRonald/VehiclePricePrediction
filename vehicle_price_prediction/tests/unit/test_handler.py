import json
import pytest
from model_inference import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": {
            "data": {
                    "Year": 2014,
                    "Mileage": 31909,
                    "State": " MD",
                    "Make": "Nissan",
                    "Model": "MuranoAWD"
                }
            }
    }


def test_lambda_handler(apigw_event):

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret['body'])

    assert ret["statusCode"] == 200
    assert data["body"]["prediction"] == 20876.814453
