import requests
from rs_fused_lib.core.udf import UDF
from rs_fused_lib.common.serializers import UniversalSerializer
from rs_fused_lib.common.customJsonEncoder import safe_model_dump, deep_serialize
from rs_fused_lib.config import get_base_url

def save_udf(
    udf: dict,
):
    url = f"{get_base_url()}/save_udf"
    response = requests.post(
        url,
        json=udf
    )
    if response.status_code != 200:
        raise Exception(f"Failed to save UDF: {response.json()}")
    return UDF(**response.json())

def run_udf(
    udf_id: str,
    x: int,
    y: int,
    z: int,
    parameters: dict,
): 
    url = f"{get_base_url()}/run_udf/{udf_id}"
    response = requests.post(url, json={"x": x, "y": y, "z": z, "kwargs": parameters})
    if response.status_code != 200:
        raise Exception(f"Failed to run UDF: {response.json()}")
    resContent = response.json()
    if resContent['result'] is not None:
        result = UniversalSerializer.deserialize(resContent['result'])
        return result
    else:
        return None

def run_udf_instance_server(
    udf_instance: UDF,
    x: int = None,
    y: int = None,
    z: int = None,
    **kwargs,
):
    url = f"{get_base_url()}/run_udf_instance"
    parameters = {}
    for k, v in kwargs.items():
        parameters[k] = UniversalSerializer.serialize(v)
    print(parameters)
    response = requests.post(url, json={"udf_instance": safe_model_dump(udf_instance), "x": x, "y": y, "z": z, "parameters": parameters})
    if response.status_code != 200:
        raise Exception(f"Failed to run UDF: {response.json()}")
    resContent = response.json()
    if resContent['result'] is not None:
        result = UniversalSerializer.deserialize(resContent['result'])
        return result
    
def load_udf(
    udf_id: str,
):
    """加载UDF函数
    
    Args:
        udf_id: UDF ID
        
    Returns:
        UDF: UDF对象，包含解析后的util_code
    """
    print(f"执行load_udf, udf_id: {udf_id}")
    url = f"{get_base_url()}/load_udf"
    print(f"执行load_udf, url: {url}")
    response = requests.post(url, json={"udf_id": udf_id})
    print(f"执行load_udf, response: {response}")
    if response.status_code != 200:
        raise Exception(f"Failed to load UDF: {response.json()}")
    
    # 获取响应数据
    data = response.json()
    
    # 创建UDF实例
    udf_instance = UDF(**data)
    
    # 解析代码中的 fused.load 调用
    udf_instance = _resolve_fused_load_calls(udf_instance)
    
    # 如果存在util_code，确保它被正确解析
    if udf_instance.util_code:
        # 触发utils属性的初始化，这将解析util_code并设置_cached_utils
        _ = udf_instance.utils

    # 主动做一次AST解析，捕获异常并写入本地文件
    import ast
    for code_label, code_str in [("code", udf_instance.code), ("util_code", udf_instance.util_code)]:
        if code_str:
            try:
                ast.parse(code_str)
            except Exception as e:
                print(f"[load_udf] 解析{code_label}时发生异常: {e}\n内容片段: {code_str[:300]}")
                # 写入本地文件
                debug_file = f"debug_{code_label}.txt"
                with open(debug_file, "w", encoding="utf-8") as f:
                    f.write(f"[load_udf] 解析{code_label}时发生异常: {e}\n\n")
                    f.write(code_str)
    
    return udf_instance

