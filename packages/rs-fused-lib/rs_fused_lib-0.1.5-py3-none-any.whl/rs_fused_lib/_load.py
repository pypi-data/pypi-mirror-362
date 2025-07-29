# load 文件夹代码
from typing import Any, Union
from pathlib import Path
from rs_fused_lib.core.udf import UDF
from rs_fused_lib.api.udf_api import load_udf
def load(url_or_udf: Union[str, Path], /, *, cache_key: Any = None) -> UDF:
    if isinstance(url_or_udf, str):
        return load_udf(url_or_udf)
    else:
        raise ValueError(f"Invalid input type: {type(url_or_udf)}")