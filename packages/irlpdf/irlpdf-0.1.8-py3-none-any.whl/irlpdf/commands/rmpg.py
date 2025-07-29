from PyPDF2 import PdfReader, PdfWriter
import typer

def parse_pages(pages: list[str]) -> list[int]:
	pages_out = set()
	for p in pages:
		if '-' in p:
			start, end = map(int, p.split("-"))
			pages_out.update(range(start, end + 1))
		else:
			pages_out.add(int(p))
	return sorted(pages_out)

def remove_pages(input_path: str, output_path: str, pages_to_remove: list[int]) -> None:
	reader = PdfReader(input_path)
	writer = PdfWriter()

	if not input_path.endswith('.pdf'):
		typer.echo("Input file must be a PDF.")
		return
	if not output_path.endswith('.pdf'):
		typer.echo("Output file must be a PDF.")
		return
	if not pages_to_remove:
		typer.echo("No pages specified for removal.")
		return
	if any(p > len(reader.pages) or p < 1 for p in pages_to_remove):
		typer.echo("One or more specified pages exceed the total number of pages in the PDF or are invalid.")
		return

	total_pages = len(reader.pages)
	pages_to_remove = set(p - 1 for p in pages_to_remove if 0 < p <= total_pages)

	for i in range(total_pages):
		if i not in pages_to_remove:
			writer.add_page(reader.pages[i])

	with open(output_path, "wb") as output_file:
		writer.write(output_file)

	typer.echo(f"Saved PDF with pages removed to: {output_path}")

def rmpg_parser(
	file: str,
	pages: list[str],
	output: str = None,
	overwrite: bool = False,
):
	if overwrite and output is not None:
		typer.echo("Cannot use both --overwrite and --output together.")
		raise typer.Exit()

	output_path = file if overwrite else output

	if not output_path:
		typer.echo("You must specify either --overwrite or --output.")
		raise typer.Exit()

	try:
		page_numbers = parse_pages(pages)
	except ValueError:
		typer.echo("Invalid page format.")
		raise typer.Exit()

	remove_pages(file, output_path, page_numbers)
