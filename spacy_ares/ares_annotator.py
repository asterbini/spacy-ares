
import spacy
from spacy.tokens.doc       import Doc
from spacy.tokens.token     import Token
from spacy.parts_of_speech  import *
from spacy.language         import Language

from gensim.models          import KeyedVectors
from spacy_transformers     import Transformer
import numpy as np
from . import get_package_basepath

class Ares:
    __ARES   = None     # ARES embeddings
    __BERT   = None     # BERT transformer
    __lang   = None     # nlp language
    __BNLANG = None     # Babelnet language

    def __init__(self, token, tensor, K=10):
        vv = np.concatenate((tensor,tensor),axis=1)[0]
        self.nearest = self.__ARES.similar_by_vector(vv, topn=K)

    def lemmas(self):
        '''Return lemmas tied to the synsets'''
        if self.__BNLANG:
            return [ s.getLemmas(self.__BNLANG) for s in self.synsets() ]
        else:
            from nltk.corpus import wordnet as wn
            print(self.nearest)
            return [ wn.lemma_from_key(k) for k,d in self.nearest ]

    def synsets(self):
        '''Return the best 10 synsets'''    # FIXME: make K parametric
        if self.__BNLANG:
            import babelnet as bn           # FIXME: move this to the annotator __init__
            return [ bn.BabelSynsetID(s).toSynset() for s,d in self.nearest ]
        else:
            return [ l.synset() for l in self.lemmas() ]

    @classmethod
    def load_data(cls, lang='en', xnet='wordnet'):
        cls.__lang = lang
        assert xnet in ['wordnet', 'babelnet'], f"Unknown {xnet} XNet"
        if xnet == 'babelnet':
            import babelnet as bn
            bn.initVM()
            cls.__BNLANG = bn.Language.fromISO(lang) 
            MODEL = 'bert-base-multilingual-cased'
            ARES  = 'ares_bert_base_multilingual'
        if xnet == 'wordnet':
            from nltk.corpus import wordnet as wn
            MODEL = 'bert-large-cased'
            ARES  = 'ares_bert_large'
        d = get_package_basepath()
        cls.__ARES = KeyedVectors.load_word2vec_format(f'~/ares_data/{ARES}.bin', binary=True)
        config = {
                    "model": {
                        "@architectures": "spacy-transformers.TransformerModel.v1",
                        "name": MODEL,
                        "tokenizer_config": {"use_fast": False}
                       }
                   } 
        nlp = spacy.blank(lang)
        trf = nlp.add_pipe('transformer', config=config)
        trf.initialize(lambda: iter([]), nlp=nlp)
        cls.__BERT = nlp


@Language.factory("ares")
class AresAnnotator:
    __FIELD = 'ares'

    def __init__(self, nlp, name, K=10, xnet='wordnet'):
        self.__lang = nlp.lang
        self.__K    = K
        Token.set_extension(self.__FIELD, default=None, force=True)
        Ares.load_data(nlp.lang, xnet)

    def __call__(self, doc: Doc):
        text = str(doc)                             # FIXME recover doc text, is this the best way?
        doc2 = Ares._Ares__BERT(text)               # process text through BERT
        tensors = doc2._.trf_data.tensors[0][0]     # get the contextual embeddings
        align   = doc2._.trf_data.align             # and the aligment token/wordpieces
        for tk, a in zip(doc, align):
            tensor = np.average(tensors[a.data], axis=0)    # FIXME average the wordpieces' tensors to get the token one
            tk._.set(self.__FIELD, Ares(tk,tensor,self.__K))
        return doc
