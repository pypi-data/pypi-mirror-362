from PyPDF2 import PdfReader, PdfWriter
import typer


def encrypt_pdf(input_path: str, output_path: str, password: str) -> None:
	reader = PdfReader(input_path)
	writer = PdfWriter()

	writer.encrypt(password)

	for page in reader.pages:
		writer.add_page(page)

	with open(output_path, "wb") as f:
		writer.write(f)

	typer.echo(f"PDF encrypted successfully and saved to: {output_path}")


def encrypt_parser(
	file: str,
	output: str=None,
	overwrite: bool=False,
):
	if overwrite and output is not None:
		typer.echo("Cannot use both --overwrite and --output together.")
		raise typer.Exit()

	output_path = file if overwrite else output

	if not output_path:
		typer.echo("You must specify either --overwrite or --output.")
		raise typer.Exit()

	if not output_path.endswith('.pdf'):
		typer.echo("Output file must be a PDF.")
		raise typer.Exit()

	if not file.endswith('.pdf'):
		typer.echo("Input file must be a PDF.")
		raise typer.Exit()

	password = typer.prompt("Enter password for the PDF", hide_input=True)

	if not password:	
		typer.echo("Password cannot be empty.")
		raise typer.Exit()

	encrypt_pdf(file, output_path, password)