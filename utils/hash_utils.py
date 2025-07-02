"""Simple hashing helpers using common algorithms."""

from __future__ import annotations

import hashlib
from typing import Generator


_CHUNK_SIZE = 8192


def _hash_data(data: bytes, algo: str) -> str:
    print(f"[hash_utils] Hashing data using {algo}")
    hasher = hashlib.new(algo)
    hasher.update(data)
    digest = hasher.hexdigest()
    print(f"[hash_utils] Digest: {digest}")
    return digest


def sha256_digest(data: bytes) -> str:
    """Return the SHA-256 hex digest for *data*."""
    print("[hash_utils] sha256_digest")
    return _hash_data(data, "sha256")


def sha1_digest(data: bytes) -> str:
    """Return the SHA-1 hex digest for *data*."""
    print("[hash_utils] sha1_digest")
    return _hash_data(data, "sha1")


def md5_digest(data: bytes) -> str:
    """Return the MD5 hex digest for *data*."""
    print("[hash_utils] md5_digest")
    return _hash_data(data, "md5")


def _file_chunks(path: str, chunk_size: int = _CHUNK_SIZE) -> Generator[bytes, None, None]:
    print(f"[hash_utils] Reading file in chunks: {path}")
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def sha256_of_file(path: str) -> str:
    """Return the SHA-256 hex digest for the contents of *path*."""
    print(f"[hash_utils] sha256_of_file: {path}")
    hasher = hashlib.sha256()
    for chunk in _file_chunks(path):
        hasher.update(chunk)
    digest = hasher.hexdigest()
    print(f"[hash_utils] SHA-256: {digest}")
    return digest


def sha1_of_file(path: str) -> str:
    """Return the SHA-1 hex digest for the contents of *path*."""
    print(f"[hash_utils] sha1_of_file: {path}")
    hasher = hashlib.sha1()
    for chunk in _file_chunks(path):
        hasher.update(chunk)
    digest = hasher.hexdigest()
    print(f"[hash_utils] SHA-1: {digest}")
    return digest


def md5_of_file(path: str) -> str:
    """Return the MD5 hex digest for the contents of *path*."""
    print(f"[hash_utils] md5_of_file: {path}")
    hasher = hashlib.md5()
    for chunk in _file_chunks(path):
        hasher.update(chunk)
    digest = hasher.hexdigest()
    print(f"[hash_utils] MD5: {digest}")
    return digest
