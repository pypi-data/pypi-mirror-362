from io import StringIO
import re
from datetime import datetime
from ipaddress import ip_network, ip_interface, ip_address


class MutableTuple(list):
    """
    Class used to identify a tuple that's been parsed
    from a string (dynamically created)
    """


# valid top-level key characters for 'show system state'
VALID_KEY_CHARS = r"[\w\.\-_]"


def system_state_value_to_type(input_string: str) -> any:
    """
    Converts a string to an int, float, bool, date, or IP
    """

    # "None", "True", or "False"
    for match, out in [("None", None), ("True", True), ("False", False)]:
        if input_string == match:
            return out

    # Integer conversion
    if re.match(r"^\d+$", input_string):
        return int(input_string)

    # Decimal/float
    if re.match(r"\d+\.\d+$", input_string):
        return float(input_string)

    # datetime, format appears to be consistent
    try:
        return datetime.strptime(input_string, "%Y/%m/%d %H:%M:%S")
    except ValueError:
        pass

    # IP
    for ip_type in [ip_network, ip_interface, ip_address]:
        try:
            return ip_type(input_string)
        except ValueError:
            pass

    return input_string


def parse_system_state(system_state: str) -> dict:
    """
    Parses "show system state", either filtered or unfiltered,
    from a raw string into structured data.

    Note that "show system state" output consists of a long list of top-level
    entries that we're saving as a dictionary. Each entry can be a string (single or multi-line),
    or a complex nested object of dicts, lists, and tuples.
    """

    # strip off xml tags
    system_state = system_state.replace('<response status="success"><result>', "")
    system_state = system_state.replace("</result></response>", "")

    # top of our structure starts off as an empty dict
    curr_node = {}

    buffer = ""
    curr_key = ""

    # for keeping track of nested object values
    obj_stack = []

    # to flag whether we're reading in the name of a top key or
    # a nested key
    reading_key = False
    reading_top_key = True

    # handling multiline values require us to keep track of the last top-level
    # node we just saved
    prev_node = {}
    prev_key = ""
    multiline_value = False

    # stream the output into our logic one character at a time
    stream = StringIO(system_state)
    while True:
        # peel off next character
        c = stream.read(1)
        if not c:
            break

        # colon denotes the end of a top-level key (unless this is a multiline value)
        if c == ":" and reading_top_key and not multiline_value:
            curr_key = buffer
            buffer = ""
            reading_top_key = False

            next_c = stream.read(1)
            if next_c != " ":
                raise ValueError(
                    f"Missing a space after reading top level key {curr_key} at idx {stream.tell()}"
                )
            continue

        # If we're at the top level and we're reading in the key but we hit an invalid character for keys,
        # we need to assume this is a multi-line value for the last top-level entry
        if not (re.match(VALID_KEY_CHARS, c)) and reading_top_key:
            multiline_value = True
            buffer += c
            continue

        # A newline almost always means we're done reading in a top-level entry's value...
        if c == "\n" and len(obj_stack) == 0:
            # unless we're reading in a multiline value, in which case
            # we need to append it to the previous entry's value
            if multiline_value:
                prev_node[prev_key] += f"\n{buffer}"
                buffer = ""

                # not sure if the next line continues a multiline value or if its the
                # start of a new top-level object. We assume it's not until we hit
                # an invalid character for a new top-level key :(
                multiline_value = False
                continue

            # othwerwise what's in the buffer is a single-line string value that we want to save
            curr_node[curr_key] = system_state_value_to_type(buffer)

            # saving the current key/value in a temporary structure in
            # case it's actually a multiline one so we can update it later if needed
            prev_node = curr_node
            prev_key = curr_key

            # starting a new top-level entry
            buffer = ""
            curr_key = ""
            reading_top_key = True

            continue

        # An open bracket, brace, or parens means we're starting a new sub-object
        if c in ["{", "[", "("] and not reading_key and not multiline_value:
            # ..but only if it's followed by a space. If it's not, we're still reading characters
            # into our buffer
            next_c = stream.read(1)
            if next_c != " ":
                buffer += c + next_c
                continue

            if buffer:
                raise ValueError(
                    f"Unexpected '{c}' at {stream.tell()}. Buffer: '{buffer}'"
                )

            obj_stack.append((curr_node, curr_key))

            if c == "{":
                curr_node = {}

            if c == "[":
                curr_node = []
            if c == "(":
                curr_node = MutableTuple()

            curr_key = ""
            continue

        # a single quote indicates the start or end of a sub-object dictionary key
        if c == "'" and not reading_key:
            if not isinstance(curr_node, dict):
                raise ValueError(f"unexpected '{c}' at {stream.tell()}")
            reading_key = True
            continue

        # if we're done reading in a sub-key we expect there to be a colon and a space
        if c == "'" and reading_key:
            if stream.read(2) != ": ":
                raise ValueError(
                    f"Expect colon after dict key {buffer} at {stream.tell()}"
                )
            curr_key = buffer
            buffer = ""
            reading_key = False
            continue

        # A comma often means we've finished reading a value in a sub-object (dict/list/tuple)...
        if c == ",":
            # ..but only if it's followed by a space. If it's not, we're still reading characters
            # into our buffer
            next_c = stream.read(1)
            if next_c != " ":
                buffer += c + next_c
                continue

            # if the next character was a space we need to save it to our current object
            if isinstance(curr_node, dict) and reading_key:
                raise ValueError(f"Unexpected comma at {stream.tell()}")

            if isinstance(curr_node, list) and buffer:
                curr_node.append(system_state_value_to_type(buffer))
            elif isinstance(curr_node, dict) and curr_key:
                curr_node[curr_key] = system_state_value_to_type(buffer)

            buffer = ""
            continue

        # A close bracket, brace, or parens means we're ending an object...
        if c in ["}", "]", ")"] and not (multiline_value or reading_key):
            # but only if the next two characters are a comma followed by a space,
            # or if the next character is a newline. If not, this is just
            # part of our value and we want to save it to the buffer and move on.
            next_c = stream.read(2)
            if len(next_c) == 2 and next_c != ", " and next_c[0] != "\n":
                buffer += c + next_c
                continue

            if c == "}" and not isinstance(curr_node, dict):
                raise ValueError(f"Unexpected '{c}' at {stream.tell()}")
            if c == "]" and not isinstance(curr_node, list):
                raise ValueError(f"Unexpected '{c}' at {stream.tell()}")
            if c == ")" and not isinstance(curr_node, MutableTuple):
                raise ValueError(f"Unexpected '{c}' at {stream.tell()}")

            # convert our 'mutable' tuple to a real one
            if isinstance(curr_node, MutableTuple):
                curr_node = tuple(curr_node)

            # save this object to the parent (either append or update as applicable)
            (parent_node, parent_key) = obj_stack.pop()
            if parent_key:
                parent_node[parent_key] = curr_node
            else:
                parent_node.append(curr_node)

            # set parent to current node
            curr_node = parent_node
            curr_key = ""

            # if the character after the close bracket/brace etc was a newline
            # and we were at the top of the stack, we started reading in
            # a new top-level object's key (one character past the newline)
            if len(next_c) == 2 and next_c[0] == "\n" and len(obj_stack) == 0:
                buffer += next_c[1]
                reading_top_key = True

            continue

        # add this key to our buffer

        buffer += c

    return curr_node
