# ##################################################################################################
#
# Title:
#
#   langworks.query.py
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
#   Part of the Langworks framework, implementing the Query class, wrapping the logic for
#   accessing an external generative AI.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from typing import (
    Any,
    Sequence
)


# Third-party ######################################################################################

# pypeworks (Rosaia)
from pypeworks import (
    Node
)

from pypeworks.typing import (
    Args,
    Param
)


# Local ############################################################################################

from langworks.messages import (
    Thread
)

from langworks.middleware.generic import (
    Middleware,
    SamplingParams
)

import langworks.config
import langworks.util.string


# ##################################################################################################
# Classes
# ##################################################################################################

# Query ############################################################################################

class Query(Node):

    """
    A `Query` is a specialised Pypeworks Node wrapping a templatable prompt that may be passed to a
    LLM.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
        self,
        query                 : str,
        role                  : str | None                  = None,
        guidance              : str | None                  = None,
        history               : Thread | None               = None,
        ignore_history        : bool                        = False,
        context               : dict | None                 = None,
        ignore_context        : bool | Sequence[str] | None = None,
        include_in_output     : Sequence[str] | None        = None,
        middleware            : Middleware | None           = None,
        clean_multiline       : bool | None                 = None,
        **kwargs
    ):
        
        """
        Sets up a `Query` object, wrapping a query stated by a human, as well as any guidance to
        pass to a LLM when prompted with this query. A `Query` object can be used standalone or in
        conjunction with a `Langwork`.

        Parameters
        ----------

        query
            The query to prompt the LLM with, optionally formatted using Langworks' static DSL.

        role
            The role of the agent stating this query, usually 'user', 'system' or 'assistant'.

        guidance
            Template for the message to be generated, formatted using Langworks' dynamic DSL.

        history 
            Conversational history (thread) to prepend to the prompt when no such history is
            available from either the input or the `Langwork`.

        ignore_history
            Flag that signals whether any preceeding conversational history should be ignored or
            not. By default this history is taken into account. If not, effectively a new 
            conversation is started, using the contents of `history` as specified for this node or
            the wrapping langwork.

        context
            Context to reference when filling in the templated parts of the `query`, `guidance` and
            `history`. In case the `Langwork` or the input also define a context, the available 
            contexts are merged. When duplicate attributes are observed, the value is copied from 
            the most specific context, i.e. input context over `Query` context, and `Query` context
            over `Langwork` context.

        ignore_context
            Controls how contexts passed by argument are handled. By default any context passed
            overwrites the keys set by `Query` and :py:class:`Langwork`. However, when 
            `ignore_context` is set, `Query` blocks this overwriting behaviour, instead maintaining
            the context as previously specified. When `ignore_context` is set to `True` none of the 
            priorly specified keys may be overwritten. Alternatively, if a sequence of keys is
            passed, only those keys passed are protected from overwriting.

        include_in_output
            Controls what items from contexts processed are included in the output generated by
            :py:meth:`Query.exec`. By default, when set to `None`, only a limited context is 
            returned, consisting of the context gathered from the input and the result. However,
            optionally a list of keys may be specified of keys to include in the output, including
            those added through `context`. 
        
        middleware
            The middleware used to connect to the LLM. If not defined, the Langwork's middleware is 
            used instead.

        clean_multiline
            Flag that controls whether or not :py:class:`~langworks.Query` automatically applies 
            :py:func:`~langworks.util.clean_multiline` to any `query` and `guidance` arguments 
            passed. Overrides whatever value :py:attr:`langworks.config.CLEAN_MULTILINE` is set to.

            .. versionadded:: 0.2.0

        kwargs
            Any additional arguments to pass to the underlying Pypeworks `Node`.
        """

        # Initialize attributes ####################################################################

        # Argument passthrough
        self.query                 : str                         = query
        self.role                  : str | None                  = role
        self.guidance              : str | None                  = guidance
        self.history               : Thread | None               = history
        self.ignore_history        : bool                        = ignore_history
        self.context               : dict | None                 = context
        self.ignore_context        : bool | Sequence[str] | None = ignore_context
        self.include_in_output     : Sequence[str] | None        = include_in_output
        self.middleware            : Middleware | None           = middleware

        # Pre-initialization
        from .langwork import Langwork
        self.parent                : Langwork = None # Assigned by Langwork


        # Post-processing ##########################################################################

        # Handle multiline cleaning.
        if (
            clean_multiline is True
            or (clean_multiline is None and langworks.config.CLEAN_MULTILINE is True)
        ):
        
            self.query = langworks.util.string.clean_multiline(self.query) 

            if self.guidance is not None:
                self.guidance = langworks.util.string.clean_multiline(self.guidance)

            if self.history is not None:

                for message in history:
                    message["content"] = langworks.util.string.clean_multiline(message["content"])
            

        # Invoke super class #######################################################################

        super().__init__(self.exec, **kwargs)


        # End of method '__init__' #################################################################
    

    # ##############################################################################################
    # Methods
    # ##############################################################################################
    
    def exec(
        self, 
        input   : Any | None            = None,
        history : Thread | None         = None, 
        context : dict | None           = None, 
        params  : SamplingParams | None = None, 
        **kwargs
    ) -> Args[Param[Thread, "history"], Param[dict, "context"]]:

        """
        Takes the given history and context, combines it with the histories and contexts included as
        part of the specification of the `Node` and `Langwork`, and forwards it to the middleware, 
        which feeds it to a LLM to generate a response. When a response can be required, a new 
        thread - `history` - is drawn up, consisting of processed historic messages, as well as the 
        message generated by the LLM. Alongside, a new `context` is returned, containing any named 
        generated content as specificied by the DSL included in the node's `guidance`.

        Parameters
        ----------

        input
            Any anonymous input passed to this node, to be included in the context under the key
            'input'.

        history
            Conversational history (thread) to prepend to the prompt. This history supersedes any
            history specified by the `Node` or `Langwork`, unless either was instructed to ignore
            the histories provided by inputs or nodes (`ignore_history=True`).

        context
            Context used by Langwork's DSL to fill in any templated parts of any queries, history
            or guidance included in the prompt passed to the LLM. In case the `Node` or `Langwork`
            also define a context, the available contexts are merged. When duplicate attributes are
            observed, the value is copied from the most specific context, i.e. input context over 
            `Query` context, and `Query` context  over `Langwork` context.

        params
            Sampling parameters, wrapped by a `SamplingParams` object, specifying how the LLM should
            select subsequent tokens.

        kwargs 
            Any key-value arguments to be passed as additional context for use in Langworks' DSL.
        
        """

        # ##########################################################################################
        # Preparation
        # ##########################################################################################

        # Pre-define variables #####################################################################

        # complete_context: context used by Langwork's DSL.
        complete_context : dict[str, Any] = None

        # local_history: list of preceeding messages to pass to the model.
        local_history : Thread = None


        # Combine arguments with predefined values #################################################

        # Merge contexts provided by the langwork, the node and the input.
        complete_context = {
            # parent (Langwork), ignorables 
            **(
                self.parent.context if (
                    self.parent is not None and self.parent.context is not None
                ) else {}
            ),
            # self (Query), ignorables
            **(self.context if self.context is not None else {}),
            # context
            **(context or {}),
            # kwargs
            **kwargs,
            # input
            **({"input": input} if input else dict()),
            # self (Query), protected
            **({
                key: self.context[key] 
                for key in (
                    [] if self.ignore_context in [False, None]
                    else self.context.keys() if isinstance(self.ignore_context, bool) # True
                    else self.ignore_context
                ) 
                if key in self.context
            } if self.context is not None else {}),
            # parent (Langwork), protected
            **({
                key: self.parent.context[key] 
                for key in (
                    [] if self.parent.ignore_context in [False, None]
                    else self.parent.context.keys() if isinstance(self.parent.ignore_context, bool)
                    else self.parent.ignore_context
                ) 
                if key in self.context
            } if self.parent is not None and self.parent.context is not None else {})
        }

        # Select most specific history available.
        local_history = (
            # Default to system messages if Langwork was set to ignore histories.
            (
                self.parent.system_msg or []
            )
            if self.parent is not None and self.parent.ignore_history is True
            # Otherwise pass history provided by Query or input.
            else (
                # Return history provided by Query if it was set to ignore input histories, or if
                # the input provided no history.
                (
                    # Prepend system messages.
                    (
                        self.parent.system_msg 
                        if self.parent is not None 
                        else []
                    )
                    # Add messages from history provided by Query.
                    + (
                        self.history or []
                    )
                )
                if self.ignore_history or history is None
                # Otherwise default to history provided by input.
                else (
                    history or []
                )
            )
        )


        # Get handle on middleware #################################################################

        # Get middleware
        middleware : Middleware = (
            self.middleware
            or (self.parent.middleware if self.parent is not None else None)
        )

        # Raise error if no handle was obtained.
        if middleware is None:
            
            raise RuntimeError(
                "Neither the query nor the langwork specified middleware to communicate with a LLM;"
                " input cannot be processed;"
            )
        

        # ##########################################################################################
        # Forward to middleware, and return result.
        # ##########################################################################################

        # Get response.
        result_history, result_context = (
            middleware.exec(
                self.query, self.role, self.guidance, local_history, complete_context, params
            )
        )

        # Return result.
        return (

            # history
            result_history,
            
            # context
            {
                # Select inputs to include in resulting context.
                **{
                    key: complete_context[key]
                    for key in {
                        "input", 
                        *(kwargs.keys()), 
                        *(self.include_in_output if self.include_in_output is not None else ())
                    }
                    if key in complete_context
                },

                # Results always overwrite all prior context inputs.
                **result_context
            }

        )
    

        # End of method 'exec' #####################################################################

# End of File ######################################################################################