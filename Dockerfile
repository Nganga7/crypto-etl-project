FROM python:3.15.0a8-slim 

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . . 

CMD ["python","crypto_etl.py"]

