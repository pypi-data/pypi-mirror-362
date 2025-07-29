from dataclasses import dataclass
import boto3


@dataclass
class S3Store:
    bucket: str
    prefix: str

    def __post_init__(self):
        self.client = boto3.client("s3")

    def _get_prefixes(self, prefix: str = ""):
        paginator = self.client.get_paginator("list_objects_v2")
        pages = paginator.paginate(
            Bucket=self.bucket, Prefix=self.prefix + prefix, Delimiter="/"
        )
        for page in pages:
            for obj in page["CommonPrefixes"]:
                yield obj["Prefix"].removeprefix(self.prefix + prefix)

    def dir(self, prefix: str = ""):
        for subprefix in self._get_prefixes(prefix):
            yield subprefix
