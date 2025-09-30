
import pickle
try:
    import redis
    r=redis.Redis(
        host='localhost',
        port=6379,
        password=None,
        decode_responses=False
    )
    use_redis=True
except:
    use_redis=False
    memory_cache={}

def cache_set(key,obj,ttl=3600): #default 1hr
    if use_redis:
        r.set(key,pickle.dumps(obj),ex=ttl)  #to make the value independent of obj structure and data type, pickle is used to convert it into bytestream
    else:
        memory_cache[key]=obj
    

def cache_get(key):
    if use_redis:
        data=r.get(key)
        if data:
            return pickle.loads(data)
        return None
    else:
        return memory_cache.get(key)