import argparse


def parse_offline_flag() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--offline",
        action="store_true",
    )
    args, _ = parser.parse_known_args()
    return args.offline
