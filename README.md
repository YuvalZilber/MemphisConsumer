# MemphisConsumer

## ⭐️ Why
For the job interview 

## 👉 Use-cases
- Job interview
- Data ingestion
- Cloud Messaging csv file line by line

## ✨ Features

- 🚀 Fully optimized message consumer in under 3 minutes
- 💻 Easy-to-use CLI

## Requirements
- memphis container running, cli running with
- host="localhost", username="root", connection_token="memphis"
- * sorry about that being static, forgot to add that to the program arguments 


## 🚀 Getting Started
- open terminal
- cd a designed empty directory
- run container:
```bash
git clone git@github.com:YuvalZilber/MemphisConsumer.git && cd MemphisConsumer/ && chmod u+x consume && sudo docker-compose up -d --scale consumer=3
```
of course, you can change the 3 at the end to whatever amount of containers you like

- start Consuming:
```bash
./consume file=~/output.csv
```

for more details, use
```bash
./consume help
```
it will tellyou how it works
