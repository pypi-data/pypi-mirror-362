import base64
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from typing import List, Dict, Any
from loguru import logger

class AEClient:
    """
    获取 token
    pip install pycryptodome
    """
    def __init__(self, SERVER: str, USER: str, PASSWORD: str):
        self.SERVER = SERVER
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.HEADERS = {"Cookie": f"token={self.get_token()}"}

    @logger.catch
    def _get_rsa_public_key(self) -> str:
        """
        获取 RSA 公钥
        :return: RSA 公钥
        """
        url = f"{self.SERVER}/gateway/get_rsa_public_key/direct"
        response = requests.get(url, verify=False)
        return f"""-----BEGIN PUBLIC KEY-----\n{response.text}\n-----END PUBLIC KEY-----"""

    @logger.catch
    def _encrypt_password(self) -> str:
        """
        RSA 加密密码
        :return: 加密后的密码
        """
        rsa_key = RSA.import_key(self._get_rsa_public_key())
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(self.PASSWORD.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')

    @logger.catch
    def get_token(self) -> str:
        """
        获取 token
        :return: token
        """
        url = f"{self.SERVER}/usercenter/userAuth/oauth/token"
        headers = {
            "Authorization": "Basic cXo6c2hxejg4NjYu"
        }
        params = {
            "username": self.USER,
            "password": self._encrypt_password()
        }
        response = requests.post(url, headers=headers, params=params, verify=False)
        return response.json().get("body")
    


class CmdbClient:
    """
    获取 token
    pip install pycryptodome
    """
    def __init__(self, SERVER: str, USER: str, PASSWORD: str):
        self.SERVER = SERVER
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.HEADERS = {"Cookie": f"token={self.get_token()}"}

    @logger.catch
    def _get_rsa_public_key(self) -> str:
        """
        获取 RSA 公钥
        :return: RSA 公钥
        """
        url = f"{self.SERVER}/qz-gateway/get_rsa_public_key/direct"
        response = requests.get(url, verify=False)
        return f"""-----BEGIN PUBLIC KEY-----\n{response.text}\n-----END PUBLIC KEY-----"""

    @logger.catch
    def _encrypt_password(self) -> str:
        """
        RSA 加密密码
        :return: 加密后的密码
        """
        rsa_key = RSA.import_key(self._get_rsa_public_key())
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(self.PASSWORD.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')

    @logger.catch
    def get_token(self) -> str:
        """
        获取 token
        :return: token
        """
        url = f"{self.SERVER}/qz-gateway/qz-auth/oauth/token"
        headers = {
            "Authorization": "Basic cXo6c2hxejg4NjYu"
        }
        params = {
            "username": self.USER,
            "password": self._encrypt_password()
        }
        response = requests.post(url, headers=headers, params=params, verify=False)
        return response.json().get("body")
    
    @logger.catch
    def search_cmdb_data(self, CI: str, query: List[Dict[str, Any]], page_size: int = 1000) -> List[Dict[str, Any]]:
        """
        搜索 CMDB 数据
        :param CI: 模型ID
        :param query: 查询条件
        :return: 数据
        """
        url = f"{self.SERVER}/cmdb/instance/page/{CI}"
        data = {
            "size":page_size,
            "current":1,
            "advancedQuery":{},
            "entityQueries":query,
            "allQuery":None
        }
        response_data = []
        while True:
            response = requests.post(url, headers=self.HEADERS, json=data, verify=False)
            response_data += response.json().get("body").get("records")
            if response.json().get("body").get("total") > len(response_data):
                data["current"] += 1
            else:
                break
        return response_data
    
    @logger.catch
    def delete_cmdb_data(self, CI: str, ids: List[str]) -> Dict[str, Any]:
        """
        删除 CMDB 数据
        :param CI: 模型ID
        :param ids: 数据ID
        :return: 返回结果
        """
        url = f"{self.SERVER}/cmdb/cmdb-sdk/deleteBath/{CI}"
        response = requests.post(url, headers=self.HEADERS, json=ids, verify=False)
        return response.json()