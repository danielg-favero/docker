# Docker

Repositório de estudos do Docker, Docker Compose, Docker Swarm e Kubernetes (k8s)

## O que é Docker?

É um software que facilita o setup de aplicações, onde cada `container` possui configurações específicas de cada aplicação, independente de Sistema Operacional ou outro ambiente. Além disso, as tecnologias que utilizamos no Docker não precisam ser instaladas localmente no computador.

### Matrix from Hell

Imagine um cenário de 6 projetos em uma empresa, cada projeto com suas dependências e ambientes para execução. Como no exemplo abaixo.

![Matrix From Hell](./assets/matrix-from-hell.png)

Sem o Docker, é preciso configurar cada depenência separadamente para cada ambiente, uma tarefa que consome muito tempo para garantir que todas elas estejam rodando com as mesmas configurações. Além disso, é preciso ter muita resiliência para dar manutenção em todos os ambientes.

## Containers

É um pacote de código que pode executar uma ação, Ex: projeto Node, projeto PHP, projeto Python. Os containers utilizam imagens para serem executados.

Diferente de uma VM (Virtual Machine), um container possui apenas um fim, não tendo um sistema operacional dedicado todo para ele, o que acaba tornando ele leve, geralmente com alguns MBs, enquanto VMs possuem GBs.

### Executar um container

1. Dar `pull` no container

```bash
docker pull <imagem>
```

2. Executar o container

```bash
docker run <imagem>
```

3. Verificar se container está executando

```bash
docker ps
```

ou

```bash
docker container ls
```

> Para verificar todos os containers que já foram executados

```bash
docker ps -a
```

### Executar um container em modo iterativo

É quando o container fica executando em um terminal, permitindo executar comandos específicos dentro do container.

```bash
docker run -it <imagem>
```

### Executar um container em background (`detached`)

É quando o container roda em plano de fundo, não ocupando uma aba no terminal

```bash
docker run -d <imagem>
```

### Parar a execução de um container

```bash
docker stop <nome ou id do container>
```

### Reiniciar o container

O comando `docker stop` para os containers, mas ele ainda ficam listados no comando `docker ps -a`, assim podemos executar eles novamente.

```bash
docker start <id do container>
```

> O comando `docker run` CRIA UM NOVO CONTAINER.
> O comando `docker start` roda o container novamente com as mesmas configurações de quando o `docker run` foi executado a primeira vez

Também é possível reiniciar o container em modo iterativo

```bash
docker start -it <id do container>
```

### Expor uma porta de um container

O container do docker é ISOLADO, ou seja, NÃO TEM CONEXÃO COM O MUNDO EXTERNO. Para possibiiltar isso é preciso export alguma porta do container.

Ex: usando o `nginx` como servidor web

1. Baixar imagem do `nginx`

```bash
docker pull nginx:stable-perl 
```

2. Executar o container e expor uma porta

```bash
docker run -d -p 80:80 nginx:stable-perl 
```

> O primeiro 80 é a porta que será aberta para o navegador, para que possamos acessar e o segundo 80 é a porta que a a plicação aplicação expõe. Se fizermos `3000:80` é possível acessar a o servidor `nginx` em `localhost:3000`.

3. Entrar no servidor web `locahost:80`

### Definir um nome para o container

Caso não seja informado, um nome aleatório será atribuído ao container.

```bash
docker run --name <nome> <imagem>
```

### Acessar logs do container

```bash
docker logs <id ou nome do container>
```

> Para exibir logs em tempo real é possível adicionar a flag `-f` (follow)

```bash
docker logs -f <id ou nome do container>
```

### Remover container

```bash
docker rm <id ou nome do container>
```

> Se o container estiver rodando ainda é preciso usar a flag `-f` (force)

```bash
docker rm -f <id ou nome do container>
```

É possível também remover um container automaticamente após a execução dele

```bash
docker run --rm <id ou nome da imagem>
```

### Copiar arquivos dentro de um container

É possível copiar e colar arquivos entre uma máquina local e um container

```bash
docker cp <id ou nome do container>:/<diretório dentro do container para copiar> <diretório de destino>
```

### Processamento de um container

```bash
docker top <id ou nome do container>
```

