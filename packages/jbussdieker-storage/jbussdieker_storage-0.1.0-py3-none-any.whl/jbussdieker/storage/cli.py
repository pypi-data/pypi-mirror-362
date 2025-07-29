def register(subparsers):
    parser = subparsers.add_parser("storage", help="Persistent storage")
    parser.set_defaults(func=main)


def main(args):
    print("storage")
