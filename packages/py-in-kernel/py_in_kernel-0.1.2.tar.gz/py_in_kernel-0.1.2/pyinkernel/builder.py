import subprocess
from pathlib import Path

class KernelBuilder:
    """Собирает ядро из транспилированного кода"""
    
    def __init__(self, project_name: str):
        self.project = project_name
        self.build_dir = Path(f"build/{project_name}")
        self.dist_dir = Path("dist")
        
        self.build_dir.mkdir(parents=True, exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
    
    def build_from_py(self, py_path: str, output: str):
        """Полный цикл сборки из Python-файла"""
        # 1. Транспиляция
        with open(py_path) as f:
            py_code = f.read()
        
        c_code = KernelCompiler().compile(py_code)
        
        # 2. Сохранение промежуточного C-кода
        c_path = self.build_dir / "kernel.c"
        with open(c_path, 'w') as f:
            f.write(c_code)
        
        # 3. Компиляция в объектный файл
        obj_path = self.build_dir / "kernel.o"
        subprocess.run([
            "gcc", 
            "-c", str(c_path),
            "-o", str(obj_path),
            "-ffreestanding",
            "-O2"
        ], check=True)
        
        # 4. Линковка
        subprocess.run([
            "ld",
            "-T", "linker.ld",
            "-o", str(self.dist_dir / output),
            str(obj_path),
            "-nostdlib"
        ], check=True)