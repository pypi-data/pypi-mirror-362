from redis import Redis as Redis


def check_if_keys_exist(client: Redis, keys: str | list[str]) -> None: ...
