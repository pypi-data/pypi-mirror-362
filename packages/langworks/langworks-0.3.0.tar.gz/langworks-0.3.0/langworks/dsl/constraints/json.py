# ##################################################################################################
#
# Title:
#
#   langworks.dsl.constraints.json.py
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
#   Part of the Langworks framework, implementing the json constraint.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard libary ###########################################################################

# Fundamentals
from dataclasses import (
    dataclass,
    field
)

from typing import (
    Any,
    Callable
)

# Utilities
import json


# Third party ######################################################################################

# jinja2_simple_tags (Mihail Mishakin)
from jinja2_simple_tags import (
    ContainerTag
)

# json-repair
try:
    import json_repair

except:

    class json_repair():
        @staticmethod
        def loads(self, *args, **kwargs):
            raise ImportError(
                "JSON cannot be processed while repair=True and json-repair is unavailable;"
            )


# Langworks ########################################################################################

from langworks.dsl.constraints.base import (
    Constraint,
    ConstraintRepr
)

from langworks.dsl.constraints.cache import (
    create_and_cache
)

from langworks.middleware.generic import (
    SamplingParams
)


# ##################################################################################################
# Classes
# ##################################################################################################

# JSON #############################################################################################

@dataclass
class JSON(Constraint):

    """
    A constraint specifying a JSON-schema that the LLM must conform to during generation. They may 
    be embedded in queries as follows::

        ```
        Ada Lovelace's personal profile can be represented in JSON as follows: 
        {% json %}
            {
                "title": "Profile",

                "type": "object",

                "properties": {
                
                    "first_name": {
                        "title": "First name",
                        "type": "string"
                    },

                    "last_name": {
                        "title": "Last name",
                        "type: "string
                    }

                },

                "required": ["first_name", "last_name"]
            }
        {% endjson %}.
        ```

    Additional constraints may be passed::

        ```
        {% json var = "profile", params = Params(temperature = 0.0) %}...{% endjson %}
        ```
    """

    # ##############################################################################################
    # Fields
    # ##############################################################################################

    spec : dict = field(default = None)
    """
    The JSON schema that specifies the constraint.
    """

    repair : bool = field(default = False)
    """
    Controls whether any malformed JSON returned by the LLM is (attempted to be) repaired.

    .. note::
        This feature requires installation of the 
        `json-repair <https://github.com/mangiucugna/json_repair>`_ package.

    .. versionadded:: 0.3.0
    """


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    finalize : Callable[[type["JSON"], str], Any] = (
        lambda self, response: (
            (json.loads if self.repair is False else json_repair.loads)(response)
        )
    )
    

    # End of class 'JSON' ##########################################################################


# JSONRepr #########################################################################################

@dataclass(frozen = True)
class JSONRepr(ConstraintRepr):

    """
    Intermediate representation of a JSON-based constraint.
    """

    # Fields #######################################################################################

    spec : str = field(default = None)
    """
    The JSON schema that specifies the constraint, as string.
    """

    repair : bool = field(default = False)
    """
    Controls whether any malformed JSON returned by the LLM is (attempted to be) repaired.

    .. note::
        This feature requires installation of the 
        `json-repair <https://github.com/mangiucugna/json_repair>`_ package.

    .. versionadded:: 0.3.0
    """

    # Methods ######################################################################################

    @staticmethod
    def instantiate(repr : type["JSONRepr"]) -> type["JSON"]:
        return JSON(
            spec = json.loads(repr.spec), 
            var = repr.var, 
            params = repr.params, 
            repair = repr.repair
        )
    
        # End of method 'instantiate' ##############################################################


    # End of class 'JSONRepr' ######################################################################


# JsonTag ##########################################################################################
    
class JSONTag(ContainerTag):

    """
    Implements a Jinja-tag for constructing constraints using a JSON schema.
    """

    # ##############################################################################################
    # Class attributes
    # ##############################################################################################

    tags = {"json"}


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # render #######################################################################################

    def render(
        self, 
        var : str = None, 
        params : SamplingParams = None, 
        repair = False, 
        caller = None
    ):

        return create_and_cache(
            JSONRepr , 
            spec    = json.dumps( json.loads(str(caller())) ), 
            var     = var, 
            params  = params,
            repair  = repair
        )
    
        # End of method 'render' ###################################################################
    
    
    # End of class 'JSONTag' #######################################################################


# End of File ######################################################################################