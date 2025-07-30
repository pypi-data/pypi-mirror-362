"""

Note: Everything inside this directory should not import from this __init__.py file
but from the actual source file. For everything outside, importing from this __init__.py is fine.
"""

from .file_indexer import make_index, sort_file_paths_with_dirs_separated, regex_glob
from .file_reader import (
    yield_chunked_bytes,
    yield_lines_from_file,
    yield_lines_from_object,
    read_bytes_from_file_or_io,
    read_text_from_file_or_io,
    open_file_or_io,
)
from .git_root_finder import find_git_root, navigate_to_git_root
from .jsonext import (
    load_json,
    loads_json,
    load_jsonl,
    loads_jsonl,
    dump_json,
    dumps_json,
    dump_jsonl,
    dumps_jsonl,
    load_json_xz,
    dump_json_xz,
)
from .misc import (
    set_working_directory,
    set_working_directory,
    get_file_size,
    get_file_size_in_mb,
    format_b_in_mb,
    format_b_in_gb,
    format_bytes_human_readable,
)
from .pathspec_matcher import (
    make_git_pathspec,
    make_regex_pathspec,
    make_pathspec,
    apply_pathspecs,
    make_and_apply_pathspecs,
    make_pathspecs,
    PathSpecWithConversion,
    PathSpecRepr,
)
from .yamlext import load_yaml, loads_yaml, dump_yaml, dumps_yaml

__all__ = [
    "set_working_directory",
    "yield_chunked_bytes",
    "yield_lines_from_file",
    "yield_lines_from_object",
    "load_json",
    "loads_json",
    "load_jsonl",
    "loads_jsonl",
    "dump_json",
    "dumps_json",
    "dump_jsonl",
    "dumps_jsonl",
    "load_json_xz",
    "dump_json_xz",
    "load_yaml",
    "loads_yaml",
    "dump_yaml",
    "dumps_yaml",
    "make_git_pathspec",
    "make_index",
    "find_git_root",
    "navigate_to_git_root",
    "open_file_or_io",
    "read_bytes_from_file_or_io",
    "read_text_from_file_or_io",
    "sort_file_paths_with_dirs_separated",
    "make_regex_pathspec",
    "make_pathspec",
    "PathSpecWithConversion",
    "regex_glob",
    "apply_pathspecs",
    "make_and_apply_pathspecs",
    "make_pathspecs",
    "set_working_directory",
    "get_file_size",
    "get_file_size_in_mb",
    "format_b_in_mb",
    "format_b_in_gb",
    "format_bytes_human_readable",
    "PathSpecRepr",
]
