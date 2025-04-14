#!/bin/bash

resource_group="RG-UPSKILL-SysAdmin"
acr_name="grupo2"
image_name="teste"
registry_username="grupo2"
registry_password="fLt0izPmW7VVsx8JrLG87SWlNx3L1ZXsefKKe98JLN+ACRDAMDNS"
location="spaincentral"

# Criação da Azure Container Registry (ACR)
echo "A criar Azure Container Registry..."
az acr create --resource-group "$resource_group" --name "$acr_name" --sku Basic --location "$location"

# Construção da imagem Docker
echo "A construir a imagem Docker..."
az acr build --registry "$acr_name" --image "$image_name" --file ./dockerfile .

# Habilitar a conta de admin na ACR
echo "A habilitar a conta de admin na ACR..."
az acr update -n "$acr_name" --admin-enabled true

# Criar o container com a configuração fornecida
echo "A criar o container na Azure..."

az container create \
  --resource-group "$resource_group" \
  --name "$acr_name" \
  --image "$acr_name.azurecr.io/$image_name" \
  --registry-login-server "$acr_name.azurecr.io" \
  --ip-address Public \
  --location "$location" \
  --os-type Linux \
  --registry-username "$(az acr credential show --name "$acr_name" --query 'username' -o tsv)" \
  --registry-password "$(az acr credential show --name "$acr_name" --query 'passwords[0].value' -o tsv)" \
  --cpu 1 \
  --memory 1.5 \
  --ports 5000

container_ip=$(az container show --resource-group RG-UPSKILL-SysAdmin --name grupo2 --query ipAddress.ip --output table)

echo "$container_ip" > container_ip.txt

echo "Container criado e a correr!"



