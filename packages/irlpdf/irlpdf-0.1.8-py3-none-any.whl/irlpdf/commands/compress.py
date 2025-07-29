from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import typer

def compress_pdf(input_path: str, output_path: str):
	path = Path(input_path)
	reader = PdfReader(str(path))
	writer = PdfWriter()

	for page in reader.pages:
		page.compress_content_streams()
		writer.add_page(page)
	
	with open(output_path, "wb") as f:
		writer.write(f)

	typer.echo(f"Compressed PDF saved to: {output_path}")

def compress_files(pdfs: list[str]):
	for pdf in pdfs:
		path = Path(pdf)
		if not path.exists() or not path.suffix.lower() == ".pdf":
			typer.echo(f"Skipping invalid PDF file: {pdf}")
			continue
		
		output_path = path.with_name(f"{path.stem}_compressed.pdf")
		compress_pdf(str(path), str(output_path))

def compress_directory(directory: str):
	path = Path(directory)
	if not path.is_dir():
		typer.echo(f"Provided path is not a directory: {directory}")
		raise typer.Exit()

	pdfs = sorted([
		str(file) for file in path.iterdir() if file.is_file() and file.suffix.lower() == ".pdf"
	])

	if not pdfs:
		typer.echo(f"No PDF files found in directory: {directory}")
		raise typer.Exit()

	compress_files(pdfs)

def compress_parser(files: list[str], directory: str = None):
	if directory and files:
		typer.echo("Please provide either files or a directory, not both.")
		raise typer.Exit()

	if not directory and not files:
		typer.echo("Please provide at least one PDF file or a directory containing PDFs.")
		raise typer.Exit()
		
	if directory:
		compress_directory(directory)
	else:
		compress_files(files)