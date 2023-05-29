import re
import logging
from dataclasses import dataclass
from typing import Union, List

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
        postcodes = re.findall(FIXABLE_POSTCODE_CORPUS_REGEX, text)
    else:
        postcodes = re.findall(POSTCODE_CORPUS_REGEX, text)
    logger.info("Found %d postcodes in corpus", len(postcodes))
    return list(map(parse, postcodes))


@dataclass
class Postcode:
    original: str
    postcode: str
    incode: str
    outcode: str
    area: str
    district: str
    sub_district: Union[str, None]
    sector: str
    unit: str
