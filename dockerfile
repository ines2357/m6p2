# Autores: 
#   - Inês Mendes
#   - Margarida Tavares
#   - Tomás Franco
# Data: abril 2025
# Objetivo: 

FROM ubuntu:latest

# Instalar dependências
RUN apt-get update && apt-get install -y apt-utils python3 python3-pip python3-venv

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Criar o ambiente virtual
RUN python3 -m venv .venv

# Instalar dependências dentro do ambiente virtual
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

# Expor a porta que o aplicativo irá rodar
EXPOSE 5000

# Definir o comando para rodar o aplicativo usando o Python do ambiente virtual
CMD [".venv/bin/python3", "app.py"]

