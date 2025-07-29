import pytest

from boxdrive import ObjectStore
from boxdrive.exceptions import BucketAlreadyExists, NoSuchBucket, NoSuchKey
from boxdrive.stores import InMemoryStore


@pytest.fixture
def store() -> ObjectStore:
    return InMemoryStore()


async def test_list_buckets(store: ObjectStore) -> None:
    assert await store.list_buckets() == []
    await store.create_bucket("bucket1")
    buckets = await store.list_buckets()
    assert len(buckets) == 1
    assert buckets[0].name == "bucket1"

    await store.create_bucket("bucket2")
    buckets = await store.list_buckets()
    assert len(buckets) == 2
    bucket_names = [bucket.name for bucket in buckets]
    assert set(bucket_names) == {"bucket1", "bucket2"}


async def test_create_bucket(store: ObjectStore) -> None:
    await store.create_bucket("bucket1")
    with pytest.raises(BucketAlreadyExists):
        await store.create_bucket("bucket1")


async def test_delete_bucket(store: ObjectStore) -> None:
    await store.create_bucket("bucket1")
    await store.delete_bucket("bucket1")
    assert await store.list_buckets() == []
    with pytest.raises(NoSuchBucket):
        await store.delete_bucket("bucket1")


async def test_list_objects(store: ObjectStore) -> None:
    await store.create_bucket("bucket1")
    await store.put_object("bucket1", "a.txt", b"a")
    await store.put_object("bucket1", "b.txt", b"b")
    await store.put_object("bucket1", "folder/c.txt", b"c")
    objects = await store.list_objects("bucket1")
    assert set(obj.key for obj in objects.objects) == {"a.txt", "b.txt", "folder/c.txt"}
    objects = await store.list_objects("bucket1", prefix="folder/")
    assert [obj.key for obj in objects.objects] == ["folder/c.txt"]
    with pytest.raises(NoSuchBucket):
        await store.list_objects("no-such-bucket")


async def test_get_object(store: ObjectStore) -> None:
    await store.create_bucket("bucket1")
    await store.put_object("bucket1", "key1", b"data")
    obj = await store.get_object("bucket1", "key1")
    assert obj.data == b"data"
    with pytest.raises(NoSuchKey):
        await store.get_object("bucket1", "no-such-key")
    with pytest.raises(NoSuchBucket):
        await store.get_object("no-such-bucket", "key1")


async def test_put_object(store: ObjectStore) -> None:
    info = await store.put_object("bucket1", "key1", b"data", "text/plain")
    obj = await store.get_object("bucket1", "key1")
    assert info.etag == obj.info.etag
    assert obj.data == b"data"
    assert obj.info.content_type == "text/plain"


async def test_delete_object(store: ObjectStore) -> None:
    await store.create_bucket("bucket1")
    await store.put_object("bucket1", "key1", b"data")
    await store.delete_object("bucket1", "key1")
    with pytest.raises(NoSuchKey):
        await store.get_object("bucket1", "key1")

    with pytest.raises(NoSuchBucket):
        await store.delete_object("no-such-bucket", "key1")
    await store.delete_object("bucket1", "no-such-key")


async def test_head_object(store: ObjectStore) -> None:
    await store.create_bucket("bucket1")
    await store.put_object("bucket1", "key1", b"data")
    meta = await store.head_object("bucket1", "key1")
    assert meta.key == "key1"
    with pytest.raises(NoSuchKey):
        await store.head_object("bucket1", "no-such-key")
    with pytest.raises(NoSuchBucket):
        await store.head_object("no-such-bucket", "key1")
