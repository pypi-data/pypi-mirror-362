# ##################################################################################################
#
# Title:
#
#   langworks.util.json.py
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
#   Part of the Langworks framework, implementing various JSON-related utility functions for use 
#   while prompting LLMs.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
import dataclasses

import typing
from typing import (
    Annotated,
    Any,
    ClassVar,
    Iterator,
    Literal,
    NotRequired,
    Optional,
    Protocol,
    Required
)

# TODO: Remove if PEP-727 is ever revisited.
from typing_extensions import (
    Doc
)

# System
import warnings

# Utilities
import json
import re


# ##################################################################################################
# Typing
# ##################################################################################################

# Protocols ########################################################################################

### DataclassType ##################################################################################

class DataclassType(Protocol):

    # TODO: Check if this classes is eventually implemented in the standard libary.

    """
    Protocol to type hint dataclasses.
    """

    __dataclass_fields__: ClassVar[dict[str, dataclasses.Field[Any]]]

    # End of protocol 'DataclassType' ##############################################################


### TypedDictType ##################################################################################

class TypedDictType(Protocol):

    """
    Protocol to type hint :py:func:`typing.TypedDict`.
    """

    __annotations__  : dict[str, Any]
    __required_keys__ : frozenset[str]
    __optional_keys__ : frozenset[str]

    # End of protocol 'TypedDictType' ##############################################################


# ##################################################################################################
# Functions
# ##################################################################################################

# JSON #############################################################################################

# cast_json_as_cls #################################################################################

