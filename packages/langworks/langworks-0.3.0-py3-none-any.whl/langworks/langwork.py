# ##################################################################################################
#
# Title:
#
#   langworks.langwork.py
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
#   Part of the Langworks framework, implementing the Langwork class, a generic pipework based on
#   the pypework framework specifically designed for working with generative AIs.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from typing import (
    Sequence,
    TypeVar
)

# System
import logging


# Third party ######################################################################################

# pypework (Rosaia)
from pypeworks import (
    Node,
    Connection,
    Pipework
)


# Local ############################################################################################

from langworks.messages import (
    Thread
)

from langworks.middleware.generic import (
    Middleware
)

from langworks.query import (
    Query
)

import langworks.config
import langworks.util.string


# ##################################################################################################
# Classes
# ##################################################################################################

T = TypeVar("T")
R = TypeVar("R")

class Langwork(Pipework[T, R]):

    """
    A `Langwork` is a specialised pypeworks' Pipework allowing for easy access to LLMs.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
        self,

        system_msg      : Thread | None                   = None,
        ignore_history  : bool                            = False,
        context         : dict | None                     = None,
        ignore_context  : bool | Sequence[str] | None     = None,
        middleware      : Middleware | None               = None,
        clean_multiline : bool | None                     = None,

        processes       : int | None                      = None,
        logger          : logging.Logger                  = None,
        ignore_errors   : Sequence[BaseException]         = None,

        join            : bool                            = False,
        join_groupby    : Sequence[str]                   = None,
        join_flatten    : bool                            = False,

        connections     : list[Connection]                = [],
        **nodes         : Query | type["Langwork"] | Node
    ):
        
        """
        Sets up a `Langwork` object, a generic pipework based on the pypeworks framework designed
        specifically to query generative AIs.

        Parameters
        ----------

        system_msg
            System messages to prepend to any history provided by a `Query`. When the input 
            specifies a specific history, the system messages are *not* prepended.

        ignore_history
            Flag that signals whether any history provided by `Query` or input should be ignored.
            By default these histories are taken into account. If set to `True`, these histories are
            ignored, and each prompt starts with the given system messages, as if starting a new 
            thread.

        context
            Context used by Langworks' DSL to fill in any templated parts of any queries, history 
            or guidance included in the prompt passed to the LLM. In case the `Query` or `Langwork` 
            also define a context, the available contexts are merged. When duplicate attributes are
            observed, the value is copied from the most specific context, i.e. input context over 
            `Query` context, and `Query` context  over `Langwork` context.

        ignore_context
            Controls how contexts passed by argument are handled. By default contexts specified by
            `Langwork` may be overwritten by :py:class:`langworks.query.Query` or contexts passed
            by argument. However, when `ignore_context` is set, `Langwork` blocks this behaviour,
            instead maintaining the context as specified by `Langwork`. When `ignore_context` is set
            to `True` none of the keys specified by `Langwork` may be overwritten. Alternatively, if
            a sequence of keys is passed, only the keys specified are protected from overwriting. 

        middleware
            The middleware used to connect to the LLM. If not defined, the framework will try to use
            any middlewares included in the specifications of individual `Query` objects.

        clean_multiline
            Flag that controls whether or not :py:class:`~langworks.Langwork` applies
            :py:func:`~langworks.util.clean_multiline` to the messages of `system_msg`. Overrides 
            whatever value :py:attr:`langworks.config.CLEAN_MULTILINE` is set to.

            .. note::
                This behaviour is only applied to the system messages directly supplied to this
                instance. Any nested nodes are subject to behaviour as locally configured or 
                prescribed by :py:attr:`langworks.config.CLEAN_MULTILINE`.

            .. versionadded:: 0.2.0

        processes
            The number of worker processes to use to operate the `Langwork`. By default this number 
            is equal to the number of logical CPUs in the system.

        connections
            Specification of connections in the langwork. See pypework's documentation for further 
            information.

        logger
            Logger compatible with Python's 
            `logging <https://docs.python.org/3/library/logging.html>`_ module, providing control 
            over the registration of events occuring within the langwork.

            .. versionadded:: 0.1.1

        ignore_errors
            Sequence of errors (and exceptions), which if raised, are ignored by the Langwork,
            allowing it to continue execution.

            .. versionadded:: 0.1.1

        join
            Whether to join all received data together before processing it. 
        
            Analog to pypeworks' 
            `Node.__init__ <https://rosaia.github.io/pypeworks/api/node.html#pypeworks.Node.__init__>`_
            `join` argument

            .. versionadded:: 0.1.2.

        join_groupby
            Parameters by which to group the inputs for the other parameters. 

            Analog to pypeworks' 
            `Node.__init__ <https://rosaia.github.io/pypeworks/api/node.html#pypeworks.Node.__init__>`_
            `join_groupby` argument

            .. versionadded:: 0.1.2.

        join_flatten
            Flag that indicates whether any grouped input should be flattened or not. 

            Analog to pypeworks' 
            `Node.__init__ <https://rosaia.github.io/pypeworks/api/node.html#pypeworks.Node.__init__>`_
            `join_flatten` argument

            .. versionadded:: 0.1.2.

        nodes
            Nodes to embed in the langwork, including 'Query' and 'Langwork' objects.
        """

        # Initialize attributes ####################################################################

        # Argument passthrough
        self.system_msg     : Thread | None        = system_msg
        self.ignore_history : bool                 = ignore_history
        self.context        : dict | None          = context
        self.ignore_context : bool | Sequence[str] = ignore_context 
        self.middleware     : Middleware | None    = middleware

        # Finish initialization of any queries passed.
        for node in nodes.values():
            
            if isinstance(node, Langwork):

                node.system_msg = node.system_msg or system_msg
                node.context    = {**(node.context or dict()), **(context or dict())}
                node.middleware = node.middleware or middleware


        # Post-processing ##########################################################################

        if (
            clean_multiline is True
            or (clean_multiline is None and langworks.config.CLEAN_MULTILINE is True)
        ):

            if self.system_msg is not None:

                for message in system_msg:
                    message["content"] = langworks.util.string.clean_multiline(message["content"])


        # Invoke super class #######################################################################

        # Initialize inner pipework.
        self.pipework = (
            super().__init__(
                processes     = processes, 
                logger        = logger,
                ignore_errors = ignore_errors,

                join          = join,
                join_groupby  = join_groupby,
                join_flatten  = join_flatten,

                connections   = connections, 
                **nodes
            )
        )

        # End of method '__init__' #################################################################

    # End of class 'Langwork' ######################################################################
        
# End of File ######################################################################################