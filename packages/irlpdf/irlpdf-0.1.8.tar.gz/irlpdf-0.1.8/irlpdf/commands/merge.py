from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import typer

def merge_from_files(pdfs: list[str], output: str):
	writer = PdfWriter()
	for pdf in pdfs:
		path = Path(pdf)
		if not path.exists() or not path.suffix.lower() == ".pdf":
			typer.echo(f"Skipping invalid PDF file: {pdf}")
			continue
		reader = PdfReader(str(path))
		for page in reader.pages:
			writer.add_page(page)
	
	with open(output, "wb") as f:
		writer.write(f)
	typer.echo(f"Merged {len(pdfs)} PDFs into {output}")

def merge_from_dirs(directory: str, output: str):
	path = Path(directory)
	if not path.is_dir():
		typer.echo(f"Provided path is not a directory: {directory}")
		raise typer.Exit()

	pdfs = sorted([
		str(file) for file in path.iterdir() if file.is_file() and file.suffix.lower() == ".pdf"
	])

	if not pdfs:
		typer.echo(f"No PDF files found in directory: {dir}")
		raise typer.Exit()

	merge_from_files(pdfs, output)

def merge_parser(files: list[str], directory: str = None):
	if directory and files:
		typer.echo("Please provide either files or a directory, not both.")
		raise typer.Exit()

	if not directory and not files:
		typer.echo("Please provide at least one PDF file or a directory containing PDFs.")
		raise typer.Exit()
		
	output = "irlpdfmerge_output.pdf"

	if directory:
		merge_from_dirs(directory, output)
	else:
		merge_from_files(files, output)