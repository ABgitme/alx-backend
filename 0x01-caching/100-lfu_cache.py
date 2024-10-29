#!/usr/bin/python3
""" LFUCache module """
from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """ LFUCache class that implements an LFU caching system. """

    def __init__(self):
        """ Initialize the class and call the parent init method. """
        super().__init__()
        # Track access frequency for each key
        self.frequency = defaultdict(int)
        # Maintain order for LRU on ties
        self.order = OrderedDict()

    def put(self, key, item):
        """ Add an item to the cache using LFU policy. """
        if key is None or item is None:
            return

        # If key is already in cache, update its value and frequency
        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            # Move to end to mark it as recently used
            self.order.move_to_end(key)
        else:
            # If cache exceeds MAX_ITEMS, evict the LFU item
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the least frequently used item
                min_freq = min(self.frequency.values())
                lfu_keys = [
                    k for k in self.order.keys()
                    if self.frequency[k] == min_freq]

                # If multiple keys have the minimum frequency,
                # remove the LRU of those
                if lfu_keys:
                    lfu_key = lfu_keys[0]
                    del self.cache_data[lfu_key]
                    del self.frequency[lfu_key]
                    self.order.pop(lfu_key)
                    print(f"DISCARD: {lfu_key}")

            # Add the new item to cache
            self.cache_data[key] = item
            self.frequency[key] = 1
            self.order[key] = True  # Add to order to maintain recency

    def get(self, key):
        """ Retrieve an item from the cache using LFU policy. """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and recency of access
        self.frequency[key] += 1
        self.order.move_to_end(key)
        return self.cache_data[key]