def _resolve_fused_load_calls(udf_instance: UDF) -> UDF:
    """解析UDF代码中的 fused.load 调用，将其转换为原始代码
    
    Args:
        udf_instance: UDF实例
        
    Returns:
        UDF: 解析后的UDF实例
    """
    import ast
    code_blocks = []  # 收集依赖代码
    inserted_udf_ids = set()  # 防止重复插入

    class FusedLoadTransformer(ast.NodeTransformer):
        def visit_Call(self, node):
            # 处理 rs_fused_lib.load 调用
            if (isinstance(node.func, ast.Attribute) and
                isinstance(node.func.value, ast.Name) and
                node.func.value.id == "rs_fused_lib" and
                node.func.attr == "load"):
                code_str, dep_code, udf_id = call_load_to_translate(node)
                if udf_id not in inserted_udf_ids:
                    code_blocks.append(dep_code)
                    inserted_udf_ids.add(udf_id)
                return ast.parse(code_str).body[0].value
            
            # 处理 fused.load 调用
            elif (isinstance(node.func, ast.Attribute) and
                  isinstance(node.func.value, ast.Name) and
                  node.func.value.id == "fused" and
                  node.func.attr == "load"):
                code_str, dep_code, udf_id = call_load_to_translate(node)
                if udf_id not in inserted_udf_ids:
                    code_blocks.append(dep_code)
                    inserted_udf_ids.add(udf_id)
                return ast.parse(code_str).body[0].value
                
            return self.generic_visit(node)

    def call_load_to_translate(node):
        """将 fused.load 调用转换为原始代码"""
        args = [ast.literal_eval(arg) for arg in node.args]
        # 直接调用服务器API，避免递归调用load_udf
        url = f"{get_base_url()}/load_udf"
        response = requests.post(url, json={"udf_id": args[0]})
        if response.status_code != 200:
            raise Exception(f"Failed to load UDF: {response.json()}")
        
        data = response.json()
        udf_obj = UDF(**data)
        
        dep_code = ""
        if udf_obj.util_code:
            dep_code += udf_obj.util_code.strip() + "\n"
        if udf_obj.code:
            dep_code += udf_obj.code.strip() + "\n"
        # 返回函数调用代码
        call_code = f"{udf_obj.name}()"
        return call_code, dep_code, udf_obj.id

    # 解析主代码
    if udf_instance.code:
        try:
            tree = ast.parse(udf_instance.code)
            new_tree = FusedLoadTransformer().visit(tree)
            ast.fix_missing_locations(new_tree)
            try:
                new_code = ast.unparse(new_tree)
            except Exception:
                import astor
                new_code = astor.to_source(new_tree)
            
            # 拼接依赖代码和主代码
            full_code = "\n".join(code_blocks) + "\n" + new_code
            udf_instance.code = full_code
            
            # 再次语法检查
            try:
                ast.parse(udf_instance.code)
            except SyntaxError as e:
                raise Exception(f"UDF主代码解析后语法错误: {e}")
        except SyntaxError as e:
            raise Exception(f"UDF主代码语法错误: {e}")

    # 解析 utils 代码（使用新的代码块集合）
    if udf_instance.util_code:
        util_code_blocks = []  # 为 utils 代码创建独立的代码块集合
        util_inserted_udf_ids = set()  # 为 utils 代码创建独立的ID集合
        
        class UtilsFusedLoadTransformer(ast.NodeTransformer):
            def visit_Call(self, node):
                # 处理 rs_fused_lib.load 调用
                if (isinstance(node.func, ast.Attribute) and
                    isinstance(node.func.value, ast.Name) and
                    node.func.value.id == "rs_fused_lib" and
                    node.func.attr == "load"):
                    code_str, dep_code, udf_id = call_load_to_translate(node)
                    if udf_id not in util_inserted_udf_ids:
                        util_code_blocks.append(dep_code)
                        util_inserted_udf_ids.add(udf_id)
                    return ast.parse(code_str).body[0].value
                
                # 处理 fused.load 调用
                elif (isinstance(node.func, ast.Attribute) and
                      isinstance(node.func.value, ast.Name) and
                      node.func.value.id == "fused" and
                      node.func.attr == "load"):
                    code_str, dep_code, udf_id = call_load_to_translate(node)
                    if udf_id not in util_inserted_udf_ids:
                        util_code_blocks.append(dep_code)
                        util_inserted_udf_ids.add(udf_id)
                    return ast.parse(code_str).body[0].value
                    
                return self.generic_visit(node)
        
        try:
            tree = ast.parse(udf_instance.util_code)
            new_tree = UtilsFusedLoadTransformer().visit(tree)
            ast.fix_missing_locations(new_tree)
            try:
                new_util_code = ast.unparse(new_tree)
            except Exception:
                import astor
                new_util_code = astor.to_source(new_tree)
            
            # 拼接依赖代码和 utils 代码
            full_util_code = "\n".join(util_code_blocks) + "\n" + new_util_code
            udf_instance.util_code = full_util_code
            
            # 再次语法检查
            try:
                ast.parse(udf_instance.util_code)
            except SyntaxError as e:
                raise Exception(f"UDF utils代码解析后语法错误: {e}")
        except SyntaxError as e:
            raise Exception(f"UDF utils代码语法错误: {e}")

    return udf_instance
