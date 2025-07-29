from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py-in-kernel",
    version="0.1.2",
    author="Korti",
    author_email="your.email@example.com",
    description="Python to OS kernel transpiler and builder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/py-in-kernel",
    packages=find_packages(),
    install_requires=[
        'click>=8.0',
        'pycparser>=2.21',
    ],
    package_data={
        'pyinkernel': ['templates/*.html'],
    },
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Compilers",
        "Topic :: System :: Operating System Kernels",
    ],
    entry_points={
        'console_scripts': [
            'pyinkernel=pyinkernel.cli:main',
        ],
    },
)