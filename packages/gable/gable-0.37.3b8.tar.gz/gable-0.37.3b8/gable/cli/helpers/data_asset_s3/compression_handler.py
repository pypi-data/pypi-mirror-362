"""
compression_handler.py
———————————————
Detect wrapper compression, infer true format, and decompress in memory.
"""

from __future__ import annotations

import gzip
import io
import os
import tempfile
import zipfile
from enum import Enum
from typing import Tuple, Optional
import pyarrow.orc as paorc
import boto3
from mypy_boto3_s3 import S3Client
import snappy
from gable.cli.helpers.data_asset_s3.logger import log_debug



class InternalCompression(Enum):
    NONE = "none"
    SNAPPY = "snappy"
    ZLIB = "zlib"
    ZSTD = "zstd"
    UNKNOWN = "unknown"

class FileFormat(Enum):
    """Supported file formats for data processing."""
    JSON = "json"
    CSV = "csv"
    TSV = "tsv"
    PARQUET = "parquet"
    ORC = "orc"
    AVRO = "avro"
    UNKNOWN = "unknown"

    @classmethod
    def from_extension(cls, ext: str) -> FileFormat:
        """Convert file extension to FileFormat enum."""
        if not ext:
            return cls.UNKNOWN
        # Remove leading dot if present
        clean_ext = ext.lstrip(".")
        try:
            return cls(clean_ext)
        except ValueError:
            return cls.UNKNOWN

    @property
    def extension(self) -> str:
        """Get the file extension with leading dot."""
        return f".{self.value}" if self != FileFormat.UNKNOWN else ""

    def __str__(self) -> str:
        return self.extension


class CompressionWrapper(Enum):
    """Supported compression wrapper types."""
    GZ = "gz"
    SNAPPY = "snappy"
    ZIP = "zip"
    ZST = "zst"
    NONE = "none"

    @classmethod
    def from_extension(cls, ext: str) -> CompressionWrapper:
        """Convert file extension to CompressionWrapper enum."""
        if not ext:
            return cls.NONE
        # Remove leading dot if present
        clean_ext = ext.lstrip(".")
        try:
            return cls(clean_ext)
        except ValueError:
            return cls.NONE

    @property
    def extension(self) -> str:
        """Get the compression extension with leading dot."""
        return f".{self.value}" if self != CompressionWrapper.NONE else ""

    def __str__(self) -> str:
        return self.extension


