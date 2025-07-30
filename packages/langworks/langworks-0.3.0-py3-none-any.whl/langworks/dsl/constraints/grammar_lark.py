# ##################################################################################################
#
# Title:
#
#   langworks.dsl.constraints.lark.py
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
#   Part of the Langworks framework, implementing the lark constraint.
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
    ContainerTag
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


# Lark #############################################################################################

@dataclass
class Lark(Constraint):

    """
    A constraint specifying a 
    `Lark(-like) grammar <https://lark-parser.readthedocs.io/en/latest/index.html>`_ that the LLM 
    must conform to during generation. They may be embedded in queries as follows::

        ```
        Present the number '7' with two leading zeroes: {% lark %}
        ?start: "0" "0" NUMBER
        %import common.NUMBER
        {% endlark %}.
        ```

    Like all embeddable constraints, this contraint also accepts the default constraint arguments::

        ```
        {% lark var = "num", params = Params(temperature = 0.0) %}...{% endlark %}
        ```

    """

    # Fields #######################################################################################

    spec : str = field(default = None)
    """
    The Lark(-like) grammar that the generated content must conform to.
    """

    # End of class 'Lark' ##########################################################################


# LarkRepr #########################################################################################

@dataclass(frozen = True)
class LarkRepr(ConstraintRepr):

    """
    Intermediate representation of :py:class:`Lark`.
    """

    # Fields #######################################################################################

    spec : str = field(default = None)
    """
    Analog to :py:attr:`Lark.spec`.
    """


    # Methods ######################################################################################

    @staticmethod
    def instantiate(repr : type["LarkRepr"]) -> Lark:
        return Lark(spec = repr.spec, var = repr.var, params = repr.params)
    
        # End of method 'instantiate' ##############################################################


    # End of class 'LarkRepr' ######################################################################


# LarkTag ##########################################################################################
    
class LarkTag(ContainerTag):

    """
    Implements a Jinja-tag for constructing constraints using a 
    `Lark(-like) grammar <https://lark-parser.readthedocs.io/en/latest/index.html>`_.
    """

    # ##############################################################################################
    # Class attributes
    # ##############################################################################################

    tags = {"lark"}


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # render #######################################################################################

    def render(self, var : str = None, params : SamplingParams = None, caller = None):

        return create_and_cache(
            LarkRepr , 
            spec     = str(caller()).encode(), 
            var      = var, 
            params   = params
        )
    
        # End of method 'render' ###################################################################
    
    # End of class 'LarkTag' #######################################################################

# End of File ######################################################################################