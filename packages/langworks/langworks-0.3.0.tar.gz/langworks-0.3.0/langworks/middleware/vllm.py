# ##################################################################################################
#
# Title:
#
#   langworks.middleware.vllm.py
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
#   Part of the Langworks framework, implementing middleware to leverage vLLM.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from dataclasses import (
    dataclass,
    field
)

from typing import (
    Any,
    Callable,
    Sequence
)

import warnings

# System
from threading import (
    Lock
)

# Utilities
import math
import statistics


# Third-party ######################################################################################

# OpenAI API (OpenAI)
try:

    import openai

    from openai.types.chat import (
        ChatCompletion
    )

except:
    pass


# Local ############################################################################################

from langworks import (
    dsl
)

from langworks.messages import (
    Message,
    Thread
)

from langworks.middleware import (
    generic
)

from langworks.util.auth import (
    Authenticator,
    AuthenticationDetails
)

from langworks.util.balancing import (
    BalancedPool
)

from langworks.util import (
    caching
)



# ##################################################################################################
# Classes
# ##################################################################################################

# Params ###########################################################################################

@dataclass(frozen = True)
class SamplingParams(generic.SamplingParams):

    """
    Specifies additional sampling parameters to be used when passing a prompt to vLLM.
    """

    # Sampling #####################################################################################

    allowed_tokens : list[int] = field(default = None)
    """
    List of encoded tokens from which the LLM may sample.

    .. note::
        Within vLLM this parameter is referred to as ``allowed_token_ids``.
    """

    bad_words : list[str] = field(default = None)
    """
    List of words that are not allowed to be generated.
    """

    min_tokens : int = field(default = 0)
    """
    The minimal number of tokens that may be generated per generation.
    """


    # Stopping #####################################################################################

    stop_tokens : list[int] = field(default = None)
    """
    List of encoded tokens, which if generated stop further generation.

    .. note::
        Within vLLM this parameter is referred to as ``stop_token_ids``.
    """


# Monkey patch in '__defaults__', a quick lookup map for default values ############################

SamplingParams.__defaults__ = generic.get_dataclass_defaults(SamplingParams)

# End of class 'Params' ############################################################################


# vLLM #############################################################################################

