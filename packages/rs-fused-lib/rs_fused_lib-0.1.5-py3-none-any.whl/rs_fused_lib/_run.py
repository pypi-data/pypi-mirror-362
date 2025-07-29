import sys
import inspect
from typing import Any, Callable, Dict, Optional, Union
import rs_fused_lib.api.udf_api as udf_api

from rs_fused_lib.core import udf
from rs_fused_lib.core.udf import UDF

ResultType = Union["xr.Dataset", "pd.DataFrame", "gpd.GeoDataFrame"]

def run(
    udf: Union[str, Callable, UDF] = None,
    parameters: Optional[Dict[str, Any]] = None,
    x: Optional[int] = None,
    y: Optional[int] = None,
    z: Optional[int] = None
) -> ResultType:
    if isinstance(udf, str):
        result = udf_api.run_udf(udf, x, y, z, parameters)
    elif isinstance(udf, UDF):
        result = udf_api.run_udf_instance_server(udf, x, y, z, parameters)
    return result