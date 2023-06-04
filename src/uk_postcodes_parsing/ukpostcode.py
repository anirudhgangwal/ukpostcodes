"""
ukpostcode.py: main module for parsing UK postcodes from text.
"""
import re
import logging
from dataclasses import dataclass, field
from typing import Union, List, Optional

from uk_postcodes_parsing.postcode_utils import (
    is_valid,
    to_normalised,
    to_outcode,
    to_incode,
    to_area,
    to_sector,
    to_unit,
    to_district,
    to_sub_district,
)
from uk_postcodes_parsing.fix import fix
from uk_postcodes_parsing.postcodes_nov_2022 import POSTCODE_NOV_2022

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uk-postcodes-parsing")

# Test for a valid postcode embedded in text
POSTCODE_CORPUS_REGEX = re.compile(r"[a-z]{1,2}\d[a-z\d]?\s*\d[a-z]{2}", re.I)
FIXABLE_POSTCODE_CORPUS_REGEX = re.compile(
    r"[a-z01]{1,2}[0-9oi][a-z\d]?\s*[0-9oi][a-z01]{2}"
)


@dataclass(order=True)
class Postcode:
    """Class to hold the parsed postcode.
    Constructor arguments:
        original (str): The raw (original) string of the postcode.
        postcode (str): The postcode as a string.
        incode (str): The inward code (the first 3 characters) of the postcode.
        outcode (str): The outward code (the last 4 characters) of the postcode.
        area (str): The area of the postcode.
        district (str): The district of the postcode.
        sub_district (str): The sub-district of the postcode.
        sector (str): The sector of the postcode.
        unit (str): The unit of the postcode.

    Additional attributes:
        is_in_ons_postcode_directory (bool): Whether the postcode was successfully verified against
            [ONS Postcode Directory](https://geoportal.statistics.gov.uk/datasets/489c152010a3425f80a71dc3663f73e1/about).
        fix_distance (int): The number of characters that the postcode string was corrected by the `fix` function during parsing.
    """

    # Calculate post initialization
    is_in_ons_postcode_directory: bool = field(init=False)
    fix_distance: int = field(init=False)
    # raw text
    original: str
    # The rest of the fields are parsed from the postcode using regex
    postcode: str
    incode: str
    outcode: str
    area: str
    district: str
    sub_district: Union[str, None]
    sector: str
    unit: str

    def __post_init__(self):
        """calculate class attributes after initialization.
        - `is_in_ons_postcode_directory` (bool)
        - `fix_distance` (int): the "edit distance" between the raw postcode and final postcode
        """
        # Convert raw (original) string in postcode format
        original = self.original.upper().strip().replace(r"\s+", "")
        inward = original[-3:].strip()
        outward = original[:-3].strip()
        formatted = f"{outward} {inward}"

        fix_distance = sum(c1 != c2 for c1, c2 in zip(formatted, self.postcode))

        self.fix_distance = fix_distance
        self.is_in_ons_postcode_directory = is_in_ons_postcode_directory(self.postcode)

    def __eq__(self, other):
        """Ignore is_in_ons_postcode_directory and fix_distance."""
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


def _parse(postcode: str) -> dict:
    """Internal function to parse postcode string using `uk_postcodes_parsing.postcode_utils`

    Args:
        postcode (str): Postcode to parse. E.g. "EC1R 1UB".
    Returns:
        dict: Parsed postcode.
    """
    if postcode.upper().startswith("NPT"):  # Edge case logging
        logger.warning("Found 'NPT' Newport postcode discontinued in 1984.")
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


def parse(postcode, attempt_fix=True) -> Optional[Postcode]:
    """Parse a postcode

    Args:
        postcode (str): Postcode to parse. E.g. "EC1R 1UB".
        attempt_fix (bool): Attempt to fix postcodes. Defaults to True.
    Returns:
        Postcode: Parsed postcode.
    """
    if is_valid(postcode):
        return Postcode(**_parse(postcode), original=postcode)
    if attempt_fix:
        fixed = fix(postcode)
        if is_valid(fixed):
            logger.info("Postcode Fixed: '%s' => '%s'", postcode, fixed)
            return Postcode(**_parse(fixed), original=postcode)
        logger.error("Unable to fix postcode")
    logger.error("Failed to parse postcode: %s", postcode)
    return None


def parse_from_corpus(text: str, attempt_fix=False) -> List[str]:
    """Parse postcodes from a text corpus

    Args:
        text (str): Text corpus. E.g. "The postcode could be EC1R 1UB or EC1R IUB"
        attempt_fix (bool): Attempt to fix postcodes. Defaults to False.
    Returns:
        List[Postcode]: List of parsed postcodes.

    """
    if attempt_fix:
        postcodes = re.findall(FIXABLE_POSTCODE_CORPUS_REGEX, text.lower())
    else:
        postcodes = re.findall(POSTCODE_CORPUS_REGEX, text.lower())
    logger.info("Found %d postcodes in corpus", len(postcodes))
    return list(map(parse, postcodes))


def is_in_ons_postcode_directory(postcode: str) -> bool:
    """Check if the postcode is valid with postcodes.io

    Args:
        postcode (str): The postcode to check

    Returns:
        bool: True if the postcode is valid, False otherwise
    """
    return postcode in POSTCODE_NOV_2022
