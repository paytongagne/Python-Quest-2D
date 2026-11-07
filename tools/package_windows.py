"""Build an offline Windows x64 archive from tracked source and pinned runtime inputs."""
import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import urllib.request
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
PYTHON_URL = "https://www.python.org/ftp/python/3.13.9/python-3.13.9-embed-amd64.zip"
PYTHON_SHA256 = "91d828c2da3a029b41699e918674a0cb379c02cf20dab9c501306885f837402a"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--runtime-zip", type=Path)
    args = parser.parse_args()
    if sys.platform != "win32" or sys.version_info[:2] != (3, 13) or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", args.tag):
        parser.error("Use Windows x64 Python 3.13 and a stable vX.Y.Z tag")
    output = ROOT / "dist" / f"Python-Quest-2D-{args.tag}-Windows-x64.zip"
    output.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        temp = Path(td)
        embedded = args.runtime_zip or temp / "python.zip"
        if not args.runtime_zip:
            urllib.request.urlretrieve(PYTHON_URL, embedded)
        if hashlib.sha256(embedded.read_bytes()).hexdigest() != PYTHON_SHA256:
            raise ValueError("Python runtime checksum mismatch")
        runtime = temp / "runtime"
        with ZipFile(embedded) as archive:
            archive.extractall(runtime)
        subprocess.run([sys.executable, "-m", "pip", "install", "--only-binary=:all:", "--no-compile", "--platform", "win_amd64", "--target", str(runtime), "-r", str(ROOT / "requirements.txt")], check=True)
        paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
        with ZipFile(output, "w", ZIP_DEFLATED) as archive:
            for path in filter(None, paths):
                archive.write(ROOT / path, "Python Quest 2D/" + path)
            for path in sorted(runtime.rglob("*")):
                rel = path.relative_to(runtime)
                if path.is_file() and "__pycache__" not in rel.parts and not any(part in {"tests", "examples", "docs"} for part in rel.parts):
                    archive.write(path, "Python Quest 2D/runtime/" + rel.as_posix())
    print(output)


if __name__ == "__main__":
    main()
