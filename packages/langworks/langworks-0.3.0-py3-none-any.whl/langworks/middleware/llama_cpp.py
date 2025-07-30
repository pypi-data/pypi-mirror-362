# ##################################################################################################
#
# Title:
#
#   langworks.middleware.llama-cpp.py
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
#   Part of the Langworks framework, implementing middleware to leverage llama.cpp.
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
    Literal,
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

from langworks.util import (
    caching
)

from langworks.util.auth import (
    Authenticator,
    AuthenticationDetails
)

from langworks.util.balancing import (
    BalancedPool
)



# ##################################################################################################
# Classes
# ##################################################################################################

# Params ###########################################################################################

@dataclass(frozen = True)
class SamplingParams(generic.SamplingParams):

    """
    Specifies additional sampling parameters to be used when passing a prompt to llama.cpp.
    """

    # ##############################################################################################
    # Fields
    # ##############################################################################################

    dry : bool = field(default = False)
    """
    Enables sampling using the DRY repetition penalty, offering more fine-grained control over
    repetitions than :py:attr:`repetition_penalty`. 

    .. seealso::
        Weidmann, P.E. (2024). *DRY: A modern repetition penalty that reliably prevents looping*.
        https://github.com/oobabooga/text-generation-webui/pull/5677.
    """

    dry_base : float = field(default = 1.75)
    """
    Controls how quickly the DRY repetition penalty grows as repetitions repeat.
    """

    dry_min_length : int = field(default = 2)
    """
    Minimal required length of repeated tokens subject to the DRY repetition penalty.

    .. note::
        Within llama.cpp this parameter is referred to as ``dry_allowed_length``.
    """

    dry_multiplier : float = field(default = 0.0)
    """
    Controls extent to which the DRY repetition penalty is applied.    
    """

    dry_last_n :int = field(default = -1)
    """
    The number of previous tokens to consider when applying DRY sampling.

    .. note::
        Within llama.cpp this parameter is referred to as ``dry_penalty_last_n``.
    """

    dry_sequence_breakers : list[str] = field(default = None)
    """
    List of character sequences, which if generated reset the DRY repetition penalty.
    """

    max_p : float = field(default = 0.1)
    """
    Puts an upper bound on the probability of the sampled tokens under consideration, allowing to 
    discard the most likely tokens, increasing originality.

    .. note::
        Within llama.cpp this parameter is referred to as ``xtc_threshold``.

    .. seealso::
        Weidmann, P.E. (2024). *Exclude Top Choices (XTC): A sampler that boosts creativity, breaks 
        writing clichés, and inhibits non-verbatim repetition*. 
        https://github.com/oobabooga/text-generation-webui/pull/6335.
    """

    max_p_allowance : float = field(default = 0.0)
    """
    Controls probability that the least likely sampled token above the threshold specified by
    :py:attr:`max_p` is included despite exceeding the threshold.

    .. note::
        Within llama.cpp this parameter is referred to as ``xtc_probability``.
    """

    mirostat : Literal[0, 1, 2] = field(default = 0)
    """
    Enables Mirostat sampling, controlling perplexity during text generation.

    A value of ``0`` disables Mirostat, ``1`` enables Mirostat, and ``2`` enables Mirostat 2.0.

    .. seealso::
        Basu et al. (2021). *Mirostat: A Neural Text Decoding Algorithm that Directly Controls 
        Perplexity.* https://arxiv.org/abs/2007.14966
    """

    mirostat_eta : float = field(default = 0.1)
    """
    Sets the Mirostat learning rate, parameter eta.
    """

    mirostat_tau : float = field(default = 5.0)
    """
    Sets the Mirostat target entropy, parameter tau.
    """

    overflow_keep : int = field(default = 0)
    """
    Specifies the number of tokens from the prompt to retain when the context size is exceeded and
    tokens need to be discarded. The number excludes the BOS token. When set to ``-1`` all tokens 
    are retained.

    .. note::
        Within llama.cpp this parameter is referred to as ``n_keep``.
    """

    repeat_last_n : int = field(default = 64)
    """
    The number of previous tokens to consider when applying :py:attr:`repetition_penalty`.
    """

    samplers : list[
        Literal["dry", "top_k", "typ_p", "top_p", "min_p", "xtc", "temperature"]
    ] = field(default = None)
    """
    The order samplers are applied in.
    """

    samplers_keep : int = field(default = 0)
    """
    The number of best tokens samplers must retain regardless of whether these tokens satisfy the
    conditions set by these samplers.

    .. note::
        Within llama.cpp this parameter is referred to as ``min_keep``.
    """

    temperature_dev : float = field(default = 0.0)
    """
    Maximum deviation allowed from 
    :py:attr:`~langworks.middleware.generic.SamplingParams.temperature`. When specified, the 
    `temperature` is heuristically adjusted proportial to the spread of the probability of the
    sampled tokens under consideration. The extent of this adjustment is capped by the value 
    `temperature_dev` is set to.

    .. note::
        Within llama.cpp this parameter is referred to as ``dynatemp_range``.

    .. seealso::
        Zhu et al. (2023). *Hot or Cold? Adaptive Temperature Sampling for Code Generation with Large 
        Language Models*. https://doi.org/10.48550/arXiv.2309.02772.
    """

    temperature_dev_exp : float = field(default = 1.0)
    """
    Controls the degree with which 
    :py:attr:`~langworks.middleware.generic.SamplingParams.temperature` is adjusted when 
    :py:attr:`temperature_dev` is specified. Above 1.0, temperature is barely adjusted unless the 
    p-values among the tokens under consideration vary considerable. Below 1.0, adjustment is more 
    pronounced even if p-values are relatively close.

    .. note::
        Within llama.cpp this parameter is referred to as ``dynatemp_exponent``.
    """

    top_n_sigma : float = field(default = -1.0)
    """
    Puts an upper bound on pre-softmax scores, stating the number of standard deviations a
    pre-softmax score may exceed the mean to be considered for sampling. Doing so is purported to
    increase coherence at higher temperatures.

    .. seealso::
        Tang et al. (2024). *Top-nσ: Not All Logits Are You Need*. 
        https://doi.org/10.48550/arXiv.2411.07641.
    """

    typical_p : float = field(default = 1.0)
    """
    Specifies a range around the average probability of the sampled tokens under consideration,
    excluding tokens outside of this range. `typical_p` is generally applied after other samplers
    have already been applied.

    .. seealso::
        Meister et al. (2022). *Locally Typical Sampling*. https://arxiv.org/abs/2202.00666.
    """


