import re

FIXABLE_REGEX = re.compile(
    r"^\s*[a-z01]{1,2}[0-9oi][a-z\d]?\s*[0-9oi][a-z01]{2}\s*$", re.I
)


def fix(s: str) -> str:
    match = FIXABLE_REGEX.match(s)
    if match is None:
        return s
    s = s.upper().strip().replace(r"\s+", "")
    inward = s[-3:].strip()
    outward = s[:-3].strip()
    return f"{coerce_outcode(outward)} {coerce_incode(inward)}"


def to_letter(c: str) -> str:
    return {
        "0": "O",
        "1": "I",
    }.get(c, c)


def to_number(c: str) -> str:
    return {
        "O": "0",
        "I": "1",
    }.get(c, c)


def coerce(pattern: str, input: str) -> str:
    """
    Coerce a given input into a pattern. For e.g.
            pattern: "LN" => signifies a letter followed by a number
            input: "01" => changes to "O1". Where the first 0 should be a letter so it
                is coverted from 0 to O. The Second 1 is already correct so no change.
    """
    return "".join(
        to_number(c) if target == "N" else to_letter(c) if target == "L" else c
        for c, target in zip(input, pattern)
    )


def coerce_outcode(i: str) -> str:
    """Coerce outcode based on length of outcode"""
    if len(i) == 2:
        return coerce("LN", i)
    elif len(i) == 3:
        return coerce("L??", i)
    elif len(i) == 4:
        return coerce("LLN?", i)
    else:
        return i


def coerce_incode(i: str) -> str:
    """Coerce incode"""
    return coerce("NLL", i)
