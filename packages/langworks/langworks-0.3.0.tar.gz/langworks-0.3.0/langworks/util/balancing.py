# ##################################################################################################
#
#  Title
#
#   langworks.util.balancing.py
#
#  License
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
#  Description
#
#    Part of the Langworks framework, implementing various utilities for load balancing.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from contextlib import (
    contextmanager
)

from dataclasses import (
    dataclass,
    field
)

import operator
import threading

from typing import (
    Generic,
    Sequence,
    TypeVar
)

# Utilities
import bisect


# ##################################################################################################
# Types
# ##################################################################################################

T = TypeVar("T")


# ##################################################################################################
# Classes
# ##################################################################################################

# Resource #########################################################################################

@dataclass
class Resource(Generic[T]):

    """
    Internal class used by :py:class:`BalancedPool` wrapping a resource alongside data required to
    handle pools' internal state.
    """

    # ##############################################################################################
    # Attributes
    # ##############################################################################################

    resource  : T   = field(compare = False)
    """Reference to managed resource."""

    id        : int = field(default = -1, compare = False)
    """Copy of resource's identifier, as retrieved by :py:func:`id`."""

    workload  : int = field(default = 0, init = False)
    """Number of tasks assigned to this resource."""

    remove_at : int = field(default = -1, init = False)
    """
    States workload level at which the resource should be removed from the queue. Set by
    :py:meth:`BalancedPool.remove` and :py:meth:`BalancedPool.remove_last`. 
    """


    # End of dataclass 'Resource' ##################################################################


# BalancedPool ####################################################################################

