from agora_config import config
from agora_logging import logger
import redis as REDIS
import fakeredis

class RedisClientSingleton(): 
    '''
    Basic wrapper to unify how the connection to Redis is declared/configured.
    '''
    _instance: object
    _mock = False
    """
    Connects to the Redis Server from Agora Core    
    """
    def __new__(cls, *args, **kwargs):
        cls.connect()
        return cls._instance

    def __init__(self):        
        self.connect_attempted = False
        pass   
      
    @staticmethod
    def connect():
        '''
        Connects to Redis
        
        Use 'AEA2:RedisClient:Server' to set the server address (default = 'redis').
        Use 'AEA2:RedisClient:Port' to set the port (default = 6379).
        
        When running on gateway, the default values are appropriate.
        '''
        RedisClientSingleton._mock = False
        server = config["AEA2:RedisClient:Server"]
        if server == "":
            logger.info(f"AEA2:RedisClient:Server not set - mocking redis client")
            RedisClientSingleton._mock = True
            #server = "alpine-redis"

        port = config["AEA2:RedisClient:Port"]
        if port == "":
            logger.info(f"AEA2:RedisClient:Port not set - mocking redis client")
            RedisClientSingleton._mock = True
            #port = "6379"  

        if not RedisClientSingleton._mock:
            logger.info(f"redis_client connecting to '{server}:{port}'")
            RedisClientSingleton._instance = REDIS.Redis(host=server, port=port, decode_responses=True, socket_keepalive=True)
            RedisClientSingleton._instance.config_set('notify-keyspace-events', 'KEA')
        else:
            logger.info(f"faking Redis")
            RedisClientSingleton._instance = fakeredis.FakeRedis()
        
        if RedisClientSingleton.is_connected():
            logger.info("redis_client connected")
      
    @staticmethod
    def is_connected():
        '''Returns 'True' if connected to Redis.'''
        try:             
            if RedisClientSingleton._mock:
                return True
            if RedisClientSingleton._instance.ping():
                return True
        except Exception as e:
            logger.error("Failed to ping redis.")
        return False

_redis_client = RedisClientSingleton()

redis = RedisClientSingleton._instance
