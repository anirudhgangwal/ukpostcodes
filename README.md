# uk-postcodes-parsing

A Python package to parge UK postcodes from text. Useful in applications such as OCR and IDP.

Install:

```bash
pip install uk-postcodes-parsing
``` 

## Usage

- Parsing text to get a list of postcodes.

```python
>>> from uk_postcodes_parsing.ukpostcode import parse_from_corpus, Postcode
>>> corpus = "this is a check to see if we can get post codes liek thia ec1r 1ub , and that e3 4ss. But also eh16 50y and ei412"          
>>> postcodes = parse_from_corpus(corpus)
INFO:uk-postcodes-parsing:Found 2 postcodes in corpus
>>> print(postcodes)
[Postcode(original='ec1r 1ub', postcode='EC1R 1UB', incode='1UB', outcode='EC1R', area='EC', district='EC1', sub_district='EC1R', sector='EC1R 1', unit='UB'), Postcode(original='e34ss', postcode='E3 4SS', incode='4SS', outcode='E3', area='E', district='E3', sub_district=None, sector='E3 4', unit='SS')]
```

- Optional auto-correct: Attempt correcting common mistakes in postcodes such as reading "O" and "0" and vice-versa.

```python
>>> from uk_postcodes_parsing.ukpostcode import parse_from_corpus, Postcode
>>> corpus = "this is a check to see if we can get post codes liek thia ec1r 1ub , and that e3 4ss. But also eh16 50y and ei412"          
>>> postcodes = parse_from_corpus(corpus, attempt_fix=True)
INFO:uk-postcodes-parsing:Postcode Fixed: 'eh16 50y' => 'EH16 5OY'
INFO:uk-postcodes-parsing:Found 3 postcodes in corpus
```

- Parsing

```python
>>> from uk_postcodes_parsing.ukpostcode import parse
>>> parse("EC1r 1ub")
Postcode(original='ec1r 1ub', postcode='EC1R 1UB', incode='1UB', outcode='EC1R', area='EC', district='EC1', sub_district='EC1R', sector='EC1R 1', unit='UB')
>>> parse("EH16 50Y", attempt_fix=True)
INFO:ukpostcode:Postcode Fixed: 'eh16 50y' => 'EH16 5OY'
Postcode(original='eh16 50y', postcode='EH16 5OY', incode='5OY', outcode='EH16', area='EH', district='EH16', sub_district=None, sector='EH16 5', unit='OY')
```

- Fixing

```python
>>> from uk_postcodes_parsing.fix import fix
>>> fix("0W1 OAA") 
OW1 0AA
```
