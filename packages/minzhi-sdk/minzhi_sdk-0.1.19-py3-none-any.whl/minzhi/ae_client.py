from typing import Any, Dict, List, Optional
from loguru import logger
import sys

class Result:
    def __init__(self, data: Dict[str, Any], context: Optional[Dict[str, Any]] = None):
        self.data = data
        self.context = context or {}

    def is_success(self) -> bool:
        """
        检查请求是否成功
        """
        return self.data and self.data.get("code") == 200 and self.data.get("body")

    def ensure_success(self):
        """
        确保请求成功，失败时抛出异常
        """
        if not self.is_success():
            error_info = self._extract_key_info(self.data)
            raise Exception(f"返回结果检查失败: {error_info}")
        return self
    
    def get_data(self):
        """
        获取处理后的数据
        """
        if not self.is_success():
            return {}
        
        method_name = self.context.get("method_name")
        if method_name == "getEnum":
            temp_list = self.data.get("body", {}).get("enum_infos", [])
            return {item["title"]: item["value"] for item in temp_list}
        
        return self.data.get("body", {})

    def to_json(self):
        """
        将结果转换为 JSON 字符串
        """
        import json
        return json.dumps(self.get_data(), ensure_ascii=False)
    
    def _extract_key_info(self, data: Dict[str, Any], max_depth: int = 2, current_depth: int = 0) -> Dict[str, Any]:
        """
        提取字典中的关键信息，限制嵌套深度和数据量
        """
        if current_depth >= max_depth:
            return {"...": "数据过深，已截断"}
        
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                # 递归处理嵌套字典，但限制深度
                if len(value) > 5:  # 如果字典太大，只显示前几个键
                    truncated = dict(list(value.items())[:3])
                    truncated["..."] = f"还有{len(value) - 3}个字段"
                    result[key] = self._extract_key_info(truncated, max_depth, current_depth + 1)
                else:
                    result[key] = self._extract_key_info(value, max_depth, current_depth + 1)
            elif isinstance(value, list):
                # 处理列表，只显示长度和前几个元素的类型
                if len(value) > 3:
                    sample = [type(item).__name__ for item in value[:3]]
                    result[key] = f"列表[长度:{len(value)}, 前3个类型:{sample}...]"
                else:
                    result[key] = f"列表[长度:{len(value)}]"
            elif isinstance(value, str) and len(value) > 100:
                # 长字符串截断
                result[key] = f"{value[:50]}...(长度:{len(value)})"
            else:
                # 基本类型直接保留
                result[key] = value
        
        return result
      
    def count(self):
        """
        获取记录数量
        """
        return len(self.get_data())
    
    def is_empty(self):
        """
        检查结果是否为空
        """
        return self.count() == 0
    
    def get_error_message(self):
        """
        获取错误信息
        """
        if self.is_success():
            return None
        return self.data.get("message", "未知错误")
    
    def to_dataframe(self):
        """
        将结果转换为pandas的DataFrame
        """
        try:
            import pandas as pd
            records = self.get_data()
            return pd.DataFrame(records) if records else pd.DataFrame()
        except ImportError:
            raise ImportError("需要安装 pandas: pip install pandas")


