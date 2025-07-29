import inspect
from typing import Any, Callable, Dict, Optional, TypeVar, Union, List
from pydantic import Field, BaseModel
import rs_fused_lib.api.udf_api as udf_api
import os
T = TypeVar('T')

class AttrDict(dict):
    """Dictionary where keys can also be accessed as attributes"""
    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            if __name in self:
                return self[__name]
            else:
                raise

    def __dir__(self) -> List[str]:
        return list(self.keys())

class UDF(BaseModel):
    """
    UDF基类，用于表示UDF函数
    """
    id: Optional[str] = Field(None, description="UDF ID")
    name: Optional[str] = Field(None, description="函数名")
    description: Optional[str] = Field(None, description="函数描述")
    func: Optional[Callable|None] = Field(None, description="函数")
    parameters: Optional[List[Dict[str, Any]]] = Field(None, description="函数参数")
    return_type: Optional[str] = Field(None, description="返回值类型")
    code: Optional[str] = Field(..., description="函数代码")
    code_path: Optional[str] = Field(None, description="函数代码路径")
    metadata_path: Optional[str] = Field(None, description="元数据路径")   
    author: Optional[str] = Field(None, description="作者")
    version: Optional[str] = Field(None, description="版本")
    created_at: Optional[str] = Field(None, description="创建时间")
    storage_path: Optional[str] = Field(None, description="存储路径")
    storage_type: Optional[str] = Field("temporary_file", description="存储类型")
    util_code: Optional[str] = Field(None, description="工具代码")
    util_code_path: Optional[str] = Field(None, description="工具代码路径")
    execute_step: Optional[list[dict]] = Field(default_factory=list, description="待执行步骤")
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
        
    def __str__(self):
        return f"UDF(name='{self.name}', description='{self.description}')"
        
    def __repr__(self):
        return self.__str__()
    
    def run(self, x:int = None, y:int = None, z:int = None, **kwargs):
        return udf_api.run_udf_instance_server(self, x, y, z, **kwargs)

    def to_fused(
        self,
        overwrite: bool | None = None,
    ) -> 'UDF':
        import ast
        code_blocks = []  # 收集依赖代码
        inserted_udf_ids = set()  # 防止重复插入

        class RSFusedRunTransformer(ast.NodeTransformer):
            def visit_Call(self, node):
                if (isinstance(node.func, ast.Attribute) and
                    isinstance(node.func.value, ast.Name) and
                    node.func.value.id == "rs_fused_lib" and
                    node.func.attr == "run"):
                    code_str, dep_code, udf_id = call_server_to_translate(node)
                    if udf_id not in inserted_udf_ids:
                        code_blocks.append(dep_code)
                        inserted_udf_ids.add(udf_id)
                    return ast.parse(code_str).body[0].value
                return self.generic_visit(node)

        class UtilsImportTransformer(ast.NodeTransformer):
            def __init__(self, code_blocks, util_code):
                self.code_blocks = code_blocks
                self.util_code = util_code
                
            def visit_ImportFrom(self, node):
                # 处理 from utils import 语句
                if (isinstance(node.module, ast.Name) and 
                    node.module.id == "utils" and 
                    self.util_code):
                    # 将 utils 代码添加到依赖代码块中
                    if self.util_code not in self.code_blocks:
                        self.code_blocks.append(self.util_code.strip())
                    # 返回 None 来删除这个 import 语句
                    return None
                return self.generic_visit(node)

        def call_server_to_translate(node):
            args = [ast.literal_eval(arg) for arg in node.args]
            kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in node.keywords}
            udf_obj = udf_api.load_udf(args[0])
            dep_code = ""
            if udf_obj.util_code:
                dep_code += udf_obj.util_code.strip() + "\n"
            if udf_obj.code:
                dep_code += udf_obj.code.strip() + "\n"
            param_str = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.get('parameters', {}).items())
            call_code = f"{udf_obj.name}({param_str})"
            return call_code, dep_code, udf_obj.id

        # 1. 语法检查
        try:
            tree = ast.parse(self.code)
        except SyntaxError as e:
            raise Exception(f"UDF代码语法错误: {e}")

        # 2. 处理 utils import
        if self.util_code:
            utils_transformer = UtilsImportTransformer(code_blocks, self.util_code)
            tree = utils_transformer.visit(tree)
            ast.fix_missing_locations(tree)

        # 3. AST 替换 rs_fused_lib.run 调用
        new_tree = RSFusedRunTransformer().visit(tree)
        ast.fix_missing_locations(new_tree)
        try:
            new_code = ast.unparse(new_tree)
        except Exception:
            import astor
            new_code = astor.to_source(new_tree)

        # 4. 拼接依赖代码和主代码
        full_code = "\n".join(code_blocks) + "\n" + new_code
        self.code = full_code

        # 5. 再次语法检查
        try:
            ast.parse(self.code)
        except SyntaxError as e:
            raise Exception(f"UDF代码替换后语法错误: {e}")

        # 6. 保存
        func = self.func
        self.func = None
        try:
            saveResult = udf_api.save_udf(self.model_dump())
        finally:
            self.func = func
        return saveResult
    
    @property
    def utils(self):
        if self.util_code is None:
            return None 
        import ast
        import types
        from dataclasses import dataclass

        def safe_get_type_name(node):
            if node is None:
                return 'Any'
            try:
                if isinstance(node, ast.Name):
                    return node.id
                elif isinstance(node, ast.Attribute):
                    value_name = safe_get_type_name(node.value)
                    return f"{value_name}.{node.attr}"
                elif isinstance(node, ast.Constant):
                    return str(node.value)
                elif isinstance(node, ast.Subscript):
                    value_name = safe_get_type_name(node.value)
                    slice_node = node.slice
                    if hasattr(slice_node, 'value'):
                        slice_name = safe_get_type_name(slice_node.value)
                    elif isinstance(slice_node, (ast.Tuple, ast.List)):
                        slice_name = ', '.join([safe_get_type_name(elt) for elt in slice_node.elts])
                    else:
                        slice_name = safe_get_type_name(slice_node)
                    return f"{value_name}[{slice_name}]"
                elif isinstance(node, ast.Tuple):
                    return ', '.join([safe_get_type_name(elt) for elt in node.elts])
                elif isinstance(node, ast.List):
                    return ', '.join([safe_get_type_name(elt) for elt in node.elts])
                else:
                    return 'Any'
            except Exception:
                return 'Any'

        @dataclass
        class PendingFunction:
            name: str
            args: list
            return_type: str
            code: str
            udf: 'UDF'

            def __call__(self, *args, **kwargs):
                step = {
                    'function': self.name,
                    'args': args,
                    'kwargs': kwargs,
                    'arg_types': dict(self.args),
                    'return_type': self.return_type,
                    'code': self.code,
                    'status': 'pending'
                }
                self.udf.execute_step.append(step)
                return self.udf

        utils_module = types.ModuleType('utils')

        tree = ast.parse(self.util_code.strip())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = self.util_code.strip().splitlines()
                func_code = '\n'.join(lines[node.lineno-1:node.end_lineno])
                # 确保函数代码可解析
                try:
                    import textwrap
                    func_code = textwrap.dedent(func_code)
                    func_ast = ast.parse(func_code)
                except SyntaxError as e:
                    print(f"警告: 跳过解析错误的函数: {e}")
                    continue
                func_def = func_ast.body[0]

                args = []
                for arg in func_def.args.args:
                    arg_name = arg.arg
                    arg_type = safe_get_type_name(arg.annotation)
                    args.append((arg_name, arg_type))

                return_type = safe_get_type_name(func_def.returns)

                pending_func = PendingFunction(
                    name=func_def.name,
                    args=args,
                    return_type=return_type,
                    code=func_code,
                    udf=self
                )

                setattr(utils_module, func_def.name, pending_func)

        return utils_module
        
