#!/usr/bin/env python3
"""
This module provides helper functions
for pagination in list-like data structures.

Functions:
    index_range(page: int, page_size: int) -> tuple[int, int]:
    Calculates the start and end index for a given page and page size.
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for the given pagination parameters.

    This function helps in determining the slice boundaries for a specific
    page of data based on the provided page number and page size.
    Page numbers are 1-indexed, meaning page 1 is the first page.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        tuple[int, int]: A tuple containing the start index (inclusive) and
        end index (exclusive) for the pagination range.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index
