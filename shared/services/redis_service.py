import redis

class RedisService:
    def __init__(self, host, username, password):
        self.r =    redis.Redis(
                    host=host,
                    port=13455,
                    decode_responses=True,
                    username=username,
                    password=password
                    )
        self.pubsub = self.r.pubsub()
    
    def publish_to_channel(self, channel, message):
        self.r.publish(channel, message)

    def subscribe_to_channel(self, channel):
        self.pubsub.subscribe(channel)

    def get_listener(self):
        return self.pubsub.listen()