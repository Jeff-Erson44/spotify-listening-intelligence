FROM public.ecr.aws/lambda/python:3.10

COPY app.py ./
COPY requirements.txt ./
COPY utils/ ./utils/

RUN pip3 install -r requirements.txt --target .

CMD ["app.lambda_handler"]