class AEClient:
    """
    AE Client
    """

    def __init__(self, businessId: str, table_name: str):
        self.businessId = businessId
        self.table_name = table_name
        self.res = self._get_res()
        self.invoke = self._get_invoke()
        self.invoke_enum = self._get_invoke_enum()
        self.params_json = self._get_params_json()

    @logger.catch
    def _get_res(self) -> Dict[str, Any]:
        try:
            from TypeConversion import res
            logger.debug("使用平台注入的 TypeConversion.res")
            return res
        except ImportError:
            logger.warning("TypeConversion 未注入，使用本地模块")
            from .local_typeconversion import res
            return res
    
    @logger.catch
    def _get_params_json(self) -> Dict[str, Any]:
        try:
            from TypeConversion import params_json
            logger.debug("使用平台注入的 TypeConversion.params_json")
            return params_json
        except ImportError:
            logger.warning("TypeConversion 未注入，使用本地模块")
            from .local_typeconversion import params_json
            return params_json

    @logger.catch
    def _get_invoke(self):
        try:
            from TypeConversion import invoke
            logger.debug("使用平台注入的 TypeConversion.invoke")
            return invoke
        except ImportError:
            logger.warning("TypeConversion 未注入，使用本地模块")
            from .local_typeconversion import invoke
            return invoke
    
    @logger.catch
    def _get_invoke_enum(self):
        try:
            from TypeConversion import invoke_enum
            logger.debug("使用平台注入的 TypeConversion.invoke_enum")
            return invoke_enum
        except ImportError:
            logger.warning("TypeConversion 未注入，使用本地模块")
            from .local_typeconversion import invoke_enum
            return invoke_enum

    @logger.catch
    def selectPage(self, current: int, pageSize: int) -> Result:
        """
        分页查询
        Args:
            current: 当前页码
            pageSize: 每页条数
        Returns:
            Result: 查询结果
        """
        data = {
            "current": current,
            "pageSize": pageSize,
        }
        result = self.invoke(
            self.table_name,
            "selectPage",
            data,
            self.businessId
        )
        return Result(result, context={"method_name": sys._getframe().f_code.co_name})
    
    @logger.catch
    def selectAll(self, fields: List[str] = [], query: Dict[str, Any] = {}) -> Result:
        """
        查询所有
        Args:
            fields: 显示字段
            query: 查询条件
        Returns:
            Result: 查询结果
        """
        query_str = " and ".join([f"{k} = '{v}'" for k, v in query.items()])
        data = {
            "query": query_str,
            "shows": fields
        }
        result = self.invoke(
            self.table_name,
            "selectAll",
            data,
            self.businessId
        )
        return Result(result, context={"method_name": sys._getframe().f_code.co_name})
    
    @logger.catch
    def deleteByIds(self, ids: List[str]) -> Result:
        """
        根据id删除
        Args:
            ids: 要删除的id列表
        Returns:
            Result: 删除结果
        """
        data = ids
        result = self.invoke(
            self.table_name,
            "deleteByIds",
            data,
            self.businessId
        )
        return Result(result, context={"method_name": sys._getframe().f_code.co_name})
    
    @logger.catch
    def delete(self, fields: List[str] = [], query: Dict[str, Any] = {}) -> Result:
        """
        根据条件删除
        Args:
            fields: 显示字段
            query: 查询条件
        Returns:
            Result: 删除结果
        """
        query_str = " and ".join([f"{k} = '{v}'" for k, v in query.items()])
        data = {
            "query": query_str,
            "shows": fields
        }
        result = self.invoke(
            self.table_name,
            "delete",
            data,
            self.businessId
        )
        return Result(result, context={"method_name": sys._getframe().f_code.co_name})
    
    @logger.catch
    def updateMany(self, data: List[Dict[str, Any]]) -> Result:
        """
        批量更新
        Args:
            data: 更新数据
        Returns:
            Result: 更新结果
        """
        result = self.invoke(
            self.table_name,
            "updateMany",
            data,
            self.businessId
        )
        return Result(result, context={"method_name": sys._getframe().f_code.co_name})
    
    @logger.catch
    def insertMany(self, data: List[Dict[str, Any]]) -> Result:
        """
        批量插入
        Args:
            data: 插入数据
        Returns:
            Result: 插入结果
        """
        result = self.invoke(
            self.table_name,
            "insertMany",
            data,
            self.businessId
        )
        return Result(result, context={"method_name": sys._getframe().f_code.co_name})
    
    @logger.catch
    def insertOrUpdate(self, data: Dict[str, Any]) -> Result:
        """
        插入或更新
        Args:
            data: 插入或更新数据
        Returns:
            Result: 插入或更新结果
        """
        result = self.invoke(
            self.table_name,
            "insertOrUpdate",
            data,
            self.businessId
        )
        return Result(result, context={"method_name": sys._getframe().f_code.co_name})
    
    @logger.catch
    def insertOne(self, data: Dict[str, Any]) -> Result:
        """
        插入一条数据
        Args:
            data: 插入数据
        Returns:
            Result: 插入结果
        """
        result = self.invoke(
            self.table_name,
            "insertOne",
            data,
            self.businessId
        )
        return Result(result, context={"method_name": sys._getframe().f_code.co_name})

    @logger.catch
    def getEnum(self, enum_name: str) -> Result:
        """
        获取枚举
        Args:
            enum_name: 枚举名称
        Returns:
            Result: 枚举结果
        """
        result = self.invoke_enum(
            enum_name,
            self.businessId
        )
        return Result(result, context={"method_name": sys._getframe().f_code.co_name})
