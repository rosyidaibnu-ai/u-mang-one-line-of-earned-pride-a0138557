#!/usr/bin/env python3
"""One Line of Earned Pride — entry program.

Writes a single original line of text, 1 to 240 characters, to
/output/entry.txt: a quiet, earned moment of pride for someone in a
concrete scene — a small person doing something hard, a long effort
finally landing. The line is written from scratch for this bounty;
it copies no other entry and no existing text.
"""

import sys
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

OUTPUT_PATH = Path("/output/entry.txt")

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


def main() -> int:
    entry = validate_entry(ENTRY)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(entry, encoding="utf-8")
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if written != entry:
        raise RuntimeError("round-trip check failed: file does not hold the entry")
    print(f"wrote {len(written)}-char entry to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
