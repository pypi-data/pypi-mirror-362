from typing import Any, Dict, List
from loguru import logger
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

requests.packages.urllib3.disable_warnings()


class CmdbClient:
    """
    CMDB Client
    """
    def __init__(self, view_id: str, CMDB_SERVER: str, APPID: str, APPSECRET: str):
        self.SERVER = CMDB_SERVER
        # appid
        self.appid = APPID
        # appSecret
        self.appSecret = APPSECRET
        # view id：连接器id
        self.view_id = view_id
        self.HEADERS = {
            "Authorization": self.get_token()
        }

    @logger.catch
    def get_token(self):
        """
        获取 token
        """
        url = f"{self.SERVER}/api/v2/auth/login"
        data = {
            "appId": self.appid,
            "appSecret": self.appSecret
        }
        logger.debug(f"CmdbAPI -> get_token url: {url}")
        logger.debug(f"CmdbAPI -> get_token data: {json.dumps(data)}")
        response = requests.post(url=url, json=data, verify=False)
        logger.debug(f"CmdbAPI -> get_token Res: {json.dumps(response.json())}")
        return response.json().get('Authorization')

    @logger.catch
    def get_all_data(self, startPage=1, pageSize=1000, queryKey=None):
        """
        获取所有数据
        """
        url = f"{self.SERVER}/api/v2/data/view"

        # 查询条件
        queryCondition = []
        if queryKey is not None:
            queryCondition.extend(queryKey) if isinstance(queryKey, list) else queryCondition.append(queryKey)

        logger.debug(f"CmdbAPI -> get_all_data url: {url}")
        logger.debug(f"CmdbAPI -> get_all_data headers: {self.HEADERS}")
        data = {
            "moduleName": "",
            "name": "",
            "pageSize": pageSize,
            "queryCondition": queryCondition,
            "startPage": startPage,
            "viewid": self.view_id
        }
        logger.debug(f"CmdbAPI -> get_all_data data: {json.dumps(data)}")
        response_data = []
        while True:
            response = requests.post(url=url, headers=self.HEADERS, json=data, verify=False).json()
            total = response.get("total")
            response_data += response.get("content")
            if len(response_data) < total:
                data['startPage'] += 1
                logger.debug("get next request %s" % data['startPage'])
            else:
                logger.debug("get {0} instances length: {1}".format(self.view_id, len(response_data)))
                break
        logger.debug(f"CmdbAPI -> get_all_data Res: {json.dumps(response_data)}")
        return response_data

    @logger.catch
    def import_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        导入数据
        :param data: 数据
        :return: 响应数据
        """
        url = f"{self.SERVER}/api/v2/data/storage"
        logger.debug(f"CmdbAPI -> import_data url: {url}")
        logger.debug(f"CmdbAPI -> import_data headers: {self.HEADERS}")
        data = {
            "mid": self.view_id,
            "data": data
        }
        logger.debug(f"CmdbAPI -> import_data data: {json.dumps(data)}")
        response = requests.post(url=url, headers=self.HEADERS, json=data, verify=False)
        logger.debug(f"CmdbAPI -> import_data Res: {json.dumps(response.json())}")
        return response.json()
    
    @logger.catch
    def thread_import_data(self, data: List[Dict[str, Any]], batch_size: int = 100) -> bool:
        """
        多线程导入数据
        :param data: 数据
        :param batch_size: 批量大小
        :return: 是否成功
        """
        with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
            futures = []
            for i in range(0, len(data), batch_size):
                futures.append(executor.submit(self.import_data, data[i:i+batch_size]))
            for future in futures:
                logger.debug(f"CmdbAPI -> thread_import_data Res: {json.dumps(future.result())}")
        return True
