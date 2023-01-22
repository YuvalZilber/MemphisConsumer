FROM python:3.8

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY consumer.py consumer.py
COPY out out
# ENTRYPOINT ["java", "Main"]
ENTRYPOINT ["bash"]