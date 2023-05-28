# ukpostcodes

NOTE: pending improvements / tests.

A Python package to parge UK postcodes from text. Useful in applications such as OCR and IDP.

Example usage:

```bash
git clone https://github.com/anirudhgangwal/ukpostcodes.git
cd ukpostcodes
pip install .
``` 

```python
from ukpostcodes import parse_from_corpus

corpus = "this is a check to see if we can get post codes liek thia ec1r 1ub , and that e3 4ss. But also eh16 50y and ei412"          

postcodes = parse_from_corpus(corpus)
print(postcodes)
```

Output

```
INFO:ukpostcode:Found 3 postcodes in corpus
INFO:ukpostcode:Postcode Fixed: 'eh16 50y' => 'EH16 5OY'
[Postcode(original='ec1r 1ub', postcode='EC1R 1UB', incode='1UB', outcode='EC1R', area='EC', district='EC1', sub_district='EC1R', sector='EC1R 1', unit='UB'), Postcode(original='e34ss', postcode='E3 4SS', incode='4SS', outcode='E3', area='E', district='E3', sub_district=None, sector='E3 4', unit='SS'), Postcode(original='eh16 50y', postcode='EH16 5OY', incode='5OY', outcode='EH16', area='EH', district='EH16', sub_district=None, sector='EH16 5', unit='OY')]
```