def cast_json_as_cls(
    json            : dict[str, Any],
    cls             : DataclassType | TypedDictType,
    on_redundancies : Literal["ignore", "warn", "raise"] = "warn",
    on_missing      : Literal["ignore", "warn", "raise"] = "raise"
):
    """
    Convert a JSON-like dictionary to an instance of the given :py:deco:`dataclasses.dataclass` or 
    :py:class:`typing.TypedDict` subclass, adhering to type hints included in this class, converting
    any properties and fields to the appropriate types (including nested dataclasses or TypedDict
    subclasses).

    Parameters
    ----------

    json
        JSON-like dictionary to convert.

    cls
        Dataclass or TypedDict subclass to convert to.

    on_redundancies
        How to handle any potential redundancies included in the passed JSON object, either emitting
        a warning (``warn``), raising an error (``raise``), or ignoring the redundancy (``ignore``).

    on_missing
        How to handle missing data in the passed JSON object, either emitting a warning (``warn``), 
        raising an error (``raise``), or ignoring the missing key (``ignore``).
        
    """
    
    # ##############################################################################################
    # Preparation
    # ##############################################################################################

    # Set-up variables for intermediate data #######################################################
    
    # Holds final result to return.
    result : Any = None

    # Stack holding reference to object at current position of traversal within passed JSON object.
    json_stack : list[dict[str, Any]] = [json]

    # Stack holding reference to type definitions at current position of traversal
    cls_stack : list[Iterator[tuple[str, type]]] = []

    if dataclasses.is_dataclass(cls):
        cls_stack.append((field.name, field.type) for field in dataclasses.fields(cls))

    elif typing.is_typeddict(cls):
        cls_stack.append(iter(cls.__annotations__.items()))

    else:

        raise TypeError(
            f"Object '{cls}' was passed, where dataclass or TypedDict subclass was expected;"
        )

    # Stack holding partially initialized objects.
    obj_stack : list[tuple[str | None, type, dict | list]] = [(None, cls, {})]    
    

    # ##############################################################################################
    # Traversal
    # ##############################################################################################

    # Traverse the definition class and its decendants.
    while len(cls_stack) > 0:

        # Attempt to retrieve name, and type from the stack.
        try:
            key, type_ = next(cls_stack[-1])

        # If no more objects can be retrieved, all items on the current level have been processed.
        except StopIteration:

            # Return to level of parent, while retrieving intermediate results.
            json_obj = json_stack.pop()
            cls_stack.pop()

            key, type_, args = obj_stack.pop()

            # Split up wrapper (origin) and wrapped (raw) type.
            while (
                (origin := typing.get_origin(type_)) in {Annotated, Required, NotRequired}
                or type_ == Optional[type_]
            ):
                type_ = typing.get_args(type_)[0]

            # Handle lists.
            if origin is list:

                result = args
                continue

            # Handle dict-like objects.
            result = type_(**args)

            if len(obj_stack) > 0 and origin is not list:

                current_obj = obj_stack[-1][2]
                current_obj[key] = result

            if on_redundancies != "ignore" and len(redundancies := (set(json_obj) - set(args))) > 0:

                msg = (
                    f"JSON contained more arguments than could be fit to object of type"
                    f" '{type_.__qualname__}': " + (", ".join(redundancies)) + ";"
                )

                if on_redundancies == "warn":
                    warnings.warn(msg)

                else:
                    raise KeyError(msg)

            continue

        # For quick access, retrieve reference to latest objects on stack.
        current_json = json_stack[-1]
        current_obj = obj_stack[-1][2]

        # Retrieve unannotated (raw) type, separating out eventual annotations.
        raw_type : type = type_
        is_optional : bool = False

        # Keep inspecting the type until all annotation types are unwrapped.
        while (
            (origin := typing.get_origin(raw_type)) in (Annotated, Required, NotRequired)
            or raw_type == Optional[raw_type]
        ):

            if origin is NotRequired or raw_type == Optional[raw_type]:
                is_optional = True

            raw_type = typing.get_args(raw_type)[0]

        # Handle missing optional and required data.
        if (isinstance(current_json, dict) and current_json.get(key, KeyError) is KeyError):

            if is_optional:
                continue
            
            msg = f"Object of type '{type_.__qualname__}' expects property '{key}';"
            
            if on_missing == "warn":
                warnings.warn(msg)

            elif on_missing == "raise":
                raise KeyError(msg)
            
            current_obj[key] = dataclasses.MISSING
            continue

        # Handle specific types.
        if origin is None:

            # Handle booleans.
            if issubclass(raw_type, bool):
                current_obj[key] = bool(current_json[key])

            # Handle numbers.
            elif issubclass(raw_type, (int, float, complex)):
                current_obj[key] = raw_type(current_json[key])

            # Handle strings.
            elif issubclass(raw_type, str):
                current_obj[key] = str(current_json[key])

            # Handle nested dataclasses.
            elif dataclasses.is_dataclass(raw_type):
                
                json_stack.append(current_json[key])
                cls_stack.append((field.name, field.type) for field in dataclasses.fields(raw_type))
                obj_stack.append((key, raw_type, {}))

            # Handle nested dataclasses and dicts.
            elif issubclass(raw_type, dict):
                
                # Handle dataclasses and TypedDict subclasses..
                if typing.is_typeddict(raw_type):

                    json_stack.append(current_json[key])
                    cls_stack.append(iter(raw_type.__annotations__.items()))
                    obj_stack.append((key, raw_type, {}))

                # Handle 'normal' unannotated dicts.
                else:
                    current_obj[key] = current_json

            # Handle None types.
            elif raw_type is type[None]:
                current_obj[key] = None

        else: # if origin is not None:

            # Handle enumerations.
            if origin is Literal:
                current_obj[key] = str(current_json)

            # Handle regular expressions.
            elif origin is re.Pattern:
                current_obj[key] = str(current_json)

            # Handle lists.
            elif issubclass(origin, list):

                ls = current_obj[key] = [None] * len(current_json[key])

                for i in range(0, len(current_json[key])):

                    json_stack.append(current_json[key])
                    cls_stack.append( iter( ((i, typing.get_args(raw_type)[0]),) ) )
                    obj_stack.append((key, raw_type, ls))


    # ##############################################################################################
    # Finalization
    # ##############################################################################################

    return result

    # End of function 'cast_json_as_cls' ###########################################################


