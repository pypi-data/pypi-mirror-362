from jbussdieker.storage.store import S3Store


def register(subparsers):
    parser = subparsers.add_parser("storage", help="Persistent storage")
    parser.set_defaults(func=main)


def main(args, config):
    if not config.storage_url:
        raise ValueError("No storage URL found in config")
    if config.storage_url.startswith("s3://"):
        bucket, prefix = config.storage_url.split("://", 1)[1].split("/", 1)
        store = S3Store(bucket, prefix)
        for subprefix in store.dir():
            print(subprefix)
    else:
        raise ValueError("Unsupported storage URL")
