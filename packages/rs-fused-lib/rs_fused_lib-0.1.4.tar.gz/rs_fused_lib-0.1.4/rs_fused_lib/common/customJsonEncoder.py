import json
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import mapping
from types import ModuleType
from typing import Any, Dict, List, Optional, Set, Tuple, Union

class CustomJSONEncoder(json.JSONEncoder):
    """
    自定义JSON编码器，用于处理非基本类型的Python对象序列化
    """
    def default(self, obj):
        # 处理GeoDataFrame
        if isinstance(obj, gpd.GeoDataFrame):
            return {
                "_type": "GeoDataFrame",
                "data": obj.to_dict("records"),
                "crs": str(obj.crs) if hasattr(obj, 'crs') and obj.crs else None
            }
        
        # 处理DataFrame
        if isinstance(obj, pd.DataFrame):
            return {
                "_type": "DataFrame",
                "data": obj.to_dict("records")
            }
        
        # 处理Series
        if isinstance(obj, pd.Series):
            return {
                "_type": "Series",
                "data": obj.to_dict(),
                "name": obj.name
            }
            
        # 处理numpy数组
        if isinstance(obj, np.ndarray):
            return {
                "_type": "ndarray",
                "data": obj.tolist(),
                "dtype": str(obj.dtype)
            }
            
        # 处理numpy数据类型
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
            
        # 处理shapely几何对象
        if hasattr(obj, "geom_type"):
            return mapping(obj)
            
        # 处理集合类型
        if isinstance(obj, set):
            return {
                "_type": "set",
                "data": list(obj)
            }
            
        # 处理ModuleType
        if isinstance(obj, ModuleType):
            return {
                "_type": "module",
                "name": obj.__name__ if hasattr(obj, "__name__") else str(obj)
            }
            
        # 处理callable对象
        if callable(obj) and not isinstance(obj, type):
            return {
                "_type": "callable",
                "name": obj.__name__ if hasattr(obj, "__name__") else str(obj)
            }
            
        # 处理自定义对象
        if hasattr(obj, "__dict__"):
            return {
                "_type": obj.__class__.__name__,
                "data": {key: value for key, value in obj.__dict__.items() 
                        if not key.startswith("_") and not callable(value)}
            }
            
        # 让默认的JSONEncoder处理其他类型
        return super().default(obj)


def deep_serialize(obj: Any) -> Any:
    """
    深度递归序列化对象，使其可JSON序列化
    
    Args:
        obj: 任何Python对象
        
    Returns:
        可JSON序列化的对象
    """
    # 基本类型直接返回
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
        
    # 字典类型递归处理每个值
    if isinstance(obj, dict):
        return {k: deep_serialize(v) for k, v in obj.items()}
        
    # 列表或元组类型递归处理每个元素
    if isinstance(obj, (list, tuple)):
        return [deep_serialize(item) for item in obj]
        
    # 使用CustomJSONEncoder处理其他类型
    encoder = CustomJSONEncoder()
    try:
        return encoder.default(obj)
    except TypeError:
        # 如果无法序列化，返回字符串表示
        return str(obj)

def safe_model_dump(model) -> Dict[str, Any]:
    """
    安全地序列化pydantic模型，处理所有特殊类型
    
    Args:
        model: pydantic模型实例
        
    Returns:
        dict: 可JSON序列化的字典
    """
    try:
        # 先使用model_dump获取字典
        data = model.model_dump()
        # 然后对每个键值对进行深度序列化
        return {k: deep_serialize(v) for k, v in data.items()}
    except Exception as e:
        # 记录异常，并尝试备用方案
        print(f"模型序列化失败: {str(e)}")
        # 备用方案：手动构建可序列化字典
        result = {}
        for key, value in model.__dict__.items():
            if not key.startswith("_"):  # 跳过私有属性
                try:
                    result[key] = deep_serialize(value)
                except Exception:
                    result[key] = str(value)  # 实在不行用字符串表示
        return result