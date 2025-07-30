'''
探针包地址，最终兜底逻辑。一旦设置只会走该地址下载。
'''
import os

PYTHON_AGENT_PATH = "PYTHON_AGENT_PATH"
'''
区域，拉去对应region的探针包
'''
REGION_ID = "ARMS_REGION_ID"
'''
探针版本
'''
VERSION = "VERSION"
'''
内网后缀
'''
INTERNAL = "-internal"
'''
oss地址后缀
'''
OSS_URL = "aliyuncs.com"
'''
oss bucket 列表
'''
OSS_BUCKET_LIST = {
    "cn-shanghai-finance-1": "arms-apm-cn-shanghai-finance-1",
    "cn-qingdao": "arms-apm-cn-qingdao",
    "cn-hongkong": "arms-apm-cn-hongkong",
    "cn-beijing": "arms-apm-cn-beijing",
    "cn-zhangjiakou": "arms-apm-cn-zhangjiakou",
    "cn-huhehaote": "arms-apm-cn-huhehaote",
    "cn-wulanchabu": "arms-apm-cn-wulanchabu",
    "cn-heyuan": "arms-apm-cn-heyuan",
    "cn-guangzhou": "arms-apm-cn-guangzhou",
    "cn-chengdu": "arms-apm-cn-chengdu",
    "cn-hangzhou": "arms-apm-cn-hangzhou",
    "cn-shanghai": "arms-apm-cn-shanghai",
    "cn-shenzhen": "arms-apm-cn-shenzhen",
    "ap-southeast-2": "arms-apm-ap-southeast-2",
    "ap-southeast-3": "arms-apm-ap-southeast-3",
    "me-east-1": "arms-apm-me-east-1",
    "us-east-1": "arms-apm-us-east-1",
    "ap-south-1": "arms-apm-ap-south-1",
    "ap-northeast-1": "arms-apm-ap-northeast-1",
    "ap-southeast-1": "arms-apm-ap-southeast-1",
    "us-west-1": "arms-apm-us-west-1",
    "eu-west-1": "arms-apm-eu-west-1",
    "eu-central-1": "arms-apm-eu-central-1",
    "ap-southeast-5": "arms-apm-ap-southeast-5",
    "cn-shenzhen-finance-1": "arms-apm-cn-shenzhen-finance-1",
    "cn-hangzhou-finance": "arms-apm-cn-hangzhou-finance",
    "cn-north-2-gov-1": "arms-apm-cn-north-2-gov-1",
    "ap-southeast-6": "arms-apm-ap-southeast-6",
    "me-central-1": "arms-apm-me-central-1",
    "ap-southeast-7": "arms-apm-ap-southeast-7",
    "cn-zhengzhou-jva": "arms-apm-cn-zhengzhou-jva"
}
'''
oss prefix
'''
OSS_PREFIX = {
    "cn-shanghai-finance-1": "oss-cn-shanghai-finance-1",
    "cn-qingdao": "oss-cn-qingdao",
    "cn-hongkong": "oss-cn-hongkong",
    "cn-beijing": "oss-cn-beijing",
    "cn-zhangjiakou": "oss-cn-zhangjiakou",
    "cn-huhehaote": "oss-cn-huhehaote",
    "cn-wulanchabu": "oss-cn-wulanchabu",
    "cn-heyuan": "oss-cn-heyuan",
    "cn-guangzhou": "oss-cn-guangzhou",
    "cn-chengdu": "oss-cn-chengdu",
    "cn-hangzhou": "oss-cn-hangzhou",
    "cn-shanghai": "oss-cn-shanghai",
    "cn-shenzhen": "oss-cn-shenzhen",
    "ap-southeast-2": "oss-ap-southeast-2",
    "ap-southeast-3": "oss-ap-southeast-3",
    "me-east-1": "oss-me-east-1",
    "us-east-1": "oss-us-east-1",
    "ap-south-1": "oss-ap-south-1",
    "ap-northeast-1": "oss-ap-northeast-1",
    "ap-southeast-1": "oss-ap-southeast-1",
    "us-west-1": "oss-us-west-1",
    "eu-west-1": "oss-eu-west-1",
    "eu-central-1": "oss-eu-central-1",
    "ap-southeast-5": "oss-ap-southeast-5",
    "eu-central-1": "oss-eu-central-1",
    "cn-shanghai-finance-1": "oss-cn-shanghai-finance-1",
    "cn-shenzhen-finance-1": "oss-cn-shenzhen-finance-1",
    "cn-hangzhou-finance": "oss-cn-hzjbp-a",
    "cn-north-2-gov-1": "oss-cn-north-2-gov-1",
    "cn-shenzhen-finance-1": "oss-cn-shenzhen-finance-1",
    "cn-qingdao": "oss-cn-qingdao",
    "cn-north-2-gov-1": "oss-cn-north-2-gov-1",
    "ap-southeast-6": "oss-ap-southeast-6",
    "me-central-1": "oss-me-central-1",
    "ap-southeast-7": "oss-ap-southeast-7",
    "cn-zhengzhou-jva": "oss-cn-zhengzhou-jva",
}

'''
控制是否使用公网的参数，做应急使用。一般不透出
正常使用auto自动判断即可
'''
PROFILER_NETWORK_STRATEGY = "PROFILER_NETWORK_STRATEGY"

'''
oss path
'''
OSS_PATH = "aliyun-python-agent"
'''
agent文件名
'''
AGENT_FILE_NAME = "aliyun-python-agent.tar.gz"
'''
默认探针地址
'''
DEFAULT_AGENT_URL = "https://arms-apm-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/aliyun-python-agent/aliyun-python-agent.tar.gz"