class CompressionHandler:
    SUPPORTED_FILE_TYPES = {fmt.value for fmt in FileFormat if fmt != FileFormat.UNKNOWN}
    COMPRESSION_EXTENSIONS = {comp.value for comp in CompressionWrapper if comp != CompressionWrapper.NONE}
    _ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"

    # ───────────────────────────── basic helpers ─────────────────────────────
    @staticmethod
    def detect_internal_compression(file_format: FileFormat, raw_bytes: bytes) -> InternalCompression:
        """
        Only ORC supported for now. Extract internal compression codec from file metadata.
        """
        if file_format == FileFormat.ORC:
            try:
                import io

                buf = io.BytesIO(raw_bytes)
                reader = paorc.ORCFile(buf)
                codec = reader.compression
                log_debug(f"[InternalCompression] ORC internal codec: {codec}")

                try:
                    return InternalCompression(codec.lower())
                except ValueError:
                    return InternalCompression.UNKNOWN

            except Exception as e:
                log_debug(f"[InternalCompression] Failed to detect ORC compression: {e}")

        return InternalCompression.NONE

    @staticmethod
    def is_compressed(file_key: str) -> bool:
        exts = set(file_key.lower().split("."))

        # If there is only one extension it's just a filename without a compression extension
        if len(exts) == 1:
            return False

        return any(ext in CompressionHandler.COMPRESSION_EXTENSIONS for ext in exts)

    @staticmethod
    def split_format_and_wrapper(file_key: str) -> tuple[FileFormat, CompressionWrapper]:
        """
        Split file key into format and wrapper enums.
        Returns (FileFormat, CompressionWrapper) tuple.
        """
        tokens = file_key.lower().split(".")

        fmt = next((FileFormat.from_extension(t) for t in tokens if t in CompressionHandler.SUPPORTED_FILE_TYPES), FileFormat.UNKNOWN)
        wrap = next((CompressionWrapper.from_extension(t) for t in tokens if t in CompressionHandler.COMPRESSION_EXTENSIONS), CompressionWrapper.NONE)

        # Use the new helper – drop '.snappy' if it's only an internal codec
        if CompressionHandler.is_internal_snappy(fmt, wrap):
            wrap = CompressionWrapper.NONE

        return fmt, wrap
    
    @staticmethod
    def is_internal_snappy(
        format_ext: FileFormat,
        wrapper_ext: CompressionWrapper,
    ) -> bool:
        """
        True when the *wrapper* token is '.snappy' **and** the *format* is a
        columnar file that normally stores Snappy *inside* (ORC/Parquet/Avro).
        """
        return (
            wrapper_ext == CompressionWrapper.SNAPPY
            and format_ext in {FileFormat.ORC, FileFormat.PARQUET, FileFormat.AVRO}
        )

    @staticmethod
    def detect_compression_by_magic_bytes(data: bytes) -> CompressionWrapper:
        if data.startswith(b"\x1f\x8b"):
            return CompressionWrapper.GZ
        if data.startswith(b"PK\x03\x04"):
            return CompressionWrapper.ZIP
        if data.startswith(b"\xff\x06\x00\x00sNaPpY"):
            return CompressionWrapper.SNAPPY
        if data.startswith(CompressionHandler._ZSTD_MAGIC):
            return CompressionWrapper.ZST
        try:
            snappy.decompress(data)
            return CompressionWrapper.SNAPPY
        except Exception:
            pass
        return CompressionWrapper.NONE

    # magic-byte probe (true format)
    @staticmethod
    def detect_format_by_magic_bytes(data: bytes) -> FileFormat:
        if data.startswith(b"PAR1"):
            return FileFormat.PARQUET
        if b"ORC" in data[-16:]:
            return FileFormat.ORC
        if data.startswith(b"Obj"):
            return FileFormat.AVRO
        if data.strip().startswith((b"{", b"[")):
            return FileFormat.JSON
        if b"," in data[:1024]:
            return FileFormat.CSV
        if b"\t" in data[:1024]:
            return FileFormat.TSV
        return FileFormat.UNKNOWN

    @staticmethod
    def get_original_format(file_key: str, file_content: bytes = b"") -> FileFormat:
        # try by explicit token first
        for token in file_key.lower().split("."):
            if token in CompressionHandler.SUPPORTED_FILE_TYPES:
                return FileFormat.from_extension(token)
        # else probe magic bytes
        return CompressionHandler.detect_format_by_magic_bytes(file_content)

    # ───────────────────────────── in-memory decompress ─────────────────────
    @staticmethod
    def decompress(file_key: str, raw_bytes: bytes) -> Tuple[io.BytesIO, FileFormat]:
        """Return (decompressed_bytes, original_format)"""
        ext_hint = CompressionHandler.detect_compression_by_magic_bytes(raw_bytes)
        if ext_hint == CompressionWrapper.NONE:
            for tok in file_key.lower().split("."):
                if tok in CompressionHandler.COMPRESSION_EXTENSIONS:
                    ext_hint = CompressionWrapper.from_extension(tok)
                    break
        
        if ext_hint == CompressionWrapper.GZ:
            data = gzip.decompress(raw_bytes)
        elif ext_hint == CompressionWrapper.SNAPPY:
            data = snappy.decompress(raw_bytes)
        elif ext_hint == CompressionWrapper.ZIP:
            with zipfile.ZipFile(io.BytesIO(raw_bytes)) as zf:
                name = zf.namelist()[0]
                data = zf.read(name)
                file_key = name  # more accurate for format detection
        else:
            raise ValueError(f"Unsupported compression wrapper: {file_key}")

        if not isinstance(data, bytes):
            data = data.encode("utf-8")
        return io.BytesIO(data), CompressionHandler.get_original_format(file_key, data)

    # ───────────────────────────── S3 helper used by schema_detection ───────
    def decompress_s3_file_to_local(
        self,
        bucket: str,
        key: str,
        s3_client: Optional[S3Client] = None,
        tmpdir: str | None = None,          # ← NEW OPTIONAL ARG
        compression_wrapper: Optional[CompressionWrapper] = None,          # ← NEW OPTIONAL ARG
    ) -> str:
        s3 = s3_client or boto3.client("s3")
        raw = s3.get_object(Bucket=bucket, Key=key)["Body"].read()

        if compression_wrapper == CompressionWrapper.NONE or not self.is_compressed(key):
            suffix = os.path.splitext(key)[1] or ".bin"
            tmp = tempfile.NamedTemporaryFile(
                delete=False, suffix=suffix, dir=tmpdir   # ← use tmpdir
            )
            tmp.write(raw)
            tmp.close()
            return tmp.name

        byte_io, orig_format = self.decompress(key, raw)
        suffix = orig_format.extension or ".bin"
        tmp = tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix, dir=tmpdir       # ← use tmpdir
        )
        tmp.write(byte_io.read())
        tmp.close()
        return tmp.name
