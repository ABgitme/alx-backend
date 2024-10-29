#!/usr/bin/env python3
"""
Implemented a method named get_page that takes two integer arguments
page with default value 1 and page_size with default value 10
"""
import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for the given pagination parameters.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index (inclusive) and
        end index (exclusive) for the pagination range.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # skip header row

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get a page from the dataset.

        Args:
            page (int): The page number (1-indexed).
            page_size (int): The number of items per page.

        Returns:
            List[List]: A list of rows representing the page of the dataset.
            Returns an empty list if page or page_size is out of range.
        """
        assert isinstance(
            page, int) and page > 0, "page must be a positive integer"
        assert isinstance(
            page_size, int) and page_size > 0, "page_size\
        must be a positive integer"

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        # Return the sliced dataset for the specified range,
        # or an empty list if out of range
        return dataset[start_index:end_index]\
            if start_index < len(dataset) else []
