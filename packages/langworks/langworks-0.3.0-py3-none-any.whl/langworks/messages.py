# ##################################################################################################
#
# Title:
#
#   langworks.messages.py
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
#   Part of the Langworks framework, specifying various type definitions related to prompt
#   messages.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Fundamentals
from typing import (
    Any,
    TypedDict
)


# ##################################################################################################
# Type definitions
# ##################################################################################################

# Message ##########################################################################################

class Message(TypedDict):

    role    : str
    """The role of the agent stating this query, usually 'user', 'system' or 'assistant'."""

    content : Any
    """The contents of the message."""

    # End of specification 'Message' ###############################################################


# Thread ###########################################################################################
    
type Thread = list[Message]


# End of File ######################################################################################