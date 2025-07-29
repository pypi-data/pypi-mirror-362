import json
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import Any, Union
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def file_exists(path: Path) -> bool:
    return path.exists()

def unlink_file(path: Path) -> None:
    if path.exists():
        path.unlink()

def read_txt(path: Union[Path, str]) -> str:
    if isinstance(path, str):
        path = Path(path)
    with path.open("r", encoding='utf-8') as f:
        return f.read()

def write_txt(content: str, path: Union[Path, str]) -> None:
    if isinstance(path, str):
        path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding='utf-8') as f:
        f.write(content)

def read_json(path: Union[Path, str]) -> Any:
    if isinstance(path, str):
        path = Path(path)
    with path.open("r", encoding='utf-8') as f:
        return json.load(f)

def _pydantic_default(obj: Any) -> Any:
    if BaseModel is not None and isinstance(obj, BaseModel):
        if hasattr(obj, "model_dump"):
            return obj.model_dump(mode="json", exclude_none=True)
        return obj.dict(exclude_none=True)
    return str(obj)

def write_json(data: Any, path: Union[Path, str]) -> None:
    path = Path(path) if isinstance(path, str) else path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=_pydantic_default)

def is_binary(file_path: Path) -> bool:
    try:
        with file_path.open("rb") as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except Exception:
        return True

def is_large_or_binary(file_path: Path) -> bool:
    one_mb_in_bytes = 1024 * 1024
    if file_path.exists():
        if file_path.stat().st_size > one_mb_in_bytes:
            return True
        if is_binary(file_path):
            return True
    return False