import ast
import unittest
from pyinkernel.docgen import DocumentationGenerator, FunctionDoc

class TestDocGen(unittest.TestCase):
    def test_parse_function(self):
        code = """
@kernel_function
def test(a: int, b: str = "hello") -> bool:
    \"\"\"Тестовая функция\"\"\"
    return True
"""
        node = ast.parse(code).body[0]
        doc = DocumentationGenerator("test")._parse_function(node)
        
        self.assertEqual(doc.name, "test")
        self.assertEqual(doc.desc, "Тестовая функция")
        self.assertEqual(doc.params, ["a: int", "b: str"])
        self.assertEqual(doc.returns, "bool")

if __name__ == "__main__":
    unittest.main()