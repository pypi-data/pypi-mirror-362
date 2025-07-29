import click
from pathlib import Path
from .docgen import DocumentationGenerator

@click.group()
def cli():
    pass

@cli.command()
@click.option("--name", required=True, help="Имя проекта")
@click.option("--format", default="html", help="Формат документации")
def docs(name, format):
    """Генерирует документацию"""
    doc_gen = DocumentationGenerator(name)
    doc_gen.generate(
        source_dir=Path("kernel"),
        output_format=format
    )
    click.echo(f"Документация сгенерирована в docx/")