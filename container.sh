#!/bin/bash

resource_group="RG-UPSKILL-SysAdmin"
acr_name="grupo2"
image_name="teste"
location="spaincentral"

# Criação da Azure Container Registry (ACR)
echo "A criar Azure Container Registry..."
az acr create --resource-group "$resource_group" --name "$acr_name" --sku Basic

# Construção da imagem Docker
echo "A construir a imagem Docker..."
az acr build --registry "$acr_name" --image "$image_name" --file ./dockerfile .

# Habilitar a conta de admin na ACR
echo "A habilitar a conta de admin na ACR..."
az acr update -n "$acr_name" --admin-enabled true

# Criar o container com a configuração fornecida
echo "A criar o container na Azure..."

username=$(az acr credential show --name grupo2 --query "username" --output tsv)
password=$(az acr credential show --name grupo2 --query "passwords[0].value" --output tsv)

az container create \
  --resource-group "$resource_group" \
  --name "$acr_name" \
  --image "$acr_name.azurecr.io/$image_name" \
  --registry-login-server "$acr_name.azurecr.io" \
  --ip-address Public \
  --location "$location" \
  --os-type Linux \
  --registry-username "$username" \
  --registry-password "$password" \
  --cpu 1 \
  --memory 1.5 \
  --ports 5000

if echo "$create_output" | grep -q '"provisioningState": "Succeeded"'; then
  container_ip=$(az container show --resource-group "$resource_group" --name "$acr_name" --query ipAddress.ip --output tsv)
  echo "$container_ip" > container_ip.txt
  echo "Container criado e a correr!"
else
  echo "Erro ao criar o container."
  echo "$create_output"
fi



