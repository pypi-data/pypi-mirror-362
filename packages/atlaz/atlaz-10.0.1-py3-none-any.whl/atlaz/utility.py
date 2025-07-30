import json
from pathlib import Path
from typing import Any, Union
from pydantic import BaseModel

def write_txt(content: str, path: Union[Path, str]) -> None:
    if isinstance(path, str):
        path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding='utf-8') as f:
        f.write(content)

def read_txt(path: Union[Path, str]) -> str:
    if isinstance(path, str):
        path = Path(path)
    with path.open("r", encoding='utf-8') as f:
        return f.read()
    
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