def udf(func: T = None) -> Union[Callable[[T], UDF], UDF]:
    if func is None:
        return udf
        
    # 获取函数定义的模块
    module = inspect.getmodule(func)
    if module is None or module.__name__ == '__main__':
        # 如果是__main__模块，尝试从函数对象获取全局变量
        module = func.__globals__
    
    # 获取源文件路径
    if isinstance(module, dict):
        file_path = module.get('__file__')
    else:
        file_path = getattr(module, '__file__', None)
    
    # 尝试加载对应的 _utils 文件
    util_code = None
    if file_path:
        # 构建 _utils 文件路径
        file_dir = os.path.dirname(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        utils_file_path = os.path.join(file_dir, f"{file_name}_utils.py")
        
        # 如果 _utils 文件存在，读取其内容
        if os.path.exists(utils_file_path):
            try:
                with open(utils_file_path, 'r', encoding='utf-8') as f:
                    util_code = f.read()
            except Exception as e:
                print(f"Warning: Failed to read utils file {utils_file_path}: {e}")
    
    # 获取所有引用的函数
    referenced_funcs = []  # 使用列表来保持顺序
    processed_funcs = set()  # 用于记录已处理的函数，避免循环引用
    
    if file_path:
        # 读取源文件内容
        with open(file_path, 'r') as f:
            file_content = f.read()
            
        # 使用ast解析源文件
        import ast
        tree = ast.parse(file_content)
        
        def collect_referenced_functions(func_node):
            """递归收集函数引用的其他函数"""
            if func_node.name in processed_funcs:
                return
            processed_funcs.add(func_node.name)
            
            # 收集当前函数中引用的所有名称
            referenced_names = set()
            for node in ast.walk(func_node):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    referenced_names.add(node.id)
            
            # 查找这些名称对应的函数定义
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name in referenced_names and not node.name == func_node.name:
                        # 获取函数源代码
                        start_line = node.lineno
                        end_line = node.end_lineno
                        lines = file_content.splitlines()
                        func_source = '\n'.join(lines[start_line-1:end_line])
                        if func_source and not func_source.strip().startswith('@udf'):
                            # 递归收集这个函数引用的其他函数
                            collect_referenced_functions(node)
                            # 添加当前函数的源代码
                            referenced_funcs.append(func_source)
        
        # 获取当前函数的AST节点
        current_func_node = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func.__name__:
                current_func_node = node
                break
                
        if current_func_node:
            # 收集所有被引用的函数
            collect_referenced_functions(current_func_node)
            
            # 获取当前函数的源代码（不包括装饰器）
            start_line = current_func_node.lineno
            end_line = current_func_node.end_lineno
            lines = file_content.splitlines()
            # 跳过装饰器行
            while lines[start_line-1].strip().startswith('@'):
                start_line += 1
            main_func_source = '\n'.join(lines[start_line-1:end_line])
            referenced_funcs.append(main_func_source)
    
    # 使用被引用的函数代码，确保依赖函数在前
    full_code = '\n'.join(referenced_funcs)
        
    udf_instance = UDF(
        func=func,
        name=func.__name__,
        description=func.__doc__,
        parameters= [{"name": k, "type": str(v), "description": func.__annotations__[k].__doc__} for k, v in func.__annotations__.items() if k != 'return'],
        return_type=str(func.__annotations__['return']) if 'return' in func.__annotations__ else None,
        code=full_code,
        author=func.__author__ if hasattr(func, '__author__') else None,
        version=func.__version__ if hasattr(func, '__version__') else None,
        util_code=util_code  # 添加 util_code
    )
    return udf_instance

