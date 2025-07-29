from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import typer


def split_pdf(input_path: str, breakpoints: list[int]):
	path = Path(input_path)
	reader = PdfReader(str(path))
	total_pages = len(reader.pages)

	breakpoints = sorted(set(bp for bp in breakpoints if 0 < bp < total_pages))
	split_points = [0] + breakpoints + [total_pages]

	parts = []
	for i in range(len(split_points) - 1):
		start, end = split_points[i], split_points[i + 1]
		writer = PdfWriter()
		for page_num in range(start, end):
			writer.add_page(reader.pages[page_num])
		parts.append(writer)

	output_files = [
		f"{path.stem}_irlpdfsplit_{i + 1}.pdf" for i in range(len(parts))
	]

	for writer, out_path in zip(parts, output_files):
		with open(out_path, "wb") as f:
			writer.write(f)
		typer.echo(f"Saved: {out_path}")


def split_parser(file: str, breakpoints: list[str]):
	try:
		breakpoints_int = [int(bp) for bp in breakpoints]
	except ValueError:
		typer.echo("All breakpoints must be integers.")
		raise typer.Exit()


	split_pdf(file, breakpoints_int)
