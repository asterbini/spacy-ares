
import spacy
from spacy_ares.ares_annotator import AresAnnotator

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('ares', config={'K':3, 'xnet':'wordnet'})

text = 'The quick brown fox jumped over the lazy dog.'
doc  =  nlp(text)

for t in doc:
    print(t, t.pos_, t._.ares.lemmas())
