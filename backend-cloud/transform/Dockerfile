FROM public.ecr.aws/lambda/python:3.10

COPY app.py ./
COPY requirements.txt ./
COPY utils/ ./utils/
COPY mock_features.py ./

RUN pip3 install -r requirements.txt -t .

CMD [ "app.lambda_handler" ]

