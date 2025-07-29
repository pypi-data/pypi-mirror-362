from pathlib import Path
import pathspec

def append_default_ignores(manual_ignore_files: list | None) -> list[str]:
    common_ignores = ['.git', "node_modules", "build", "dist", "__pycache__", "venv", '*.log', 'node_modules/', '*.tmp', '.env', 'dist/', 'atlaz.egg-info', "LICENSE", 'MANIFEST.in']
    manual_ignore_files = list(manual_ignore_files or [])
    for pattern in common_ignores:
        if pattern not in manual_ignore_files:
            manual_ignore_files.append(pattern)
    return manual_ignore_files

def compile_ignore_patterns(base_path: Path, manual_patterns: list | None, *, use_gitignore: bool=True):
    patterns: list[str] = []
    if use_gitignore:
        patterns.extend(load_gitignore_patterns(base_path))
    if manual_patterns:
        patterns.extend(manual_patterns)
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns) if patterns else None

def load_gitignore_patterns(base_path: Path) -> list[str]:
    gitignore_path = base_path / '.gitignore'
    if gitignore_path.exists():
        with gitignore_path.open("r", encoding='utf-8') as f:
            return f.readlines()
    return []