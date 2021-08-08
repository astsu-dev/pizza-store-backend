import hashlib
from pathlib import Path

import aiofiles
from fastapi import UploadFile


async def get_binary_file_hash(file: UploadFile, read_buffer: int) -> str:
    """Read file and compute hash.

    NOTE: use only with files opened in binary mode.

    Args:
        file (UploadFile)
        read_buffer (int): max bytes for read

    Returns:
        str: computed hash
    """

    file_hash = hashlib.sha256()
    data = await file.read(read_buffer)
    while data:
        file_hash.update(data)
        data = await file.read(read_buffer)

    return file_hash.hexdigest()


async def write_binary_file(path: Path, file: UploadFile, read_buffer: int) -> None:
    """Writes file to disk.

    NOTE: write in binary mode.

    Args:
        path (Path): future file path
        file (UploadFile)
    """

    async with aiofiles.open(path, "wb") as dst_file:
        data = await file.read(read_buffer)
        while data:
            await dst_file.write(data)
            data = await file.read(read_buffer)