### Verificar processos que estão sendo executados em um container

```bash
docker stats <id ou nome do container>
```

### Inspecionar um container

Exibe todas as configurações do container

```bash
docker inspect <id ou nome do container>
```

## Imagens

É o projeto que será executado pelo container, todas as instruções para rodar o container são feitas dentro de de um arquivo `Dockerfile` que é a imagem. Uma imagem pode levar como base uma imagem pronta.

Imagens prontas podem ser hospedadas no [DockerHub](https://hub.docker.com/).

### Criando arquivo `Dockerfile`

Utilizando um servidor `node` com `express` como exemplo:

1. Na raiz de um projeto criar um arquivo `Dockerfile`

```Dockerfile
FROM node:latest

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]
```

2. Fazer o `build` da imagem

```bash
docker build <diretorio da imagem>
```

3. Verificar se a imagem foi criada com sucesso

```bash
docker image ls
```

ou 

```bash
docker image ls
```

3. Copiar o id da imagem e executar o container

```bash
docker run -d -p 3000:3000 <id da imagem>
```

### Atualizando uma imagem no `Dockerfile`

Sempre o `Dockerfile` é alterado, é preciso executar o `build` novamente, pois para o Docker ela será é imagem completamente nova. Após isso é preciso executar o `docker run` com o novo id da imagem.

### Cache das camadas da imagem

Cada instrução dentro do `Dockerfile` é uma camada. Quando algo é atualizado, apenas as camadas abaixo da linha atualizada são refeitas, o restante permanece em cache.

### Renomear imagens

Sempre que uma imagem é gerada um nome anônimo é criado

```bash
docker tag <id da imagem> <nome>
```

ou

```bash
docker tag <id da imagem> <nome>:<tag> 
```

> Por default `:<tag>` é `:latest`

É possível também nomear atribuir um nome a imagem ao executar o build.

```bash
docker build -t <nome>:<tag> .
```

### Remover imagens

```bash
docker rmi <id ou nome da imagem>
```

ou para remover todas as imagens

```bash
docker rmi -f $(docker images -q)
```

### Remover tudo que não está sendo utilizado

Caso nenhum recurso do docker esteja sendo utilizado, como containers e imagens, é possível rodar o seguinte comando para remover todos:

```bash
docker system prune
```

## Volumes

Uma forma prática de persistir dados (fazer backup) em aplicações para não depender de um container (Todo dado criado em um container é salvo nele, quando ele é removido, todos os dados também são).

### Tipos de volume

- Anonymous: Volumes com nomes aleatórios (Criados com a flag `-v`)

```bash
docker run -v /<diretorio do volume anonimo>
```

Ex:

```bash
docker run -d -p 80:80 --name php-messages-container -v /data php-messages 
```

- Named: Volumes com nomes definidos

```bash
docker run -v <nome do volume>:/<diretorio do volume>
```

Ex:

```bash
docker run -d -p 80:80 --name php-messages-container -v php-volume:/var/www/html/messages --rm php-messages
```

> O diretório do volume precisa ser o mesmo do `WORKDIR` do `Dockerfile`

- Bind Mounts: Forma de salvar na máquina local, sem gerenciamento do docker.

```bash
docker run <diretorio da maquina local>:/<diretorio do volume>
```

Ex:

```bash
docker run -d -p 80:80 --name php-messages-container -v /Users/danielg.favero/Documents/estudos/docker/2-volumes/messages:/var/www/html/messages --rm php-messages
```

- Apenas para leitura: Nesse tipo de volume não é possível escrever nenhum arquivo

```bash
docker run <diretorio da maquina local>:/<diretorio do volume>:ro
```

> `:ro` é abreviação para *Read Only*

### Criar volume manualmente

É possível criar volume sem precisar rodar um container

```bash
docker volume create <nome do volume>
```

Posteriormente é possível atrelar esse volume a um container.

### Listar volumes

```bash
docker volume ls
```

### Inspecionando volume

```bash
docker volume inspect <nome do volume>
```

### Removendo volumes

```bash
docker volume rm <nome do volume>
```

> Remover um volume REMOVE TODOS OS DADOS dentro dele

É possível também remover todos os volumes não utilizados

```bash
docker volume prune
```