class vLLM(generic.Middleware):

    """
    `vLLM <https://docs.vllm.ai/en/stable/>`_ is an open source library for efficiently serving
    various LLMs using self-managed hardware. Langworks' vLLM middleware provides a wrapper to 
    access these LLMs using vLLM's server API.
    """

    # ##############################################################################################
    # Class fundamentals
    # ##############################################################################################

    # __init__ #####################################################################################

    def __init__(
            
            self, 

            # Connection
            url                 : str | Sequence[str],
            model               : str,
            authenticator       : Authenticator | Sequence[Authenticator] | None = None,
            timeout             : int                                            = 5,
            retries             : int                                            = 2,

            # Autoscaling
            autoscale_threshold : tuple[float, float]                            = (0, 0),
            
            # Configuration
            params              : SamplingParams                                 = None,
            output_cache        : caching.ScoredCache                            = None
            
    ):
        
        """
        Initializes the vLLM middleware.

        Parameters
        ----------

        Connection
        ^^^^^^^^^^

        url
            URL or URLs of vLLM-instances where the model may be accessed.

            .. versionchanged:: 0.3.0
                A list of URLs may be specified, allowing to simultaneously access multiple
                inference endpoints.

        model
            Name of the model as used in the Hugging Face repository.

        authenticator
            :py:class:`Authenticator` that may be used to acquire an authentication key when the 
            vLLM-instance requests for authentication. Optionally, a list of authenticators may also
            be provided, allowing to specify an authenticator per vLLM-instance as identified by the
            URLs in `url`.

            .. versionchanged:: 0.3.0
                A list of authenticators may be specified, making it possible to manage
                authentication per vLLM-instance as specified using `url`.

        timeout
            The number of seconds the client awaits the response of the vLLM-instance.

        retries
            The number of times the client tries to submit the same request again *after* a timeout.

        Balancing
        ^^^^^^^^^

        autoscale_threshold
            Pair specifying at what number of tasks per instance to scale up (first item) or scale
            down (second item). By default this is set to `(0, 0)`, setting the middleware up to
            immediately scale up to use all resources, while never scaling down.

            .. versionadded:: 0.3.0

        Configuration
        ^^^^^^^^^^^^^

        params
            Default sampling parameters to use when processing a prompt, specified using an instance
            of `SamplingParams`.

        output_cache
            Cache to use for caching previous prompt outputs. Should be a `ScoredCache` or subclass.

        """

        # ##########################################################################################
        # Initialize attributes
        # ##########################################################################################

        # Argument passthrough #####################################################################

        self.model               : str                 = model
        self.timeout             : int                 = timeout
        self.retries             : int                 = retries
        self.autoscale_threshold : tuple[float, float] = autoscale_threshold
        self.params              : SamplingParams      = params
        self.output_cache        : caching.ScoredCache = output_cache


        # Argument transformation ##################################################################

        self.url : Sequence[str] = (
            (url, ) if isinstance(url, str) else url
        )

        self.authenticator : Authenticator | Sequence[Authenticator] | None = (
            (authenticator, ) if isinstance(authenticator, Callable) else authenticator
        )


        # Class members ############################################################################

        self.clients           : BalancedPool[openai.OpenAI] = BalancedPool[openai.OpenAI]([])
        self.clients_lock      : Lock                        = Lock()

        self.output_cache_lock : Lock                        = Lock()

        # End of '__init__' ########################################################################


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
        
        # ##########################################################################################
        # Prepare initial prompt
        # ##########################################################################################

        # Render initial messages.
        messages : Thread = [
            # Construct new message.
            {
                # Maintaining original role.
                "role"   : message.get("role", None),
                # Replacing the content with the rendered variant.
                "content": (
                    # Join rendered chunks.
                    "".join(
                        # Pass to static DSL environment.
                        dsl.render(
                            message.get("content", None), context, mode = dsl.RenderingMode.STATIC
                        )
                    )
                )
            }
            # Process each message separately.
            for message in (
                # Append query to the history.
                (history or []) + [{"content": query or "", "role": role or "user"}]
            )
        ]


        # ##########################################################################################
        # Prepare rendering
        # ##########################################################################################

        # Get connection with vLLM instance ########################################################

        # Lock access to `clients`, preventing potential double instantiations.
        with self.clients_lock:

            # Locally store commonly reused data.
            clients_n           : int   = len(self.clients)
            workload_per_client : float = self.clients.workload_average

            # Handle cases wherein more clients may be instantiated.
            if (
                clients_n == 0
                or (
                    clients_n < len(self.url) and workload_per_client >= self.autoscale_threshold[0]
                )
            ):

                # Retrieve URL of llama.cpp instance.
                url : str = self.url[clients_n]

                # Retrieve appropriate authenticator.
                authenticator : Authenticator = None

                if self.authenticator is not None:
                    authenticator = self.authenticator[clients_n]

                # Retrieve token if an authenticator was passed.
                token : str | None = None

                if authenticator is not None:
                    
                    details : AuthenticationDetails = authenticator(self)

                    if details is not None:
                        token = details.token

                    if token is None:

                        warnings.warn(
                            f"Authenticator passed could not provide authentication details;"
                            " defaulting to token 'EMPTY';"
                        )
            
                # Instantiate OpenAI client to make a connection to vLLM instance.
                self.clients.add(openai.OpenAI(base_url = url, api_key = token or "EMPTY"))

            # Handle cases wherein number of clients need to be reduced.
            elif clients_n > 1 and workload_per_client < self.autoscale_threshold[1]:
                self.clients.remove_last()
            
            # Retrieve client.
            client : openai.OpenAI = self.clients.get()


        # Prepare context ##########################################################################

        context : dict = {
            **context,
            "Params": SamplingParams
        }


        # Combine default sampling parameters ######################################################

        # Combine sampling parameters specified at different levels.
        params = (

            # Do NOT create a new SamplingParams object, maintaining instead a dictionary as to
            # minimize the required computation when mixin constraint-level sampling parameters
            # later on.
            {

                # Middleware
                **{
                    key: value 
                    for key, value in 
                    (self.params.__dict__ if self.params is not None else {}).items()
                    if value != SamplingParams.__defaults__.get(key, None)
                },

                # Input
                **{
                    key: value 
                    for key, value in 
                    (params.__dict__ if params is not None else {}).items()
                    if value != SamplingParams.__defaults__.get(key, None)
                }
            }

        )


        # ##########################################################################################
        # Rendering
        # ##########################################################################################

        # Define intermediate variables ############################################################

        # Set-up new message.
        message : Message = {
            "role"    : "assistant",
            "content" : ""
        }

        messages.append(message)

        # Variable to hold generated variables.
        vars : dict[str, Any] = dict()


        # Main logic ###############################################################################

        # Process the guide tag by tag.
        for chunk in dsl.render(
            guidance or "{% gen %}", context, mode = dsl.RenderingMode.DYNAMIC
        ):

            # Differentiate constraints and non-constraints ########################################

            # Add any strings to the buffer and prompt, and skip until a constraint is found.
            if isinstance(chunk, str):

                message["content"] += chunk
                continue

            # Check if a constraint was passed.
            elif not isinstance(chunk, dsl.Constraint):

                raise ValueError(
                    f"Object of type '{type(chunk)}' was passed where 'str' or subtype of 'dsl."
                    "constraints.Constraint was expected;"
                )


            # Mixin final sampling parameters ######################################################
            
            # Combine sampling parameters stored in the constraint with default constraints.
            prompt_params : SamplingParams = {

                **{
                    key: value for key, value in params.items()
                },

                **{
                    key: value 
                    for key, value in 
                    (chunk.params.__dict__ if chunk.params is not None else {}).items()
                    if value != SamplingParams.__defaults__.get(key, None)
                }
            }


            # Generate response ####################################################################

            # Predefine variable to hold text response.
            txt : str | None = None

            # Check cache to see if a response needs to be generated.
            if self.output_cache is not None:

                # Generate hash for the request.
                request_hash : int = hash(message["content"] + self.model + str(prompt_params))

                # Access cache, and attempt to retrieve response.
                with self.output_cache_lock:

                    try:
                        txt = self.output_cache[request_hash]
                    except:
                        pass

            # Only retrieve response, if a response was not previously cached.
            if txt is None:

                # Prepare an object, holding all request arguments.
                request : dict = dict(

                    messages           = messages,
                    model              = self.model,
                    timeout            = self.timeout,

                    # Sampling parameters.
                    **{
                        remote_param: prompt_params[local_param]
                        for local_param, remote_param in [

                            # Generic
                            ("max_tokens"  , "max_tokens"),
                            ("stop"        , "stop"),

                            # Generic: Randomization
                            ("temperature" , "temperature"),
                            ("top_p"       , "top_p"),
                            ("seed"        , "seed"),
                            ("logprobs"    , "logprobs"),

                            # Generic: Repetition
                            ("presence_penalty", "presence_penalty"),
                            ("frequence_penalty", "frequency_penalty")

                        ]
                        if local_param in prompt_params
                    },

                    # Sampling parameters with additional processing.
                    **({
                        "logit_bias": [[k, v] for k, v in prompt_params["logit_bias"].items()]
                    } if "logit_bias" in prompt_params else {}),

                    # Parameters passed through the extra body.
                    extra_body = dict(

                        add_generation_prompt  = False,
                        continue_final_message = True,

                        # Sampling parameters.
                        **{
                            remote_param: prompt_params[local_param]
                            for local_param, remote_param in [

                                # Generic: Stopping
                                ("include_stop"          , "include_stop_str_in_output"),
                                ("ignore_eos"            , "ignore_eos"),

                                # Generic: Randomization
                                ("min_p"                 , "min_p"),
                                ("top_k"                 , "top_k"),
                                ("repetition_penalty"    , "repetition_penalty"),

                                # vLLM: Sampling
                                ("allowed_tokens"        , "allowed_token_ids"),
                                ("bad_words"             , "bad_words"),
                                ("min_tokens"            , "min_tokens"),
                                ("stop_tokens"           , "stop_token_ids")

                            ]
                            if local_param in prompt_params
                        },                       

                        # Guided generation
                        **(
                            {} if isinstance(chunk, dsl.Gen)
                            else {
                                "guided_json": chunk.spec
                            } if isinstance (chunk, dsl.JSON)
                            else {
                                "guided_json": chunk.schema
                            } if isinstance(chunk, dsl.Dataclass)
                            else {
                                "guided_choice": chunk.spec
                            } if isinstance(chunk, dsl.Choice) and len(chunk.spec) > 0
                            else {
                                "guided_regex": chunk.spec
                            } if isinstance(chunk, dsl.Regex)
                            else {
                                "guided_grammar": chunk.spec
                            } if isinstance(chunk, dsl.GBNF)
                            else {
                                "guided_grammar": chunk.spec
                            } if isinstance(chunk, dsl.Lark)
                            else {}
                        )

                    ),

                )

                # Query the vLLM-instance.
                attempt : int = -1
                response : ChatCompletion = None

                while attempt < self.retries:

                    try:
                        
                        response = client.chat.completions.create(**request)

                    except openai.APITimeoutError:

                        attempt += 1
                        continue

                    break

                if attempt >= self.retries:

                    self.clients.release(client) # Clean up before throwing error.

                    raise TimeoutError(
                        f"Connection with '{client.base_url}' timed out despite {self.retries}"
                        f" retries;"
                    )

                # Get response text.
                txt : str = response.choices[0].message.content

                # Cache if needed.
                if self.output_cache is not None:

                    # Retrieve logprobs, to be used as the score for comparison.
                    logprobs = response.choices[0].logprobs

                    if logprobs is not None:
                        logprobs = (logprob.logprob for logprob in logprobs.content)

                    # Convert to average p-value
                    p = math.exp(statistics.fmean(logprobs)) if logprobs is not None else 0.0

                    # Add to cache.
                    with self.output_cache_lock:
                        self.output_cache[request_hash] = caching.ScoredItem(txt, p)


            # Process response #####################################################################

            # Append response to message.
            message["content"] += txt

            # Store response if needed.
            if isinstance(chunk, dsl.constraints.Constraint) and chunk.var is not None:
                vars[chunk.var] = chunk.finalize(chunk, txt)


        # ##########################################################################################
        # Finalization
        # ##########################################################################################

        # Clean up.
        self.clients.release(client)

        # Return result.
        return (messages, vars)
    
        # End of method 'exec' #####################################################################
        

# End of File ######################################################################################