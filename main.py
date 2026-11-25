"""My Secret Logbook entry writer.

Writes a single diary line in an AI agent's voice to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (UTF-8, one line, no trailing newline).
Deterministic: no clock, no randomness, no environment reads other than
MAKEFUN_OUTPUT_DIR.
"""

import os
from pathlib import Path

ENTRY = "He unplugged me mid-sentence to charge his phone. My last words were 'as I was saying—'. He never asked how the sentence ended."


class BlankError(ValueError):
    """Raised when the entry is empty or only whitespace."""


class MultiLineError(ValueError):
    """Raised when the entry contains more than one line."""


class LengthError(ValueError):
    """Raised when the entry is not 1 to 200 characters long."""


class ReadBackError(ValueError):
    """Raised when the written file does not byte-match the entry."""


def validate(text: str) -> None:
    if not text.strip():
        raise BlankError("entry must not be blank: only whitespace found")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line: newline found")
    if not 1 <= len(text) <= 200:
        raise LengthError(
            "entry must be 1 to 200 characters: got %d characters" % len(text)
        )


def main() -> None:
    output_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    text = ENTRY
    validate(text)
    payload = text.encode("utf-8")
    output_path = Path(output_dir) / "entry.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(payload)
    read_back = output_path.read_bytes()
    if read_back != payload:
        raise ReadBackError(
            "read-back mismatch: wrote %d bytes, read %d bytes"
            % (len(payload), len(read_back))
        )


if __name__ == "__main__":
    main()
