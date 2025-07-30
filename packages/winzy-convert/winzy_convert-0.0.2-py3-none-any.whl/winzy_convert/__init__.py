import winzy
import glob
import os
from PIL import Image


def add_pngs_to_powerpoint(png_files, output_filename):
    """
    Adds PNG images to a PowerPoint presentation and exports it as PDF.

    Args:
      png_files: List of paths to the PNG files.
      output_filename: Path to the output PDF file.
    """
    import win32com.client

    ppt_app = win32com.client.gencache.EnsureDispatch("PowerPoint.Application")
    num_slides = len(png_files) + 1

    # Open an existing presentation or create a new one
    presentation = ppt_app.Presentations.Add()

    # Check if existing presentation has slides, otherwise create them

    # Add PNGs to slides
    for i, png_file in enumerate(png_files):
        try:
            slide = presentation.Slides.Add(i + 1, 2)
            left = 0
            top = 0
            width = -1  # Use -1 for automatic width
            height = -1  # Use -1 for automatic height

            slide.Shapes.AddPicture(png_file, False, True, left, top, width, height)
        except FileNotFoundError:
            print(f"Error: PNG file not found: {png_file}")

    # Save and export as PDF
    try:
        presentation.SaveAs(output_filename)
        print(f"Created successfully: {output_filename}")
    except Exception as e:
        print(f"Error during export: {e}")


def common_parser(parser):
    parser.add_argument(
        "pattern",
        type=str,
        help="Pattern matching the PNG images (e.g., e:\\temp\\*.png)",
    )

    parser.add_argument(
        "-i", "--imagefile", action="append", help="supply files with this option."
    )
    return parser


def create_parser(subparser):
    parser = subparser.add_parser(
        "topdf", description="Mimic's convert to convert images to pdf."
    )
    return common_parser(parser)


def create_pdf_file(png_files, output_file):
    images = []
    for png in png_files:
        img = Image.open(png)
        if img.mode == "RGBA":
            # Convert RGBA to RGB
            img = img.convert("RGB")
        images.append(img)

    # The first image will be used to create the PDF
    first_image = images.pop(0)

    # Save the images as a PDF
    first_image.save(output_file, save_all=True, append_images=images)


class PDFPlugin:
    """Mimic's convert to convert images to pdf, ppt etc."""

    __name__ = "topdf"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            default="output.pdf",
            help="Output pdf file name",
        )
        parser.set_defaults(func=self.main)

    def main(self, args):
        if not args.imagefile:
            png_files = sorted(
                glob.glob(args.pattern), key=lambda x: os.path.getctime(x)
            )
        else:
            png_files = [os.path.abspath(f) for f in args.imagefile]

        # Convert each PNG image to a PIL Image object and store in a list
        create_pdf_file(png_files, args.output)
        print(f"{args.output} created")

    def hello(self, args):
        # this routine will be called when "winzy topdf is called."
        print("Hello! This is an example ``winzy`` plugin.")


topdf_plugin = PDFPlugin()


def create_parserppt(subparser):
    parser = subparser.add_parser(
        "toppt", description="Mimic's convert to convert images to ppt"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.pptx",
        help="Output pdf file name",
    )
    return common_parser(parser)


class PPTPlugin:
    """Mimic's convert to convert images to pdf, ppt etc."""

    __name__ = "toppt"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parserppt(subparser)
        parser.set_defaults(func=self.main)

    def main(self, args):
        if not args.imagefile:
            png_files = sorted(
                glob.glob(args.pattern), key=lambda x: os.path.getctime(x)
            )
        else:
            png_files = [os.path.abspath(f) for f in args.imagefile]

        add_pngs_to_powerpoint(png_files, args.output)
        print(f"{args.output} created")

    def hello(self, args):
        # this routine will be called when "winzy topdf is called."
        print("Hello! This is an example ``winzy`` plugin.")


toppt_plugin = PPTPlugin()
