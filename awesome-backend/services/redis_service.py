import redis

class RedisService:
    def __init__(self):
        self.r =    redis.Redis(
                    host='redis-13455.c1.us-central1-2.gce.redns.redis-cloud.com',
                    port=13455,
                    decode_responses=True,
                    username="default",
                    password="D065ssmyFdtSej2UXWp5Vdvvkc9E3Ygd",
)