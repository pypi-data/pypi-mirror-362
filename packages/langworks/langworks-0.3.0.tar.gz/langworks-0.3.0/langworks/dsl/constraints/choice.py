# ##################################################################################################
#
# Title:
#
#   langworks.dsl.constraints.choice.py
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
from dataclasses import (
    dataclass,
    field
)


# Third party ######################################################################################

# jinja2_simple_tags (Mihail Mishakin)
from jinja2_simple_tags import (
    StandaloneTag
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

# Choice ###########################################################################################

@dataclass
class Choice(Constraint):

    """
    Specifies a limited list of options the LLM may choose from during generation.

    In its minimal form, the constraint can be applied as follows::

        ```
        The sentiment is: {% choice ["positive", "negative"] %}.
        ```

    As subclass of :py:class:`~langworks.dsl.constraints.base.Constraint`, any of the default
    arguments may also be passed::

        ```
        The answer is {% 
            choice ["positive", "negative"], var = "sentiment", params = Params(max_tokens = 1) 
        %}
        ```
    """

    # Fields #######################################################################################

    spec : tuple[str] = field(default = None)
    """
    The list of options that the LLM may choose from.
    """

    # End of class 'Choice' ########################################################################


# ChoiceRepr #######################################################################################

@dataclass(frozen = True)
class ChoiceRepr(ConstraintRepr):

    """
    Intermediate representation of :py:class:`Choice`.
    """

    # Fields #######################################################################################

    spec : tuple[str] = field(default = None)
    """
    Analog to :py:attr:`Choice.spec`.
    """


    # Methods ######################################################################################

    @staticmethod
    def instantiate(repr : type["ChoiceRepr"]) -> Choice:
        return Choice(spec = repr.spec, var = repr.var, params = repr.params)
    
        # End of method 'instantiate' ##############################################################


    # End of class 'ChoiceRepr' ####################################################################


# ChoiceTag ########################################################################################

class ChoiceTag(StandaloneTag):

    """
    Implements a Jinja-tag for constructing constraints prescribing a limited list of choices. 
    """

    # ##############################################################################################
    # Class attributes
    # ##############################################################################################

    tags = {"choice"}


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # render #######################################################################################

    def render(self, options : list[str], var : str = None, params : SamplingParams = None):

        # Check validity of the passed content.
        if not (hasattr(options, "__len__") or hasattr(options, "__iter__")):

            raise ValueError(
                f"Object of type '{type(options)}' was passed for 'options'-argument of choice-tag"
                f" where list-like or iterable was expected;"
            )

        for i, option in enumerate(options):

            if not isinstance(option, str):

                raise ValueError(
                    f"Object of type '{type(option)}' was passed for 'options'-argument at index"
                    f" '{i}' where type 'string' was expected;"
                )

        # Delegate
        return create_and_cache(
            ChoiceRepr, spec = tuple(options), var = var, params = params
        )
    
        # End of method 'render' ###################################################################
    
    # End of class 'ChoiceTag' #####################################################################


# End of File ######################################################################################