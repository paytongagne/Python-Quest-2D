"""One short-lived interpreter per submission. Use only local practice code."""

import ast
import copy
from pathlib import Path

if __name__ == "__main__":
    sys_path = str(Path(__file__).resolve().parent)
    import sys

    sys.path.insert(0, sys_path)
    from object_cases import exercise
    from route import trace
    from expedition_contract import validate
else:
    from .object_cases import exercise
    from .route import trace
    from .expedition_contract import validate
import contextlib
import io
import json
import sys
import traceback


class Output(io.StringIO):
    def write(self, value):
        if self.tell() + len(value) > 8192:
            raise ValueError("Console output exceeds 8192 characters")
        return super().write(value)


def match(actual, expected):
    if type(actual) in (int, float) and type(expected) in (int, float):
        return abs(actual - expected) < 1e-9
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(match(a, b) for a, b in zip(actual, expected))
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            match(actual[k], v) for k, v in expected.items()
        )
    return actual == expected


def evaluate(ch, code):
    try:
        compiled = compile(code, "terminal.py", "exec")
        if ch.get("contract") == "log" and not any(
            isinstance(n, ast.With) for n in ast.walk(ast.parse(code))
        ):
            return {
                "status": "finished",
                "passed": False,
                "rows": ["Use a with statement to manage the service-log file."],
            }
    except SyntaxError as exc:
        return {
            "status": "syntax_error",
            "passed": False,
            "line": exc.lineno,
            "rows": [f"Line {exc.lineno}: {exc.msg}"],
        }
    effect = None
    rows, successes, line = [], 0, None
    cases = ch.get("cases", [{}] + ch.get("variants", []))
    if not cases:
        return {
            "status": "invalid_challenge",
            "passed": False,
            "rows": ["No test cases configured"],
        }
    for i, case in enumerate(cases, 1):
        try:
            ns = {}
            with contextlib.redirect_stdout(Output()) as out, contextlib.redirect_stderr(out):
                program = compiled
                if "override" in case:
                    name, value = next(iter(case["override"].items()))
                    tree = ast.parse(code)
                    for node in tree.body:
                        targets = (
                            node.targets
                            if isinstance(node, ast.Assign)
                            else [node.target]
                            if isinstance(node, ast.AnnAssign)
                            else []
                        )
                        if any(isinstance(t, ast.Name) and t.id == name for t in targets):
                            node.value = ast.copy_location(ast.Constant(value=value), node)
                            break
                    else:
                        raise ValueError(
                            "Assign "
                            + name
                            + " at the top level so alternate inputs can be tested."
                        )
                    program = compile(tree, "terminal.py", "exec")
                exec(program, ns)
                if ch["kind"] == "script":
                    expected = case.get("expected_stdout", ch["expected_stdout"])
                    actual = out.getvalue()
                    ok = actual == expected
                    detail = (
                        f"{case['override']}  " if "override" in case else ""
                    ) + f"stdout expected {expected!r}, got {actual!r}"
                    for k, v in (
                        ch.get("expected_variables", {}) | case.get("override", {})
                    ).items():
                        if k not in ns or not match(ns[k], v):
                            ok = False
                            detail += f"; {k} expected {v!r}, got {ns.get(k)!r}"
                else:
                    if ch["kind"] == "object":
                        actual = exercise(ns, ch, case)
                    else:
                        fn = ns.get(ch["function_name"])
                        if not callable(fn):
                            raise NameError(
                                "Define " + ch["function_name"] + " before running tests"
                            )
                        actual = fn(*copy.deepcopy(case["args"]))
                    if ch.get("simulation") == "expedition":
                        try:
                            validated = validate(ch, case, actual)
                            ok = True
                            detail = f"Validated {str(actual)[:300]}"
                            if i == 1:
                                effect = validated
                        except ValueError as exc:
                            ok = False
                            detail = str(exc)
                    elif ch.get("simulation") == "route":
                        try:
                            trace(case["args"], actual)
                            ok = True
                            detail = f"Dock reached in {len(actual)} moves."
                            if i == 1:
                                effect = actual
                        except ValueError as exc:
                            ok = False
                            detail = str(exc)
                        detail += f" Grid/start/goal: {case['args']!r}"
                    else:
                        expected = case["expected"]
                        ok = match(actual, expected)
                        detail = f"{case['args']!r}: expected {expected!r}, got {actual!r}"
                        if (
                            i == 1
                            and ok
                            and (ch["id"] == "hydro_02" or ch.get("simulation") == "instrument")
                        ):
                            effect = actual
            successes += int(ok)
            rows.append(f"{'PASS' if ok else 'FAIL'}  {i}  {detail[:480]}")
        except BaseException as exc:
            frames = [
                f for f in traceback.extract_tb(exc.__traceback__) if f.filename == "terminal.py"
            ]
            line = frames[-1].lineno if frames else None
            rows.append(
                f"ERROR  {i}  {type(exc).__name__}: {str(exc)[:300]}"
                + (f" (line {line})" if line else "")
            )
    return {
        "status": "runtime_error" if any(r.startswith("ERROR") for r in rows) else "finished",
        "passed": successes == len(cases),
        "effect": effect if successes == len(cases) else None,
        "passed_count": successes,
        "total_count": len(cases),
        "line": line,
        "rows": rows,
    }


def evaluate_plan(request):
    from protocol import ContractError, safe_json, validate_action_plan

    obs = request["observation"]
    try:
        with contextlib.redirect_stdout(Output()) as out, contextlib.redirect_stderr(out):
            namespace = {}
            exec(compile(request["source"], "terminal.py", "exec"), namespace)
            actions = namespace["plan"](copy.deepcopy(obs))
            plan = {"schema": 1, "snapshot_id": obs["snapshot_id"], "actions": actions}
            safe_json(plan)
            validate_action_plan(obs, plan)
        return dict(
            status="finished",
            passed=True,
            passed_count=1,
            total_count=1,
            effect=plan,
            rows=["Plan produced; verify against the current world before use."],
        )
    except ContractError as exc:
        step = f"Step {exc.step + 1}: " if exc.step is not None else ""
        return dict(status="runtime_error", passed=False, rows=[f"{step}{exc.code}: {exc}"])
    except SyntaxError as exc:
        return dict(status="syntax_error", passed=False, line=exc.lineno, rows=[exc.msg])
    except BaseException as exc:
        return dict(
            status="runtime_error", passed=False, rows=[f"{type(exc).__name__}: {str(exc)[:380]}"]
        )


if __name__ == "__main__":
    payload = json.load(sys.stdin)
    if "protocol_version" in payload:
        from protocol import validate_request, normalize_legacy_result

        req = validate_request(payload)
        report = (
            evaluate(req["challenge"], req["source"])
            if req["kind"] == "legacy_mission"
            else evaluate_plan(req)
        )
        report = normalize_legacy_result(
            mission_id=req["mission_id"], request_id=req["request_id"], report=report
        )
    else:
        report = evaluate(**payload)
    print(json.dumps(report, allow_nan=False))
