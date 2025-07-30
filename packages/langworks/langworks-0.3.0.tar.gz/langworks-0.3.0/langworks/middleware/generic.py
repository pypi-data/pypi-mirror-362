 # ##################################################################################################
#
# Title:
#
#   langworks.middleware.generic.py
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
#   Part of the Langworks framework, implementing various generic classes for use by middlewares.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
import dataclasses
from dataclasses import (
    dataclass,
    field
)

import functools

import typing
from typing import (
    Any
)


# Local ############################################################################################

from langworks.messages import (
    Thread
)


# ##################################################################################################
# Functions
# ##################################################################################################

# get_dataclass_defaults ###########################################################################

@functools.cache
def get_dataclass_defaults(cls : dataclass) -> dict[str, Any]:

    """
    Utility function used to draw up a lookup map for the default values of the fields of a 
    dataclass.
    """

    return {
        # Index by field name.
        field.name: (
            # Get default value or use default factory to create a new default instance.
            field.default 
            if field.default is not None
            else (
                field.default_factory() 
                if not isinstance(field.default_factory, dataclasses._MISSING_TYPE)
                else None
            )
        )
        # Iterate over all fields.
        for field in dataclasses.fields(cls)
        # But only the fields that are initialized and comparable.
        if field.init == True and field.compare == True
    }

    # End of function 'get_dataclass_defaults' #####################################################


# ##################################################################################################
# Classes
# ##################################################################################################

# SamplingParams ###################################################################################

@dataclass(frozen = True)
class SamplingParams:

    """
    Generic class used to specify with which sampling parameters a prompt should be processed.
    """

    # Stopping #####################################################################################

    max_tokens         : int            = field(default = None)
    """
    The number of tokens that may be generated per generation.
    """

    stop               : list[str]      = field(default = None)
    """
    List of character sequences, which if generated stop further generation.
    """

    include_stop       : bool           = field(default = True)
    """
    Flag that controls whether stop sequences are included in the output.
    """

    ignore_eos         : bool           = field(default = False)
    """
    Flag that controls whether or not generation should continue after the End of Sequence (EOS) 
    token has been generated.
    """


    # Randomization ################################################################################

    temperature        : float          = field(default = 1.0)
    """
    A number between 0.0 and 2.0, with higher values increasing randomization, whereas lower values 
    encourage deterministic output.
    """

    top_p              : float          = field(default = 1.0)
    """
    A number between `0.0` and `1.0`, specifying what is considered a top  percentile, constraining 
    the selection of tokens to tokens with probabilities considered among these top percentiles. For 
    example, when `0.2` is specified, a selection is made from the tokens with probabilities among 
    the top 20 percentiles.
    """

    min_p              : float          = field(default = 0.0)
    """
    A number between `0.0` and `1.0`, specifying what a token's minimal likelihood must be to be 
    considered for selection.
    """

    top_k              : int            = field(default = -1)
    """
    The number of tokens to consider when deciding on the next token when generating.
    """

    logit_bias         : dict[int, int] = field(default = None)
    """
    A dictionary indexed by encoded tokens, each assigned a number between -100 and 100 controlling 
    the likelihood that a specific token is selected or ignored, with a positive number increasing 
    this likelihood, whereas a negative number decreases it.
    """

    seed               : int            = field(default = None)
    """
    A number used to initialize any pseudorandom number generations that the model may used. It can 
    be used to enforce a degree of determinism even when using non-nil temperatures.
    """

    logprobs           : int            = field(default = None)
    """
    The number of tokens to generate per position in the generated sequences, ordered by 
    probability.
    """


    # Repetition ###################################################################################
    
    presence_penalty   : float          = field(default = 0.0)
    """
    A number between -2.0 and 2.0 that controls the likelihood that tokens appear that have not yet 
    appeared in the generated text, whereby a positive  coeffient increases these odds, whereas a 
    negative coefficient decreases them.
    """

    frequency_penalty  : float          = field(default = 0.0)
    """
    A number between -2.0 and 2.0 that controls the number of times a tokens appears in the 
    generated text, whereby a positive coefficient puts a constraint on repetition, whereas a 
    negative coefficient encourages repetition.
    """

    repetition_penalty : float          = field(default = 0.0)
    """
    A number between -2.0 and 2.0 that controls the degree of repetition, taking into account both 
    the generated text and the initial prompt. A positive number encourages usage of new tokens, 
    whereas a negative number favours repetition.
    """

    # End of class 'Params' ########################################################################


# Middleware #######################################################################################

class Middleware:

    """
    Generalised interface for accessing LLMs.
    """

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
        
        """
        Generate a new message, following up on the message passed using the given guidance and
        sampling parameters.

        Parameters
        ----------

        query
            The query to prompt the LLM with, optionally formatted using Langworks' static DSL.

        role
            The role of the agent stating this query, usually 'user', 'system' or 'assistant'.

        guidance
            Template for the message to be generated, formatted using Langworks' dyanmic DSL.

        history
            Conversational history (thread) to prepend to the prompt.

        context
            Context to reference when filling in the templated parts of the `query`, `guidance` and
            `history`. In case the `Langwork` or the input also define a context, the available 
            contexts are merged. When duplicate attributes are observed, the value is copied from 
            the most specific context, i.e. input context over `Query` context, and `Query` context
            over `Langwork` context.

        params
            Sampling parameters, wrapped by a `SamplingParams` object, specifying how the LLM should 
            select subsequent tokens.
        """

        raise NotImplementedError(
            f"Middleware '{self.__qualname__}' does not implement the 'exec' method;"
        )
    
        # End of method 'exec' #####################################################################

# End of File ######################################################################################