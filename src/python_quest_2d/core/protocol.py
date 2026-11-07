"""Opt-in v1 envelopes around the unchanged legacy curriculum evaluator."""

import copy, os, re, uuid

if __package__:
    from .contracts import (
        ContractError,
        safe_json,
        source_digest,
        canonical_digest,
        normalize_legacy_result,
        validate_action_plan,
    )
else:
    from contracts import (
        ContractError,
        safe_json,
        source_digest,
        canonical_digest,
        normalize_legacy_result,
        validate_action_plan,
    )

REGISTRY = {"execution_request": 1, "evaluation_result": 1, "mica.plan": 1}
MAX_RESPONSE_BYTES = 262144


def enabled():
    return os.environ.get("PYTHONQUEST_CONTRACTS_V1") == "1"


def validate_request(req):
    safe_json(req)
    if (
        type(req) is not dict
        or type(req.get("protocol_version")) is not int
        or req["protocol_version"] != 1
    ):
        raise ContractError("SCHEMA_MISMATCH", "Unsupported protocol version")
    allowed = {
        "kind",
        "protocol_version",
        "request_id",
        "mission_id",
        "source",
        "challenge",
        "observation",
        "program_contract",
        "fixture_set_id",
        "source_hash",
    }
    if set(req) - allowed:
        raise ContractError("SCHEMA_MISMATCH", "Unknown request fields")
    for name in ("request_id", "mission_id"):
        if not isinstance(req.get(name), str) or not re.fullmatch(
            "[a-z][a-z0-9_.-]{0,63}", req[name]
        ):
            raise ContractError("SCHEMA_MISMATCH", "Invalid " + name)
    digest = source_digest(req.get("source"))
    if req.get("source_hash", digest) != digest:
        raise ContractError("STALE_SNAPSHOT", "Source revision changed")
    if req.get("kind") == "legacy_mission":
        if (
            type(req.get("challenge")) is not dict
            or req["challenge"].get("id") != req["mission_id"]
        ):
            raise ContractError("SCHEMA_MISMATCH", "Challenge mismatch")
    elif req.get("kind") == "program_plan":
        if (
            req.get("program_contract") != "mica.plan.v1"
            or type(req.get("observation")) is not dict
            or "source_hash" not in req
        ):
            raise ContractError("SCHEMA_MISMATCH", "Missing plan contract")
    else:
        raise ContractError("SCHEMA_MISMATCH", "Unknown request kind")
    return copy.deepcopy(req)


def request(ch, source):
    return validate_request(
        dict(
            kind="legacy_mission",
            protocol_version=1,
            request_id="request-" + uuid.uuid4().hex,
            mission_id=ch["id"],
            source=source,
            source_hash=source_digest(source),
            challenge=ch,
        )
    )


def decode_result(raw, req=None):
    import json

    if len(raw) > MAX_RESPONSE_BYTES:
        raise ContractError("INVALID_OUTPUT", "Response byte limit exceeded")
    report = json.loads(raw)
    if type(report) is not dict:
        raise ContractError("SCHEMA_MISMATCH", "Worker result must be an object")
    if req is not None:
        for name in ("protocol_version", "request_id", "mission_id"):
            if type(report.get(name)) is not type(req[name]) or report.get(name) != req[name]:
                raise ContractError("SCHEMA_MISMATCH", "Worker request identity mismatch")
    return normalize_legacy_result(
        mission_id=req["mission_id"] if req else "legacy",
        request_id=req["request_id"] if req else "legacy",
        report=report,
    )


def validate_candidate(observation, plan, *, snapshot_digest, source, source_hash):
    if canonical_digest(observation) != snapshot_digest or source_digest(source) != source_hash:
        raise ContractError("STALE_SNAPSHOT", "World or source changed; rescan before verification")
    return validate_action_plan(copy.deepcopy(observation), copy.deepcopy(plan))
