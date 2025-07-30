import redis
from datetime import date, datetime
import json
from typing import Any
import re

from dgredis.conf import RedisConfig


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


class RedisClient:
    def __init__(self, cfg: RedisConfig):
        self.client = redis.StrictRedis(
            host=cfg.host,
            port=cfg.port,
            password=cfg.password,
            decode_responses=True
        )
        self.encoder = DateTimeEncoder()
        # Регулярное выражение для определения строк в формате ISO
        self.iso_date_pattern = re.compile(
            r'^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?)?$'
        )

    def _serialize(self, value: Any) -> Any:
        if isinstance(value, (dict, list, tuple, set, date, datetime)):
            return json.loads(self.encoder.encode(value))
        return value

    def _deserialize(self, data: Any) -> Any:
        if isinstance(data, str) and self.iso_date_pattern.match(data):
            try:
                if 'T' in data:
                    return datetime.fromisoformat(data.replace('Z', '+00:00'))
                return date.fromisoformat(data)
            except ValueError:
                return data
        elif isinstance(data, dict):
            return {k: self._deserialize(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._deserialize(item) for item in data]
        return data

    def get_json_key(self, key: str) -> Any:
        result = self.client.json().get(key)
        return self._deserialize(result)

    def set_json_key(self, key: str, value: Any, ttl: int = None):
        serialized_value = self._serialize(value)
        self.client.json().set(key, "$", serialized_value)
        if ttl:
            self.client.expire(key, ttl)

    def get_key(self, key: str) -> Any:
        value = self.client.get(key)
        if value is not None:
            try:
                # Пробуем десериализовать JSON строку
                json_value = json.loads(value)
                return self._deserialize(json_value)
            except json.JSONDecodeError:
                # Если это не JSON, проверяем на дату/время
                return self._deserialize(value)
        return value

    def set_key(self, key: str, value: Any, ttl: int = None):
        if isinstance(value, (dict, list, tuple, set, date, datetime)):
            value = self.encoder.encode(value)
        self.client.set(key, value, ex=ttl)

    def get_key_type(self, key: str) -> str:
        return self.client.type(key)