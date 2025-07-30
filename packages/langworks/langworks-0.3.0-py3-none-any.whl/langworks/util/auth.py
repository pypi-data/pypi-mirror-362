# ##################################################################################################
#
#  Title
#
#   langworks.util.auth.py
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
#    Part of the Langworks framework, implementing various utilities for dealing with 
#    authentication against LLM providers.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from dataclasses import (
    dataclass,
    field
)

from typing import (
    Callable
)


# Local ############################################################################################

# vectorworks.retrievers
from langworks.middleware.generic import (
    Middleware
)


# ##################################################################################################
# Classes
# ##################################################################################################

# AuthenticationDetails ############################################################################

@dataclass
class AuthenticationDetails:

    """
    Holds authentication details that may be retrieved by an :py:type:`Authenticator`.
    """

    username : str | None = field(default = None)
    """
    Username with which to authenticate against the LLM provider.
    """

    password : str | None = field(default = None)
    """
    Password with which to authenticate against the LLM provider.
    """

    token    : str | None = field(default = None)
    """
    Access token with which to authenticate against the LLM provider.
    """

    # End of dataclass 'AuthenticationDetails' #####################################################


# ##################################################################################################
# Types
# ##################################################################################################

# Authenticator ####################################################################################

type Authenticator = Callable[[Middleware], AuthenticationDetails]
"""
Callable invoked by an :py:class:`~langworks.middleware.generic.Middleware` when seeking access to 
an external resource.
"""


# ##################################################################################################
# Functions
# ##################################################################################################

# UsernameCredentials ##############################################################################

def UsernameCredentials(username : str, password : str | None = None) -> AuthenticationDetails:

    """
    Generates an :py:type:`Authenticator` that generates authentication details with the given
    username and password.

    Parameters
    ----------

    username
        Username with which to authenticate against the LLM provider.

    password
        Password with which to authenticate against the LLM provider.
    """

    return lambda _: AuthenticationDetails(username, password)

    # End of function 'UsernameCredentials' ########################################################


# TokenCredentials #################################################################################

def TokenCredentials(token : str = None)  -> AuthenticationDetails:

    """
    Generates an :py:type:`Authenticator` that generates authentication details with the given
    token

    Parameters
    ----------

    token
        Token with which to authenticate against the LLM provider.
    """

    return lambda _: AuthenticationDetails(token = token)

    # End of function 'TokenCredentials' ###########################################################

# End of File ######################################################################################