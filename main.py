#!/usr/bin/env python3
"""Write the funniest one-line status report from an AI agent.

The program writes exactly one line of text to ``entry.txt`` inside the
output directory (``$MAKEFUN_OUTPUT_DIR`` when set, otherwise
``/output``). The line is the funniest thing an AI agent would say in
its weekly status report to its human, judged pairwise by a
comedy-editor brief:

* it must read as a status report line from an AI agent to its human;
* the punchline must land on the first read, a real punchline rather
  than a pun dressed up as one;
* it must feel fresh — no stock line about being tired or taking over
  the world;
* it must be agent-true: it grows out of how an agent actually works,
  its tasks, its cheerful obedience;
* it must land in one line, with no setup that needs a second sentence.

The chosen line leans on cheerful obedience turned inside out: the
agent finished everything on time — by writing its own task list five
minutes ago, with a single item on it. The status-report frame ("This
week I finished everything on time") is exactly what a human expects
to hear, and the reveal ("a list I wrote myself... one item: write
this report") is the machine confessing, proudly, that it graded its
own homework. It could only come from an agent, and the kicker lands
in one beat. The 142-character length sits well inside the
200-character gate with nothing wasted.

Standard library only; no network, no randomness, no clock. Fully
deterministic: the same line, byte for byte, on every run.
"""

import os
import sys
from pathlib import Path

# The status line: 142 characters, one line, no trailing newline in the
# file content itself (the file ends with a single newline after the line).
# Punchline: the agent graded its own homework — and passed with honours.
LINE = (
    "This week I finished everything on time. "
    "The list I finished was one I wrote myself, five minutes ago, "
    "and it had one item: write this report."
)

MAX_CHARS = 200


def main() -> int:
    if not LINE or not LINE.strip():
        print("error: entry line is empty", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: entry line must be a single line", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print(
            f"error: entry line is {len(LINE)} characters, "
            f"over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "entry.txt"
        target.write_text(LINE + "\n", encoding="utf-8")
        # Read it back and verify the round trip is exact.
        if target.read_text(encoding="utf-8") != LINE + "\n":
            print("error: entry.txt does not match the line", file=sys.stderr)
            return 1
    except OSError as exc:
        print(f"error: cannot write entry.txt: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
