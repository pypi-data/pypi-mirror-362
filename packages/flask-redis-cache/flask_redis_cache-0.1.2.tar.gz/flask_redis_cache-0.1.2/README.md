# flask-redis-cache

```
poetry add flask-redis-cache
```

## 设置项

| Variable | Default Value |
| --- | --- |
| REDIS_HOST | 127.0.0.1 |
| REDIS_PORT | 6379 |
| REDIS_DB | 1 |

## 使用


### 初始化

```python
from flask_redis_cache import FlaskRedisCache

cache = FlaskRedisCache()
```


### redis client的使用方法
```python
cache.redis.set("key", "value")
```
