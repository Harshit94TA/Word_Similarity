#!/usr/bin/env python3
# -*- coding:utf-8 -*-
''' 
# download data from http://download.wikimedia.org/enwiki/ 
# run the command below to get data, and it takes hours time to preprocess
# python -m gensim.scripts.make_wiki
'''
import os

import gensim
from gensim.matutils import hellinger, cossim


class LSAModel:
    def __init__(self):
        if os.path.isfile("lsa.model"):
            self.mm = gensim.corpora.MmCorpus('_tfidf.mm')
            self.model = gensim.models.lsimodel.LsiModel.load("lsa.model")
        else:
            id2word = gensim.corpora.Dictionary.load_from_text(
                '_wordids.txt.bz2')
            self.mm = gensim.corpora.MmCorpus('_tfidf.mm')
            self.model = gensim.models.lsimodel.LsiModel(
                corpus=self.mm, id2word=id2word, num_topics=400)
            self.model.save("lsa.model")

    def similarity(self, word1: str, word2: str):
        if word1 is None or word2 is None:
            return None
        else:
            try:
                vec_word1 = self.model.id2word.doc2bow([word1])
                vec_word2 = self.model.id2word.doc2bow([word2])
                lsa_bow_word1 = self.model[vec_word1]
                lsa_bow_word2 = self.model[vec_word2]
                cos_similarity = cossim(lsa_bow_word1, lsa_bow_word2)
            except KeyError:
                cos_similarity = 0
            return cos_similarity


class LDAModel:
    def __init__(self):
        if os.path.isfile("lda.model"):
            self.mm = gensim.corpora.MmCorpus('_tfidf.mm')
            self.model = gensim.models.ldamodel.LdaModel.load("lda.model")
        else:
            id2word = gensim.corpora.Dictionary.load_from_text(
                '_wordids.txt.bz2')
            self.mm = gensim.corpora.MmCorpus('_tfidf.mm')
            self.model = gensim.models.ldamodel.LdaModel(
                corpus=self.mm, id2word=id2word, num_topics=400, update_every=1, passes=1)
            self.model.save("lda.model")

    def similarity(self, word1: str, word2: str):
        if word1 is None or word2 is None:
            return None
        else:
            try:
                vec_word1 = self.model.id2word.doc2bow([word1])
                vec_word2 = self.model.id2word.doc2bow([word2])
                lda_bow_word1 = self.model[vec_word1]
                lda_bow_word2 = self.model[vec_word2]
                cos_similarity = cossim(lda_bow_word1, lda_bow_word2)
            except KeyError:
                cos_similarity = 0
            return cos_similarity
