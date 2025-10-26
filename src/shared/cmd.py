import argparse


def parse_offline_flag() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--offline",
        action="store_true",
    )
    args, _ = parser.parse_known_args()
    return args.offline


def parse_no_server_flag() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-server",
        action="store_true",
    )
    args, _ = parser.parse_known_args()
    return args.no_server
