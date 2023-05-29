import pandas as pd

from uk_postcodes_parsing.fix import fix
from uk_postcodes_parsing import ukpostcode
from uk_postcodes_parsing.ukpostcode import parse_from_corpus, Postcode


def test_fix():
    # Trims postcode
    assert fix(" SW1A 2AA ") == "SW1A 2AA"
    # Upper case
    assert fix(" Sw1A 2aa ") == "SW1A 2AA"
    # Fixes spacing
    assert fix(" Sw1A2aa ") == "SW1A 2AA"
    assert fix(" Sw1A    2aa ") == "SW1A 2AA"
    # Return original if not fixble
    assert fix(" 1A2aa ") == " 1A2aa "

    ## Outward code
    # Fixes LN format
    assert fix("01 OAA") == "O1 0AA"
    assert fix("SO OAA") == "S0 0AA"

    # Fixes L?? format
    assert fix("0W1 OAA") == "OW1 0AA"
    # ambiguous
    assert fix("S01 OAA") == "S01 0AA"
    assert fix("SO1 OAA") == "SO1 0AA"
    assert fix("SWO OAA") == "SWO 0AA"
    assert fix("SW0 OAA") == "SW0 0AA"

    # Fixes LNN?
    assert fix("0W1A OAA") == "OW1A 0AA"
    assert fix("S01A OAA") == "SO1A 0AA"
    assert fix("SWOA OAA") == "SW0A 0AA"
    # ambiguous
    assert fix("SW10 OAA") == "SW10 0AA"
    assert fix("SW1O OAA") == "SW1O 0AA"

    ## Inward code
    # first character
    assert fix(" SW1A OAA") == "SW1A 0AA"
    # second character
    assert fix("SW1A 20A") == "SW1A 2OA"
    # third character
    assert fix("SW1A 2A0") == "SW1A 2AO"
    # 1 <=> I
    assert fix("SWIA 2AA") == "SW1A 2AA"
    assert fix("1W1A 2AA") == "IW1A 2AA"


def test_parsing():
    corpus = "this is a check to see if we can get post codes liek thia ec1r   1ub , and that e3 4ss. But also eh16 50y and ei412"
    lst = parse_from_corpus(corpus)
    assert lst == [
        Postcode(
            original="ec1r   1ub",
            postcode="EC1R 1UB",
            incode="1UB",
            outcode="EC1R",
            area="EC",
            district="EC1",
            sub_district="EC1R",
            sector="EC1R 1",
            unit="UB",
        ),
        Postcode(
            original="e3 4ss",
            postcode="E3 4SS",
            incode="4SS",
            outcode="E3",
            area="E",
            district="E3",
            sub_district=None,
            sector="E3 4",
            unit="SS",
        ),
    ]

    corpus = "this is a check to see if we can get post codes liek thia ec1r 1ub , and that e34ss. But also eh16 50y and ei412"
    lst = parse_from_corpus(corpus, attempt_fix=True)
    assert lst == [
        Postcode(
            original="ec1r 1ub",
            postcode="EC1R 1UB",
            incode="1UB",
            outcode="EC1R",
            area="EC",
            district="EC1",
            sub_district="EC1R",
            sector="EC1R 1",
            unit="UB",
        ),
        Postcode(
            original="e34ss",
            postcode="E3 4SS",
            incode="4SS",
            outcode="E3",
            area="E",
            district="E3",
            sub_district=None,
            sector="E3 4",
            unit="SS",
        ),
        Postcode(
            original="eh16 50y",
            postcode="EH16 5OY",
            incode="5OY",
            outcode="EH16",
            area="EH",
            district="EH16",
            sub_district=None,
            sector="EH16 5",
            unit="OY",
        ),
    ]

def test_parsing_detailed():
    df = pd.read_csv("tests/data/postcode_parse_test.csv")
    df = df.where(pd.notnull(df), None)

    parsed_postcodes = df["Postcode"].apply(ukpostcode.parse)

    for i, parsed_postcode in enumerate(parsed_postcodes):
        assert parsed_postcode.outcode == df.iloc[i][".outcode"]
        assert parsed_postcode.incode == df.iloc[i][".incode"]
        assert parsed_postcode.area == df.iloc[i][".area"]
        assert parsed_postcode.district == df.iloc[i][".district"]
        assert parsed_postcode.sub_district == df.iloc[i][".subDistrict"]
        assert parsed_postcode.sector == df.iloc[i][".sector"]
        assert parsed_postcode.unit == df.iloc[i][".unit"]