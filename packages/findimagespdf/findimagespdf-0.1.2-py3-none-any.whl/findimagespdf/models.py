# -*- coding: utf-8 -*-
"""
Models
"""


class Xref:
    """
    Represents an entry of table XREF on file.

    Stores information such as byte offset, generation number and status of the
    object.
    """
    def __init__(
        self,
        bytes_offset: str,
        generation_number: str,
        status: str,
    ) -> None:
        """
        """
        self.bytes_offset = bytes_offset
        self.generation_number = generation_number
        self.status = status
        self.in_use = True if self.status == "n" else False

    def get_bytes_offset(self) -> int:
        """
        Returns int of bytes offset.
        """
        return int(self.bytes_offset)

    def __lt__(self, other) -> bool:
        """
        """
        return isinstance(other, Xref) and self.bytes_offset < other.bytes_offset

    def __str__(self) -> str:
        """
        """
        return "%s %s %s" % (
                        self.bytes_offset,
                        self.generation_number,
                        self.in_use,
                    )

    def __repr__(self) -> str:
        """
        """
        return "<[ XREF: %s ]>" % self.__str__()


class ObjectsPDF:
    """
    Represents any object in file.

    Stores information such as location in the file and size.
    """
    def __init__(
        self,
        id: int,
        start: int,
        end: int,
        n_bytes: int,
    ) -> None:
        """
        """
        self.id = id
        self.start = start
        self.end = end
        self.n_bytes = n_bytes

    def __str__(self) -> str:
        """
        """
        return "%i, %i, %i, %i" % (
                        self.id,
                        self.start,
                        self.end,
                        self.n_bytes,
                    )

    def __repr__(self) -> str:
        """
        """
        return "<[ ObjectsPDF: %s ]>" % self.__str__()


class ImagePDF:
    """
    Represents to images on file.

    Stores information such as the location in the file, its size, width and
    height.
    """
    def __init__(
        self,
        id: int,
        start: int,
        end: int,
        n_bytes: int,
        width: int,
        height: int,
    ) -> None:
        """
        """
        self.id = id
        self.start = start
        self.end = end
        self.n_bytes = n_bytes
        self.width = width
        self.height = height
        self.hash = None

    def __lt__(self, other) -> bool:
        """
        """
        return isinstance(other, ImagePDF) and self.id < other.id

    def __eq__(self, other) -> bool:
        """
        """
        return isinstance(other, ImagePDF) and self.hash == other.hash

    def __str__(self) -> str:
        """
        """
        return "%i, %i, %i, %i" % (
                        self.id,
                        self.start,
                        self.end,
                        self.n_bytes,
                    )

    def __repr__(self) -> str:
        """
        """
        return "<[ Image: %s ]>" % self.__str__()
