FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ./
COPY ./model/price_xgboost3477.pkl /opt/ml/model/

RUN pip install --upgrade pip
RUN python3.9 -m pip install -r requirements.txt -t .

COPY app.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]