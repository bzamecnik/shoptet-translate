FROM python:3.4

WORKDIR /opt/s3dt-shoptet-translate
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
