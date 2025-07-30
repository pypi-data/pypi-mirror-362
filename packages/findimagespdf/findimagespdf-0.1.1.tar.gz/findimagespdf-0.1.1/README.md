# findimagespdf

Tool to extract images from PDF files, avoiding duplicates and storing images in a structured way.

The main directory is stored on the desktop and contains all subdirectories with PDF file names with their images.

* Directory structure:
```bash
FindImagesPDF
├── file1
│   └── image1.jpeg
├── file2
│   ├── image1.jpeg
│   ├── image2.jpeg
│   └── image3.jpeg
└── file3
    ├── image1.jpeg
    ├── image2.jpeg
    └── image3.jpeg
```


# Install

```bash
$ pip install findimagespdf
```


# CLI

```bash
$ findimagespdf --help
usage: findimagespdf [-h] -p PATH [-d DEST] [-v]

Extract images of PDF files.

options:
  -h, --help            show this help message and
                        exit
  -p PATH, --path PATH  Path of PDF file or
                        directory of PDF files.
  -d DEST, --dest DEST  Path of the directory to
                        store the images, by
                        default the directory is on
                        the desktop.
  -v, --verbose         Verbose

extracts images and stores them in a directory on
the desktop.
```

## Examples

```bash
$ findimagespdf --path pdf_samples

$ findimagespdf --path pdf_samples --dest .

$ findimagespdf --path pdf_samples --dest . --verbose
```


# Usage

* Using `with`

```python
from findimagespdf.pdffile import PDFFile

files = ["file1.pdf", "file2.pdf", "file3.pdf"]

for file in files:
    with PDFFile(path_or_bytes=file) as pdf:
        pdf.find_startxref()  # searches the xref table.
        pdf.search_deep()     # searches the entire archive for images
        pdf.search_images()   # searches the images.
        pdf.get_images()      # extracts and saves the images.
```

It is recommended to use `with`, because once the process is finished the file will be closed automatically. But you can open and close the file manually.

* Manually

```python
file = 'file1.pdf'

pdf = PDFFile(file)

pdf.open()            # open pdf file.

pdf.find_startxref()  # searches the xref table.
pdf.search_deep()     # searches the entire archive for images
pdf.search_images()   # searches the images.
pdf.get_images()      # extracts and saves the images.

pdf.close()           # closes pdf file.
```


# Methods

The main pdf processing methods for image search are:

| Method | Description |
|-|-|-|
| `find_startxref` | find the xref table of the file. |
| `search_deep` | optional but necessary in case the xref table is corrupted or to search for hidden or unlinked images. |
| `search_images` | search and filter images from the collected data. |
| `get_images` | extract and save images to the directory on the desktop. |
