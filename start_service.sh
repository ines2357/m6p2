#!/bin/bash

# Exemplo de inicialização de um serviço
echo "A iniciar o serviço..."

# Navega até o diretório da aplicação
cd /home/grupo2/m6p2

# Ativa o ambiente virtual, se necessário (para aplicações Python, por exemplo)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Inicia o serviço da aplicação (por exemplo, um servidor web)
python3 app.py

# ou, se for um Docker container
# docker run -d -p 5000:5000 your_image_name

echo "Serviço iniciado com sucesso!"
