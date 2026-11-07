"""Runtime contract primitives adapted from the reviewed Stage09 reference; no world mutation."""

from __future__ import annotations

import copy
import hashlib
import json
import math
from typing import Any


class ContractError(ValueError):
    def __init__(self, code: str, message: str, *, step: int | None = None):
        super().__init__(message)
        self.code = code
        self.step = step


_ALLOWED_ACTION_FIELDS = {
    "move": {"type", "direction"},
    "scan": {"type", "direction"},
    "interact": {"type", "target"},
    "wait": {"type", "ticks"},
    "report": {"type", "label"},
}
_DIRECTIONS = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
_ALLOWED_LEGACY_STATUSES = {
    "finished",
    "syntax_error",
    "runtime_error",
    "invalid_challenge",
    "timeout",
    "worker_crash",
}


def _strict_integer(x: Any, low: int = 0, high: int = 2**31 - 1) -> bool:
    return type(x) is int and low <= x <= high


def safe_json(value: Any, *, max_bytes: int = 262144, max_depth: int = 16) -> bytes:
    """Reject non-JSON types, nonfinite scalars, key abuse and excessive nesting/size.

    This is input hygiene, *not* OS containment or protection against hostile Python.
    """

    def walk(obj: Any, depth: int, budget: list[int]) -> None:
        if depth > max_depth:
            raise ContractError("INVALID_INPUT", "JSON nesting limit exceeded")
        budget[0] += 1
        if budget[0] > 35000:
            raise ContractError("INVALID_INPUT", "Too many JSON nodes")
        if obj is None or type(obj) in (str, bool, int):
            if type(obj) is str and len(obj) > 65536:
                raise ContractError("INVALID_INPUT", "Individual string too large")
            return
        if type(obj) is float:
            if not math.isfinite(obj):
                raise ContractError("INVALID_INPUT", "Non-finite float rejected")
            return
        if type(obj) is list:
            if len(obj) > 8192:
                raise ContractError("INVALID_INPUT", "Array length limit exceeded")
            for part in obj:
                walk(part, depth + 1, budget)
            return
        if type(obj) is dict:
            if len(obj) > 512 or any(type(k) is not str or len(k) > 128 for k in obj):
                raise ContractError("INVALID_INPUT", "Invalid or excessive object keys")
            for part in obj.values():
                walk(part, depth + 1, budget)
            return
        raise ContractError("INVALID_INPUT", f"Not a JSON value: {type(obj).__name__}")

    walk(value, 0, [0])
    try:
        encoded = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except (ValueError, TypeError, OverflowError) as exc:
        raise ContractError("INVALID_INPUT", "Invalid JSON payload") from exc
    if len(encoded) > max_bytes:
        raise ContractError("INVALID_INPUT", "JSON byte budget exceeded")
    return encoded


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(safe_json(value)).hexdigest()


def source_digest(code: str) -> str:
    if type(code) is not str or len(code.encode("utf-8")) > 65536:
        raise ContractError("INVALID_INPUT", "Python source exceeds 64 KiB")
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def normalize_legacy_result(*, mission_id: str, request_id: str, report: dict) -> dict:
    """Adapt current core.grade.grade output without allowing unvalidated live effects."""
    if type(report) is not dict or report.get("status") not in _ALLOWED_LEGACY_STATUSES:
        raise ContractError("SCHEMA_MISMATCH", "Unrecognized legacy worker status")
    if type(report.get("passed")) is not bool or type(report.get("rows")) is not list:
        raise ContractError("SCHEMA_MISMATCH", "Missing pass flag or rows")
    if len(report["rows"]) > 128 or any(
        type(r) is not str or len(r) > 1024 for r in report["rows"]
    ):
        raise ContractError("INVALID_OUTPUT", "Unbounded worker report")
    line = report.get("line")
    if line is not None and not _strict_integer(line, 1):
        raise ContractError("SCHEMA_MISMATCH", "Invalid traceback line number")
    if report["passed"] and report["status"] != "finished":
        raise ContractError("SCHEMA_MISMATCH", "Only finished evaluations can pass")
    effect = report.get("effect") if report["passed"] else None
    safe_json(effect)
    pc = report.get("passed_count", 0)
    total = report.get("total_count", len(report["rows"]))
    if not _strict_integer(pc) or not _strict_integer(total) or pc > total:
        raise ContractError("SCHEMA_MISMATCH", "Invalid test counts")
    if report["passed"] and (total == 0 or pc != total):
        raise ContractError("SCHEMA_MISMATCH", "Passed evaluation must pass all cases")
    code = (
        {
            "syntax_error": "SYNTAX_ERROR",
            "runtime_error": "RUNTIME_ERROR",
            "invalid_challenge": "INVALID_INPUT",
            "timeout": "TIMEOUT",
            "worker_crash": "WORKER_CRASH",
        }
    ).get(report["status"], "TEST_FAILED")
    out = {
        "protocol_version": 1,
        "request_id": request_id,
        "mission_id": mission_id,
        "status": report["status"],
        "passed": report["passed"],
        "passed_count": pc,
        "total_count": total,
        "line": line,
        "rows": list(report["rows"]),
        "errors": []
        if report["passed"]
        else [
            {
                "code": code,
                "message": str(report["rows"][0] if report["rows"] else report["status"])[:480],
            }
        ],
        "effect": copy.deepcopy(effect),
    }
    safe_json(out)
    return out


