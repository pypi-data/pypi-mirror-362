"""
Redis Wrapper from viso.ai
"""
import json
import threading
from typing import Any, Optional, Union
import cv2  # type: ignore
import redis


from viso_sdk.logging.logger import get_logger


logger = get_logger("REDIS")


class RedisWrapper:
    """Represents a redis client specified for the containers.

    Args:
        thread(bool): Use threading or not
        host(str): Redis server host
        port(int): Redis server port
    """

    def __init__(
            self,
            thread: bool = True,
            host: str = "localhost",
            port: int = 6379,
    ):
        self._use_thread = thread
        self._redis_client = redis.StrictRedis(host, port)

        _img_arr = None

    def _write_(
            self,
            data: dict,
            redis_key: str
    ) -> bool:
        """
        Internal function that is executed in background thread
        Args:
            data,
            redis_key:
        Returns:

        """
        if isinstance(data, dict):
            str_as_data = json.dumps(data)
        elif data is None:
            return bool(self._redis_client.delete(redis_key))
        else:
            str_as_data = data

        try:
            return bool(self._redis_client.set(redis_key, str_as_data))
        except Exception as err:
            logger.error(f"Failed to write data to redis`{redis_key}` - {err}")
        return False

    def write_viso_data(
            self,
            data: dict,
            redis_key: str,
    ) -> bool:
        """
        Write video frame to the target redis key
        Args:
                data:
                redis_key(str): Target redis key.
        """
        if self._use_thread:
            threading.Thread(
                target=self._write_, args=(data, redis_key)
            ).start()
            return True
        return self._write_(data, redis_key)

    def delete_data(self, redis_key: str) -> bool:
        """Delete data from the target redis location

        Args:
            redis_key(str): Target redis key.
        """
        return bool(self._redis_client.delete(redis_key))

    def write_data(self, redis_key: str, data: Union[str, dict]) -> bool:
        """Write data to the target redis location

        Args:
            redis_key(str): Target redis key.
            data(str): Data to be written.
        """
        if isinstance(data, dict):
            return bool(self._redis_client.set(redis_key, json.dumps(data)))
        else:
            return bool(self._redis_client.set(redis_key, data))

    def read_data(self, redis_key: str) -> Any:
        """Read data from the target redis location

        Args:
            redis_key(str): Target redis key.
        """
        return self._redis_client.getdel(redis_key)

    def read_viso_data(
            self,
            redis_key: str,
    ):
        """Read video frame from a given redis key

        Args:
            redis_key(str): Target redis key.
        """
        try:
            data = self.read_data(redis_key=redis_key)
            if isinstance(data, bytes):
                return json.loads(data.decode())
            return data
        except Exception as err:
            logger.warning(f"Failed to get redis frame from {redis_key} - {err}")
        return None
