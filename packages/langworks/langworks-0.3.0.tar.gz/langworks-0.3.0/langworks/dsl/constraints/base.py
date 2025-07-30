# ##################################################################################################
#
# Title:
#
#   langworks.dsl.constraints.base.py
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
#   Part of the Langworks framework, implementing base classes necessary to define a constraint 
#   within Langworks' DSL. 
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

# Langworks ########################################################################################

from langworks.middleware.generic import (
    SamplingParams
)


# ##################################################################################################
# Classes
# ##################################################################################################

# Constraint #######################################################################################

@dataclass
class Constraint:

    """
    Specifies a generic constraint on the generation by an LLM, to be processed by a
    :py:class:`~langworks.middleware.generic.Middleware`. Any constraint implemented needs to
    sub-class from this constraint.
    """

    # ##############################################################################################
    # Fields
    # ##############################################################################################

    spec    : Any                            = field(default = None)
    """
    The specification of the constraint.
    """

    var     : str | None                     = field(default = None)
    """
    Name of the variable used to store the content.
    """

    params  : SamplingParams                 = field(default = None)
    """
    Sampling parameters to apply when generating the content specified by this constraint.
    """


    # ##############################################################################################
    # Methods
    # ##############################################################################################

    # finalize #####################################################################################

    finalize : Callable[[type["Constraint"], str], Any] | None = field(default = None)
    """
    Invoked by :py:class:`~langworks.middleware.generic.Middleware` upon generation of the text
    specified by the constraint, allowing for post-processing of the output, and inclusion of the
    output in the DSL's context.
    """

    # End of class 'Constraint' ####################################################################


# ConstraintRepr ###################################################################################

@dataclass(frozen = True)
class ConstraintRepr:

    """
    Generic class implementing an intermediate representation of a generation constraint. This 
    intermediate representation is generated when a constraint tag is initially parsed by Jinja.
    This is done to make available the data passed to the tag outside the Jinja rendering process.
    
    """

    # Fields #######################################################################################

    spec    : Any                            = field(default = None)
    """
    Analog to :py:attr:`Constraint.spec`.
    """

    var     : str | None                     = field(default = None)
    """
    Analog to :py:attr:`Constraint.var`.
    """

    params  : SamplingParams                 = field(default = None)
    """
    Analog to :py:attr:`Constraint.params`.
    """


    # Methods ######################################################################################

    @staticmethod
    def instantiate(repr : type["ConstraintRepr"]) -> Constraint:

        """
        May be invoked to convert the intermediate representation to an actual Constraint object.
        """

        raise NotImplementedError()
    
        # End of method 'instantiate' ##############################################################

    # End of class 'ConstraintRepr' ################################################################


# End of File ######################################################################################