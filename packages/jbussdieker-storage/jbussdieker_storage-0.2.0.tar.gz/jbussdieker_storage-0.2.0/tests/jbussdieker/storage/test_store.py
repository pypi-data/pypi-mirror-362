import unittest
from unittest.mock import patch, MagicMock
from jbussdieker.storage.store import S3Store


class TestS3Store(unittest.TestCase):
    @patch("jbussdieker.storage.store.boto3")
    def test_post_init_sets_client(self, mock_boto3):
        store = S3Store("bucket", "prefix/")
        mock_boto3.client.assert_called_once_with("s3")
        self.assertTrue(hasattr(store, "client"))

    def make_store_with_client(self):
        store = S3Store("bucket", "prefix/")
        store.client = MagicMock()
        return store

    def test_get_prefixes_yields_expected(self):
        store = self.make_store_with_client()
        paginator = MagicMock()
        store.client.get_paginator.return_value = paginator
        paginator.paginate = MagicMock(
            return_value=[
                {
                    "CommonPrefixes": [
                        {"Prefix": "prefix/foo/"},
                        {"Prefix": "prefix/bar/"},
                    ]
                }
            ]
        )
        result = list(store._get_prefixes())
        self.assertEqual(result, ["foo/", "bar/"])

    def test_dir_yields_from_get_prefixes(self):
        store = self.make_store_with_client()
        store._get_prefixes = MagicMock(return_value=["foo/", "bar/"])
        result = list(store.dir())
        self.assertEqual(result, ["foo/", "bar/"])


if __name__ == "__main__":
    unittest.main()