# json_dict_schema_from_cls ########################################################################

def json_dict_schema_from_cls(
    schema   : DataclassType | TypedDictType, 
    use_refs : bool = False
) -> dict:

    """
    Generates from a :py:deco:`dataclasses.dataclass` or :py:class:`typing.TypedDict` subclass a 
    JSON schema compliant with the standard governed by The JSON Schema Organization, represented
    as a Python dictionary. If a string-based representation is desired, use 
    :py:func:`json_schema_from_cls` instead.

    Parameters
    ----------

    schema
        The dataclass or TypedDict subclass from which to generate the schema. Attributes may have
        any of the following types:

        - Boolean
        - Numeric (``int``, ``float``, or ``complex``)
        - String
        - Literal
        - Regular expressions (``re.Pattern[...]``)
        - None (``type[None]``)
        - List
        - TypedDict subclass

        When wrapped by annotation types like :py:class:`Required` or :py:class:`NotRequired`, 
        these requirements are also included in the schema generated.

    use_refs
        Flag that controls whether or not nested TypedDict objects are included directly or through
        references, the latter allowing for recursive  definitions.
    """

    # ##############################################################################################
    # Preparation
    # ##############################################################################################

    # Set-up variables for intermediate data #######################################################

    ### Construct top-level object #################################################################

    # Set-up base object.
    result = {
        "type": "object",
        "properties": {}
    }

    # Set required properties.
    if dataclasses.is_dataclass(schema):

        result["required"] = [
            field.name
            for field in dataclasses.fields(schema)
            if not field.type == Optional[field.type] # Hack to easily test for Optional
        ]

    elif typing.is_typeddict(schema):
        result["required"] = list(schema.__required_keys__)

    else:

        raise TypeError(
            f"Object '{schema}' was passed, where dataclass or TypedDict subclass was expected;"
        )

    # Initialize defs if necessary.
    if use_refs is True:
        result["$defs"] = {}


    # Set-up utilities #############################################################################

    # Stack to keep track of traversal through given TypedDict and decendants.
    stack        : list[Iterator[tuple[str, Any]]] = []

    # Stack holding references to recently constructed schema objects.
    object_stack : list[dict] = [result["properties"]]


    # ##############################################################################################
    # Traverse the class
    # ##############################################################################################

    # Take the passed object, retrieve key-value pairs, and pass it via an iterable to the stack.
    if dataclasses.is_dataclass(schema):

        stack.append(
            ((field.name, field.type) for field in dataclasses.fields(schema))
        )

    else: # elif typing.is_typeddict(schema): # Implicit due to earlier type checks.
        stack.append(iter(schema.__annotations__.items()))

    # Traverse the TypedDict and its decendants till no members are left.
    while len(stack) > 0:

        # Attempt to retrieve key-value from the stack.
        try:
            key, value = next(stack[-1])

        except StopIteration:

            stack.pop()
            object_stack.pop()

            continue

        # For quick access, retrieve reference to latest object on stack.
        current_object = object_stack[-1]

        # Retrieve unannotated (raw) type, separating out eventual annotations.
        raw_type : type = value

        while (
            (origin := typing.get_origin(raw_type)) in {Annotated, Required, NotRequired}
            or raw_type == Optional[raw_type]
        ):
            raw_type = typing.get_args(raw_type)[0]

        # Handle specific types.
        if origin is None:

            # Handle booleans.
            if issubclass(raw_type, bool):
                current_object[key] = {"type": "boolean"}

            # Handle numbers.
            elif issubclass(raw_type, (int, float, complex)):
                current_object[key] = {"type": "number"}

            # Handle strings.
            elif issubclass(raw_type, str):
                current_object[key] = {"type": "string"}

            # Handle nested dataclasses and dicts.
            elif issubclass(raw_type, dict) or dataclasses.is_dataclass(raw_type):

                # Start building object.
                next_object = {
                    "type": "object"
                }
                
                # Handle dataclasses and TypedDict subclasses..
                if typing.is_typeddict(raw_type) or dataclasses.is_dataclass(raw_type):

                    if use_refs is False or not raw_type.__qualname__ in result["$defs"]:

                        # Add attribute to hold object properties.
                        next_object["properties"] = {}

                        # Optionally, add required properties.
                        if typing.is_typeddict(raw_type):
                            next_object["required"] = list(raw_type.__required_keys__)

                        else:

                            next_object["required"] = [
                                field.name
                                for field in dataclasses.fields(raw_type)
                                if not field.type == Optional[field.type] # Optional-test
                            ]
                            

                        # Optionally, mark the object as closed for further additions.
                        # TODO: Uncomment upon implementation of PEP 728.
                        #if hasattr(raw_type, "__closed__"):
                        #    next_object["additionalProperties"] = not raw_type.__closed__
                        
                        if use_refs is True:
                            result["$defs"][raw_type.__qualname__] = next_object
                    
                    # Either add object by reference.
                    if use_refs is True:
                        current_object[key] = {"$ref": f"#/$defs/{raw_type.__qualname__}"}
                        next_object = result["$defs"][raw_type.__qualname__]

                    # Or directly.
                    else:
                        current_object[key] = next_object

                    # Add annotations or fields to stack.
                    if typing.is_typeddict(raw_type):
                        stack.append(iter(raw_type.__annotations__.items()))

                    else: # if dataclasses.is_dataclass(raw_type): # Implicit

                        stack.append(
                            ((field.name, field.type) for field in dataclasses.fields(raw_type))
                        )
                        

                    object_stack.append(next_object["properties"])

                # Handle 'normal' unannotated dicts.
                else:

                    # Add the newly built object as a property to the latest object on the stack.
                    current_object[key] = next_object

            # Handle None types.
            elif raw_type is type[None]:
                current_object[key] = {"type": "null"}  

        else: # if origin is not None:

            # Handle enumerations.
            if origin is Literal:
                current_object[key] = {"enum": list(typing.get_args(raw_type))}

            # Handle regular expressions.
            elif origin is re.Pattern:
                current_object[key] = {"type": "string", "pattern": typing.get_args(raw_type)}

            # Handle lists.
            elif issubclass(origin, list):

                # Start building object.
                next_object = {"type": "array"}

                # Add the newly built object as a property to the latest object on the stack.
                current_object[key] = next_object

                # Add to stack.
                stack.append(iter( (("items", typing.get_args(raw_type)[0]), ) ))
                object_stack.append(next_object)


    # ##############################################################################################
    # Finalization
    # ##############################################################################################

    return result


    # End of function 'json_dict_schema_from_cls' ##################################################


