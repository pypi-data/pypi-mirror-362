import os, redis

# 싱글톤 클라이언트 정의
REDIS_ADDR = os.getenv('REDIS_ADDR')
REDIS_PASS = os.getenv('REDIS_PASS')

client: redis.Redis = None

def get_redis_client(port: int = 6379) -> redis.Redis:
    global client
    if client is None:
        client = redis.Redis(host=REDIS_ADDR,
                             port=port,
                             password=REDIS_PASS,
                             decode_responses=True)
    return client
