import asyncio
import base64
import datetime
import hashlib
import itertools
import logging
from collections.abc import Callable, Iterable

import aiorwlock
import pydantic

from boxdrive import constants, exceptions
from boxdrive.schemas import (
    BaseListObjectsInfo,
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
from boxdrive.schemas.store import validate_bucket_name, validate_key
from boxdrive.store import ObjectStore

from .. import _utils
from .client import CreateFile, DeleteFile, GitlabClient, TreeParams, UpdateFile, raise_for_gitlab_response

logger = logging.getLogger(__name__)

type FilterObjects[L] = Callable[[list[ObjectInfo]], L]

MAX_PAGE = 10_000
MIN_PER_PAGE = 20
BATCH_SIZE = 20
DEFAULT_TIMEOUT = 60


def get_etag(data: bytes) -> ETag:
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()


def default_object_info(key: str) -> ObjectInfo:
    dt = datetime.datetime.min
    return ObjectInfo(
        key=key,
        etag="",
        size=0,
        last_modified=dt,
        content_type=constants.DEFAULT_CONTENT_TYPE,
    )


class GitlabStore(ObjectStore):
    """Object store implementation backed by a GitLab repository branch via the GitLab API."""

    def __init__(
        self,
        repo_id: int,
        branch: str,
        *,
        access_token: str,
        api_url: str = "https://gitlab.com/api/v4/",
        placeholder_name: Key = ".gitkeep",
        timeout: float | None = None,
    ):
        timeout = DEFAULT_TIMEOUT if timeout is None else timeout
        self.placeholder_name = validate_key(placeholder_name)
        self.branch = branch
        self.gitlab_client = GitlabClient(repo_id, access_token, api_url, timeout=timeout)
        self.lock = aiorwlock.RWLock()

    async def list_buckets(self) -> list[BucketInfo]:
        """List all buckets in the store."""
        now = datetime.datetime.now(datetime.UTC)
        async with self.lock.reader:
            tree = await self.gitlab_client.get_tree(TreeParams(ref=self.branch))
        buckets = []
        items = [item for item in tree.items if item.type == "tree"]
        for item in items:
            try:
                bucket = BucketInfo(name=item.name, creation_date=now)
            except pydantic.ValidationError:
                logger.exception("invalid bucket info")
                continue
            buckets.append(bucket)
        return buckets

    async def create_bucket(self, bucket_name: BucketName) -> None:
        """Create a new bucket in the store by adding a placeholder file to the bucket directory."""
        bucket_name = validate_bucket_name(bucket_name)
        file_path = _object_path(bucket_name, self.placeholder_name)
        body = CreateFile(
            branch=self.branch,
            commit_message=f"create bucket {bucket_name}",
        )
        async with self.lock.writer:
            resp = await self.gitlab_client.create_file(file_path, body)
        if resp.status_code == 201:
            logger.info("created bucket")
            return
        if resp.status_code == 400:
            logger.info("gitlab create_file failed (400): %s", resp.text)
            raise exceptions.BucketAlreadyExists
        raise_for_gitlab_response(resp)

    async def delete_bucket(self, bucket_name: BucketName) -> None:
        """Delete a bucket from the store."""
        per_page = constants.MAX_KEYS

        def is_enough(keys: list[Key]) -> bool:
            _ = keys
            return False

        async with self.lock.writer:
            keys = await self._fetch_object_keys(bucket_name, is_enough, per_page=per_page)
            for key in keys:
                await self._delete_object(bucket_name, key, keep_placeholder=False)

    async def list_objects(
        self,
        bucket_name: BucketName,
        *,
        prefix: Key | None = None,
        delimiter: str | None = None,
        max_keys: MaxKeys = constants.MAX_KEYS,
        marker: Key | None = None,
    ) -> ListObjectsInfo:
        """List objects in a bucket."""

        def filter_objects(objects: list[ObjectInfo]) -> ListObjectsInfo:
            objects = [obj for obj in objects if obj.key != self.placeholder_name]
            return _utils.filter_objects(
                objects,
                prefix=prefix,
                delimiter=delimiter,
                max_keys=max_keys,
                marker=marker,
            )

        async with self.lock.reader:
            per_page = max(MIN_PER_PAGE, max_keys)
            return await self._collect_objects(bucket_name, filter_objects, per_page=per_page)

    async def list_objects_v2(
        self,
        bucket_name: BucketName,
        *,
        continuation_token: Key | None = None,
        delimiter: str | None = None,
        encoding_type: str | None = None,
        max_keys: MaxKeys = constants.MAX_KEYS,
        prefix: Key | None = None,
        start_after: Key | None = None,
    ) -> ListObjectsV2Info:
        """List objects in a bucket."""

        def filter_objects(objects: list[ObjectInfo]) -> ListObjectsV2Info:
            objects = [obj for obj in objects if obj.key != self.placeholder_name]
            return _utils.filter_objects_v2(
                objects,
                continuation_token=continuation_token,
                encoding_type=encoding_type,
                prefix=prefix,
                delimiter=delimiter,
                max_keys=max_keys,
                start_after=start_after,
            )

        async with self.lock.reader:
            per_page = max(MIN_PER_PAGE, max_keys)
            return await self._collect_objects(bucket_name, filter_objects, per_page=per_page)

    async def get_object(self, bucket_name: BucketName, key: Key) -> Object:
        """Get an object by bucket and key."""
        if key == self.placeholder_name:
            raise exceptions.NoSuchKey
        file_path = _object_path(bucket_name, key)
        async with self.lock.reader:
            resp = await self.gitlab_client.get_raw_file(file_path, ref=self.branch)
        if resp.status_code == 200:
            data = resp.content
            return Object(
                data=data,
                info=ObjectInfo(
                    key=key,
                    size=len(data),
                    last_modified=datetime.datetime.now(datetime.UTC),
                    etag=get_etag(data),
                    content_type=constants.DEFAULT_CONTENT_TYPE,
                ),
            )
        if resp.status_code == 404:
            raise exceptions.NoSuchKey
        raise_for_gitlab_response(resp)

    async def put_object(
        self, bucket_name: BucketName, key: Key, data: bytes, content_type: ContentType | None = None
    ) -> ObjectInfo:
        bucket_name = validate_bucket_name(bucket_name)
        key = validate_key(key)

        if key == self.placeholder_name:
            raise ValueError("key not allowed")
        file_path = _object_path(bucket_name, key)
        content = base64.b64encode(data).decode("utf-8")
        body = CreateFile(
            branch=self.branch,
            commit_message=f"put object {file_path}",
            content=content,
            encoding="base64",
        )
        async with self.lock.writer:
            obj = ObjectInfo(
                key=key,
                size=len(data),
                last_modified=datetime.datetime.now(datetime.UTC),
                etag=get_etag(data),
                content_type=constants.DEFAULT_CONTENT_TYPE,
            )
            resp = await self.gitlab_client.create_file(file_path, body)
            if resp.status_code == 201:
                return obj
            if resp.status_code == 400:
                logger.info("gitlab create_file failed (400): %s", resp.text)
                await self._update_object(file_path, body)
                return obj
        raise_for_gitlab_response(resp)

    async def _update_object(
        self,
        file_path: str,
        body: UpdateFile,
    ) -> None:
        resp = await self.gitlab_client.update_file(file_path, body)
        if resp.status_code == 200:
            return
        raise_for_gitlab_response(resp)

    async def delete_object(self, bucket_name: BucketName, key: Key, *, keep_placeholder: bool = True) -> None:
        """Delete an object from a bucket."""
        async with self.lock.writer:
            await self._delete_object(bucket_name, key, keep_placeholder=keep_placeholder)

    async def _delete_object(self, bucket_name: BucketName, key: Key, *, keep_placeholder: bool = True) -> None:
        """Delete an object from a bucket."""
        if key == self.placeholder_name and keep_placeholder:
            logger.info("skipped placeholder delete")
            return
        file_path = _object_path(bucket_name, key)
        params = DeleteFile(
            branch=self.branch,
            commit_message=f"delete object {file_path}",
        )
        resp = await self.gitlab_client.delete_file(file_path, params)
        if resp.status_code == 204:
            return
        if resp.status_code == 400:
            logger.info("gitlab delete_file failed (400): %s", resp.text)
            return
        raise_for_gitlab_response(resp)

    async def head_object(self, bucket_name: BucketName, key: Key) -> ObjectInfo:
        async with self.lock.reader:
            return await self._head_object(bucket_name, key)

    async def _head_object(self, bucket_name: BucketName, key: Key) -> ObjectInfo:
        if key == self.placeholder_name:
            raise exceptions.NoSuchKey
        head = await self.gitlab_client.head_file(_object_path(bucket_name, key), ref=self.branch)
        if head is None:
            raise exceptions.NoSuchKey
        return ObjectInfo(
            key=key,
            size=head.gitlab_size,
            last_modified=datetime.datetime.now(datetime.UTC),
            etag=head.gitlab_content_sha256,
            content_type=constants.DEFAULT_CONTENT_TYPE,
        )

    async def _collect_objects[L: BaseListObjectsInfo](
        self,
        bucket_name: BucketName,
        filter_objects: FilterObjects[L],
        *,
        per_page: int,
    ) -> L:
        def keys_to_objects(keys: Iterable[Key]) -> list[ObjectInfo]:
            return [default_object_info(key) for key in keys]

        def is_enough(keys: list[Key]) -> bool:
            return filter_objects(keys_to_objects(keys)).is_truncated

        _keys = await self._fetch_object_keys(bucket_name, is_enough, per_page=per_page)

        objects_info = filter_objects(keys_to_objects(_keys))
        keys = [obj.key for obj in objects_info.objects]

        objects: list[ObjectInfo] = []
        for batch in itertools.batched(keys, n=BATCH_SIZE):
            coros = [self._head_object(bucket_name, key) for key in batch]
            heads = await asyncio.gather(*coros)
            objects.extend(heads)

        objects_info.objects = objects
        return objects_info

    async def _fetch_object_keys(
        self,
        bucket_name: BucketName,
        is_enough: Callable[[list[Key]], bool],
        *,
        per_page: int,
    ) -> list[Key]:
        keys: list[Key] = []
        for page in range(1, MAX_PAGE):
            params = TreeParams(
                ref=self.branch,
                path=bucket_name,
                recursive=True,
                page=page,
                per_page=per_page,
            )
            tree = await self.gitlab_client.get_tree(params)
            items = [item for item in tree.items if item.type == "blob"]
            for item in items:
                try:
                    _bucket, key = _split_path(item.path)
                except ValueError:
                    logger.exception("failed to parse object path")
                    continue
                assert _bucket == bucket_name
                keys.append(key)

            if page == tree.headers.total_pages:
                return keys
            if is_enough(keys):
                return keys

        return keys


def _object_path(bucket: BucketName, key: Key, *, delimiter: str = "/") -> str:
    return f"{bucket}{delimiter}{key}"


def _split_path(path: str, *, delimiter: str = "/") -> tuple[BucketName, Key]:
    bucket, *parts = path.split(delimiter)
    return validate_bucket_name(bucket), validate_key(delimiter.join(parts))