# Monkey patch in '__defaults__', a quick lookup map for default values ############################

SamplingParams.__defaults__ = generic.get_dataclass_defaults(SamplingParams)

# End of class 'SamplingParams' ####################################################################


# LlamaCpp #########################################################################################

class LlamaCpp(generic.Middleware):

    """
    `Llama.cpp <https://github.com/ggml-org/llama.cpp/>`_ is an open source LLM inference engine
    designed to efficiently run on a wide range of hardware, including CPU-only and CPU+GPU hybrid 
    configurations.
    
    Langworks' llama.cpp middleware provides a wrapper to access the LLMs served using 
    `llama.cpp server API <https://github.com/ggml-org/llama.cpp/tree/master/tools/server>`_.
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
        Initializes the llama.cpp middleware.

        Parameters
        ----------

        Connection
        ^^^^^^^^^^

        url
            URL or URLs of llama.cpp-instances where the model may be accessed.

            .. versionchanged:: 0.3.0
                A list of URLs may be specified, allowing to simultaneously access multiple
                inference endpoints.

        model
            Name of the model as assigned by the instance.

        authenticator
            :py:class:`Authenticator` that may be used to acquire an authentication key when the 
            llama.cpp-instance requests for authentication. Optionally, a list of authenticators may 
            also be provided, allowing to specify an authenticator per llama.cpp
            -instance as identified by the URLs in `url`.

            .. versionchanged:: 0.3.0
                A list of authenticators may be specified, making it possible to manage
                authentication per llama.cpp-instance as specified using `url`.

        timeout
            The number of seconds the client awaits the response of the llama.cpp-instance.

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
            of :py:class:`SamplingParams`.

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

        # Get connection with llama.cpp instance ###################################################

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
            
                # Instantiate OpenAI client to make a connection to llama.cpp instance.
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

                    # Sampling parameters passed through the extra body.
                    extra_body = {

                        # Sampling parameters.
                        **{
                            remote_param: prompt_params[local_param]
                            for local_param, remote_param in [

                                # Generic: Stopping
                                #("include_stop"          , "include_stop"),
                                ("ignore_eos"            , "ignore_eos"),

                                # Generic: Randomization
                                ("min_p"                 , "min_p"),
                                ("top_k"                 , "top_k"),
                                ("repetition_penalty"    , "repeat_penalty"),

                                # Llama.cpp: DRY
                                ("dry_base"              , "dry_base"),
                                ("dry_min_length"        , "dry_allowed_length"),
                                ("dry_last_n"            , "dry_penalty_last_n"),
                                ("dry_sequence_breakers" , "dry_sequence_breakers"),

                                # Llama.cpp: XTC
                                ("max_p"                 , "xtc_threshold"),
                                ("max_p_allowance"       , "xtc_probability"),

                                # Llama.cpp: Mirostat
                                ("mirostat"              , "mirostat"),
                                ("mirostat_eta"          , "mirostat_tau"),
                                ("mirostat_tau"          , "mirostat_tau"),

                                # Llama.cpp: Misc
                                ("overflow_keep"         , "overflow_keep"),
                                ("repeat_last_n"         , "repeat_last_n"),
                                ("samplers"              , "samplers"),
                                ("samplers_keep"         , "min_keep"),

                                # Llama.cpp: Dynamic temperature
                                ("temperature_dev"       , "dynatemp_range"),
                                ("temperature_dev_exp"   , "dynatemp_exponent"),

                                # Top-n-sigma
                                ("top_n_sigma"           , "top_n_sigma"),

                                # Locally typical sampling
                                ("typical_p"             , "typical_p"),

                                
                            ]
                            if local_param in prompt_params
                        },

                        # Sampling parameters with additional processing.
                        **({
                            "dry_multiplier": prompt_params["dry_multiplier"]
                        } if "dry" in prompt_params else {}),

                        # Guided generation
                        **(
                            {} if isinstance(chunk, dsl.Gen)
                            else {
                                "json_schema": chunk.spec
                            } if isinstance (chunk, dsl.JSON)
                            else {
                                "json_schema": chunk.schema
                            } if isinstance(chunk, dsl.Dataclass)
                            else {
                                "grammar": f"root ::= \"{"kwargs=\", \"".join(chunk.spec)}\""
                            } if isinstance(chunk, dsl.Choice) and len(chunk.spec) > 0
                            else {
                                "grammar": f"%llguidance\nstart: /{chunk.spec}/"
                            } if isinstance(chunk, dsl.Regex)
                            else {
                                "grammar": chunk.spec
                            } if isinstance(chunk, dsl.GBNF)
                            else {
                                "grammar": f"%llguidance\n{chunk.spec}"
                            } if isinstance(chunk, dsl.Lark)
                            else {}
                        )
                    },

                )

                # Query the llama.cpp-instance.
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

                    self.clients.release(client)

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

            # Add stop words if necessary.
            if prompt_params.get("include_stop", False) is True:

                stop_words : list[str] = prompt_params.get("stop", [])

                if len(stop_words) == 1:
                    txt += stop_words[0]

                elif len(stop_words) > 1:

                    raise ValueError(
                        "Attempted to add stopping word to output, but cannot not deduce which"
                        " stopping word to include; llama.cpp middleware supports only one stop"
                        " word;"
                    )


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