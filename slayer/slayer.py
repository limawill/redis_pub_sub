import redis
import json
import os
 
# Conexão com o Redis
redis_client = redis.StrictRedis(
    host="redis",  # Nome do serviço do Redis no Docker Compose
    port=6379,
    decode_responses=True
)
 
# Função para processar a mensagem no Redis
def process_message(uuid_key):
    # Busca os dados no Redis
    data = redis_client.get(uuid_key)
    if not data:
        print(f"Nenhuma mensagem encontrada para UUID: {uuid_key}")
        return
 
    # Processa os dados
    message = json.loads(data)
    print(f"Mensagem processada: {message}")
 
    # Remove a mensagem do Redis
    redis_client.delete(uuid_key)
    print(f"Mensagem com UUID {uuid_key} removida do Redis.")
 
if __name__ == "__main__":
    slayer_name = os.getenv("SLAYER_NAME", "slayer")
    print(f"{slayer_name} aguardando UUIDs...")
 
    try:
        while True:
            # Aguarda o UUID no terminal
            uuid_key = input("Digite o UUID para processar: ").strip()
            process_message(uuid_key)
    except KeyboardInterrupt:
        print(f"\n{slayer_name} encerrado.")