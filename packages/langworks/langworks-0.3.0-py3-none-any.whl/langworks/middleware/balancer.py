 # ##################################################################################################
#
# Title:
#
#   langworks.middleware.balancer.py
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
#   Part of the Langworks framework, implementing a middleware that helps balance workloads among
#   other middleware.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
import threading

from typing import (
    Any,
    Sequence
)


# Langworks ########################################################################################

from langworks.middleware.generic import (
    Middleware,
    SamplingParams
)

from langworks.messages import (
    Thread
)

from langworks.util.balancing import (
    BalancedPool
)


# ##################################################################################################
# Classes
# ##################################################################################################

class Balancer(Middleware):

    """
    Middleware allowing to distribute queries among other middleware, allowing for load balancing.
    Optionally, load balancing may be enhanced with autoscaling, allowing to control at what rate
    middleware are made available or unavailable.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    def __init__(
        self, 
        middleware          : Sequence[Middleware] ,
        autoscale_threshold : tuple[float, float]  = (0, 0)
        
    ):
        
        """
        Initialized the :py:class:`Balancer`.

        Parameters
        ----------

        middleware
            Instantiated middleware to which queries may be distributed, giving priority to 
            middleware specified first.

        autoscale_threshold
            Pair of thresholds specifying at what number of queries per middleware to scale up 
            (first item) or scale down (second item). By default this is set to `(0, 0)`, setting 
            the balancer up to immediately scale up to use all resources, while never scaling down.

        """

        # ##########################################################################################
        # Initialize attributes
        # ##########################################################################################

        # Argument passthrough #####################################################################

        self.middleware_available : Sequence[Middleware]     = middleware
        self.middleware_active    : BalancedPool[Middleware] = BalancedPool[Middleware]([])
        self.autoscale_threshold  : tuple[float, float]      = autoscale_threshold


        # Initialize other members #################################################################

        self.middleware_active_lock : threading.Lock           = threading.Lock()

        
        # End of '__init__' ########################################################################


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # exec #########################################################################################

    def exec(
        self, 
        query      : str                        = None,
        role       : str                        = None,
        guidance   : str                        = None,
        history    : Thread                     = None,
        context    : dict                       = None,
        params     : SamplingParams             = None
    ) -> tuple[Thread, dict[str, Any]]:
        
        with self.middleware_active_lock:

            # Locally store commonly reused data.
            middlewares_n           : int   = len(self.middleware_active)
            workload_per_middleware : float = self.middleware_active.workload_average

            # Handle cases wherein more middleware may be deployed.
            if (
                middlewares_n == 0
                or (
                    middlewares_n < len(self.middleware_available) 
                    and workload_per_middleware >= self.autoscale_threshold[0]
                )
            ):
                
                self.middleware_active.add(self.middleware_available[middlewares_n])

            # Handle cases wherein number of middleware need to be reduced.
            elif middlewares_n > 1 and workload_per_middleware < self.autoscale_threshold[1]:
                self.middleware_active.remove_last()
            
            # Retrieve client.
            middleware : Middleware = self.middleware_active.get()

        # Defer to selected middleware.
        result = middleware.exec(query, role, guidance, history, context, params)

        # Clean-up
        self.middleware_active.release(middleware)

        # Return result
        return result
        
        # End of method 'exec' #####################################################################

    # End of class 'Balancer' ######################################################################

# End of File ######################################################################################