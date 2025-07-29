import unittest
from pyinkernel.compiler import KernelCompiler

class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.compiler = KernelCompiler()

    def test_simple_function(self):
        code = """
@kernel_function
def test(a: int, b: str) -> bool:
    \"\"\"Тестовая функция\"\"\"
    return True
"""
        c_code = self.compiler.compile(code)
        self.assertIn("int32_t a", c_code)
        self.assertIn("char* b", c_code)
        self.assertIn("// Тестовая функция", c_code)

if __name__ == "__main__":
    unittest.main()