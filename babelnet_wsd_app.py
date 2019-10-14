
import babelnet as bn

import spacy
from bag_of_words import BagOfWords
from ext_lesk import ExtLesk
from morph_it import MorphIT
import time
from sentence_reader import WSDFileReader



Reader = WSDFileReader("wsd_test.json")
import os
BABELNET_TOKEN = os.environ["BABELNET_TOKEN"]

Morph = MorphIT() 
BOW = BagOfWords(Morph, "stop_words")
BN = bn.Babelnet(BABELNET_TOKEN, "IT")

EL = ExtLesk(BN,BOW)

print("Inizializzazione contesti...")
t = time.time()
for word in Reader.words_dict:
    EL.compute_word_context(word, "")
    print("\tContesto inizializzato per", word + ".")
print("Fine inizializzazione contesti, tempo trascorso: ", (time.time()-t), "secondi")
print("Chiamate a Babelnet:",BN.API_call_number)


tot = 0
correct = 0
for word in Reader.words_dict:
    
    print("WORD:", word)
    for context in Reader.words_dict[word]:
        tot += 1
        sentence = context[0]
        real_sense = context[1]
        best_sense = EL.best_sense_extended(word, sentence)

        print("SENTENCE:", sentence[:70], "[...]")
        if real_sense is None:
            print("REAL_SENSE:", None)
        else:
            print("REAL_SENSE:", real_sense)
            print("\t", BN.get_synset_definition(real_sense)[:70], "[...]")

        print("BEST_SENSE:", best_sense)
        print("\t", BN.get_synset_definition(best_sense)[:70], "[...]")
        if real_sense == best_sense:
            correct += 1

print("ACCURACY =", correct/tot * 100, "%")


print("Chiamate a Babelnet:",BN.API_call_number)        
    
