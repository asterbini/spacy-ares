import glob
import os
from collections import defaultdict
from typing import Optional, List, Dict, Set

from nltk.corpus.reader.wordnet import \
    ADJ  as WN_ADJ, \
    ADV  as WN_ADV, \
    NOUN as WN_NOUN, \
    VERB as WN_VERB, Synset

from spacy.parts_of_speech import ADJ, ADV, NOUN, VERB, AUX

from spacy_ares import get_package_basepath

# The Open Multi Wordnet corpus contains the following languages:
#   als arb bul cat cmn dan ell eus fas fin fra glg heb hrv ind ita jpn nld nno nob pol por qcn slv spa swe tha zsm
#   ('deu' can be found in Extended Open Multi Wordnet)
# the available spacy languages are:
# af am ar bg bn ca cs da de el en es et eu fa fi fr ga gu he hi hr hu hy id is it ja kn ko ky lb lij
# lt lv mk ml mr nb ne nl pl pt ro ru sa si sk sl sq sr sv ta te th ti tl tn tr tt uk ur vi xx yo zh
# then the full mapping is
__DEFAULT_LANG = 'spa'
__WN_LANGUAGES_MAPPING = dict(
  en ='eng', # English (from wordnet)
  # TODO: select only the best ones?
  # other languages from omw  
  sq ='als', # Albanian
  ar ='arb', # Arabic
  bg ='bul', # Bulgarian
  ca ='cat', # Catalan
  zh ='cmn', # Chinese Open Wordnet
  da ='dan', # Danish
  el ='ell', # Greek
  eu ='eus', # Basque
  fa ='fas', # Persian
  fi ='fin', # Finnish
  fr ='fra', # French
# ?? ='glg',  # Galician
  he ='heb', # Hebrew
  hr ='hrv', # Croatian
  id ='ind', # Indonesian
  it ='ita', # Italian
  ja ='jpn', # Japanese
  nl ='nld', # Dutch
# no ='nno', # Norwegian
# nb ='nob', # Norwegian Bokmal
  pl ='pol', # Polish
  pt ='por', # Portuguese
# ?? ='qcn', # Chinese (Taiwan)
  sl ='slv', # Slovenian
  es ='spa', # Spanish
  sv ='swe', # Swedish
  th ='tha', # Thai
  ml ='zsm', # Malayalam
)
__WN_POS_MAPPING = {
    ADJ:  WN_ADJ,
    NOUN: WN_NOUN,
    ADV:  WN_ADV,
    VERB: WN_VERB,
    AUX:  WN_VERB
}


def spacy2wordnet_pos(spacy_pos: int) -> Optional[str]:
    return __WN_POS_MAPPING.get(spacy_pos)


def fetch_wordnet_lang(lang: Optional[str] = None) -> str:
    language = __WN_LANGUAGES_MAPPING.get(lang, None)

    if not language:
        raise Exception('Language {} not supported'.format(lang))

    return language

