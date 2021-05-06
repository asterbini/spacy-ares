
# spacy-ares
# disambiguating spacy tokens with BERT+ARES

The spacy-ares pipeline module finds for each token in the processed text the best K synsets (meanings) in Wordnet/Babelnet network by:
* processing the text through the BERT transformer (bert-core-multilingual-cased or bert-large-cased) to obtain the contextual embedding of each token
  (here we leverage the token/wordpieces alignment computed by spacy to average the wordpieces' tensors of the token)
* then retrieving the nearest K (normally 10) synsets available in the corresponding ARES embeddings.

For more info on ARES see http://sensembert.org and the paper:
* Bianca Scarlini, Tommaso Pasini and Roberto Navigli
  **With More Contexts Comes Better Performance: Contextualized Sense Embeddings for All-Round Word Sense Disambiguation**
  Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020)

Be aware that both ARES embedding and BERT transformers are big (some Gb)

This module can be used with either one of: 
* nltk's Wordnet 3
* Babelnet 5.0 (see https://github.com/asterbini/spacy-babelnet)

# INSTALL

Just type
```
make
```
The Makefile will:
- download ARES' embeddings
- convert them to binary form by using convertvec
- download/install Wordnet and OMW (Open Multi Wordnet)
- install BERT transformers
- install spacy-ares

# EXAMPLES
To run the Babelnet example in the ``examples`` directory you must have a ``config`` directory configured with your Babelnet API key

# TODO
- tests

