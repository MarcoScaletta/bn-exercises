
from bag_of_words import BagOfWords
from babelnet import Babelnet
import string
import time

class ExtLesk:

    def __init__(self, babelnet: Babelnet, bag_of_words: BagOfWords):
        self.babelnet = babelnet
        self.bag_of_words = bag_of_words
        self.cached_word_contexts = dict()
        
    def compute_word_context(self, word, variation=None):
        if not word in self.cached_word_contexts: 
            self.cached_word_contexts[word] = dict()
        synset_ids = self.babelnet.get_synset_ids(word)
        edges_num = 0
        check_for_edge = False
        for synset_id in synset_ids: 
            if not synset_id['id'] in self.cached_word_contexts[word]:
                context_synset = self.context_of_synset(synset_id['id'])
                if "EXTENDED" in variation:

                    check_for_edge = True
                    edges = self.babelnet.get_outgoing_edges(synset_id['id'])
                    for edge in edges:
                        relation = edge['pointer']['relationGroup']
                        # print(relation)
                        # if relation == "HYPERNYM" or (relation != "HYPONYM" and relation != "OTHER"):
                        if relation == "HYPERNYM":
                            edges_num += 1
                            context_synset = context_synset.union(self.context_of_synset(edge['target']))
                self.cached_word_contexts[word][synset_id['id']] = context_synset
        if check_for_edge:
            print("numero edges=", edges_num)



    
    def best_sense(self, word: str, sentence: str, variation=None):
        word = word
        context_sentence = self.bag_of_words.bag_of_words(sentence)
        if variation == "EXTENDED_NO_WORD":
            context_sentence.remove(word)
        max_score = 0
        best_sense = None
        first_sense = None
        self.compute_word_context(word, variation)

        for syn_id in self.cached_word_contexts[word]:
            score = len(context_sentence.intersection(self.cached_word_contexts[word][syn_id]))
            if score > max_score:
                max_score = score
                best_sense = syn_id
            if first_sense is None:
                first_sense = syn_id
        if best_sense is None:
            print("NONE BEST_SENSE", word, "->", sentence)
            best_sense = first_sense
        return best_sense

    def context_of_synset(self, id):
        synset = self.babelnet.get_synset(id)
        context_synset = set()
        for gloss in synset['glosses']:
            # print("\t", gloss['gloss'])
            sub_glosses = gloss['gloss'].split(";")
            for sub_gloss in sub_glosses:
                bow = self.bag_of_words.bag_of_words(sub_gloss)
                context_synset = context_synset.union(bow)
        return context_synset

