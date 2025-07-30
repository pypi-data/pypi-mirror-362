# ##################################################################################################
#
# Title:
#
#   langworks.dsl.constraints.regex.py
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
#   Part of the Langworks framework, implementing the regex constraint.
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

# Regex ############################################################################################

@dataclass
class Regex(Constraint):

    """
    A constraint specifying a regular expression that the LLM must conform to during generation.
    They may be embedded in queries as follows::

        ```
        The sentiment is: {% regex "(positive)|(negative)" %}.
        ```

    Any of the default constraint arguments may also be passed::

        ```
        The sentiment is: {% 
            regex "(positive)|(negative)", var = "sentiment", params = Params(max_tokens = 2) 
        %}
        ```
    """

    # Fields #######################################################################################

    spec : str = field(default = None)
    """
    The regular expression that specifies the constraint.
    """

    # End of class 'Regex' #########################################################################


# RegexRepr ########################################################################################

@dataclass(frozen = True)
class RegexRepr(ConstraintRepr):

    """
    Intermediate representation of :py:class:`Regex`.
    """

    # Fields #######################################################################################

    spec : str = field(default = None)
    """
    Analog to :py:attr:`Regex.spec`.
    """


    # Methods ######################################################################################

    @staticmethod
    def instantiate(repr : type["RegexRepr"]) -> type["Regex"]:
        return Regex(spec = repr.spec, var = repr.var, params = repr.params)
    
        # End of method 'instantiate' ##############################################################


    # End of class 'RegexRepr' #####################################################################


# RegexTag #########################################################################################

class RegexTag(StandaloneTag):

    """
    Implements a Jinja-tag for constructing regex-based constraints.
    """

    # ##############################################################################################
    # Class attributes
    # ##############################################################################################

    tags = {"regex"}


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # render #######################################################################################

    def render(self, regex : str, var : str = None, params : SamplingParams = None):
        return create_and_cache(RegexRepr, spec = regex, var = var, params = params)
    
        # End of method 'render' ###################################################################
    
    # End of class 'RegexTag' ######################################################################


# End of File ######################################################################################