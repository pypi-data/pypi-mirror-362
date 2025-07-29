"""BoxDrive - Generic object store with S3 compatible API."""

from . import exceptions, stores
from ._create_app import create_app
from .schemas import (
    BucketInfo,
    BucketName,
    ContentType,
    ETag,
    Key,
    ListObjectsInfo,
    ListObjectsV2Info,
    MaxKeys,
    Object,
    ObjectInfo,
)
from .store import ObjectStore
from .version import __version__

__all__ = [
    "__version__",
    "exceptions",
    "stores",
    "create_app",
    "ObjectStore",
    "ObjectInfo",
    "BucketInfo",
    "Object",
    "ListObjectsInfo",
    "ListObjectsV2Info",
    "BucketName",
    "ContentType",
    "ETag",
    "Key",
    "MaxKeys",
]
