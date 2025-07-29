# rs-fused-lib

一个用于遥感数据处理的Python库，提供UDF（用户定义函数）功能。

## 安装

```bash
pip install rs-fused-lib
```

## 使用方法

### 1. 使用UDF装饰器

```python
from rs_fused_lib import udf

@udf(
    name="ndvi_calculator",
    description="计算NDVI指数",
    parameters={
        "red_band": {"type": "int", "description": "红波段索引"},
        "nir_band": {"type": "int", "description": "近红外波段索引"}
    }
)
def calculate_ndvi(data, red_band=3, nir_band=4):
    red = data[..., red_band]
    nir = data[..., nir_band]
    return (nir - red) / (nir + red)
```

### 2. 运行UDF函数

```python
from rs_fused_lib import run

# 直接运行UDF函数
result = run(calculate_ndvi, data, red_band=3, nir_band=4)

# 或者通过函数名运行
result = run("calculate_ndvi", data, red_band=3, nir_band=4)
```

## 功能特点

- 支持UDF函数装饰器
- 支持通过函数名或函数对象运行UDF
- 支持参数传递和验证
- 支持元数据管理 