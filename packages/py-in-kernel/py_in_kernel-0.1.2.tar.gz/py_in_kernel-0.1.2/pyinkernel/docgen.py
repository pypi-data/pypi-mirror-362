"""
Генератор документации для py-in-kernel
"""

import ast
from pathlib import Path
from dataclasses import dataclass

@dataclass
class FunctionDoc:
    name: str
    desc: str
    params: list
    returns: str

class DocumentationGenerator:
    def __init__(self, project_name: str):
        self.project = project_name
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .function {{ margin-bottom: 2em; border-bottom: 1px solid #eee; padding-bottom: 1em; }}
        .param {{ color: #0066cc; font-weight: bold; }}
        .returns {{ color: #009933; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {content}
</body>
</html>
        """

    def generate(self, source_dir: Path, output_format: str = "html"):
        """Основной метод генерации"""
        docs = []
        
        for py_file in source_dir.glob("**/*.py"):
            with open(py_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    docs.append(self._parse_function(node))
        
        if output_format == "html":
            self._to_html(docs)

    def _parse_function(self, func_node) -> FunctionDoc:
        """Разбирает функцию в структурированные данные"""
        return FunctionDoc(
            name=func_node.name,
            desc=ast.get_docstring(func_node) or "No description",
            params=[
                f"{arg.arg}: {self._get_type(arg.annotation)}"
                for arg in func_node.args.args
            ],
            returns=self._get_type(func_node.returns)
        )

    def _get_type(self, annotation) -> str:
        """Извлекает информацию о типах"""
        if not annotation:
            return "any"
        if isinstance(annotation, ast.Name):
            return annotation.id
        return "unknown"

    def _to_html(self, functions: list[FunctionDoc]):
        """Генерирует HTML-документ"""
        content = []
        for func in functions:
            content.append(f"""
            <div class="function">
                <h2>{func.name}</h2>
                <p>{func.desc}</p>
                <h3>Parameters</h3>
                <ul>
                    {''.join(f'<li><span class="param">{p}</span></li>' for p in func.params)}
                </ul>
                <h3>Returns</h3>
                <p class="returns">{func.returns}</p>
            </div>
            """)
        
        html = self.template.format(
            title=f"{self.project} API Reference",
            content='\n'.join(content)
        )
        
        (Path("docx") / "api.html").write_text(html, encoding='utf-8')