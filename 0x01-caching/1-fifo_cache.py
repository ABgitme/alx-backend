#!/usr/bin/python3
""" FIFOCache module """
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class that implements a FIFO caching system. """

    def __init__(self):
        """ Initialize the class and call the parent init method. """
        super().__init__()
        self.order = []  # List to track the order of keys for FIFO

    def put(self, key, item):
        """ Add an item to the cache using FIFO policy. """
        if key is not None and item is not None:
            # Check if key already exists, to update its value without adding to order list
            if key not in self.cache_data:
                self.order.append(key)

            # Add item to cache
            self.cache_data[key] = item

            # Check if cache exceeds maximum limit
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # FIFO: Remove the oldest item added
                oldest_key = self.order.pop(0)
                del self.cache_data[oldest_key]
                print(f"DISCARD: {oldest_key}")

    def get(self, key):
        """ Retrieve an item from the cache. """
        return self.cache_data.get(key, None)
