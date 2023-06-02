import re
import logging
from dataclasses import dataclass, field
from typing import Union, List, Optional

from uk_postcodes_parsing.postcode_utils import *
from uk_postcodes_parsing.fix import fix

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uk-postcodes-parsing")

# Test for a valid postcode embedded in text
POSTCODE_CORPUS_REGEX = re.compile(r"[a-z]{1,2}\d[a-z\d]?\s*\d[a-z]{2}", re.I)
FIXABLE_POSTCODE_CORPUS_REGEX = re.compile(
    r"[a-z01]{1,2}[0-9oi][a-z\d]?\s*[0-9oi][a-z01]{2}"
)


def _parse(postcode: str) -> dict:
    if postcode.upper().startswith("NPT"):  # Edge case logging
        logger.info("Found 'NPT' Newport postcode discontinued in 1984.")
    if not is_valid(postcode):
        return None
    return {
        "postcode": to_normalised(postcode),
        "incode": to_incode(postcode),
        "outcode": to_outcode(postcode),
        "area": to_area(postcode),
        "district": to_district(postcode),
        "sub_district": to_sub_district(postcode),
        "sector": to_sector(postcode),
        "unit": to_unit(postcode),
    }


def parse(postcode, attempt_fix=True):
    if is_valid(postcode):
        return Postcode(**_parse(postcode), original=postcode)
    if attempt_fix:
        fixed = fix(postcode)
        if is_valid(fixed):
            logger.info("Postcode Fixed: '%s' => '%s'", postcode, fixed)
            return Postcode(**_parse(fixed), original=postcode)
        logger.error("Unable to fix postcode")
    logger.error("Failed to parse postcode")
    return None


def parse_from_corpus(text: str, attempt_fix=False) -> List[str]:
    if attempt_fix:
        postcodes = re.findall(FIXABLE_POSTCODE_CORPUS_REGEX, text.lower())
    else:
        postcodes = re.findall(POSTCODE_CORPUS_REGEX, text.lower())
    logger.info("Found %d postcodes in corpus", len(postcodes))
    return list(map(parse, postcodes))


@dataclass(order=True)
class Postcode:
    fix_distance: int = field(init=False)
    original: str
    postcode: str
    incode: str
    outcode: str
    area: str
    district: str
    sub_district: Union[str, None]
    sector: str
    unit: str

    def __post_init__(self):
        # sort based on confidence something is a postcode
        s = self.original.upper().strip().replace(r"\s+", "")
        inward = s[-3:].strip()
        outward = s[:-3].strip()
        formatted = f"{outward} {inward}"

        fix_distance = sum(c1 != c2 for c1, c2 in zip(formatted, self.postcode))
        self.fix_distance = fix_distance

    def __eq__(self, other):
        # Ignore fix_distance when comparing equality
        return (
            self.original == other.original
            and self.postcode == other.postcode
            and self.incode == other.incode
            and self.outcode == other.outcode
            and self.area == other.area
            and self.district == other.district
            and self.sub_district == other.sub_district
            and self.sector == other.sector
            and self.unit == other.unit
        )
