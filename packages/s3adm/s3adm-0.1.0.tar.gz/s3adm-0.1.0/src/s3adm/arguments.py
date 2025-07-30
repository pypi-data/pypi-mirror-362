import argparse
import os


def base_arguments() -> argparse.Namespace:
    """
    Base arguments for the S3 admin CLI.
    """
    arguments = argparse.ArgumentParser(description="S3 Bucket Monitoring CLI")
    arguments.add_argument(
        "--log-level",
        type=str,
        default="warning",
        help="Set the logging level (default: %(default)s)",
        choices=["debug", "info", "warning", "error", "critical"]
    )
    arguments.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="RadosGw host to connect to"
    )
    arguments.add_argument(
        "--schema",
        type=str,
        default="http",
        help="Schema for the RadosGw connection (default: %(default)s)"
    )
    arguments.add_argument(
        "--port",
        type=int,
        default=80,
        help="Port for the RadosGw connection (default: %(default)s)"
    )
    arguments.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout for API requests in seconds (default: %(default)s)"
    )
    arguments.add_argument(
        "--insecure",
        type=str,
        default="true",
        help="Insecure connection flag (true/false), (default: %(default)s)",
    )
    arguments.add_argument(
        "--access-key",
        type=str,
        help="S3 access key, can be set via environment variable S3_ACCESS_KEY",
        default=os.getenv("S3_ACCESS_KEY", None)
    )
    arguments.add_argument(
        "--secret-key",
        type=str,
        help="S3 secret key, can be set via environment variable S3_SECRET_KEY",
        default=os.getenv("S3_SECRET_KEY", None)
    )
    arguments.add_argument(
        "--sort-by",
        type=str,
        default="size",
        help="Sort results by 'size' or 'objects' (default: %(default)s)",
        choices=["size", "objects", "owner"]
    )
    arguments.add_argument(
        "--human-readable",
        action="store_true",
        help="Display in human-readable format"
    )
    arguments.add_argument(
        "--sort-reverse",
        action="store_true",
        default=False,
        help="Sort results in reverse order"
    )
    return arguments.parse_args()