def validate_action_plan(observation: dict, plan: dict) -> dict:
    """Pure candidate validation. No changes to game objects, XP or world_flags.

    Parent must independently inspect the real current world at commit time.
    The returned trace is NOT a commit authorization by itself.
    """
    safe_json(observation)
    safe_json(plan)
    if type(observation) is not dict or observation.get("schema") != 1 or type(plan) is not dict:
        raise ContractError("SCHEMA_MISMATCH", "Require observation-v1 and action-plan-v1 objects")
    if set(plan) - {"schema", "snapshot_id", "actions", "program_id"} or plan.get("schema") != 1:
        raise ContractError("SCHEMA_MISMATCH", "Unrecognized action plan envelope")
    if type(plan.get("snapshot_id")) is not str or plan["snapshot_id"] != observation.get(
        "snapshot_id"
    ):
        raise ContractError("STALE_SNAPSHOT", "Plan targets a different world snapshot")
    actions = plan.get("actions")
    if type(actions) is not list:
        raise ContractError("INVALID_ACTION", "Plan actions must be a list")
    rules = observation.get("rules", {})
    max_actions = rules.get("max_actions")
    if not _strict_integer(max_actions, 1, 64) or len(actions) > max_actions:
        raise ContractError("INVALID_ACTION", "Action budget exceeded")
    visible = observation.get("visible", {})
    width, height = visible.get("width"), visible.get("height")
    if not _strict_integer(width, 1, 256) or not _strict_integer(height, 1, 256):
        raise ContractError("INVALID_INPUT", "Invalid world bounds")

    def parse_cell(point: Any):
        if type(point) is not list or len(point) != 2 or not all(_strict_integer(v) for v in point):
            raise ContractError("INVALID_INPUT", "Expected nonnegative integer cell")
        return tuple(point)

    blocked = set()
    for point in visible.get("walls", []):
        blocked.add(parse_cell(point))
    for point in blocked:
        if point[0] >= width or point[1] >= height:
            raise ContractError("INVALID_INPUT", "Wall outside declared bounds")
    robot = observation.get("robot", {})
    pos = parse_cell(robot.get("cell"))
    if not (pos[0] < width and pos[1] < height) or pos in blocked:
        raise ContractError("INVALID_INPUT", "Robot start collides with world")
    energy = robot.get("energy")
    if not _strict_integer(energy):
        raise ContractError("INVALID_INPUT", "Robot energy must be nonnegative integer")
    abilities = set(robot.get("abilities", []))
    devices = {}
    for device in visible.get("devices", []):
        if type(device) is not dict or type(device.get("id")) is not str:
            raise ContractError("INVALID_INPUT", "Invalid visible device")
        target = parse_cell(device.get("cell"))
        if target[0] >= width or target[1] >= height or device["id"] in devices:
            raise ContractError("INVALID_INPUT", "Invalid or duplicate device")
        devices[device["id"]] = target
    intents, trace = [], []
    spent = 0
    for i, action in enumerate(actions):
        if type(action) is not dict or action.get("type") not in _ALLOWED_ACTION_FIELDS:
            raise ContractError("INVALID_ACTION", "Unknown action type", step=i)
        kind = action["type"]
        if set(action) != _ALLOWED_ACTION_FIELDS[kind]:
            raise ContractError("INVALID_ACTION", "Action fields do not match contract", step=i)
        before = pos
        cost = 0
        if kind in ("move", "scan"):
            if action.get("direction") not in _DIRECTIONS:
                raise ContractError("INVALID_ACTION", "Invalid cardinal direction", step=i)
            if kind not in abilities:
                raise ContractError("MISSING_CAPABILITY", kind + " unavailable", step=i)
            if kind == "move":
                dx, dy = _DIRECTIONS[action["direction"]]
                candidate = (pos[0] + dx, pos[1] + dy)
                if (
                    candidate[0] < 0
                    or candidate[1] < 0
                    or candidate[0] >= width
                    or candidate[1] >= height
                    or candidate in blocked
                ):
                    raise ContractError("COLLISION", f"Blocked destination {candidate}", step=i)
                pos = candidate
                cost = rules.get("step_energy", 1)
            else:
                cost = rules.get("scan_energy", 2)
        elif kind == "interact":
            if kind not in abilities:
                raise ContractError("MISSING_CAPABILITY", "interact unavailable", step=i)
            name = action.get("target")
            if type(name) is not str or name not in devices:
                raise ContractError("INVALID_ACTION", "Target not in visible devices", step=i)
            at = devices[name]
            if abs(at[0] - pos[0]) + abs(at[1] - pos[1]) != 1:
                raise ContractError("DEVICE_NOT_ADJACENT", f"{name} not adjacent", step=i)
            cost = rules.get("interact_energy", 1)
            intents.append({"device_id": name, "operation": "activate", "at_step": i})
        elif kind == "wait":
            if not _strict_integer(action.get("ticks"), 1, 5):
                raise ContractError("INVALID_ACTION", "wait ticks must be 1..5", step=i)
        elif kind == "report":
            if type(action.get("label")) is not str or not 1 <= len(action["label"]) <= 120:
                raise ContractError(
                    "INVALID_ACTION", "report label must have 1..120 characters", step=i
                )
        if not _strict_integer(cost):
            raise ContractError("INVALID_INPUT", "Invalid energy tariff", step=i)
        energy -= cost
        spent += cost
        if energy < 0:
            raise ContractError("ENERGY_EXHAUSTED", "Insufficient energy", step=i)
        trace.append(
            {
                "step": i,
                "action": copy.deepcopy(action),
                "from_cell": list(before),
                "to_cell": list(pos),
                "energy_remaining": energy,
            }
        )
    result = {
        "final_cell": list(pos),
        "remaining_energy": energy,
        "energy_used": spent,
        "trace": trace,
        "proposed_intents": intents,
        "snapshot_id": plan["snapshot_id"],
    }
    safe_json(result)
    return result
