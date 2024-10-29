#!/usr/bin/python3
""" BasicCache module """
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache class that inherits from BaseCaching, no limit to cache """

    def put(self, key, item):
        """ Assigns the item to the key in cache_data dictionary.
            If key or item is None, does nothing.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Retrieves the item from cache_data associated with the key.
            If key is None or not found, returns None.
        """
        return self.cache_data.get(key, None)
