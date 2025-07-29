import sys
import json
import uuid
import hashlib
import datetime
from enum import Enum
from pathlib import Path
from loguru import logger
from loguru._logger import Logger


def file_name(path: Path, suffix: str | None = None) -> str:
    file_name = path.name

    if suffix != None:
        file_name = file_name.rsplit(".", 1)[0] + suffix

    return file_name


def ensure_dir(path: str) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_file(path: Path | str) -> Path:
    if isinstance(path, str):
        path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def init_logger(
    level: str = "WARNING", logs_path: Path = Path("logs")
) -> logger.__class__:
    if getattr(logger, "_configured", False):
        return logger

    logger.remove()
    logger.add(
        sink=sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        level=level,
    )
    if logs_path:
        logs_path.mkdir(parents=True, exist_ok=True)
        log_path = logs_path / f"{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.log"
        logger.add(
            str(log_path),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
            level=level,
            encoding="utf-8",
        )
    logger._configured = True
    return logger


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


class NonSerializable:
    """标记字段为不可序列化：序列化时将跳过此字段"""

    def __repr__(self):
        return "<NonSerializable>"


NON_SERIALIZABLE = NonSerializable()


def serialize(obj):
    result = None
    # 基础类型或 None
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        result = obj
    # 字典
    elif isinstance(obj, dict):
        result = {k: serialize(v) for k, v in obj.items() if v is not NON_SERIALIZABLE}
    # 列表/元组/集合
    elif isinstance(obj, (list, tuple, set)):
        result = [serialize(v) for v in obj if v is not NON_SERIALIZABLE]
    # 普通对象
    elif hasattr(obj, "__dict__"):
        filtered = {
            k: v for k, v in vars(obj).items() if not isinstance(v, NonSerializable)
        }
        result = serialize(filtered)
    else:
        raise TypeError(f"Unsupported serialization type: {type(obj)}")
    return result


def write_json(data, json_path: Path, indent=2):
    with open(json_path, "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=indent, default=serialize)


def hash_string(s: str, method="md5") -> str:
    h = hashlib.new(method)
    h.update(s.encode("utf-8"))
    return h.hexdigest()


def partial_hash(file: Path, chunk_size=4 * 1024 * 1024) -> str:
    size = file.stat().st_size
    md5 = hashlib.md5()

    ranges = []
    ranges.append((0, chunk_size))  # 开头

    if size > chunk_size * 2:
        middle = max((size // 2) - (chunk_size // 2), chunk_size)
        ranges.append((middle, chunk_size))  # 中间

    if size > chunk_size:
        ranges.append((size - chunk_size, chunk_size))  # 结尾

    with file.open("rb") as f:
        for offset, length in ranges:
            f.seek(offset)
            md5.update(f.read(length))

    return md5.hexdigest()


def get_uuid():
    # 获取uuid
    random_uuid = uuid.uuid4()
    return str(random_uuid)


def get_timestamp():
    time = datetime.datetime.now()
    return time.strftime("%Y.%m.%d-%H:%M:%S.%f")
