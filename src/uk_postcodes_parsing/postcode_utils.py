import re
from typing import Union

# Tests for district
DISTRICT_SPLIT_REGEX = re.compile(r"^([a-z]{1,2}\d)([a-z])$", re.I)

# Tests for the unit section of a postcode
UNIT_REGEX = re.compile(r"[a-z]{2}$", re.I)

# Tests for the inward code section of a postcode
INCODE_REGEX = re.compile(r"\d[a-z]{2}$", re.I)

# Tests for the outward code section of a postcode
OUTCODE_REGEX = re.compile(r"^[a-z]{1,2}\d[a-z\d]?$", re.I)

# Tests for a valid postcode
POSTCODE_REGEX = re.compile(r"^[a-z]{1,2}\d[a-z\d]?\s*\d[a-z]{2}$", re.I)

# Tests for the area section of a postcode
AREA_REGEX = re.compile(r"^[a-z]{1,2}", re.I)


def sanitize(s: str) -> str:
    return s.replace(" ", "").upper()


def is_valid(postcode: str) -> bool:
    return re.match(POSTCODE_REGEX, postcode) is not None


def is_valid_outcode(outcode: str) -> bool:
    return re.match(OUTCODE_REGEX, outcode) is not None


def to_normalised(postcode: str) -> Union[str, None]:
    outcode = to_outcode(postcode)
    if outcode is None:
        return None
    incode = to_incode(postcode)
    return None if incode is None else f"{outcode} {incode}"


def to_outcode(postcode: str) -> Union[str, None]:
    if not is_valid(postcode):
        return None
    return re.sub(INCODE_REGEX, "", sanitize(postcode))


def to_incode(postcode: str) -> Union[str, None]:
    if not is_valid(postcode):
        return
    incode = re.findall(INCODE_REGEX, sanitize(postcode))
    return incode[0] if incode else None


def to_area(postcode: str) -> Union[str, None]:
    if not is_valid(postcode):
        return None
    area = re.findall(AREA_REGEX, sanitize(postcode))
    return area[0] if area else None


def to_sector(postcode: str) -> Union[str, None]:
    outcode = to_outcode(postcode)
    if outcode is None:
        return None
    incode = to_incode(postcode)
    return None if incode is None else f"{outcode} {incode[0]}"


def to_unit(postcode: str) -> Union[str, None]:
    if not is_valid(postcode):
        return None
    unit = re.findall(UNIT_REGEX, sanitize(postcode))
    return unit[0] if unit else None


def to_district(postcode):
    outcode = to_outcode(postcode)
    if outcode is None:
        return None
    district = re.match(DISTRICT_SPLIT_REGEX, outcode)
    return district[1] if district else outcode


def to_sub_district(postcode):
    outcode = to_outcode(postcode)
    if outcode is None:
        return None
    split = re.match(DISTRICT_SPLIT_REGEX, outcode)
    return None if split is None else outcode
