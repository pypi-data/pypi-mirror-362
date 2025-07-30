# ##################################################################################################
#
# Title:
#
#   langworks.util.cache.py
#
# License:
#
#   Copyright 2025 Rosaia B.V.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except 
#   in compliance with the License. You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software distributed under the 
#   License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#   express or implied. See the License for the specific language governing permissions and 
#   limitations under the License.
#
#   [Apache License, version 2.0]
#
# Description: 
#
#   Part of the Langworks framework, implementing various caches to cache prompt outputs.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
import collections

from dataclasses import (
    dataclass,
    field
)

from typing import (
    Any,
    Callable,
    Hashable
)


# Third party ######################################################################################

# cachetools (Thomas Kemmer)
import cachetools


# ##################################################################################################
# Classes
# ##################################################################################################

# ScoredItem #######################################################################################

@dataclass
class ScoredItem:

    """
    Wrapping class to store any cachable item alongside a score. To be used in conjunction with
    `ScoredCache` or any of its derivates.
    """

    item  : Any   = field(default = None)
    """Item stored."""

    score : float = field(default = 0)
    """Score attributed to the item."""

    # End of class 'ScoredItem' ####################################################################
    

# ScoredCache ######################################################################################

class ScoredCache(cachetools.Cache):

    """
    A regular cache with a scoring mechanism added to it to control overwrites, only overwriting a
    cached value if the new value is associated with a higher score as defined by the user.

    .. note::
        As ScoredCache is implemented on top of Thomas Kemmer's 
        `cachetools <https://github.com/tkem/cachetools>`_, ScoredCache may also be used under
        `the MIT License <https://opensource.org/license/mit>`_ under the copyright of Rosaia B.V.
        (2025).
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
        self,
        maxsize   : int,
        getsizeof : Callable[[Any], int] = None
    ):
        
        """
        Initializes the cache.

        Parameters
        ----------

        maxsize
            Maximum size up until which the cache may grow, after which the cache will start pruning
            items to make room for new keys.
        getsizeof
            Callable used to determine the size of cached items.
        """

        # Initialize inner constructs ##############################################################

        # Initialize super class.
        cachetools.Cache.__init__(self, maxsize, getsizeof)


        # End of '__init__' ########################################################################


    # __getitem__ ##################################################################################

    def __getitem__(
        self, 
        key               : Hashable, 
        __cache_getitem__ : Callable = cachetools.Cache.__getitem__ # Micro optimization
    ) -> Any:
        
        """
        Retrieves item from the cache.

        Parameters
        ----------

        key
            Key of the item to retrieve.
        """

        # Retrieve item from cache, and return wrapped value.
        return __cache_getitem__(self, key).item
    
        # End of '__getitem__' #####################################################################


    # __setitem__ ##################################################################################
    
    def __setitem__(
        self, 
        key               : Hashable, 
        item              : ScoredItem, 
        __cache_getitem__ : Callable    = cachetools.Cache.__getitem__, # Micro optimization
        __cache_setitem__ : Callable    = cachetools.Cache.__setitem__  # Micro optimization
    ):
        
        """
        Adds an item to the cache. 
        
        Unlike regular caches, these items need to be wrapped using a `ScoredItem` object, holding
        the actual item, as well as the score attributed to this item.

        Parameters
        ----------

        key
            Key used to index the item.
        item
            Item to store, wrapped in a `CachedItem`, consisting of an item and a score.
        """

        # Check if an item was stored with the given key.
        if key in self:
            
            # If it was, retrieve the item.
            cached_item = __cache_getitem__(self, key)

            # Compare scores, only proceeding if the new item's score is better.
            if item.score <= cached_item.score:
                return
            
        # Cache the new item.
        __cache_setitem__(self, key, item)

        # End of '__setitem__' #####################################################################

    # End of class 'ScoredCache' ###################################################################


# ScoredLazyLFUCache ###############################################################################

class ScoredLazyLFUCache(ScoredCache):

    """
    A scored Least Frequently Used (LFU) cache, implemented in a 'lazy' manner, only returning cache
    hits for a key if said key has been requested more than a set number of times during
    availability for retrieval. In doing so, this cache effectively samples items before storing
    them.

    .. note::
        As ScoredLazyLFUCache is implemented on top of Thomas Kemmer's 
        `cachetools <https://github.com/tkem/cachetools>`_, ScoredLazyLFUCache may also be used 
        under `the MIT License <https://opensource.org/license/mit>`_ under the copyright of 
        Rosaia B.V. (2025).
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
        self, 
        maxsize   : int, 
        getsizeof : Callable[[Any], int] = None,
        threshold : int = 3
    ):
        
        """
        Initializes the cache.

        Parameters
        ----------

        maxsize
            Maximum size up until which the cache may grow, after which the cache will start pruning
            items to make room for new keys.
        getsizeof
            Callable used to determine the size of cached items.
        threshold
            Minimum number of hits required before the cache starts returning for a key.
        """

        # Initialize inner constructs ##############################################################

        # Initialize super class.
        ScoredCache.__init__(self, maxsize, getsizeof)

        # Requests counter.
        self.__requests = collections.Counter()


        # Initialize attributes ####################################################################

        # Argument passthrough
        self.threshold = threshold


        # End of '__init__' ########################################################################


    # __getitem__ ##################################################################################

    def __getitem__(
        self, 
        key                     : Hashable, 
        __scoredcache_getitem__ : Callable = ScoredCache.__getitem__ # Micro optimization
    ):
        
        """
        Retrieves item from the cache.

        Parameters
        ----------

        key
            Key of the item to retrieve.
        """

        # Attempt to retrieve item from cache.
        item : ScoredItem = __scoredcache_getitem__(self, key)

        # Double check for availability, in case missings are handled differently by any subclasses.
        if key in self:

            # Push up usage counter.
            self.__requests[key] -= 1

            # Check if the threshold was reached.
            if self.__requests[key] > (-self.threshold):

                # If not, pretend the item not to have been cached yet.
                return self.__missing__(key)
            
        # Return the item. 
        return item
    
        # End of '__getitem__' #####################################################################


    # __setitem__ ##################################################################################

    def __setitem__(
        self,
        key                     : Hashable,
        value :                 ScoredItem,
        __scoredcache_setitem__ : Callable = ScoredCache.__setitem__ # Micro optimization
    ):
        
        """
        Adds an item to the cache. 
        
        Unlike regular caches, these items need to be wrapped using a `ScoredItem` object, holding
        the actual item, as well as the score attributed to this item.

        Parameters
        ----------

        key
            Key used to index the item.
        item
            Item to store, wrapped in a `CachedItem`, consisting of an item and a score.
        """
        
        # Store item.
        __scoredcache_setitem__(self, key, value)

        # Initialize counter for object.
        self.__requests[key] += 0
        
        # End of '__setitem__' #####################################################################


    # __delitem__ ##################################################################################

    def __delitem__(
        self,
        key           : Hashable,
        __scoredcache_delitem__ : Callable = ScoredCache.__delitem__ # Micro optimization
    ):
        
        """
        Deletes item from the cache.

        Parameters
        ----------

        key
            Key to delete from the cache.
        """
        
        # Delete from cache.
        __scoredcache_delitem__(self, key)

        # Remove counter for item.
        del self.__requests[key]

        # End of '__delitem__' #####################################################################

    
    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # popitem ######################################################################################

    def popitem(self) -> tuple[Hashable, Any]:

        """
        Remove and return the key of the least frequently used item, as well as the item itself.
        """

        # Attempt to retrieve the key of the least frequently used item.
        try:
            ((key, _),) = self.__requests.most_common(1)
        except:
            raise KeyError("%s is empty" % type(self).__name__) from None
        else:

            # Set requests counter for key beyond the threshold as to ensure that the cache does
            # not report a missing value, when we retrieve the value.
            self.__requests[key] -= self.threshold

            # Return a key-value pair.
            return (key, self.pop(key))
        
        
        # End of method 'popitem' ##################################################################
        
    # End of class 'ScoredLazyLFUCache' ############################################################


