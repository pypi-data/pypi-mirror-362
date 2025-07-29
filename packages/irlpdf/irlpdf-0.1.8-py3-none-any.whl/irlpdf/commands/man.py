import typer

manual = {
	"stats": """
Usage:
  irlpdf stats FILE

Description:
  Displays basic statistics about the PDF like page count, encryption, metadata, and file size.
        """,

        "split": """
Usage:
  irlpdf split FILE BREAKPOINTS... 

Description:
  Splits the input PDF at the specified breakpoints (page numbers).
  Output files will be auto-named as FILE_split_N.pdf.

Examples:
  irlpdf split file.pdf 2 4 6
        """,

        "rmpg": """
Usage:
  irlpdf rmpg FILE PAGES... [--output OUTPUT_FILE | --overwrite]

Description:
  Removes the specified pages from the input PDF.
  Pages can be individual numbers or ranges (e.g., 2 3 5-7).

Examples:
  irlpdf rmpg input.pdf 2 4 6-8 --output cleaned.pdf
  irlpdf rmpg input.pdf 2 4 6-8 --overwrite
        """,

        "merge": """
Usage:
  irlpdf merge FILE1.pdf FILE2.pdf ...
  irlpdf merge -d DIRECTORY

Description:
  Merges multiple PDF files into a single file.
  You can either specify multiple PDF files or a directory containing PDFs.

Example:
  irlpdf merge f1.pdf f2.pdf f3.pdf
  irlpdf merge -d folder_with_pdfs
        """,

        "encrypt": """
Usage:
  irlpdf encrypt FILE [--output OUTPUT_FILE | --overwrite]

Description:
  Encrypts the input PDF with a password (prompted interactively).
  You can choose to overwrite the file or save it to a new path.

Examples:
  irlpdf encrypt file.pdf --output encrypted.pdf
  irlpdf encrypt file.pdf --overwrite
        """,

        "decrypt": """
Usage:
  irlpdf decrypt FILE [--output OUTPUT_FILE | --overwrite]

Description:
  Decrypts the PDF (password will be prompted interactively).
  You can overwrite the file or save to a new file.

Examples:
  irlpdf decrypt encrypted.pdf --output plain.pdf
  irlpdf decrypt encrypted.pdf --overwrite
        """,

        "compress": """
Usage:
  irlpdf compress FILE1.pdf FILE2.pdf ...
  irlpdf compress -d DIRECTORY

Description:
  Compresses PDF files using lossless compression.
  Accepts multiple files or a directory of PDFs.

Example:
  irlpdf compress file1.pdf file2.pdf
  irlpdf compress -d folder_with_pdfs
        """,

        "help": """
Available Commands:
  stats      Show PDF metadata and file information.
  split      Split a PDF into multiple smaller PDFs.
  rmpg       Remove pages from a PDF.
  merge      Merge multiple PDFs into one.
  encrypt    Encrypt a PDF with a password.
  decrypt    Decrypt a password-protected PDF.
  compress   Compress PDF(s) using lossless compression.
  help       Show this help message.

Usage:
  irlpdf man [COMMAND]
        """
}


def man_parser(command: str):
	command = command.lower()
	
	if command in manual:
		typer.echo(manual[command])
	else:
		typer.echo(f"No manual entry found for command: {command}")
		raise typer.Exit()
