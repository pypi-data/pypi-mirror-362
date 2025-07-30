import pytest
import winzy_convert as w
import os
from PIL import Image
import tempfile

from argparse import Namespace, ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(["hello"])
    assert result.pattern == "hello"


def test_plugin(capsys):
    w.topdf_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``winzy`` plugin." in captured.out


def test_create_pdf_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some dummy PNG files
        png_files = []
        for i in range(3):
            file_path = os.path.join(tmpdir, f"test_image_{i}.png")
            img = Image.new("RGB", (100, 100), color="red")
            img.save(file_path, "PNG")
            png_files.append(file_path)

        # Define the output PDF file path
        output_pdf = os.path.join(tmpdir, "output.pdf")

        # Call the function to create the PDF
        w.create_pdf_file(png_files, output_pdf)

        # Check if the PDF file was created
        assert os.path.exists(output_pdf)
