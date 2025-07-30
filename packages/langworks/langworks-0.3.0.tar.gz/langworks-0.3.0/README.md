# Langworks

Langworks is an open-source framework build on top of 
[Pypeworks](https://rosaia.github.io/langworks/) to procedurally query LLM's in Python. It offers 
the following features:

* Chained prompting with conditional pathways
* Templatable prompts and responses using Jinja
* Guided generation constrained by regex and context-free grammar
* Mixing and matching of LLM's and LLM servers (with support for llama.cpp and vLLM)
* Distributed inference with autoscaling support
* Fine-tuning of sampling parameters per prompt


## Install

Langworks is available through the PyPI repository and can be installed using `pip`:

```bash
pip install langworks
```


## Quickstart

A `Langwork` represents a specialised pipework consisting of `Query` and `Node` objects. A Query 
object encapsulates a templatable prompt that may be passed to a LLM, as well as any guidance on 
how that LLM may process that prompt. Nodes serve as processing units, to be used to prepare input 
for Query objects, or to process output received from these objects.

Assuming a vLLM-backend running Llama-3 is available, a Langwork may be instantiated as follows:

```python
from langworks import (
    Connection,
    Langwork,
    Query
)

from pypeworks import (
    Node
)

from langworks.middleware.vllm import (
    SamplingParams,
    vLLM
)

langwork = Langwork(

    # Configuration
    middleware = vLLM(
        url          = "http://127.0.0.1:4000/v1",
        model        = "meta-llama/Meta-Llama-3-8B-Instruct",
        params       = SamplingParams(temperature = 0.3)
    ),

    system_msg = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant knowledgable about popular trivia."
            )
        }
    ],

    # Logic
    query = Query(

        query = (
            """
            Who or what is more popular: {{ input[0] }} or {{ input[1] }}? Think step-by-step \\
            before stating your final answer, either '{{ input[0] }}' or '{{ input[1] }}', \\
            delimited by triple asterisks (i.e. ***{{ input[0] }}*** or ***{{ input[1] }}***).
            """
        ),

        guidance = (
            """
            Let's think step-by-step\\
            {% gen params = Params(stop = ["***"], include_stop = True) %}\\
            {% choice input, var = "hit" %, params = Params(temperature = 0)}\\
            ***
            """
        )

    ),

    extract = Node(
        lambda context, history: context.get("hit", None)
    ),

    # Connections
    connections = [

        Connection("enter"   , "query"),
        Connection("query"   , "extract"),
        Connection("extract" , "exit")
        
    ]

)

for result in langwork(
    iter([("cats", "dogs"), ("werewolves", "vampires"), ("rock", "pop")])
):
    
    print(result)

```