
all: data_bin wordnet build install

data_bin: data/ares_bert_base_multilingual.bin data/ares_bert_large.bin BERT

data/%.bin: ares_embedding/%.txt data convertvec/convertvec
	convertvec/convertvec txt2bin $< $@

convertvec:
	git clone https://github.com/marekrei/convertvec
convertvec/convertvec: convertvec
	make -C convertvec

ares_embedding: ares_embedding.tar.gz
	tar xzvf ares_embedding.tar.gz

data:
	mkdir data

ares_embedding.tar.gz:
	wget http://sensembert.org/resources/ares_embedding.tar.gz

ares_data:
	mv data ~/ares_data

wordnet:
	python -m nltk.downloader wordnet omw

BERT:
	transformers-cli download bert-base-multilingual-cased
	transformers-cli download bert-large-cased

build:
	python setup.py build

install: build
	python setup.py install

clean:
	rm -rf ares_embedding* convertvec build dist
