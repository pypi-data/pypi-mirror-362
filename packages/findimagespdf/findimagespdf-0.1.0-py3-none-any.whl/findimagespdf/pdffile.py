# -*- coding: utf-8 -*-
"""
PDFFile manages the PDF file, finds the images and saves them in the
`FindImagesPDF` directory on the user's desktop.
"""

from findimagespdf.models import (
    Xref,
    ImagePDF,
    ObjectsPDF,
)

from findimagespdf.pathclass import PathClass
from findimagespdf.utils import (
    get_md5_hash
)


from PIL import Image
import zlib
import io
import re


from typing import Union


class PDFFile:

    DIRECTORY = "FindImagesPDF"

    def __init__(
        self,
        path_or_bytes: Union[str, bytes] = None,
    ) -> None:
        self.path_or_bytes = path_or_bytes
        self.file = None
        self.table_xref = []
        self.images = []
        self.objects_pdf = {}

        self.base_path = None
        self.current_directory_name()


    def current_directory_name(self) -> None:
        """
        Creates the base directory path.
        """
        if isinstance(self.path_or_bytes, str):
            dir_name = PathClass.splitext(
                                    PathClass.basename(self.path_or_bytes)
                                )[0].replace(" ", "_")

        elif isinstance(self.path_or_bytes, (bytes, io.BytesIO)):
            try:
                dir_name = get_md5_hash(self.path_or_bytes)
            except TypeError as e:
                dir_name = get_md5_hash(self.path_or_bytes.getvalue())

        self.base_path = PathClass.join(
                                    PathClass.get_desktop(),
                                    PDFFile.DIRECTORY,
                                    dir_name
                                )

    def open(
        self,
        path: str = None
    ) -> None:
        """
        Open file.

        Args
            path: str, default is None. Path of file.
        """
        if path is not None:
            self.file = open(path, 'rb')
        else:
            if self.path_or_bytes is None:
                return
            elif isinstance(self.path_or_bytes, str):
                self.file = open(self.path_or_bytes, 'rb')
            elif isinstance(self.path_or_bytes, bytes):
                self.file = io.BytesIO(self.path_or_bytes)
            elif isinstance(self.path_or_bytes, io.BytesIO):
                self.file = self.path_or_bytes
            else:
                return

    def read(
        self,
        byte_offset: int = None,
        byte_size: int = None,
        seek: int = 0,
    ) -> io.BufferedIOBase:
        """
        Reads the contents of the file.

        Args
            byte_offset: int, byte offset.
            byte_size: int, bytes a leer.

        Returns
            bytes: content read.
        """
        if byte_offset is not None:
            self.file.seek(seek)
            self.file.seek(byte_offset)
        if byte_size is not None:
            return self.file.read(byte_size)
        return self.file.read()

    def close(self) -> None:
        """
        Clear and close the current file.
        """
        if self.file:
            self.table_xref = []
            self.images = []
            try:
                self.file.close()
            except Exception as e:
                pass
            finally:
                self.file = None

    def find_startxref(
        self,
    ) -> None:
        """
        Find the xref table in the file.
        """
        data = self.read()
        position = data.find(b'startxref')
        # print(position)
        if position > 0:
            self.file.seek(position)

            # startxref = self.file.read().decode("utf-8").split("\n")[1]
            startxref = self.read().decode("utf-8").split("\n")[1]

            # print(position, startxref)
            self.table_xref = self.get_xref_table(byte_offset=startxref)
            self.table_xref.sort()
            # print(self.table_xref)

    def get_xref_table(
        self,
        byte_offset: str,
    ) -> list:
        """
        Gets the data from the xref table and creates `Xref` objects to store
        them in a list.

        Args
            byte_offset: str, integer position of xref table.

        Returns
            list: list of `Xref` objects.
        """
        xref_table = []
        self.file.seek(int(byte_offset))

        for line in self.file.readlines():
            # print(line)
            matches = re.findall(
                            r'\d+\s\d+\s[n,f]',
                            line.decode("utf-8"),re.IGNORECASE
                        )
            if matches:
                # print(line, matches)
                data = matches[0].strip().split(" ")
                xref = Xref(
                    bytes_offset=data[0],
                    generation_number=data[1],
                    status=data[2],
                )
                xref_table.append(xref)

        return xref_table

    def search_deep(
        self,
    ) -> None:
        """
        Iterates over all file searching objects and stored.
        """
        self.file.seek(0)
        data = self.read()
        # print(data)

        for data_obj in re.findall(rb'\d+\s\d+\sobj\n?', data):
            start = data.find(data_obj)
            self.file.seek(start)
            end = re.search(rb'endobj\n?', self.read())

            if end is None:
                continue

            end = end.end()
            n_bytes = (start + end) - start
            # print(start, end, n_bytes)
            # self.file.seek(start)
            # print(self.file.read(n_bytes))
            # print()

            object_number, generation_number, *c = data_obj.decode("utf-8").split(" ")
            # print(">" , object_number, generation_number, c)

            self.objects_pdf[int(object_number)] = ObjectsPDF(
                                                        id=int(object_number),
                                                        start=start,
                                                        end=end,
                                                        n_bytes=n_bytes,
                                                    )

    def regex_get_width_height(
        self,
        data: bytes
    ) -> tuple:
        """
        Search by image width and height in the raw data.

        Args
            data: bytes, raw data of image.

        Returns
            tuple: (width, height).
        """
        width_match = re.findall(rb'/Width\s\d+\s\d+\sR|/Width\s\d+', data)
        height_match = re.findall(rb'/Height\s\d+\s\d+\sR|/Height\s\d+', data)
        if width_match:
            w = width_match[0].decode("utf-8")
        else:
            w = ""
        if height_match:
            h = height_match[0].decode("utf-8")
        else:
            h = ""
        return w, h

    def inspect_xref_table(
        self,
    ) -> None:
        """
        Inspects the objects in the xref table list and filters the images.
        """
        id_ = 1
        for i in range(0, len(self.table_xref)):
            try:
                start = self.table_xref[i].get_bytes_offset()
                end = self.table_xref[i + 1].get_bytes_offset()
                n_bytes = end - start

                # self.file.seek(start)
                # data = self.file.read(n_bytes)
                data = self.read(byte_offset=start, byte_size=n_bytes)

                is_saved = self.__filter_images(data, id_, start, end, n_bytes)
                if is_saved:
                    id_ += 1
            except IndexError as e:
                # print("END", self.table_xref[i])
                pass

    def inspect_pdf_objs(
        self,
    ) -> None:
        """
        Inspects the objects in the pdf objects list and filters the images.
        """
        id_ = 1
        for id, item in self.objects_pdf.items():
            try:
                # item.id
                data = self.read(byte_offset=item.start, byte_size=item.n_bytes)
                # print("> ", data)
                # print()
                is_saved = self.__filter_images(
                                    data,
                                    id_,
                                    item.start,
                                    item.end,
                                    item.n_bytes
                                )
                if is_saved:
                    id_ += 1
            except Exception as e:
                # print(e)
                pass

    def __filter_images(
        self,
        data: bytes,
        id_image: int,
        start: int,
        end: int,
        n_bytes: int,
    ) -> bool:
        """
        Filter images from raw data.

        Args
            data: bytes, raw data.
            id_image: int, image identifier.
            start: int, offset in bytes of the data.
            end: int, end position of the data.
            n_bytes: int, size of the data.

        Returns
            bool: `True` if the image is stored in image list, otherwise,
                  `False`.
        """
        if data.find(b'/Image') > -1:
            # print(data)
            # print()
            id = data[:10].decode("utf-8").split(" ")[0]

            w_match, h_match = self.regex_get_width_height(data)
            # if not w_match and not h_match:
            if w_match == "" or h_match == "":
                return

            width = None
            height = None

            if 'R' in w_match and 'R' in h_match:
                id_obj_width = w_match.split(" ")[1]
                id_obj_height = h_match.split(" ")[1]

                try:
                    sizes = []
                    items = [
                            self.objects_pdf[int(id_obj_width)],
                            self.objects_pdf[int(id_obj_height)]
                        ]
                    for item in items:
                        # print("> ", item, item.start, item.n_bytes)
                        # self.file.seek(0)
                        # self.file.seek(item.start)
                        size = self.read(
                                        byte_offset=item.start,
                                        byte_size=item.n_bytes
                                    )
                        # print(size)
                        x = re.search(rb'\d+\s\d+\sobj[\s|\n]?', size)
                        numbers_ = re.split(
                                        "\s|\n",
                                        size[x.end():].decode("utf-8").strip()
                                    )
                        if numbers_:
                            try:
                                sizes.append(int(numbers_[0]))
                            except ValueError as e:
                                sizes.clear()
                                break

                    if sizes:
                        # print(sizes)
                        width = sizes[0]
                        height = sizes[1]

                except KeyError as e:
                    pass
            else:
                width = int(w_match.split(" ")[1])
                height = int(h_match.split(" ")[1])

            # print(width, height)
            if width is not None and height is not None:

                image = ImagePDF(
                            id=id_image,
                            start=start,
                            end=end,
                            n_bytes=n_bytes,
                            width=width,
                            height=height,
                        )
                hash = self.__get_hash_image(start, n_bytes)
                image.hash = hash

                if image not in self.images:
                    self.images.append(image)
                    return True
        return False

    def __get_hash_image(
        self,
        start: int,
        size: int,
    ) -> str:
        """
        Calculates the hash of the raw image data.

        Args:
            start: offset in bytes of the image data.
            size: image size in bytes.

        Returns
            str: md5 hash of the raw image data.
        """
        data = self.read(
            byte_offset=start,
            byte_size=size
        )
        # print(data)
        match_start = re.search(b'stream\n', data)
        match_end = re.search(b'\n?endstream\n', data)

        image_raw = data[match_start.end():match_end.start()]

        return get_md5_hash(image_raw)

    def search_images(
        self,
    ) -> None:
        """
        It searches for images by two mechanisms: using the xref table and
        iterating over the file.
        """
        self.inspect_xref_table()
        self.inspect_pdf_objs()

    def get_images(
        self,
    ) -> None:
        """
        Extracts the image data and saves it in a directory with a file name.

        The image size is the original size described in the data.
        """
        if not self.images:
            return

        PathClass.makedirs(self.base_path)

        for image in self.images:
            data = self.read(
                            byte_offset=image.start,
                            byte_size=image.n_bytes
                        )

            start = data.find(b'stream\n') + len(b'stream\n')
            end = data.find(b'\nendstream')
            n_bytes = end - start

            try:
                image_raw = zlib.decompress(data[start : end])
            except zlib.error:
                image_raw = data[start : end]

            im = Image.open(io.BytesIO(image_raw))
            im.resize((image.width, image.height))

            image_path = PathClass.join(
                                    self.base_path,
                                    f"image{image.id}.{im.format.lower()}"
                                )
            # print(image_path)
            im.save(image_path)
            im.close()


    def __enter__(self) -> None:
        """
        Enter the runtime context related to this object.

        Open the given file.
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exit the runtime context related to this object.

        Closes the current file.
        """
        self.close()

    def __del__(self) -> None:
        """
        Called when the instance is about to be destroyed.

        It is used when `with` is not used, i.e. when the file is opened
        manually.
        """
        self.close()
