import json
import base64
import pickle
import numpy as np
import pandas as pd
import geopandas as gpd
from typing import Union, Dict, Any
from rs_fused_lib.common.logger import logger
import io

class DataFrameSerializer:
    
    @staticmethod
    def to_json(df: Any) -> Dict[str, Any]:
        """
        将DataFrame或GeoDataFrame转换为JSON格式
        
        Args:
            df: pandas DataFrame或GeoDataFrame对象
            
        Returns:
            Dict: 包含序列化数据的字典
        """
        try:
            # 将DataFrame转换为JSON字符串
            if isinstance(df, gpd.GeoDataFrame):
                return {
                    'type': 'geodataframe',
                    'data': json.loads(df.to_json())
                }
            elif isinstance(df, pd.DataFrame):
                return {
                    'type': 'dataframe',
                    'data': json.loads(df.to_json())
                }
            elif isinstance(df, np.ndarray):
                return {
                    'type': 'ndarray',
                    'data': df.tolist()
                }
            else:
                return {
                    'type': 'object',
                    'data': df
                }
            
        except Exception as e:
            logger.error(f"序列化DataFrame失败: {str(e)}")
            raise
    
    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        """
        从JSON格式恢复DataFrame或GeoDataFrame
        
        Args:
            json_data: 包含序列化数据的字典
            
        Returns:
            DataFrame或GeoDataFrame对象
        """
        try:
            data_type = json_data.get('type')
            data = json_data.get('data', [])
            
            # 如果是GeoDataFrame，添加几何信息
            if data_type == 'geodataframe':
                return gpd.GeoDataFrame.from_features(data.get('features'))
            elif data_type == 'dataframe':
                return pd.DataFrame.from_dict(data)
            elif data_type == 'ndarray':
                return np.array(data)
            elif data_type == 'object':
                return data
            else:
                raise ValueError(f"不支持的类型: {data_type}")
            
        except Exception as e:
            logger.error(f"反序列化DataFrame失败: {str(e)}")
            raise
        
        
    @staticmethod
    def to_parquet_base64(df: Union[pd.DataFrame, gpd.GeoDataFrame]) -> str:
        """
        将DataFrame或GeoDataFrame转换为Base64编码的Parquet格式
        
        Args:
            df: pandas DataFrame或GeoDataFrame对象
            
        Returns:
            str: Base64编码的Parquet数据
        """
        try:
            buffer = io.BytesIO()
            df.to_parquet(buffer)
            buffer.seek(0)
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
        except Exception as e:
            logger.error(f"转换为Parquet格式失败: {str(e)}")
            raise
    
    @staticmethod
    def from_parquet_base64(base64_str: str) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        """
        从Base64编码的Parquet格式恢复DataFrame或GeoDataFrame
        
        Args:
            base64_str: Base64编码的Parquet数据
            
        Returns:
            DataFrame或GeoDataFrame对象
        """
        try:
            buffer = io.BytesIO(base64.b64decode(base64_str))
            return pd.read_parquet(buffer)
        except Exception as e:
            logger.error(f"从Parquet格式恢复失败: {str(e)}")
            raise
    
    @staticmethod
    def to_csv_base64(df: Union[pd.DataFrame, gpd.GeoDataFrame]) -> str:
        """
        将DataFrame或GeoDataFrame转换为Base64编码的CSV格式
        
        Args:
            df: pandas DataFrame或GeoDataFrame对象
            
        Returns:
            str: Base64编码的CSV数据
        """
        try:
            buffer = io.StringIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            return base64.b64encode(buffer.getvalue().encode('utf-8')).decode('utf-8')
        except Exception as e:
            logger.error(f"转换为CSV格式失败: {str(e)}")
            raise
    
    @staticmethod
    def from_csv_base64(base64_str: str) -> pd.DataFrame:
        """
        从Base64编码的CSV格式恢复DataFrame
        
        Args:
            base64_str: Base64编码的CSV数据
            
        Returns:
            DataFrame对象
        """
        try:
            buffer = io.StringIO(base64.b64decode(base64_str).decode('utf-8'))
            return pd.read_csv(buffer)
        except Exception as e:
            logger.error(f"从CSV格式恢复失败: {str(e)}")
            raise 

class UniversalSerializer:
    @staticmethod
    def serialize(obj):
        import numpy as np
        import base64
        import pickle

        # numpy array
        if isinstance(obj, np.ndarray):
            return {
                "__type__": "ndarray",
                "dtype": str(obj.dtype),
                "shape": obj.shape,
                "data": base64.b64encode(obj.tobytes()).decode("utf-8")
            }
        # pandas DataFrame
        elif isinstance(obj, pd.DataFrame) and not isinstance(obj, gpd.GeoDataFrame):
            return {
                "__type__": "dataframe",
                "data": obj.to_dict(orient="split")
            }
        # geopandas GeoDataFrame
        elif isinstance(obj, gpd.GeoDataFrame):
            # geometry转为WKT字符串
            df = obj.copy()
            df["geometry"] = df["geometry"].apply(lambda g: g.wkt if g is not None else None)
            return {
                "__type__": "geodataframe",
                "data": df.to_dict(orient="split"),
                "crs": str(obj.crs) if obj.crs else None
            }
        # 基本类型
        elif isinstance(obj, (int, float, str, bool)) or obj is None:
            return obj
        # dict/list/tuple
        elif isinstance(obj, (dict, list, tuple)):
            if isinstance(obj, dict):
                return {k: UniversalSerializer.serialize(v) for k, v in obj.items()}
            else:
                return [UniversalSerializer.serialize(v) for v in obj]
        # 其他对象，使用pickle+base64
        else:
            return {
                "__type__": "pickle",
                "data": base64.b64encode(pickle.dumps(obj)).decode("utf-8")
            }

    @staticmethod
    def deserialize(obj):
        import numpy as np
        import pandas as pd
        import geopandas as gpd
        import base64
        import pickle

        if isinstance(obj, dict) and obj.get("__type__") == "ndarray":
            arr = np.frombuffer(base64.b64decode(obj["data"]), dtype=obj["dtype"])
            return arr.reshape(obj["shape"])
        elif isinstance(obj, dict) and obj.get("__type__") == "dataframe":
            return pd.DataFrame(**obj["data"])
        elif isinstance(obj, dict) and obj.get("__type__") == "geodataframe":
            df = pd.DataFrame(**obj["data"])
            if "geometry" in df.columns:
                from shapely import wkt
                df["geometry"] = df["geometry"].apply(lambda x: wkt.loads(x) if x else None)
                gdf = gpd.GeoDataFrame(df, geometry="geometry")
                if obj.get("crs"):
                    gdf.set_crs(obj["crs"], inplace=True)
                return gdf
            else:
                return df
        elif isinstance(obj, dict) and obj.get("__type__") == "pickle":
            return pickle.loads(base64.b64decode(obj["data"]))
        elif isinstance(obj, dict):
            return {k: UniversalSerializer.deserialize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [UniversalSerializer.deserialize(v) for v in obj]
        else:
            return obj

    @staticmethod
    def dumps(obj):
        """序列化为json字符串"""
        return json.dumps(UniversalSerializer.serialize(obj))

    @staticmethod
    def loads(s):
        """从json字符串反序列化"""
        return UniversalSerializer.deserialize(json.loads(s)) 