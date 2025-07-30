# ##################################################################################################
#
# Title:
#
#   langworks.util.string.py
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
#   Part of the Langworks framework, implementing various string-related utility functions for use 
#   while prompting LLMs.
#
# ##################################################################################################

# ##################################################################################################
# Dependencies
# ##################################################################################################

# Python standard library ##########################################################################

# Utilities
import re
import textwrap


# ##################################################################################################
# Functions
# ##################################################################################################

# clean_multiline ##################################################################################

def clean_multiline(string : str):

    """
    Removes unwanted newlines and indentations from Python multiline string blocks (triple quote 
    strings).

    By default this function removes only indentations automatically. Newlines that need to be
    removed need to be marked as such by inserting ``\\\\`` before the end of the line::

        clean_multiline(
            \"""
            This is a wrapping \\\\
            line
            \"""
        ) == "This is a wrapping line"

    Parameters
    ----------
    string
        String to clean.
    """

    return re.sub(r"\\\n", "", textwrap.dedent(string)).strip()

    # End of function 'clean_multiline' ############################################################

# End of File ######################################################################################