from pathlib import Path
import os
from atlaz.old_overview.file_operations import gather_directory_tree, read_file_data
from atlaz.old_overview.file_utils import filter_dirs, filter_files, skip_depth
from atlaz.old_overview.ignore_utils import append_default_ignores, compile_ignore_patterns
from atlaz.io_operations.file_mediator import is_large_or_binary

def gather_repository(*, script_path: Path, focus_directories: list[str], max_size_mb: int=5, max_lines: int=100000, max_depth: int=20, manual_ignore_patterns: list | None=None, manual_ignore_files: list | None=None, use_gitignore: bool=False) -> tuple[list[dict], str]:
    base_path = script_path.parent.parent.parent
    max_size_bytes = max_size_mb * 1024 * 1024
    ignore_spec = compile_ignore_patterns(base_path, manual_ignore_patterns, use_gitignore=use_gitignore)
    manual_ignore_files = append_default_ignores(manual_ignore_files)
    directory_structure = gather_directory_tree(focus_directories, ignore_spec, manual_ignore_files, max_depth, base_path)
    directory_data: list[dict] = []
    current_line_count = 0
    for focus_dir in focus_directories:
        focus_path = Path(focus_dir)
        if focus_path.is_file():
            if is_large_or_binary(focus_path):
                continue
            current_line_count, file_content = read_file_data(focus_path, max_size_bytes, max_lines, current_line_count)
            abs_path = focus_path.resolve()
            try:
                full_name = abs_path.relative_to(base_path).as_posix()
            except ValueError:
                full_name = abs_path.as_posix()
            directory_data.append({"name": full_name, "content": file_content})
            continue
        for root, dirs, files in os.walk(focus_path):
            root_path = Path(root)
            if skip_depth(root_path, focus_path, max_depth):
                continue
            dirs[:] = filter_dirs(root_path, dirs, ignore_spec, manual_ignore_files)
            files = filter_files(root_path, files, ignore_spec, manual_ignore_files)
            for file_name in files:
                file_path = root_path / file_name
                if is_large_or_binary(file_path):
                    continue
                new_line_count, file_content = read_file_data(file_path, max_size_bytes, max_lines, current_line_count)
                current_line_count = new_line_count
                relative_to_focus = file_path.relative_to(focus_path).as_posix()
                full_name = f'{focus_dir}/{relative_to_focus}'
                directory_data.append({"name": full_name, "content": file_content})
                if current_line_count >= max_lines:
                    break
            if current_line_count >= max_lines:
                break
    return (directory_data, directory_structure)