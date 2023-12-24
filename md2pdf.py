import os
import subprocess

def convert_md_to_pdf(md_file):
    # Get the current directory
    current_dir = os.getcwd()

    # Get the absolute path of the markdown file
    md_file_path = os.path.join(current_dir, md_file)

    # Create the output PDF file path
    pdf_file_path = os.path.splitext(md_file_path)[0] + ".pdf"

    # Check if the markdown file exists
    if not os.path.isfile(md_file_path):
        print(f"Error: {md_file} does not exist.")
        return

    # Check if the pandoc command is available
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("Error: pandoc is not installed.")
        return

    # Convert the markdown file to PDF using pandoc
    try:
        subprocess.run(["pandoc", md_file_path, "-o", pdf_file_path], check=True)
        print(f"Successfully converted {md_file} to {pdf_file_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to convert {md_file} to PDF.")
        print(e.stderr.decode())

# Example usage
convert_md_to_pdf("README_Refined.md")
