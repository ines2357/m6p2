# Autores: 
#   - Inês Mendes
#   - Margarida Tavares
#   - Tomás Franco
# Data: abril 2025
# Objetivo: 

FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip

COPY ./jogo /jogo

WORKDIR /jogo

EXPOSE 8000

CMD ["python3", "app.py"]
