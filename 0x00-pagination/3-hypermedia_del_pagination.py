#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Optional


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """
        Deletion-resilient pagination to get a page of data from a dataset.

        Args:
            index (int): The starting index for the page.
            page_size (int): The number of items per page.

        Returns:
            Dict: A dictionary with the following keys:
                - index: The current start index of the returned page.
                - next_index: The next index to query with.
                - page_size: The current page size.
                - data: The list of items for the current page.
        """
        indexed_dataset = self.indexed_dataset()
        dataset_length = len(indexed_dataset)

        # Validate that the index is within the valid range of the dataset
        assert 0 <= index < dataset_length, "Index is out of range"
        assert page_size > 0, "Page size must be a positive integer"

        data = []
        current_index = index
        dataset_length = len(indexed_dataset)

        # Loop through the dataset until
        # we collect enough items for the page size
        while len(data) < page_size and current_index < dataset_length:
            if current_index in indexed_dataset:
                data.append(indexed_dataset[current_index])
            current_index += 1

        # The next index to query, which should
        # be the first index after the current page
        next_index = current_index if current_index < dataset_length else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }
