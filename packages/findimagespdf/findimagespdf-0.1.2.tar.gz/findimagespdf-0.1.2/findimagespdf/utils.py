# -*- coding: utf-8 -*-
"""
"""

from hashlib import md5


def get_md5_hash(
    data: bytes
) -> str:
    """
    Calculates and returns the MD5 hash.
    """
    return md5(data).hexdigest()