# ScoredLazyLRUCache ###############################################################################

class ScoredLazyLRUCache(ScoredCache):

    """
    A scored Least Recently Used (LRU) cache, implemented in a 'lazy' manner, only returning cache
    hits for a key if said key has been requested more than a set number of times during
    availability for retrieval. In doing so, this cache effectively samples items before storing
    them.

    .. note::
        As ScoredLazyLRUCache is implemented on top of Thomas Kemmer's 
        `cachetools <https://github.com/tkem/cachetools>`_, ScoredLazyLRUCache may also be used 
        under `the MIT License <https://opensource.org/license/mit>`_ under the copyright of 
        Rosaia B.V. (2025).
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
        self, 
        maxsize   : int, 
        getsizeof : Callable[[Any], int] = None,
        threshold : int = 3
    ):
        
        """
        Initializes the cache.

        Parameters
        ----------

        maxsize
            Maximum size up until which the cache may grow, after which the cache will start pruning
            items to make room for new keys.
        getsizeof
            Callable used to determine the size of cached items.
        threshold
            Minimum number of hits required before the cache starts returning for a key.
        """

        # Initialize inner constructs ##############################################################

        # Initialize super class.
        ScoredCache.__init__(self, maxsize, getsizeof)

        # Requests counter, which also doubles as a position tracker.
        self.__requests = collections.OrderedDict()


        # Initialize attributes ####################################################################

        # Argument passthrough
        self.threshold : int = threshold


        # End of '__init__' ########################################################################


    # __getitem__ ##################################################################################

    def __getitem__(
        self, 
        key                     : Hashable, 
        __scoredcache_getitem__ : Callable = ScoredCache.__getitem__ # Micro optimization
    ):
        
        """
        Retrieves item from the cache.

        Parameters
        ----------

        key
            Key of the item to retrieve.
        """

        # Attempt to retrieve item from cache.
        item : ScoredItem = __scoredcache_getitem__(self, key)

        # Double check for availability, in case missings are handled differently by any subclasses.
        if key in self:

            # Push up requests counter.
            self.__requests[key] -= 1

            # Update position.
            self.__requests.move_to_end(key)

            # Check if the threshold was reached.
            if self.__requests[key] > (-self.threshold):

                # If not, pretend the item not to have been cached yet.
                return self.__missing__(key)
            
        # Return the item. 
        return item
    
        # End of '__getitem__' #####################################################################


    # __setitem__ ##################################################################################

    def __setitem__(
        self,
        key                     : Hashable,
        value :                 ScoredItem,
        __scoredcache_setitem__ : Callable = ScoredCache.__setitem__ # Micro optimization
    ):
        
        """
        Adds an item to the cache. 
        
        Unlike regular caches, these items need to be wrapped using a `ScoredItem` object, holding
        the actual item, as well as the score attributed to this item.

        Parameters
        ----------

        key
            Key used to index the item.
        item
            Item to store, wrapped in a `CachedItem`, consisting of an item and a score.
        """
        
        # Store item.
        __scoredcache_setitem__(self, key, value)

        # Attempt to move the key to the end of the position tracker.
        try:
            self.__requests.move_to_end(key)
        # If that cannot be done, the tracker has not yet been initialized, and needs to be.
        except:
            self.__requests[key] = 0
        
        # End of '__setitem__' #####################################################################


    # __delitem__ ##################################################################################

    def __delitem__(
        self,
        key           : Hashable,
        __scoredcache_delitem__ : Callable = ScoredCache.__delitem__ # Micro optimization
    ):
        
        """
        Deletes item from the cache.

        Parameters
        ----------

        key
            Key to delete from the cache.
        """
        
        # Delete from cache.
        __scoredcache_delitem__(self, key)

        # Remove counter (and position tracker) for item.
        del self.__requests[key]

        # End of '__delitem__' #####################################################################

    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # popitem ######################################################################################

    def popitem(self) -> tuple[Hashable, Any]:

        """
        Remove and return the key of the least frequently used item, as well as the item itself.
        """

        # Attempt to retrieve the key of least recently used item
        try:
            key = next(iter(self.__requests))
        except:
            raise KeyError("%s is empty" % type(self).__name__) from None
        else:

            # Set requests counter for key beyond the threshold as to ensure that the cache does
            # not report a missing value, when we retrieve the value.
            self.__requests[key] -= self.threshold

            # Return a key-value pair.
            return (key, self.pop(key))
        
        
        # End of method 'popitem' ##################################################################
        
# End of File ######################################################################################