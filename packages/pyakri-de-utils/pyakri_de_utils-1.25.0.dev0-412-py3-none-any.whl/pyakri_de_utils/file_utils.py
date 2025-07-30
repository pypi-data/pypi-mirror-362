import os
import re
from typing import Any
from typing import List
from typing import Optional
from typing import Set
import json
import os.path
import shutil
import tempfile
from pathlib import Path


def create_directory(directory: str):
    create_directories([directory])


def create_directories(directories: List[str]):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def _should_consider_file(
    file_name: str,
    extension: Optional[str] = None,
    extensions_to_not_consider: Optional[Set[str]] = None,
    pattern: Optional[re.Pattern] = None,
) -> bool:
    # If file is of type extension, return True
    if extension:
        return file_name.endswith(extension)

    # If file extension is in the blacklist, return False
    if extensions_to_not_consider:
        for ext in extensions_to_not_consider:
            if file_name.endswith(ext):
                return False

    # if file extension is in the pattern, return True
    if pattern:
        return pattern.match(file_name) is not None

    return True


def get_input_files_batch(
    directory,
    batch_size: Optional[int] = None,
    extension: Optional[str] = None,
    filter_extensions: Optional[Set[str]] = None,
    glob_pattern: Optional[str] = None,
):
    pattern: re.Pattern = re.compile(glob_pattern) if glob_pattern else None
    file_list = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if not _should_consider_file(
                file_name=filename,
                extension=extension,
                extensions_to_not_consider=filter_extensions,
                pattern=pattern,
            ):
                continue

            file_path = Path(root).joinpath(filename)
            file_list.append(file_path)

    file_list.sort(key=lambda k: str(k))

    if batch_size:
        yield from get_files_in_batches(file_list=file_list, batch_size=batch_size)
    else:
        yield file_list


def get_files_in_batches(file_list: List[Any], batch_size: int):
    for i in range(0, len(file_list), batch_size):
        yield file_list[i : i + batch_size]


def get_input_files_dir(
    directory,
    extension: Optional[str] = None,
    filter_extensions: Optional[Set[str]] = None,
) -> List[Path]:
    try:
        return next(
            get_input_files_batch(
                directory=directory,
                extension=extension,
                filter_extensions=filter_extensions,
            )
        )
    except StopIteration:
        return []


def get_dest_file_path(
    file_path: Path, src_dir, dst_dir, extn: Optional[str] = None
) -> Path:
    src_dir = src_dir.rstrip("/")
    rel_file_path = Path(str(file_path)[len(src_dir) + 1 :])
    if extn:
        rel_file_path = f"{rel_file_path}{extn}"

    return Path(dst_dir).joinpath(rel_file_path)


def create_parent_directory(path: Path):
    create_directory(str(path.parent))


def copy_file(src_path, dst_path: Path):
    create_parent_directory(dst_path)

    shutil.copyfile(src_path, dst_path)


def copy_files_to_dir(files: List[str], dst_dir: str):
    for file in files:
        # file[1:] -> to get the file path without "/"
        dest_file_path = Path(dst_dir, *Path(file).parts[1:])

        create_directory(str(dest_file_path.parent))
        shutil.copy(file, dest_file_path)


def get_file_name_from_path(filepath: str) -> str:
    return Path(filepath).name


def create_temp_directory(dir_path: str):
    return tempfile.TemporaryDirectory(dir=dir_path)


def remove_directory(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def concat_file_paths(*file_path_list) -> str:
    return str(Path(*file_path_list))


def get_filter_output_dir(
    par_dir: str,
    filter_type: str,
    token_number: Optional[int] = None,
) -> str:
    output_dir = concat_file_paths(par_dir, filter_type, "outputs")
    if token_number is not None:
        output_dir = concat_file_paths(output_dir, str(token_number), "o1")
    return output_dir


def get_sorted_dirs_from_path(path: str):
    def get_creation_time(item):
        item_path = concat_file_paths(path, item)
        return os.path.getctime(item_path)

    items = os.listdir(path)
    sorted_items = sorted(items, key=get_creation_time)
    return sorted_items


def get_json_from_file(file: str, obj_hook: Optional[Any] = None) -> Any:
    with open(file, "rb") as f:
        return json.load(f, object_hook=obj_hook)
