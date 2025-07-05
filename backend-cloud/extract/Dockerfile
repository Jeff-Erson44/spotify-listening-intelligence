FROM public.ecr.aws/lambda/python:3.10

COPY app.py ./
COPY requirements.txt ./
COPY utils/ ./utils/

# Installation des dépendances
RUN pip3 install -r requirements.txt --target .

# Handler
CMD ["app.lambda_handler"]