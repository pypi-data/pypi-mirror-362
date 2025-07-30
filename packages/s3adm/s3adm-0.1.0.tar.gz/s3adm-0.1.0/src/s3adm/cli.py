import json
import time
import logging
from tabulate import tabulate
from typing import List
from .api import CephAdminApi
from ._helpers import convert_to_human_size, convert_to_human_number
from .arguments import base_arguments

_logger = logging.getLogger("s3-adm")

def bucket_stats(api: CephAdminApi, buckets: list) -> list:
    results = []
    for bucket in buckets:
        _logger.debug("Collecting bcket %s statistics", bucket)
        bucket_info = api.request(request="bucket", params=f"bucket={bucket}").json()
        owner: str = bucket_info.get("owner", "unknown")
        rgw_main = bucket_info.get("usage").get("rgw.main", {})
        size = rgw_main.get("size_actual", 0)
        utilized = rgw_main.get("size_utilized", 0)
        objects = rgw_main.get("num_objects", 0)
        bucket_stats = {
            "bucket": bucket,
            "owner": owner,
            "objects": objects,
            "size": size,
            "used": utilized,
        }
        results.append(bucket_stats)
    _logger.debug("Buckets stats:\n%s", json.dumps(results, indent=2))
    return results

def sort_results(results: List[dict], sort_by: str, reverse: bool = True) -> List[dict]:
    _logger.debug("Sorting results by '%s' in %s order", sort_by, "descending" if reverse else "ascending")
    return sorted(results, key=lambda d: d[sort_by], reverse=reverse)

def convert_to_human(results: List[dict]) -> List[dict]:
    _logger.debug("Converting results to human-readable format")
    for result in results:
        size, size_unut = convert_to_human_size(result["size"])
        used, size_used_unit = convert_to_human_size(result["used"])
        objects, objects_unit = convert_to_human_number(result["objects"])
        result["size"] = f"{size} {size_unut}"
        result["used"] = f"{used} {size_used_unit}"
        result["objects"] = f"{objects} {objects_unit}"
    return results

def main() -> None:
    strt_time = time.perf_counter()
    args = base_arguments()
    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    _logger.info("Starting S3 bucket monitoring CLI")
    _logger.debug("Parsed arguments: %s", args)
    with CephAdminApi(
        schema=args.schema,
        host=args.host,
        port=args.port,
        access_key=args.access_key,
        secret_key=args.secret_key,
        insecure=args.insecure,
        timeout=args.timeout
    ) as admin:
        _logger.debug("Connected to Ceph Admin API at %s", admin._api_url)
        buckets: list = admin.request("bucket").json()
        results: List[dict]= bucket_stats(api=admin, buckets=buckets)
    results = sort_results(results=results, sort_by=args.sort_by, reverse=args.sort_reverse)
    if args.human_readable:
        results = convert_to_human(results=results)
    print(tabulate(results, headers="keys"))
    end_time = time.perf_counter()
    _logger.info("Finished S3 bucket monitoring CLI in %.2f seconds", end_time - strt_time)