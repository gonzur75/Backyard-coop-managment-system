FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
# root
WORKDIR /app
#copiowanie

# && jeśli wykona się pierwszy to instaluj następny
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
# 1. "apka" do  2. "root"
# cztery zera wild card acceptuje dowolny server
#mapowanie
