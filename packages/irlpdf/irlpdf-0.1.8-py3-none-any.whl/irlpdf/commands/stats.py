from PyPDF2 import PdfReader
from pathlib import Path
import os
import typer

def get_stats(input_path: str) -> dict:
	path = Path(input_path)

	if not path.exists():
		typer.echo(f"File '{input_path}' does not exist.")
		return
	if not input_path.endswith('.pdf'):
		typer.echo("Input file must be a PDF.")
		return
	if not path.is_file():
		typer.echo(f"'{input_path}' is not a valid file.")
		return

	try:
		reader = PdfReader(input_path)
		num_pages = len(reader.pages)
		is_encrypted = reader.is_encrypted
		file_size_mb = os.path.getsize(input_path) / (1024 * 1024)

		metadata = reader.metadata or {}
		if not metadata:
			metadata = "No metadata available"
		else:
			metadata = {str(k).strip().replace('\\', '').replace('/', ''): v for k, v in metadata.items() if v}

		return {
			"file_path": input_path,
			"num_pages": num_pages,
			"is_encrypted": is_encrypted,
			"file_size_mb": round(file_size_mb, 2),
			"metadata": metadata
		}
	except Exception as e:
		typer.echo(f"An error occurred while reading the PDF: {e}")
		return

def print_stats(stats: dict):
	if not stats:
		typer.echo("No stats to display.")
		return

	typer.echo("\nPDF Statistics")
	typer.echo("-" * 40)
	typer.echo(f"File Path    : {stats['file_path']}")
	typer.echo(f"Page Count   : {stats['num_pages']}")
	typer.echo(f"Encrypted    : {'Yes' if stats['is_encrypted'] else 'No'}")
	typer.echo(f"File Size    : {stats['file_size_mb']} MB")

	metadata = stats.get("metadata", {})
	if metadata and isinstance(metadata, dict):
		typer.echo("\nMetadata:")
		for key, value in metadata.items():
			typer.echo(f"   {key:15}: {value}")
	else:
		typer.echo("\nMetadata: No metadata available")

	typer.echo("-" * 40)

def stats_parser(file: str):
	stats_data = get_stats(file)
	if stats_data:
		print_stats(stats_data)
	else:
		typer.echo("No Data found")
