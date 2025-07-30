# ##################################################################################################
#
# Title:
#
#   langworks.dsl.constraints.gen.py
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
#   Part of the Langworks framework, implementing the gen constraint.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard libary ###########################################################################

# Fundamentals
from dataclasses import (
    dataclass
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



# Gen ##############################################################################################

@dataclass
class Gen(Constraint):

    """
    A non-constraint, actually specifying no restriction on generation, instead instructing the LLM
    to generate as it sees fit. They may be embedded in queries as follows::

        ```
        Today I'm feeling {% gen %}
        ```

    As subclass of :py:class:`~langworks.dsl.constraints.base.Constraint`, any of the default
    arguments may also be passed::

        ```
        Today I'm feeling {% gen var = "answer", params = Params(max_tokens = 1) %}.
        ```
    """

    pass # No additions

    # End of class 'Gen' ###########################################################################


# GenRepr ##########################################################################################

@dataclass(frozen = True)
class GenRepr(ConstraintRepr):

    """
    Intermediate representation of :py:class:`Gen`.
    """

    # Fields #######################################################################################

    # No additions.


    # Methods ######################################################################################

    @staticmethod
    def instantiate(repr : type["GenRepr"]) -> Gen:
        return Gen(spec = None, var = repr.var, params = repr.params)
    
        # End of method 'instantiate' ##############################################################


    # End of class 'GenRepr' #######################################################################
    

# GenTag ###########################################################################################

class GenTag(StandaloneTag):

    """
    Implements a Jinja-tag for constructing non-constraints, constraints that actually specify no
    content-wise restrictions for generation. They may be embedded in queries as follows::

        ```
        Today I'm feeling {% gen %}
        ```

    Any of the default constraint arguments may be passed, however::

        ```
        Today I'm feeling {% gen var = "answer", params = Params(max_tokens = 1) %}.
        ```
    """

    # ##############################################################################################
    # Class attributes
    # ##############################################################################################

    tags = {"gen"}


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    def render(self, var : str = None, params : SamplingParams = None):
        return create_and_cache(GenRepr, spec = None, var = var, params = params)
    
    # End of class 'GenTag' ########################################################################


# End of File ######################################################################################