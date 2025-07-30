# -*- coding: utf-8 -*-
import asyncio
from typing import Optional, Dict
from ..lib import cfg, logger
from ..exception.exceptions import NoConfigException

LOGGER = logger.get('Oss2Client')


# oss2客户端简易封装
class Oss2Client(object):
    def __init__(self, endpoint: str = None, access_key: str = None, secret_key: str = None):
        import oss2

        self.access_key = access_key or cfg.get("OSS2_ACCESS_KEY")
        self.secret_key = secret_key or cfg.get("OSS2_SECRET_KEY")
        self.endpoint = endpoint or cfg.get("OSS2_ENDPOINT") or "https://oss-cn-beijing.aliyuncs.com"
        # 文件下载链接：示例 https://%s.oss-cn-beijing.aliyuncs.com
        self.share_url = cfg.get('OSS2_SHARE_URL_FORMAT') or self.endpoint.replace('://', '://%s.').replace('-internal.', '.')
        if not self.access_key:
            raise NoConfigException("oss2 access key not config!")
        if not self.secret_key:
            raise NoConfigException("oss2 secret key not config!")

        self.auth = oss2.Auth(self.access_key, self.secret_key)
        self.bucket_map = dict()

    async def async_put_stream(self, bucket_name: str, object_name: str, image_content: bytes, content_type='application/octet-stream') -> Dict:
        __bucket = self._get_bucket(bucket_name)
        headers = dict()
        if content_type:
            headers["Content-Type"] = content_type
        if object_name:
            await asyncio.to_thread(__bucket.put_object, key=object_name, data=image_content, headers=headers)
            file_url = self.get_object_url(bucket_name, object_name)
            return {
                "url": file_url,
                "file_path": f"{bucket_name}/{object_name}"
            }

    def put_stream(self, bucket_name: str, object_name: str, image_content: bytes, content_type='application/octet-stream') -> Dict:
        bucket = self._get_bucket(bucket_name)
        headers = dict()
        if content_type:
            headers["Content-Type"] = content_type
        if object_name:
            bucket.put_object(key=object_name, data=image_content, headers=headers)
            file_url = self.get_object_url(bucket_name, object_name)
            return {
                "url": file_url,
                "file_path": f"{bucket_name}/{object_name}"
            }

    async def async_put_object(self, bucket_name: str, object_name: str, file_path: str, content_type='application/octet-stream') -> Dict:
        __bucket = self._get_bucket(bucket_name)
        headers = dict()
        if content_type:
            headers["Content-Type"] = content_type
        if object_name:
            await asyncio.to_thread(__bucket.put_object_from_file, filename=file_path, key=object_name, headers=headers)
            file_url = self.get_object_url(bucket_name, object_name)
            return {
                "url": file_url,
                "file_path": object_name
            }

    def put_object(self, bucket_name: str, object_name: str, file_path: str, content_type='application/octet-stream') -> Dict:
        bucket = self._get_bucket(bucket_name)
        headers = dict()
        if content_type:
            headers["Content-Type"] = content_type
        if object_name:
            bucket.put_object_from_file(filename=file_path, key=object_name, headers=headers)
            file_url = self.get_object_url(bucket_name, object_name)
            return {
                "url": file_url,
                "file_path": object_name
            }

    def _get_bucket(self, bucket_name: str):
        bucket = self.bucket_map.get(bucket_name)
        if not bucket:
            import oss2
            bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name)
            self.bucket_map[bucket_name] = bucket

        return bucket

    def get_object_url(self, bucket_name: str, object_name: str) -> Optional[str]:
        # 桶均为公共读私有写，可直接访问对象
        if '%s' in self.share_url:
            return f'{self.share_url % bucket_name}/{object_name}'

        # 自有域名
        return f'{self.share_url}/{object_name}'
