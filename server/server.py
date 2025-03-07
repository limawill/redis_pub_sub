import redis
import json
import uuid
import time
 
# Conexão com o Redis
redis_client = redis.StrictRedis(
    host="redis",  # Nome do serviço do Redis no Docker Compose
    port=6379,
    decode_responses=True
)
 
# Função para carregar os JSONs
def load_jsons():
    json_files = {
        "slayer1": "jsons/message1.json",
        "slayer2": "jsons/message2.json",
        "slayer3": "jsons/message3.json"
    }
    messages = {}
    for slayer, file_path in json_files.items():
        with open(file_path, "r") as f:
            messages[slayer] = json.load(f)
    return messages
 
# Função para gerar mensagem e salvar no Redis
def send_message_to_redis(slayer, messages):
    if slayer not in messages:
        print(f"Slayer '{slayer}' não encontrado. Tente: slayer1, slayer2 ou slayer3.")
        return
 
    # Gera UUID e salva a mensagem no Redis
    uuid_key = str(uuid.uuid4())
    redis_client.set(uuid_key, json.dumps(messages[slayer]))
    redis_client.expire(uuid_key, 3600)  # Define TTL de 1 hora
    print(f"Mensagem de {slayer} salva no Redis com UUID: {uuid_key}")
 
if __name__ == "__main__":
    print("Server online. Digite o nome do Slayer para gerar mensagens (slayer1, slayer2, slayer3).")
    print("Pressione Ctrl+C para sair.")
 
    # Carrega os JSONs
    messages = load_jsons()
 
    try:
        while True:
            # Aguarda o comando no terminal
            slayer = input("Digite o nome do Slayer (slayer1, slayer2, slayer3): ").strip()
            send_message_to_redis(slayer, messages)
    except KeyboardInterrupt:
        print("\nServer encerrado.")