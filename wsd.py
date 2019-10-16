
from sentence_reader import WSDFileReader
from morph_it import MorphIT
from bag_of_words import BagOfWords
from babelnet import Babelnet
from ext_lesk import ExtLesk
import time
import json

class WSD:
    def __init__(self, wsd_file, token, stop_words, variation):
        self.Reader = WSDFileReader(wsd_file)
        self.BOW = BagOfWords(MorphIT() , stop_words)
        self.BN = Babelnet(token, "IT")
        self.EL = ExtLesk(self.BN,self.BOW)
        self.variation = variation
        self.results = dict()
        self.accuracy_for_word = dict()
        self.correctness = dict()
        self.accuracy = 0
        self.init_context()
        self.wsd()
        self.jsonify()
    
    def init_context(self):
        print("Inizializzazione contesti...")
        t = time.time()
        for word in self.Reader.words_dict:
            self.EL.compute_word_context(word, self.variation)
            self.EL.compute_word_context(word, self.variation)
            # self.EL.compute_word_context(word, "")
            self.results[word] = list()
            print("\tContesto inizializzato per", word + ".")
        print("Fine inizializzazione contesti, tempo trascorso: ", (time.time()-t), "secondi")
        print("Chiamate a Babelnet:", self.BN.API_call_number)

    def wsd(self, variation=None):
        tot = 0
        correct = 0
        for word in self.Reader.words_dict:
            word_tot = 0
            word_correct = 0
            self.correctness[word] = list()
            print("WORD:", word)
            for context in self.Reader.words_dict[word]:
                tot += 1
                word_tot += 1
                sentence = context[0]
                real_sense = context[1]
                best_sense = self.EL.best_sense(word, sentence)
                if best_sense is None:
                    self.results[word].append((None, None))
                else:
                    self.results[word].append((best_sense, self.BN.get_all_synonyms(best_sense)))

                print("SENTENCE:", sentence[:70], "[...]")
                if real_sense is None:
                    print("REAL_SENSE:", None)
                else:
                    print("REAL_SENSE:", real_sense)
                    print("\t", self.BN.get_synset_definition(real_sense)[:70], "[...]")

                print("BEST_SENSE:", best_sense)
                definition = self.BN.get_synset_definition(best_sense)
                if definition is not None:
                    print("\t", self.BN.get_synset_definition(best_sense)[:70], "[...]")
                else:
                    print('\tNO DEFINITION')
                if real_sense == best_sense:
                    correct += 1        
                    word_correct += 1
                    self.correctness[word].append('CORRECT')
                else:
                    self.correctness[word].append('WRONG')
            self.accuracy_for_word[word] = word_correct/word_tot
        self.accuracy = correct/tot
                
            
    
    def jsonify(self):
        wsd_list = []
        data = {}
        
        for word in self.Reader.words_dict:
            sentences = []
            for i in range(len(self.Reader.words_dict[word])):
                context = self.Reader.words_dict[word][i]
                result = self.results[word][i]
                sentences.append({
                    "sentence": context[0],
                    "sense": context[1],
                    "best_sense": result[0],
                    "correctness": self.correctness[word][i],
                    "synonyms": result[1]
                })

            wsd_list.append({
                "word": word,
                "accuracy" : self.accuracy_for_word[word],
                "sentences": sentences
            })
        data = {
            "accuracy": self.accuracy,
            "wsd_list": wsd_list
        }

        with open('wsd_results_'+self.variation+'.json', 'w') as outfile:
            json.dump(data, outfile,  indent=4, ensure_ascii=False)