FROM python:3.10.0-slim

WORKDIR /usr/src/app

COPY requirements.prod.txt .
RUN pip install -r requirements.prod.txt

COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]