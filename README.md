# Módulo 6 - Projeto 2
## Introdução
 
O projeto teve como objetivo a elaboração de um ficheiro de especificação OpenAPI para a REST API da aplicação app.py, cuja finalidade era a gestão de encomendas para fornecer o Continente do Centro Comercial Colombo, tendo em conta o impacto ambiental que a produção e transporte dos seus produtos provocam. Para além disso, fez-se o deploy da aplicação para um Container Instance da Azure. Por último, efetuou-se uma pipeline CI/CD, que tem por objetivo cobrir várias etapas do DevOps, tendo sido a aplicação deployed numa máquina virtual.

## Pipeline CI/CD

A pipeline CI/CD foi desenvolvida para ser executada num agent pool self-hosted, com um deploy final para uma VM. 

### Criar o agent pool

Para criar uma pool, ir ao portal do Azure DevOps:
> Definições de projeto > Pipelines > Agent pool > Adicionar pool > Self-hosted

Criar novo agente na pool:
> Definições de projeto > Pipelines > Agent pool > Selecionar pool criada > Adicionar agente

Adicionar o agente na máquina local: 

- Download do agente
```
~/$ mkdir myagent && cd myagent
~/myagent$ tar zxvf ~/Downloads/ficheiro-de-download.tar.gz
```

- Configurar agente
```
 ~/myagent$ ./config.sh
```

 - Correr o agente na máquina local:
```
 cd myagent > ./run.sh
```

### Criar VM

 #### Criar a VNet
 1. Criar a VNet

```
az network vnet create \
    --resource-group Grupo-Recursos \
    --name VNet \
    --subnet-name Subnet \
    --address-prefix "10.0.0.0/16" \
    --subnet-prefix "10.0.0.0/24" \
    --location spaincentral
```

 2. Criar o Grupo de Segurança
```
az network nsg create \
  --resource-group Grupo-Recursos \
  --name NSG \
  --location spaincentral
```
 3. Abrir o porto 22 para ligações SSH
```
az network nsg rule create \
  --resource-group Grupo-Recursos \
  --nsg-name NSG \
  --name AllowSSH \
  --priority 1000 \
  --destination-port-ranges 22 \
  --protocol Tcp \
  --access Allow \
  --direction Inbound
```
4. Criar um IP Público
```
az network public-ip create \
  --resource-group Grupo-Recursos \
  --name PublicIP \
  --sku Standard \
  --location spaincentral
```
5. Criar a interface de rede (NIC)
```
az network nic create \
  --resource-group Grupo-Recursos \
  --name NIC \
  --vnet-name VNet \
  --subnet Subnet \
  --network-security-group NSG \
  --public-ip-address PublicIP \
  --location spaincentral
```
#### Criação da VM
1. Criar da VM
```
az vm create \
--resource-group Grupo-Recursos \
--name nomeVM \
--image Ubuntu2404 \
--size Standard_B1s \
--admin-username admin \
--nics NIC \
--generate-ssh-keys \
--location spaincentral
```
2. Ver o endereço de IP público para aceder à VM

`az vm show -d -g Grupo-Recursos -n pipeline --query publicIps -o tsv`

3. Entrar na VM

`ssh [admin@IPPublico]`


### 3.3. Criar e correr pipeline

A pipeline tem por objetivo correr testes nos ficheiros de python do repositório do projeto, fazer build do projeto, e fazer deploy da app.py numa VM. A pipeline tem as seguintes etapas: 
 - CI e build:
		 - Teste linter;
		 - Testes unitário;
		 - Testes de aceitação;
		 - Build do artefacto do projeto.
 - CD:
		 - Clonagem do código e execução da app.py na VM.


#### 3.3.1. Criar pipeline

> Ir ao portal Azure DevOps > Criar nova organização > Novo projeto > Pipelines > Nova pipeline > Selecionar repositório Git > Selecionar ficheiro YAML da pipeline desejada:
> - CI-Build-pipelines.yml
> - CD-pipelines.yml

Nota: se o repositório for do GitHub, é necessário fazer uma ligação entre o Azure DevOps e a conta Github:
>  Project settings > Service connections > New service connection > GitHub

- Ativar a ligação SSH no Azure DevOps:
> Project settings > Service connections > New service connection > SSH

#### 3.3.2. Preparação da VM para deploy

- Entrar na VM
`ssh admin@IPPublico`

- Adicionar as chaves SSH públicas dos agentes:

	- Copiar as chaves para o ficheiro 'authorized_keys' (VM):
	`sudo nano ~/.ssh/authorized_keys`
	
	-  Configurar o servidor ssh (VM) no ficheiro 'sshd_config':
`sudo nano /etc/ssh/sshd_config`
	- Descomentar as seguintes linhas:
	>PubkeyAuthentication yes
    >AuthorizedKeysFile .ssh/authorized_keys 
    
- Abrir os portos de entrada e saída 5000 no NSG da VM:
	>Entrar na VM 'pipeline' > Definições de rede > Regras > Criar regras de porta

- Instalar os seguintes pacotes:
```
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3.12-venv
```
- Clonar o repositório 
`git clone https://github.com/ines2357/m6p2`

#### Correr pipeline
- CI/Build: Com um commit e push para o branch 'develop'.
- CD: Com um Pull Request do branch 'develop' para o branch 'main'.
