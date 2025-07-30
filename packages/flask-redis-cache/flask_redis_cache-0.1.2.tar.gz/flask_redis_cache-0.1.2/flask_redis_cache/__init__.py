import redis
from flask import Flask, g


class FlaskRedisCache:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self._redis_host = app.config.get("REDIS_HOST", "127.0.0.1")
        self._redis_port = app.config.get("REDIS_PORT", 6379)
        self._redis_db = app.config.get("REDIS_DB", 1)
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        g_redis = g.pop("g_redis", None)
        if g_redis:
            g_redis.close()

    @property
    def redis(self) -> redis.Redis:
        g_redis = g.get("g_redis", None)
        if not g_redis:
            g_redis = redis.Redis(
                host=self._redis_host, port=self._redis_port, db=self._redis_db
            )
            g.g_redis = g_redis
        return g_redis
