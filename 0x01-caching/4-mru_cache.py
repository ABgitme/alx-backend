#!/usr/bin/python3
""" MRUCache module """
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class that implements an MRU caching system. """

    def __init__(self):
        """ Initialize the class and call the parent init method. """
        super().__init__()
        self.order = []  # List to track the order of key access

    def put(self, key, item):
        """ Add an item to the cache using MRU policy. """
        if key is None or item is None:
            return

        # If key already exists,
        # update the item and remove it from the order list
        if key in self.cache_data:
            self.order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # If cache is full, discard the MRU item
            # (last item in the access order list)
            mru_key = self.order.pop(-1)
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")

        # Add item to cache and update the access order
        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key):
        """ Retrieve an item from the cache using MRU policy. """
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed key to the end of
        # the access order list (most recently used)
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
