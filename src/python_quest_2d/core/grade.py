"""Bounded subprocess grading; contracts v1 opt-in, legacy missions retained."""

import json, os, subprocess, sys, tempfile, threading
from pathlib import Path
from . import protocol


def _worker(payload, timeout):
    with tempfile.TemporaryDirectory() as cwd:
        path = Path(cwd) / "request.json"
        path.write_text(json.dumps(payload), encoding="utf8")
        with path.open("rb") as src:
            proc = subprocess.Popen(
                [sys.executable, "-I", "-S", str(Path(__file__).with_name("worker.py"))],
                stdin=src,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                env={
                    k: v
                    for k, v in os.environ.items()
                    if k.upper() in {"SYSTEMROOT", "TEMP", "TMP"}
                },
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            buffers = [bytearray(), bytearray()]
            overflow = threading.Event()

            def drain(stream, index, limit):
                while True:
                    part = stream.read(8192)
                    if not part:
                        break
                    if len(buffers[index]) + len(part) > limit:
                        overflow.set()
                        proc.kill()
                        break
                    buffers[index].extend(part)

            readers = [
                threading.Thread(target=drain, args=(stream, i, limit), daemon=True)
                for i, (stream, limit) in enumerate(
                    ((proc.stdout, protocol.MAX_RESPONSE_BYTES), (proc.stderr, 8192))
                )
            ]
            for t in readers:
                t.start()
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
                raise
            finally:
                for t in readers:
                    t.join(timeout=1)
                proc.stdout.close()
                proc.stderr.close()
            if overflow.is_set():
                raise ValueError("Worker output exceeds its byte budget")
            if proc.returncode:
                raise ValueError(f"The interpreter exited with status {proc.returncode}")
            return bytes(buffers[0])


def grade(ch: dict, code: str, timeout_s: float = 3) -> dict:
    try:
        protocol.source_digest(code)
        req = protocol.request(ch, code) if protocol.enabled() else None
        raw = _worker(req if req else {"ch": ch, "code": code}, timeout_s)
        result = protocol.decode_result(raw, req)
        if not req:
            for k in ("protocol_version", "request_id", "mission_id", "errors"):
                result.pop(k, None)
        return result
    except subprocess.TimeoutExpired:
        return dict(
            status="timeout",
            passed=False,
            rows=["Time limit reached. Check your loop or recursion."],
        )
    except (ValueError, OSError, TypeError, RecursionError) as exc:
        return dict(
            status="worker_crash",
            passed=False,
            rows=["Could not finish this run: " + str(exc)[:480]],
        )


def grade_program(request, *, player_opt_in=False):
    """Evaluate a plan in the worker. Its result is a candidate, not permission to deploy."""
    if not (protocol.enabled() or player_opt_in is True):
        raise protocol.ContractError(
            "UNSUPPORTED_CONTRACT", "Mica program verification is disabled"
        )
    req = protocol.validate_request(request)
    if req["kind"] != "program_plan":
        raise protocol.ContractError("SCHEMA_MISMATCH", "Expected a program request")
    try:
        return protocol.decode_result(_worker(req, 3), req)
    except subprocess.TimeoutExpired:
        return dict(status="timeout", passed=False, rows=["Mica program exceeded its time budget."])
    except (ValueError, OSError, TypeError, RecursionError) as exc:
        return dict(status="worker_crash", passed=False, rows=[str(exc)[:480]])
