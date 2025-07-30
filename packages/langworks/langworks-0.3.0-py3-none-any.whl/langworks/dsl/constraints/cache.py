# ##################################################################################################
#
# Title:
#
#   langworks.dsl.constraints.py
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
#   Part of the Langworks framework, implementing various constraints to guide LLM generation.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Third party ######################################################################################

# cachetools (Thomas Kemmer)
import cachetools


# Local ############################################################################################

from langworks.dsl.constraints.base import (
    ConstraintRepr
)


# ##################################################################################################
# Globals
# ##################################################################################################

cache : cachetools.LRUCache[int, ConstraintRepr] = cachetools.LRUCache(maxsize = 256)
"""Cache of constraint objects indexed by the hashes of these objects."""


# ##################################################################################################
# Functions
# ##################################################################################################

# create_and_cache #################################################################################

def create_and_cache(cls : type[ConstraintRepr], *args, **kwargs):

    """
    Creates an intermediate representation using the given class, to be initialized with the passed
    arguments, caching the object, and return an escaped hash to access said object.
    """

    # Create an object for intermediate representation.
    obj = cls(*args, **kwargs)

    # Acquire hash of the object.
    try:

        # Try to hash the object.
        _hash = hash(obj)

    except:

        # If it fails, the object is mutable, and needs to be converted to a string before hashing.
        _hash = hash(str(obj))

    # Add object to cache.
    global cache
    cache[_hash] = obj

    # Return formatted reference.
    return f"|% {_hash} %|"

    # End of function 'create_and_cache' ###########################################################

# End of File ######################################################################################