class BalancedPool(Generic[T]):

    """
    Provides a container for similar reusable resources, managing these resources so that they are
    all utilized equally.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(self, resources : Sequence[T]):

        """
        Initializes :py:class:`BalancedPool`.

        Parameters
        ----------

        resources
            Collection of resources to add to the pool.
        """

        # Initialize members #######################################################################

        ## Public

        self.queue          : list[Resource[T]] = [Resource(r, id(r), 0) for r in resources]
        """Internal queue dynamically ordered by current workload."""

        self.queue_lock     : threading.Lock    = threading.Lock()
        """Lock to manage access to internal queue, providing thread safety."""

        self.stack          : list[Resource[T]] = [r.id for r in self.queue]
        """Internal stack keeping track of the order in which resource where added."""

        self.stack_lock     : threading.Lock    = threading.Lock() 
        """Lock to manage access to internal stack, providing thread safety."""

        ## Private

        self._workload      : int               = 0
        self._workload_lock : threading.Lock    = threading.Lock()
        

        # End of '__init__' ########################################################################


    # __len__ ######################################################################################
    
    def __len__(self):
        
        with self.stack_lock:
            return len(self.stack)
    
        # End of '__len__' #########################################################################


    # ##############################################################################################
    # Attributes
    # ##############################################################################################

    @property
    def workload(self) -> int:

        """
        Current number of tasks handled by the pool
        """

        with self._workload_lock:
            return self._workload
        
        # End of property 'workload' ###############################################################


    @property
    def workload_average(self) -> float:

        """
        Average number of tasks per resource.
        """

        with self.queue_lock, self._workload_lock:
            return self._workload / max(1, len(self.queue))
        
        # End of property 'workload' ###############################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # access #######################################################################################

    @contextmanager
    def access(self):

        """
        Context manager that retrieves one resource from the queue, automatically calling
        :py:meth:`release` after utilization of the resource has finished.
        """

        resource = self.get()

        try:
            yield resource
        finally:
            self.release(resource)


        # End of method 'access' ###################################################################

    # add ##########################################################################################

    def add(self, resource : T) -> None:

        """
        Adds a new resource to the pool.

        Parameters
        ----------

        resource
            Resource to add to the pool.
        """

        with self.queue_lock, self.stack_lock:

            # Wrap resource.
            resource_wrapped = Resource(resource, id(resource))

            # Add resource to beginning of queue, allowing for immediate utilization.
            self.queue.insert(0, resource_wrapped)

            # Add to stack to keep track of last registered resource.
            self.stack.append(resource_wrapped)

        # End of method 'put' ######################################################################


    # get ##########################################################################################

    def get(self) -> T:

        """
        Retrieves least burdened, least recently used resource from the queue.
        """

        # Micro-optimize by getting a direct reference to the internal queue.
        queue = self.queue

        # Access the internal queue.
        with self.queue_lock:

            # First, acquire the resource.
            resource = queue.pop(0)

            # Update workload.
            resource.workload += 1

            with self._workload_lock:
                self._workload += 1

            # Reinsert resource into queue to maintain its availability.
            bisect.insort_right(queue, resource, key = operator.attrgetter("workload"))

        # Return resource.
        return resource.resource
    
        # End of method 'get' ######################################################################


    # release ######################################################################################

    def release(self, resource : T) -> None:

        """
        Lowers workload associated with the resource, improving its availability when a new resource
        is requested.

        Parameters
        ----------

        resource
            Resource for which to lower the workload.

        .. important::
            All clients that retrieve a resource using :py:meth:`get`, must always call ``release``
            to ensure that the resource remains managed correctly by the pool. This may also be done
            automatically by using :py:meth:`access`'s context manager.
        """

        # Micro-optimize by getting a direct references to commonly reused data.
        resource_id = id(resource)
        queue       = self.queue

        # Access internal queue.
        with self.queue_lock:

            # Retrieve position in queue of given resource.
            try:
                idx = next(
                    i for i, r in zip( range(len(queue) - 1, -1, -1), reversed(queue) ) 
                    if r.id == resource_id
                )

            except:
                raise LookupError(f"Could not find resource '{resource}' in pool;")

            # Remove resource from queue, while getting handle on it for further relocation..
            resource_wrapped = queue.pop(idx)

            # Update resource's workload.
            resource_wrapped.workload -= 1

            with self._workload_lock:
                self._workload -= 1

            # Reinsert resource into queue to maintain its availability, if not pending removal.
            if resource_wrapped.workload > resource_wrapped.remove_at:

                bisect.insort(
                    queue, resource_wrapped, hi = idx, key = operator.attrgetter("workload")
                )


        # End of method 'release' ##################################################################


    # remove #######################################################################################

    def remove(self, resource : T) -> None:

        """
        Remove given resource from pool, preventing it from being access through the pool.
        """

        # Micro-optimize by getting a direct references to commonly reused data.
        resource_id : int = id(resource)
        queue             = self.queue
        stack             = self.stack

        # Access internal queue and stack.
        with self.queue_lock, self.stack_lock:

            # Retrieve position in stack of given resource.
            try:
                idx = next(i for i, r in enumerate(stack) if r.id == resource_id)

            except:
                raise LookupError(f"Could not find resource '{resource}' in stack;")
            
            # Remove the resource from the stack.
            resource_wrapped = stack.pop(idx)
            
            # Immediately remove resource from queue if it has no outstanding workload.
            if resource_wrapped.workload == 0:

                # Retrieve position in queue of given resource.
                try:
                    idx = next(i for i, r in enumerate(queue) if r.id == resource_id)

                except:
                    raise LookupError(f"Could not find resource '{resource}' in stack;")
                
                # Remove from queue.
                self.queue.pop(idx)

            # Otherwise configure resource for self-removal (as handled by `release`).
            else:
                resource_wrapped.remove_at = 2 ** 32 - resource_wrapped.workload
                resource_wrapped.workload  = 2 ** 2


        # End of method 'remove' ###################################################################


    # remove_last ##################################################################################

    def remove_last(self) -> None:

        """
        Removes last added resource (using :py:meth:`add`) from the pool.
        """

        # Micro-optimize by getting a direct references to commonly reused data.
        queue             = self.queue

        # Access internal queue and stack.
        with self.queue_lock, self.stack_lock:

            # Remove last resource from stack.
            resource : Resource[T] = self.stack.pop()

            # Immediately remove resource from queue if it has no outstanding workload.
            if resource.workload == 0:

                # Retrieve position in queue of given resource.
                resource_id = resource.id

                try:
                    idx = next(i for i, r in enumerate(queue) if r.id == resource_id)

                except:
                    raise LookupError(f"Could not find resource '{resource}' in stack;")
                
                # Remove from queue.
                queue.pop(idx)

            # Otherwise configure resource for self-removal (as handled by `release`).
            else:
                resource.remove_at = 2 ** 32 - resource.workload
                resource.workload  = 2 ** 2


        # End of method 'remove_last' ##############################################################


# End of File ######################################################################################