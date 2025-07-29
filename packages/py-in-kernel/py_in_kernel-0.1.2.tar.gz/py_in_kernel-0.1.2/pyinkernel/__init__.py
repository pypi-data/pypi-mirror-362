"""Основной пакет py-in-kernel"""
from .compiler import KernelCompiler
from .builder import KernelBuilder
from .docgen import DocumentationGenerator

__version__ = "0.1.2"
__all__ = ['KernelCompiler', 'KernelBuilder', 'DocumentationGenerator']