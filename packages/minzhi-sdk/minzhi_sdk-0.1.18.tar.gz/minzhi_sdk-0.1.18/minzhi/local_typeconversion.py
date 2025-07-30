# -*- coding: utf-8 -*-
"""
本地开发时的 TypeConversion 模块替代
在平台运行时，真正的 TypeConversion 模块会被动态注入
"""
import os
import json
import requests
from loguru import logger

def read_json_file(json_path):
    """读取 JSON 配置文件"""
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except IOError:
        logger.error(f"无法打开文件: {json_path}")
        return None

def _load_params():
    """加载 params.json 配置文件"""
    # 尝试多个可能的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(current_dir, "params.json"),
        os.path.join(current_dir, "../params.json"),
        "params.json",
        "./params.json"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            params = read_json_file(path)
            if params:
                logger.info(f"本地开发模式：加载配置文件 {path}")
                return params
    
    raise FileNotFoundError("未找到 params.json 配置文件，请确保文件存在于项目目录中")

# 加载配置
try:
    params_json = _load_params()
    res = params_json.get("params", {})
    recallData = params_json.get("recallData")
    recallLogUrl = params_json.get("recallLogUrl")
    platform = params_json.get("platform")
except Exception as e:
    logger.error(f"加载配置失败: {e}")
    # 提供默认值避免导入错误
    params_json = {}
    res = {}
    recallData = {}
    recallLogUrl = ""
    platform = "dev"

def invoke(entity, api, params, businessId=None, platform=platform):
    """实体操作调用"""
    if businessId is None and recallData:
        thirdParams = recallData.get("thirdParams", {})
        businessId = thirdParams.get("businessId")
    
    tenantName = params_json.get("tenantName")
    tenantId = params_json.get("tenantId")
    engineAddress = params_json.get("engineAddress")
    token = params_json.get("token")
    username = params_json.get("username")
    
    url = f"{engineAddress}/web/entityOperation?tenantName={tenantName}&tenantId={tenantId}&platform={platform}&entity={entity}&api={api}&businessId={businessId}&username={username}"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.post(url, json=params, headers=headers, timeout=30)
        return response.json()
    except Exception as e:
        logger.error(f"API 调用失败: {e}")
        raise

def invoke_enum(enum_name, businessId=None, platform=platform):
    """枚举操作调用"""
    if businessId is None and recallData:
        thirdParams = recallData.get("thirdParams", {})
        businessId = thirdParams.get("businessId")
    
    tenantName = params_json.get("tenantName")
    tenantId = params_json.get("tenantId")
    engineAddress = params_json.get("engineAddress")
    token = params_json.get("token")
    username = params_json.get("username")
    
    params = {
        "name": enum_name,
        "username": username,
        "tenantName": tenantName,
        "tenantId": tenantId,
        "token": token,
        "platform": platform,
        "businessId": businessId,
        "params": {},
    }
    
    url = f"{engineAddress}/web/enumOperation"
    headers = {
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.post(url, json=params, headers=headers, timeout=30)
        return response.json()
    except Exception as e:
        logger.error(f"枚举调用失败: {e}")
        raise

def ae_headers():
    """获取 AE 请求头"""
    tenantId = params_json.get("tenantId")
    token = params_json.get("token")
    platform = params_json.get("platform")
    headers = {
        "tenantId": tenantId,
        "token": token,
        "platform": platform,
    }
    return headers 