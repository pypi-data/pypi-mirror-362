import json
import logging
import os
import threading
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

PUT_TAG_ACTION_NAME = "PutBucketDoubleMeterTagging"
GET_TAG_ACTION_NAME = "GetBucketTagging"
DEL_TAG_ACTION_NAME = "DeleteBucketTagging"
EMR_OPEN_API_VERSION = "2022-12-29"


service_info_map = {
    "cn-beijing": ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                              Credentials('', '', "emr", "cn-beijing"), 60 * 5, 60 * 5, "http"),
    "cn-guangzhou": ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                                Credentials('', '', "emr", "cn-guangzhou"), 60 * 5, 60 * 5, "http"),
    "cn-shanghai": ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                               Credentials('', '', "emr", "cn-shanghai"), 60 * 5, 60 * 5, "http"),
    "ap-southeast-1": ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                               Credentials('', '', "emr", "ap-southeast-1"), 60 * 5, 60 * 5, "http"),
    "cn-beijing-selfdrive": ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                                Credentials('', '', "emr", "cn-beijing-selfdrive"), 60 * 5, 60 * 5, "http"),
    "cn-beijing-autodriving": ServiceInfo("emr.cn-beijing-autodriving.volcengineapi.com", {'accept': 'application/json', },
                                Credentials('', '', "emr", "cn-beijing-autodriving"), 60 * 5, 60 * 5, "https"),
    "cn-shanghai-autodriving": ServiceInfo("emr.cn-shanghai-autodriving.volcengineapi.com", {'accept': 'application/json', },
                                Credentials('', '', "emr", "cn-shanghai-autodriving"), 60 * 5, 60 * 5, "https"),
    "cn-beijing-qa": ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                                 Credentials('', '', "emr_qa", "cn-beijing"), 60 * 5, 60 * 5, "http"),
}

api_info = {
    PUT_TAG_ACTION_NAME: ApiInfo("POST", "/", {
        "Action": PUT_TAG_ACTION_NAME, "Version": EMR_OPEN_API_VERSION}, {}, {}),
    GET_TAG_ACTION_NAME: ApiInfo("GET", "/", {
        "Action": GET_TAG_ACTION_NAME, "Version": EMR_OPEN_API_VERSION}, {}, {}),
    DEL_TAG_ACTION_NAME: ApiInfo("POST", "/", {
        "Action": DEL_TAG_ACTION_NAME, "Version": EMR_OPEN_API_VERSION}, {}, {}),
}

class BucketTagAction(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(BucketTagAction, "_instance"):
            with BucketTagAction._instance_lock:
                if not hasattr(BucketTagAction, "_instance"):
                    BucketTagAction._instance = object.__new__(cls)
        return BucketTagAction._instance

    def __init__(self, access_key = None, secret_key = None, region = "cn-beijing"):
        if region is None:
            region = "cn-beijing"
        super().__init__(self.get_service_info(region), self.get_api_info())
        if access_key is not None and secret_key is not None:
            self.set_ak(access_key)
            self.set_sk(secret_key)

    @staticmethod
    def get_api_info():
        return api_info

    @staticmethod
    def get_service_info(region):
        service_info = service_info_map.get(region, None)
        if service_info:
            return service_info
        elif 'VOLC_REGION' in os.environ:
            return ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                               Credentials('', '', "emr", region), 60 * 5, 60 * 5, "http")
        else:
            raise Exception('do not support region %s' % region)
        return service_info

    def put_Bucket_tag(self, bucket):
        params = {"Bucket": bucket,}

        try:
            res = self.json(PUT_TAG_ACTION_NAME, params, json.dumps(""))
            res_json = json.loads(res)
            logging.debug("Put tag for bucket %s is success. The result of put_Bucket_tag is %s.", bucket, res_json)
            return (bucket, True)
        except Exception as e:
            logging.error("Put tag for bucket %s is failed: %s", bucket, e)
            return (bucket, False)

    def get_Bucket_tag(self, bucket):
        params = {"Bucket": bucket,}
        try:
            res = self.get(GET_TAG_ACTION_NAME, params)
            res_json = json.loads(res)
            logging.debug("The result of get_Bucket_tag is %s", res_json)
            return True
        except Exception as e:
            logging.error("Get tag for %s is failed: %s", bucket, e)
            return False

    def del_Bucket_tag(self, bucket):
        params = {"Bucket": bucket,}
        try:
            res = self.json(DEL_TAG_ACTION_NAME, params, json.dumps(""))
            res_json = json.loads(res)
            logging.debug("The result of del_Bucket_tag is %s", res_json)
        except Exception as e:
            logging.error("Delete tag for %s is failed: %s", bucket, e)
