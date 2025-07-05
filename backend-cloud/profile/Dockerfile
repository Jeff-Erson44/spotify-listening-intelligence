FROM public.ecr.aws/lambda/python:3.10

COPY app.py ./
COPY emotion_mapper.py ./
COPY requirements.txt ./
COPY utils/ ./utils/

RUN pip3 install -r requirements.txt -t .

CMD ["app.lambda_handler"]