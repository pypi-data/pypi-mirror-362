import ast
from typing import Dict, List

class KernelCompiler:
    """Транспилятор Python-кода ядра в оптимизированный C-код"""
    
    def __init__(self, arch: str = 'x86_64'):
        self.arch = arch
        self._type_map = {
            'int': 'int32_t',
            'str': 'char*',
            'bool': 'uint8_t'
        }
    
    def compile(self, py_source: str) -> str:
        """Основной метод компиляции"""
        tree = ast.parse(py_source)
        
        # 1. Анализ AST Python
        kernel_functions = self._find_kernel_functions(tree)
        
        # 2. Генерация C-кода
        c_code = [
            '#include <kernel.h>',
            '// Auto-generated from Python',
            ''
        ]
        
        for func in kernel_functions:
            c_code.append(self._compile_function(func))
        
        return '\n'.join(c_code)
    
    def _find_kernel_functions(self, node: ast.AST) -> List[ast.FunctionDef]:
        """Находит все функции с декораторами ядра"""
        kernel_funcs = []
        
        for item in ast.walk(node):
            if isinstance(item, ast.FunctionDef):
                for decorator in item.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == 'kernel_function':
                        kernel_funcs.append(item)
        
        return kernel_funcs
    
    def _compile_function(self, func: ast.FunctionDef) -> str:
        """Транслирует одну функцию"""
        c_params = []
        for arg in func.args.args:
            py_type = arg.annotation.id if arg.annotation else 'void'
            c_params.append(f"{self._type_map.get(py_type, 'void*')} {arg.arg}")
        
        c_body = []
        for node in func.body:
            c_body.append(self._compile_statement(node))
        
        return (
            f"void {func.name}({', '.join(c_params)}) {{\n"
            f"    {''.join(c_body)}\n"
            "}"
        )