# json_schema_from_cls #############################################################################

def json_schema_from_cls(
    schema   : DataclassType | TypedDictType, 
    indent   : str = 2, 
    use_refs : bool = False
) -> str:
    
    """
    Generates from a :py:deco:`dataclasses.dataclass` or :py:class:`typing.TypedDict` subclass a 
    string-based JSON schema compliant with the standard governed by The JSON Schema Organization. 
    If a dictionary is desired, use :py:func:`json_dict_schema_from_cls` instead.

    Parameters
    ----------

    schema
        The dataclass or TypedDict subclass from which to generate the schema. Attributes may have
        any of the following types:

        - Boolean
        - Numeric (``int``, ``float``, or ``complex``)
        - String
        - Literal
        - Regular expressions (``re.Pattern[...]``)
        - None (``type[None]``)
        - List
        - TypedDict subclass

        When wrapped by annotation types like :py:class:`Required` or :py:class:`NotRequired`, 
        these requirements are also included in the schema generated.

    indent
        The number of whitespaces to use per level when formatting the scheme.

    use_refs
        Flag that controls whether or not nested TypedDict objects are included directly or through
        references, the latter allowing for recursive  definitions.
    """
    
    # Defer, transform and return.
    return json.dumps(json_dict_schema_from_cls(schema, use_refs), indent = indent)
    

    # End of function 'json_schema_from_cls' #######################################################


