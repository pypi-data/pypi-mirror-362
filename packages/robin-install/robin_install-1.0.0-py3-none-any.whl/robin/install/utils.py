import os
from robin.install import envs
import logging
import requests

logger = logging.getLogger(__name__)
'''
获取agent 下载地址。
'''


def get_agent_path():
    url = os.getenv(envs.PYTHON_AGENT_PATH, None)
    if url is not None:
        return url
    region_id = os.getenv(envs.REGION_ID, None)
    if region_id is None:
        return None
    bucket_name = envs.OSS_BUCKET_LIST[region_id]
    if bucket_name is None:
        return None
    oss_prefix = envs.OSS_PREFIX[region_id]
    if oss_prefix is None:
        return None

    # Check if version is specified
    version = os.getenv("VERSION", None)
    if version:
        # Use version-specific path
        path_segment = f"{envs.OSS_PATH}/{version}/{envs.AGENT_FILE_NAME}"
    else:
        # Use default path
        path_segment = f"{envs.OSS_PATH}/{envs.AGENT_FILE_NAME}"

    # Try internal URL first
    url = f"https://{bucket_name}.{oss_prefix}{envs.INTERNAL}.{envs.OSS_URL}/{path_segment}"
    internal_connect = check_network(url=url)
    if internal_connect:
        logger.info(f"use internal region url {url}")
        return url
        
    # Fallback to public URL
    url = f"https://{bucket_name}.{oss_prefix}.{envs.OSS_URL}/{path_segment}"
    public_connect = check_network(url=url)
    if public_connect:
        logger.info(f"use public region url {url}")
        return url
    return None


'''
判断网络是否通
'''


def check_network(url, timeout=1):
    try:
        response = requests.request("GET", url, timeout=timeout)
        if response.status_code == 200:
            return True
    except Exception:
        return False
