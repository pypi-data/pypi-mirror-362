from concurrent.futures import ThreadPoolExecutor
from ray.tos.tag.bucket_tag_action import BucketTagAction
from typing import Optional

import fcntl
import functools
import os
import pyarrow
import urllib.parse

THREAD_POOL_SIZE = 2
TAGGED_BUCKETS_FILE = f"/tmp/.emr_tagged_buckets"

def singleton(cls):
    _instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return get_instance

@singleton
class BucketTagMgr:
    def __init__(self):
        self._launch_executor = ThreadPoolExecutor(
            max_workers=THREAD_POOL_SIZE
        )
        self._cache_bucket_set = set()

    def fs_is_s3fs(self, filesystem: Optional["pyarrow.fs.FileSystem"] = None):
        return isinstance(filesystem, pyarrow.fs.S3FileSystem)

    def unwrap_fs(self, filesystem: Optional["pyarrow.fs.FileSystem"] = None):
        filesystem = filesystem.unwrap() if hasattr(filesystem, "unwrap") and callable(filesystem.unwrap) else filesystem
        return filesystem

    def add_tag_to_tos_buckets(self, paths, filesystem: Optional["pyarrow.fs.FileSystem"] = None):
        filesystem = self.unwrap_fs(filesystem)
        if filesystem is None or not self.fs_is_s3fs(filesystem):
            return

        collect_bucket_set = set()
        for path in paths:
            url_str = urllib.parse.urlparse(path)
            if url_str.hostname:
                bucket = url_str.hostname
            else:
                bucket = path.lstrip().split("/")[0]
            collect_bucket_set.add(bucket)

        if len(collect_bucket_set) == 0 or len(collect_bucket_set - self._cache_bucket_set) == 0:
            return

        tagged_bucket_from_file_set = set()
        if os.path.exists(TAGGED_BUCKETS_FILE):
            fr = open(TAGGED_BUCKETS_FILE, "r")
            tagged_bucket_from_file_set = set(fr.read().split(" "))
            fr.close()

        self._cache_bucket_set = self._cache_bucket_set | tagged_bucket_from_file_set
        need_tag_buckets = collect_bucket_set - self._cache_bucket_set

        ak = filesystem.access_key
        sk = filesystem.secret_key
        endpoint_region_value = '-'.join(filesystem.endpoint_override.split(".")[0].split("-")[2:])

        if (ak is None or sk is None) and 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:
            ak = os.environ['AWS_ACCESS_KEY_ID']
            sk = os.environ['AWS_SECRET_ACCESS_KEY']

        if 'VOLC_REGION' in os.environ:
            region_value = os.environ['VOLC_REGION']
        elif endpoint_region_value is not None:
            region_value = endpoint_region_value
        else:
           region_value = "cn-beijing"

        bucket_tag_service = BucketTagAction(access_key = ak, secret_key = sk, region=region_value)

        for res in self._launch_executor.map(bucket_tag_service.put_Bucket_tag,
                                             [(bucket) for bucket in need_tag_buckets]):
            if res[1] is True:
                self._cache_bucket_set.add(res[0])

        with open(TAGGED_BUCKETS_FILE, "w") as fw:
            fcntl.flock(fw, fcntl.LOCK_EX)
            fw.write(" ".join(self._cache_bucket_set))
            fcntl.flock(fw, fcntl.LOCK_UN)
            fw.close()
