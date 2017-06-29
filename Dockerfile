from ubuntu:16.04

COPY . /

RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip \
  sqlite
  

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

VOLUME /data

CMD ["python3", "/perform_blasts.py"] 
