# ##################################################################################################
#
# Title:
#
#   langworks.dsl.constraints.dataclass.py
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
#   Part of the Langworks framework, implementing the choice constraint.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard libary ###########################################################################

# Fundamentals
import dataclasses
from dataclasses import (
    dataclass,
    field
)

import typing
from typing import (
    Any,
    Callable
)

# Utilities
import json


# Third party ######################################################################################

# jinja2_simple_tags (Mihail Mishakin)
from jinja2_simple_tags import (
    StandaloneTag
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

from langworks.util.json import (
    cast_json_as_cls,
    json_dict_schema_from_cls,
    DataclassType,
    TypedDictType
)


# ##################################################################################################
# Classes
# ##################################################################################################

# Dataclass ########################################################################################

@dataclass
class Dataclass(Constraint):

    """
    A constraint enforcing a JSON-schema as drawn up from the :py:deco:`dataclasses.dataclass` or 
    :py:class:`typing.TypedDict` subclass passed. After acquiring generated output, it automatically
    cast this output to an object of the given class.
     
    This constraint may be applied as follows::

        ```
        {% dataclass cls, var = "data" %}.
        ```

    With `cls` referring to a dataclass or TypedDict as passed to the context.

    As subclass of :py:class:`~langworks.dsl.constraints.base.Constraint`, any of the default
    arguments may also be passed::

        ```
        The answer is {% dataclass cls, var = "data", params = Params(max_tokens = 1) %}
        ```
    """

    # ##############################################################################################
    # Fields
    # ##############################################################################################

    spec : DataclassType | TypedDictType = field(default = None)
    """
    The list of options that the LLM may choose from.
    """

    schema : dict = field(default = None)
    """
    The class stored in :py:attr:`spec`, but represented as a JSON schema, stored in a Python dict.
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

    finalize : Callable[[type["Dataclass"], str], Any] = (
        lambda self, response: (
            cast_json_as_cls(
                (json.loads if self.repair else json_repair.loads)(response), 
                self.spec
            )
        )
    )

    # End of class 'Dataclass' #####################################################################


# DataclassRepr ####################################################################################

@dataclass(frozen = True)
class DataclassRepr(ConstraintRepr):

    """
    Intermediate representation of :py:class:`Dataclass`.
    """

    # Fields #######################################################################################

    spec : DataclassType | TypedDictType = field(default = None)
    """
    Analog to :py:attr:`Dataclass.spec`.
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
    def instantiate(repr : type["DataclassRepr"]) -> Dataclass:

        return Dataclass(
            spec   = repr.spec, 
            schema = json_dict_schema_from_cls(repr.spec),
            var    = repr.var, 
            params = repr.params,
            repair = repr.repair
        )
    
        # End of method 'instantiate' ##############################################################


    # End of class 'DataclassRepr' #################################################################


# DataclassTag #####################################################################################

class DataclassTag(StandaloneTag):

    """
    Implements a Jinja-tag for constructing constraints prescribing a JSON-schema as defined by a
    :py:deco:`dataclasses.dataclass` or :py:class:`typing.TypedDict`.
    """

    # ##############################################################################################
    # Class attributes
    # ##############################################################################################

    tags = {"dataclass"}


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # render #######################################################################################

    def render(
        self, 
        cls    : DataclassType | TypedDictType , 
        var    : str                           = None , 
        params : SamplingParams                = None ,
        repair : bool                          = False
    ):

        # Check validity of the passed content.
        if not (dataclasses.is_dataclass(cls) or typing.is_typeddict(cls)):

            raise ValueError(
                f"Object of type '{type(cls)}' was passed for 'cls'-argument of dataclass-tag"
                f" where list-like or iterable was expected;"
            )

        # Delegate
        return create_and_cache(
            DataclassRepr, 
            spec   = cls, 
            var    = var, 
            params = params, 
            repair = repair
        )
    
        # End of method 'render' ###################################################################
    
    # End of class 'DataclassTag' ##################################################################


# End of File ######################################################################################