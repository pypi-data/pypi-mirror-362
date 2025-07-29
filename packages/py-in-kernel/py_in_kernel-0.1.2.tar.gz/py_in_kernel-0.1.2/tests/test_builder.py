import unittest
import subprocess
from unittest.mock import patch, MagicMock
from pathlib import Path
from pyinkernel.builder import KernelBuilder

class TestKernelBuilder(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_build")
        self.test_dir.mkdir(exist_ok=True)
        (self.test_dir / "test_kernel.py").write_text("""
@kernel_function
def test():
    pass
""")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    @patch('subprocess.run')
    def test_build_process(self, mock_run):
        """Тест полного процесса сборки"""
        # Настройка mock-объектов
        mock_run.return_value = MagicMock(returncode=0)

        builder = KernelBuilder("test_kernel")
        builder.build_dir = self.test_dir
        
        # Тестируем
        builder.build_from_py(
            str(self.test_dir / "test_kernel.py"),
            "test_kernel.bin"
        )

        # Проверяем вызовы
        self.assertEqual(mock_run.call_count, 2)
        
        # Проверяем аргументы gcc
        gcc_call = mock_run.call_args_list[0].args[0]
        self.assertIn("gcc", gcc_call)
        self.assertIn("-ffreestanding", gcc_call)
        
        # Проверяем аргументы ld
        ld_call = mock_run.call_args_list[1].args[0]
        self.assertIn("ld", ld_call)
        self.assertIn("-nostdlib", ld_call)

    def test_directory_creation(self):
        """Тест автоматического создания директорий"""
        builder = KernelBuilder("test_kernel")
        self.assertTrue(builder.build_dir.exists())
        self.assertTrue(builder.dist_dir.exists())

    @patch('subprocess.run')
    def test_failed_compilation(self, mock_run):
        """Тест обработки ошибок компиляции"""
        mock_run.return_value = MagicMock(returncode=1)

        builder = KernelBuilder("test_kernel")
        with self.assertRaises(RuntimeError):
            builder.build_from_py(
                str(self.test_dir / "test_kernel.py"),
                "test_kernel.bin"
            )

if __name__ == "__main__":
    unittest.main()