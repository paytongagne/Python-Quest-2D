"""Trusted object fixtures, executed only inside the disposable Python worker."""

import copy


def exercise(ns, ch, case):
    if ch.get("contract"):
        if __package__:
            from .engineering_cases import exercise as engineering
        else:
            from engineering_cases import exercise as engineering
        return engineering(ns, ch, case)
    cls = ns.get(ch["class_name"])
    if not isinstance(cls, type):
        raise TypeError("Define class " + ch["class_name"])
    if ch.get("property") and not isinstance(getattr(cls, ch["property"], None), property):
        raise TypeError(ch["property"] + " must be a property")
    objects = [cls(*copy.deepcopy(args)) for args in case["construct"]]
    if len({id(o) for o in objects}) != len(objects):
        raise ValueError("Instances must be independent")
    returns = []
    for step in case.get("steps", []):
        expected_error = step.get("raises")
        try:
            if step["op"] == "new":
                cls(*copy.deepcopy(step["args"]))
            elif step["op"] == "set":
                value = copy.deepcopy(step["value"])
                if isinstance(value, dict) and "special_float" in value:
                    value = float(value["special_float"])
                setattr(objects[step["object"]], step["name"], value)
            else:
                returns.append(
                    getattr(objects[step["object"]], step["name"])(*copy.deepcopy(step["args"]))
                )
        except (TypeError, ValueError) as exc:
            if type(exc).__name__ != expected_error:
                raise
        else:
            if expected_error:
                raise ValueError("Expected " + expected_error + " for " + str(step))
    state = [{name: getattr(o, name) for name in ch["attributes"]} for o in objects]
    return {"state": state, "returns": returns}
