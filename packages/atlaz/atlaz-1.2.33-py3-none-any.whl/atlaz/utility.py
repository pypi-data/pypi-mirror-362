import json
import os
from pathlib import Path
import tiktoken
from typing import Optional, List, Union
from atlaz.old_overview.main_overview import gather_repository
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Union

def count_tokens(string_inp):
    encc = tiktoken.encoding_for_model('gpt-4')
    encoded_str = encc.encode(string_inp)
    return len(encoded_str)

def build_code_prompt(file_contents: list[dict]):
    output_text = '\n'
    for file in file_contents:
        output_text += f"```{file["name"]}\n{file["content"]}\n```\n\n\n"
    return output_text[:-2]

def manual_overview(
    *,
    focus_directories: Optional[List[str]] = None,
    manual_ignore_files: Optional[List[str]] = None,
    project_root: Union[str, Path, None] = None,
    use_gitignore: bool = False,
) -> str:
    project_root = Path(project_root or Path.cwd()).resolve()
    focus_directories = _compress_focus_items(focus_directories or [project_root])

    # ---- collect file contents exactly as before ---------------------------
    fake_script_path = project_root / "__atlaz_dummy__" / "__atlaz_dummy__" / "__dummy__.py"
    directory_data, _ = gather_repository(
        script_path=fake_script_path,
        focus_directories=[str(p) for p in focus_directories],
        manual_ignore_files=manual_ignore_files or [],
        use_gitignore=use_gitignore,
    )

    # ---- build ONE coherent tree ------------------------------------------
    all_paths = [Path(d["name"]).resolve() for d in directory_data]
    tree = _build_path_tree(all_paths, project_root)
    aligned_tree = "\n".join(_tree_to_ascii(tree))

    # ---- normalise names for the code-prompt ------------------------------
    for fd in directory_data:
        abs_path = Path(fd["name"]).resolve()
        try:
            fd["name"] = abs_path.relative_to(project_root).as_posix()
        except ValueError:     # shouldn’t happen, but keep it safe
            fd["name"] = abs_path.name

    prompt = aligned_tree + "\n\n" + build_code_prompt(directory_data)
    return f"```CodeOverview\n{prompt}\n```"


def get_directory_data(focus_directories: list[str], manual_ignore_files: list[str]) -> list[dict]:
    directory_data, _ = gather_repository(script_path=Path(__file__).resolve().parent, focus_directories=focus_directories, manual_ignore_files=manual_ignore_files)
    return directory_data

def analyze_long_files(directory_data: list[dict], min_lines: int=150) -> list[str]:
    long_files = []
    for file in directory_data:
        line_count = len(file["content"].splitlines())
        if line_count > min_lines:
            long_files.append(f"{file["name"]}: {line_count} lines")
    return long_files

def analyze_folders(focus_directories: list[str], ignore_set: set=None, threshold: int=6) -> list[str]:
    if ignore_set is None:
        ignore_set = {'__init__.py', "__pycache__"}
    folders_info = []
    for focus_dir in focus_directories:
        focus_path = Path(focus_dir)
        if focus_path.is_file():
            continue
        for root, dirs, files in os.walk(focus_path):
            dirs[:] = [d for d in dirs if d not in ignore_set]
            if Path(root).name in ignore_set:
                continue
            items = dirs + files
            filtered_items = [item for item in items if item not in ignore_set]
            if len(filtered_items) > threshold:
                try:
                    rel_path = Path(root).relative_to(focus_path)
                except ValueError:
                    rel_path = Path(root)
                folder_name = str(rel_path) if str(rel_path) != '.' else focus_dir
                folders_info.append(f"Folder '{folder_name}': {len(filtered_items)} items")
    return folders_info

def build_report(long_files: list[str], folders_info: list[str]) -> str:
    report_lines = []
    if long_files:
        report_lines.append('Files longer than 150 lines:')
        report_lines.extend(long_files)
    else:
        report_lines.append('No files longer than 150 lines found.')
    if folders_info:
        report_lines.append('\nFolders with more than 6 items:')
        report_lines.extend(folders_info)
    else:
        report_lines.append('\nNo folders with more than 6 items found.')
    return '\n'.join(report_lines)

def analyse_codebase(focus_directories: list[str], manual_ignore_files: list[str]) -> str:
    directory_data = get_directory_data(focus_directories, manual_ignore_files)
    long_files = analyze_long_files(directory_data, min_lines=150)
    folders_info = analyze_folders(focus_directories, ignore_set={'__init__.py', "__pycache__"}, threshold=6)
    return build_report(long_files, folders_info)

def _compress_focus_items(items: List[Union[str, Path]]) -> List[Path]:
    """Remove any path that is already covered by one of its ancestors."""
    paths = sorted({Path(p).resolve() for p in items}, key=lambda p: (len(p.parts), str(p)))
    kept: List[Path] = []
    for p in paths:
        if not any(parent in kept for parent in p.parents):
            kept.append(p)
    return kept


def _build_path_tree(paths: List[Path], root: Path) -> Dict:
    tree: Dict[str, Dict] = defaultdict(dict)
    for p in paths:
        rel = p.relative_to(root)
        node = tree
        for part in rel.parts:
            node = node.setdefault(part, {})
    return tree


def _tree_to_ascii(tree: Dict, prefix: str = "") -> List[str]:
    lines: List[str] = []
    entries = sorted(tree.items())
    for i, (name, child) in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        lines.append(f"{prefix}{connector}{name}")
        if child:  # directory
            extender = "    " if i == len(entries) - 1 else "│   "
            lines.extend(_tree_to_ascii(child, prefix + extender))
    return lines