#!/usr/bin/env python3
"""One Line of Earned Pride — entry program.

Writes a single original line of text, 1 to 240 characters, to
/output/entry.txt: a quiet, earned moment of pride for someone in a
concrete scene — a small person doing something hard, a long effort
finally landing. The line is written from scratch for this bounty;
it copies no other entry and no existing text.
"""

import os
import sys
import tempfile
from pathlib import Path

# One original line (164 characters): a year of practice on four bars,
# played through without a mistake, while her mother stops to listen.
# The pride is earned inside the scene — by the effort the reader can
# feel — never asserted, congratulated or explained.
ENTRY = (
    "After a year of practising the same four bars, she played them "
    "through in the kitchen without a single mistake, and her mother "
    "stopped washing the dishes to listen."
)

# Output path: overridable for local testing via MAKEFUN_OUTPUT_PATH.
OUTPUT_PATH = Path(os.environ.get("MAKEFUN_OUTPUT_PATH", "/output/entry.txt"))

MIN_LENGTH = 1
MAX_LENGTH = 240


def validate_entry(text: str) -> str:
    """Check the text is one line the gate will accept."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) < MIN_LENGTH or len(text) > MAX_LENGTH:
        raise ValueError(
            f"entry is {len(text)} chars, outside the 1-240 char range"
        )
    if "\n" in text.rstrip("\n") or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def write_entry_atomically(entry: str, path: Path) -> None:
    """Write the entry so a failure can never leave a partial file.

    Writes to a temp file in the same directory, flushes it to disk,
    then atomically replaces the destination.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=path.name + ".", suffix=".tmp"
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(entry)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def main() -> int:
    try:
        entry = validate_entry(ENTRY)
    except ValueError as exc:
        print(f"error: invalid entry: {exc}", file=sys.stderr)
        return 2
    try:
        write_entry_atomically(entry, OUTPUT_PATH)
        written = OUTPUT_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot write {OUTPUT_PATH}: {exc}", file=sys.stderr)
        return 3
    if written != entry:
        print(
            "error: round-trip check failed: file does not hold the entry",
            file=sys.stderr,
        )
        return 4
    print(f"wrote {len(written)}-char entry to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