# json_shorthand_schema_from_cls ###################################################################

def json_shorthand_schema_from_cls(
    schema : DataclassType | TypedDictType, 
    indent : str = 2
) -> str:

    """
    Generates a shorthand JSON schema from a :py:deco:`dataclasses.dataclass` or 
    :py:class:`typing.TypedDict` subclass
    

    .. note::
        Shorthand JSON schemas are not compliant with `JSON Schema <https://json-schema.org/>`_ as 
        defined by the The JSON Schema Organization. Shorthand JSON schemas only serve to succinctly 
        instruct LLMs when requesting these LLMs to output JSON. If you wish to generate compliant
        schema, look at :py:func:`json_schema_from_cls`.

    Parameters
    ----------

    schema
        The TypedDict subclass from which to generate the schema. Attributes may have any of the 
        following types:

        - Boolean
        - Numeric (int, float, complex)
        - String
        - Literal
        - Regular expressions (``re.Pattern[...]``)
        - None (passed as ``type[None]``)
        - List
        - TypedDict subclass

        Optionally, attributes may also be annotated using :py:class:`typing.Annotated`. When these
        annotations include an :py:class:`typing_extensions.Doc` object, their contents will be 
        treated as docstrings to include in the schema alongside the attributes. These docstrings
        may be further enhanced through the use of :py:class:`typing.NotRequired` annotations. 
        For example::

            class Item(TypedDict):
                value : Annotated[str, Doc("A wrapped value")]
                index : NotRequired[int]

            json_shorthand_schema_from_dict(Item) == \"""{
              "value": "string", // A wrapped value
              "index": "number" // (optional) 
            }\"""

    indent
        The number of whitespaces to use per level when formatting the scheme.
    """

    # ##############################################################################################
    # Preparation
    # ##############################################################################################

    # Set-up variables for intermediate data #######################################################

    # Holds chunks of the final string to be returned.
    result : list[str] = []

    # List that functions as a stack to easily navigate through the schema's hierarchy.
    stack : list[Iterator[tuple[str, Any]]] = []

    # Tracks current level with the hierarchy, used when moving between levels.
    depth : int = 0

    # Keeps track of closing parentheses.
    closing_parentheses : list[str] = []

    # Holds docstring associated with most recently inspected item.
    doc_string : str | None = None


    # ##############################################################################################
    # Walk through the schema
    # ##############################################################################################

    # Take the passed object, retrieve key-value pairs, and pass it via an iterable to the stack.
    if dataclasses.is_dataclass(schema):

        stack.append(
            ((field.name, field.type) for field in dataclasses.fields(schema))
        )

    elif typing.is_typeddict(schema):
        stack.append(iter(schema.__annotations__.items()))

    else:

        raise TypeError(
            f"Object '{schema}' was passed, where dataclass or TypedDict subclass was expected;"
        )

    # Keep walking till there are no more objects available on the stack.
    while len(stack) > 0:

        # Attempt to retrieve key-value from the stack.
        try:
            key, value = next(stack[-1])

        except StopIteration:
            
            # If no key-value pairs are available anymore, close off the current level, outputting
            # any remaining docstring and adding the closing parantheses.
            if doc_string is not None:

                result.append(doc_string[:-1]) # Skip newline, already included with parentheses
                doc_string = None

            result.append(closing_parentheses.pop())

            # Remove current level from stack, and continue to previous level.
            stack.pop()
            depth -= 1

            continue

        # Precalculate whitespace to prefix to any output.
        whitespace : str = " " * indent * depth

        # Check if inspection has moved to a deeper level of the scheme.
        if depth < len(stack):

            # If no key was passed, the current level represents a list object.
            if key is None:

                result.append("[\n" + whitespace + " " * indent)
                closing_parentheses.append(f"\n{whitespace}]")

            # Otherwise it is a compound object.
            else:

                result.append("{\n")
                closing_parentheses.append(f"\n{whitespace}{"}"}")

            # Increase depth counter, and increase whitespace accordingly.
            depth += 1
            whitespace += " " * indent

        # Check cases wherein inspection is continuing on the same level.
        elif depth == len(stack):

            # Output a comma to mark continuation on the same level.
            result.append(",")
            
            # Add any postfix docstrings if necessary.
            if doc_string is not None:

                result.append(doc_string)
                doc_string = None

            else:
                result.append("\n")

        # Retrieve unannotated (raw) type, separating out eventual annotations.
        raw_type : type = value
        
        doc : str | None = None
        is_optional : bool = False

        # Keep inspecting the type until all annotation types are unwrapped.
        while (
            (origin := typing.get_origin(raw_type)) in (Annotated, Required, NotRequired)
            or raw_type == Optional[raw_type]
        ):

            if origin is Annotated:
                
                for annotation in typing.get_args(raw_type)[1:]:

                    if isinstance(annotation, Doc):

                        doc = annotation.documentation
                        break

            if origin is NotRequired or raw_type == Optional[raw_type]:
                is_optional = True

            raw_type = typing.get_args(raw_type)[0]

        # Generate docstring from annotations retrieved.
        doc_string = None

        if doc is not None or is_optional is True:

            doc_string = (
                f" // "
                f"{'(optional) ' if is_optional is True else ''}"
                f"{doc if doc is not None else ''}"
                f"\n"  
            )

        # Generate type-dependent output.
        if origin is None:

            # Handle booleans.
            if issubclass(raw_type, bool):
                result.append(f"{whitespace}\"{key}\": \"boolean\"")

            # Handle numbers.
            elif issubclass(raw_type, (int, float, complex)):
                result.append(f"{whitespace}\"{key}\": \"number\"")

            # Handle strings.
            elif issubclass(raw_type, str):
                result.append(f"{whitespace}\"{key}\": \"string\"")

            # Handle nested dicts.
            elif issubclass(raw_type, dict):
                
                # Handle TypedDict and dependents.
                if typing.is_typeddict(raw_type):

                    if doc_string is not None:

                        result.append(whitespace[:-1] + doc_string)
                        doc_string = None

                    if key is not None:
                        result.append(f"{whitespace}\"{key}\": ")

                    stack.append(iter(raw_type.__annotations__.items()))

                # Handle 'normal' unannotated dicts.
                else:
                    result.append(f"{whitespace}\"{key}\": \"object\"")

            # Handle dataclasses.
            elif dataclasses.is_dataclass(raw_type):

                if doc_string is not None:

                    result.append(whitespace[:-1] + doc_string)
                    doc_string = None

                if key is not None:
                    result.append(f"{whitespace}\"{key}\": ")

                stack.append(
                    ((field.name, field.type) for field in dataclasses.fields(raw_type))
                )

            # Handle None types.
            elif raw_type is type[None]:
                result.append(f"{whitespace}\"{key}\": \"null\"")

        else: # if origin is not None:

            # Handle enumerations.
            if origin is Literal:

                literals = typing.get_args(raw_type)
                literals = (
                    "\"null\"" 
                    if len(literals) == 0 else 
                    ("\"enum['" + ("'|'".join(literals)) + "']\"")
                )

                result.append(f"{whitespace}\"{key}\": {literals}")

            # Handle regular expressions.
            elif origin is re.Pattern:
                result.append(f"{whitespace}\"{key}\": \"string[{typing.get_args(raw_type)[0]}]\"")

            # Handle lists.
            elif issubclass(origin, list):

                if doc_string is not None:

                    result.append(whitespace[:-1] + doc_string)
                    doc_string = None

                if key is not None:
                    result.append(f"{whitespace}\"{key}\": ")
                
                stack.append(iter( ((None, typing.get_args(raw_type)[0]), ) ))

        

    # ##############################################################################################
    # Finalization
    # ##############################################################################################

    return "".join(result)


    # End of function 'json_shorthand_schema_from_cls' #############################################


# End of File ######################################################################################