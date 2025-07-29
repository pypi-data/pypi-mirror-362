from pathlib import Path
from fnmatch import fnmatch

def skip_depth(root_path: Path, base_path: Path, max_depth: int) -> bool:
    return len(root_path.relative_to(base_path).parts) > max_depth

def filter_dirs(root_path: Path, dirs: list, ignore_spec, manual_ignore_files: list) -> list:
    return [d for d in dirs if not is_ignored_file(root_path / d, ignore_spec, manual_ignore_files)]

def filter_files(root_path: Path, files: list, ignore_spec, manual_ignore_files: list) -> list:
    return [f for f in files if not is_ignored_file(root_path / f, ignore_spec, manual_ignore_files)]

def is_ignored_file(file_path: Path, ignore_spec, manual_ignore_files: list) -> bool:
    if ignore_spec and ignore_spec.match_file(file_path.relative_to(file_path.anchor).as_posix()):
        return True
    if manual_ignore_files:
        base_names = {Path(p).name for p in manual_ignore_files}
        name = file_path.name
        if name in base_names or file_path.as_posix() in manual_ignore_files or any((fnmatch(name, pattern) for pattern in manual_ignore_files)):
            return True
    return False