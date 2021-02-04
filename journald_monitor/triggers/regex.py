import re

from re import Match
from typing import cast, Any, AnyStr, Optional

def regex(line: AnyStr, config: dict, regex: AnyStr) -> Optional[Match]:
    return re.match(regex, line)

def regex_execute_action(trigger_result: Any, action_params: dict, action_function):
    match: Match = trigger_result

    for param, value in action_params.items():
        if isinstance(value, str):
            for i, val in enumerate(match.groups(), start=1):
                action_params[param] = action_params[param].replace('$' + str(i), val)

    action_function(**action_params)
