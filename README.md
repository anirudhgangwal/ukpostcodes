# uk-postcodes-parsing

[![Test](https://github.com/anirudhgangwal/ukpostcodes/actions/workflows/test.yml/badge.svg)](https://github.com/anirudhgangwal/ukpostcodes/actions/workflows/test.yml) 
[![Upload Python Package](https://github.com/anirudhgangwal/ukpostcodes/actions/workflows/python-publish.yml/badge.svg)](https://github.com/anirudhgangwal/ukpostcodes/actions/workflows/python-publish.yml)

A Python package to parge UK postcodes from text. Useful in applications such as OCR and IDP.

## Install

```bash
pip install uk-postcodes-parsing
```

## Capabilities

- Search and parse UK postcode from text/OCR results
  - Extract parts of the postcode: incode, outcode etc.  


| Postcode | .outcode | .incode | .area | .district | .subDistrict | .sector | .unit |
|----------|----------|---------|-------|-----------|--------------|---------|-------|
| AA9A 9AA | AA9A     | 9AA     | AA    | AA9       | AA9A         | AA9A 9  | AA    |
| A9A 9AA  | A9A      | 9AA     | A     | A9        | A9A          | A9A 9   | AA    |
| A9 9AA   | A9       | 9AA     | A     | A9        | `None`       | A9 9    | AA    |
| A99 9AA  | A99      | 9AA     | A     | A99       | `None`       | A99 9   | AA    |
| AA9 9AA  | AA9      | 9AA     | AA    | AA9       | `None`       | AA9 9   | AA    |
| AA99 9AA | AA99     | 9AA     | AA    | AA99      | `None`       | AA99 9  | AA    |  

- Fix common mistakes in UK postcode
- Utilities to validate postcode


## Usage

- Parsing text to get a list of postcodes.

```python
>>> from uk_postcodes_parsing import ukpostcode
>>> corpus = "this is a check to see if we can get post codes liek thia ec1r 1ub , and that e3 4ss. But also eh16 50y and ei412"          
>>> postcodes = ukpostcode.parse_from_corpus(corpus)
INFO:uk-postcodes-parsing:Found 2 postcodes in corpus
>>> print(postcodes)
[Postcode(original='ec1r 1ub', postcode='EC1R 1UB', incode='1UB', outcode='EC1R', area='EC', district='EC1', sub_district='EC1R', sector='EC1R 1', unit='UB'), Postcode(original='e34ss', postcode='E3 4SS', incode='4SS', outcode='E3', area='E', district='E3', sub_district=None, sector='E3 4', unit='SS')]
```

- Optional auto-correct: Attempt correcting common mistakes in postcodes such as reading "O" and "0" and vice-versa.

```python
>>> from uk_postcodes_parsing import ukpostcode
>>> corpus = "this is a check to see if we can get post codes liek thia ec1r 1ub , and that e3 4ss. But also eh16 50y and ei412"          
>>> postcodes = ukpostcode.parse_from_corpus(corpus, attempt_fix=True)
INFO:uk-postcodes-parsing:Postcode Fixed: 'eh16 50y' => 'EH16 5OY'
INFO:uk-postcodes-parsing:Found 3 postcodes in corpus
```

- Parsing

```python
>>> from uk_postcodes_parsing import ukpostcode
>>> ukpostcode.parse("EC1r 1ub")
Postcode(original='ec1r 1ub', postcode='EC1R 1UB', incode='1UB', outcode='EC1R', area='EC', district='EC1', sub_district='EC1R', sector='EC1R 1', unit='UB')
```
```python
>>> ukpostcode.parse("EH16 50Y")
INFO:uk-postcodes-parsing:Postcode Fixed: 'eh16 50y' => 'EH16 5OY'
Postcode(original='eh16 50y', postcode='EH16 5OY', incode='5OY', outcode='EH16', area='EH', district='EH16', sub_district=None, sector='EH16 5', unit='OY')
```
```python
>>> ukpostcode.parse("EH16 50Y", attempt_fix=False) # Don't attempt fixes during parsing
ERROR:uk-postcodes-parsing:Failed to parse postcode
>>> ukpostcode.parse("0W1") 
ERROR:uk-postcodes-parsing:Unable to fix postcode
ERROR:uk-postcodes-parsing:Failed to parse postcode
```

- Validity check

```python
>>> from uk_postcodes_parsing import postcode_utils
>>> postcode_utils.is_valid("0W1 0AA")
False
>>> postcode_utils.is_valid("OW1 0AA")
True
```

- Fixing

```python
>>> from uk_postcodes_parsing.fix import fix
>>> fix("0W1 OAA") 
'OW1 0AA'
```

# Testing

```bash
pytest tests/
```

## Similar works

Most of this work is based on this JavaScript library: https://github.com/ideal-postcodes/postcode
