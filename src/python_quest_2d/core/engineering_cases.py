"""Trusted advanced fixtures, executed only in the short-lived worker."""

import builtins
import tempfile
from pathlib import Path


def exercise(ns, ch, case):
    mode = ch["contract"]
    if mode == "family":
        base = ns.get("Rover")
        classes = [ns.get("SurveyRover"), ns.get("CargoRover")]
        if not isinstance(base, type) or any(
            not isinstance(c, type) or not issubclass(c, base) or c is base for c in classes
        ):
            raise TypeError("SurveyRover and CargoRover must inherit Rover")
        robots = [c(name) for c, name in zip(classes, case["names"])]
        reports = [o.report() for o in robots]
        robots[0].name = "changed"
        if robots[1].name != case["names"][1]:
            raise ValueError("Independent instance names required")
        return reports
    if mode == "composition":
        battery = ns["Battery"]
        rover = ns["Rover"]
        first, second = [battery(n) for n in case["charges"]]
        calls = []
        for core in (first, second):
            consume = core.consume

            def recorded(amount, method=consume):
                calls.append(amount)
                return method(amount)

            core.consume = recorded
        bot = rover(first)
        if bot.battery is not first:
            raise ValueError("Rover must hold the supplied Battery object")
        results = []
        for step in case["actions"]:
            if step == "swap":
                bot.battery = second
                continue
            try:
                result = bot.drive(step)
            except ValueError:
                results.append("rejected")
            else:
                results.append(result)
        if calls != [a for a in case["actions"] if a != "swap"]:
            raise ValueError("Delegate each drive to battery.consume")
        return dict(charges=[first.charge, second.charge], results=results)
    if mode == "sensor":
        fault = ns.get("SensorFault")
        if not isinstance(fault, type) or not issubclass(fault, ValueError) or fault is ValueError:
            raise TypeError("Define SensorFault as a subclass of ValueError")
        probe = ns["Sensor"](*case["limits"])
        results = []
        for value in case["readings"]:
            try:
                results.append(probe.read(value))
            except Exception as exc:
                if type(exc) is not fault:
                    raise TypeError("Raise exactly SensorFault")
                results.append("fault")
        return results
    if mode == "log":
        handles = []

        def tracked_open(*args, **kwargs):
            handle = builtins.open(*args, **kwargs)
            handles.append(handle)
            return handle

        ns["open"] = tracked_open
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "service.txt"
            if not case.get("missing"):
                path.write_bytes(case["text"].encode("utf8"))
            try:
                try:
                    result = ns["count_errors"](str(path))
                except FileNotFoundError:
                    if not case.get("missing"):
                        raise
                    result = "missing"
                if any(not h.closed for h in handles):
                    raise ValueError("Close the service log with a context manager")
                if not case.get("missing") and not handles:
                    raise ValueError("Read the supplied path with open()")
                return result
            finally:
                for h in handles:
                    h.close()
    raise ValueError("Unknown engineering contract")
