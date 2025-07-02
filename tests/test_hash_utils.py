import hashlib
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils import hash_utils


def test_hash_digests():
    data = b"hello world"
    assert hash_utils.sha256_digest(data) == hashlib.sha256(data).hexdigest()
    assert hash_utils.sha1_digest(data) == hashlib.sha1(data).hexdigest()
    assert hash_utils.md5_digest(data) == hashlib.md5(data).hexdigest()


def test_file_hashes(tmp_path):
    path = tmp_path / "sample.txt"
    content = b"sample content"
    path.write_bytes(content)

    assert hash_utils.sha256_of_file(str(path)) == hashlib.sha256(content).hexdigest()
    assert hash_utils.sha1_of_file(str(path)) == hashlib.sha1(content).hexdigest()
    assert hash_utils.md5_of_file(str(path)) == hashlib.md5(content).hexdigest()


def test_chunked_file_hash(tmp_path):
    """Files larger than the default chunk size should still hash correctly."""
    path = tmp_path / "big.bin"
    data = b"a" * 10000  # larger than 8k default chunk
    path.write_bytes(data)

    assert hash_utils.sha256_of_file(str(path)) == hashlib.sha256(data).hexdigest()

