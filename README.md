# Projeto Redis-Based Messaging System

Este projeto demonstra um sistema de **comunicação baseada no Redis**, onde um **Server** gera mensagens com UUIDs únicos e as salva no Redis, e **Slayers** (consumidores) processam essas mensagens em containers separados. O objetivo é simular a comunicação entre máquinas diferentes utilizando o Redis como intermediário.

---

## **Estrutura do Projeto**

A estrutura do projeto é organizada da seguinte forma:

```
project/
├── docker-compose.yml                              # Orquestração dos containers
├── server/                                         # Código do server principal
│ ├── Dockerfile                                    # Dockerfile do server
│ ├── server.py                                     # Script principal do server
│ ├── jsons/                                        # Diretório com os arquivos JSON
│ │ ├── message1.json                               # Mensagem 1
│ │ ├── message2.json                               # Mensagem 2
│ │ ├── message3.json                               # Mensagem 3
├── slayer/                                         # Código dos consumidores (slayers)
│ ├── Dockerfile                                    # Dockerfile para os slayers
│ ├── slayer.py                                     # Script principal dos slayers
```

---

## **Fluxo do Sistema**

1. **Server:**

   - O Server fica rodando e aguarda comandos no terminal.
   - Quando um Slayer é especificado (`slayer1`, `slayer2`, ou `slayer3`), ele:
     - Gera um **UUID único**.
     - Salva a mensagem correspondente no Redis.
     - Retorna o UUID gerado no terminal.

2. **Redis:**

   - Atua como o ponto central de comunicação.
   - Armazena as mensagens temporariamente associadas aos UUIDs.

3. **Slayers:**
   - Cada Slayer roda em um container separado e aguarda um **UUID** ser fornecido no terminal.
   - Quando o UUID é informado:
     - O Slayer busca a mensagem no Redis.
     - Processa e imprime o conteúdo no terminal.
     - Remove a mensagem do Redis.

---

## **Como Configurar e Rodar**

### **1. Pré-requisitos**

- **WSL2**, **Docker** e **Docker Compose** instalados no ambiente.

---

### **2. Configuração**

1. Clone o repositório ou copie os arquivos para o seu ambiente local:
   ```bash
   git clone git@github.com:limawill/redis_pub_sub.git
   cd redis_pub_sub/
   ```

# Iniciando do docker

```
docker-compose up --build
```

Isso irá:

- Criar e rodar os containers:
  - redis (servidor Redis).
  - server (server principal).
  - slayer1, slayer2, slayer3 (consumidores).

# Acessar o server

```
docker exec -it server bash
python server.py
```

# Acessar os slayers

```
docker exec -it slayer1 bash
python slayer.py
```

```
docker exec -it slayer2 bash
python slayer.py
```

```
docker exec -it slayer3 bash
python slayer.py
```

## Validar o Redis

Você pode acessar o Redis diretamente para validar as mensagens armazenadas:

Entre no container do Redis:

```
docker exec -it redis redis-cli
```

Liste todas as chaves armazenadas:

```
keys *
```

Verifique o conteúdo de uma mensagem (exemplo, com o UUID 6a8c0b68-8c56-4c34-a0c7-23d21c8461a3):

```
get 6a8c0b68-8c56-4c34-a0c7-23d21c8461a3
```

## Comportamento Esperado

1. O Server gera mensagens com UUIDs e as salva no Redis.
2. Os Slayers aguardam UUIDs no terminal.
3. Quando um UUID é fornecido:
   - O Slayer busca a mensagem correspondente no Redis.
   - Processa e imprime o conteúdo no terminal.
   - Remove a mensagem do Redis.

# Testar o Fluxo

## No terminal do Server, digite o nome de um Slayer (ex.: slayer1):

```
Digite o nome do Slayer (slayer1, slayer2, slayer3): slayer1
Mensagem de slayer1 salva no Redis com UUID: 6a8c0b68-8c56-4c34-a0c7-23d21c8461a3
```

## No terminal do Slayer correspondente (ex.: Slayer 1), digite o UUID gerado:

```
Digite o UUID para processar: 6a8c0b68-8c56-4c34-a0c7-23d21c8461a3
Mensagem processada: {"key1": "value1", "key2": "value2"}
Mensagem com UUID 6a8c0b68-8c56-4c34-a0c7-23d21c8461a3 removida do Redis.
```

## Personalizações

**Adicionar Mais Mensagens:**

- Adicione novos arquivos JSON no diretório server/jsons/.

**Ajustar o Tempo de Expiração no Redis:**

- O TTL das mensagens é configurado como 3600 segundos (1 hora). Para alterar, edite o valor em server.py:

```
redis_client.expire(uuid_key, 3600)
```

## Comandos Úteis

Parar os containers:

```
docker-compose down
```

Recriar os containers:

```
docker-compose up --build
```

Limpar todos os containers e redes:

```
docker system prune -a
```
