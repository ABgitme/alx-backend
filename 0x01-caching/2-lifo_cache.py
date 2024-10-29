#!/usr/bin/python3
""" LIFOCache module """
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache class that implements a LIFO caching system. """

    def __init__(self):
        """ Initialize the class and call the parent init method. """
        super().__init__()
        self.stack = []  # Stack to track the order of keys added

    def put(self, key, item):
        """ Add an item to the cache using LIFO policy. """
        if key is None or item is None:
            return

        # Add the item to cache and update the stack
        if key in self.cache_data:
            self.stack.remove(key)  # Remove it from the current position in stack
        self.cache_data[key] = item
        self.stack.append(key)  # Append the new key to the stack

        # Check if cache exceeds maximum limit
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # LIFO: Remove the last added item in the stack
            last_key = self.stack.pop(-2)
            del self.cache_data[last_key]
            print(f"DISCARD: {last_key}")

    def get(self, key):
        """ Retrieve an item from the cache. """
        return self.cache_data.get(key, None)
