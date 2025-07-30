# -*- coding: utf-8 -*-
"""
"""
import argparse
import sys

from findimagespdf.pdffile import PDFFile
from findimagespdf.pathclass import PathClass
from findimagespdf.version import VERSION


from typing import Union


def run_process(
    path: str,
    dest: str = None,
    verbose: bool = True,
) -> None:
    """
    """
    try:
        with PDFFile(path_or_bytes=path, destination=dest) as pdf:
            if verbose:
                print(f"> Location: {pdf.base_path}")
                print(f"  > File: {PathClass.basename(path)}\n")
            pdf.find_startxref()
            pdf.search_deep()
            pdf.search_images()
            pdf.get_images()

    except Exception as e:
        print(e)
        return




def get_files(
    path: str
) -> Union[str, list, None]:
    """
    """
    if PathClass.is_dir(path):
        files = PathClass.get_files_recursive(
                                                extensions="pdf",
                                                directory=path
                                            )
        return [PathClass.join(path, file) for file in files]
    elif PathClass.is_file(path):
        return path
    else:
        return None


def cli() -> None:
    """
    """
    main = argparse.ArgumentParser(
                        prog="findimagespdf",
                        description="Extract images of PDF files.",
                        epilog="extracts images and stores them in a directory on the desktop.",
                    )
    main.add_argument(
        "-p",
        "--path",
        required=True,
        help="Path of PDF file or directory of PDF files."
    )

    main.add_argument(
        "-d",
        "--dest",
        required=False,
        help="Path of the directory to store the images, by default the directory is on the desktop."
    )

    main.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        help="Verbose"
    )

    args = main.parse_args()
    path = args.path
    dest = args.dest
    verbose = args.verbose

    content = get_files(path=path)

    if isinstance(content, list):
        for item in content:
            run_process(item, dest, verbose)

    elif isinstance(content, str):
        run_process(content, dest, verbose)

    else:
        print("`path` argument must be a PDF file or directory with PDF files.")
        return




if __name__ == '__main__':
    cli()
