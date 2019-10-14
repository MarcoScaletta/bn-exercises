import spacy


class BagOfWords:

    def __init__(self, morph, stop_words_filename: str):
        f = open(stop_words_filename)
        self.stop_words = set() 
        self.morph = morph
        self.meaning_tags = set(["NOUN", "PROPN", "ADJ", "VERB"])
        for line in f:
            words = line.split()
            if len(words) > 0 and words[0] != "|":
                self.stop_words.add(words[0]) 
        self.nlp = spacy.load("it")

    def bag_of_words(self, sentence):
        doc = self.nlp(sentence.lower())
        bag_of_words_set = set()
        for w in doc:
            if w.text not in self.stop_words and w.pos_ in self.meaning_tags:
                if w.text.lower() not in self.morph.lemma_dict:
                    bag_of_words_set.add(w.text.lower())
                elif len(self.morph.lemma_dict[w.text.lower()]) == 1:
                    pos_tag = list(self.morph.lemma_dict[w.text.lower()].keys())[0]
                    # print(w.text.lower())
                    # print(pos_tag)
                    bag_of_words_set.add(self.morph.lemma_dict[w.text.lower()][pos_tag])
                elif w.pos_ not in self.morph.lemma_dict[w.text.lower()]: 

                    # print(">", w.text.lower())
                    # print(">", w.pos_)
                    # print(">", self.morph.lemma_dict[w.text.lower()])
                    pos_tag = w.pos_
                    if w.pos_ == "VERB":
                        pos_tag = "NOUN"
                    elif w.pos_ == "NOUN":
                        pos_tag = "ADJ"
                    elif w.pos_ == "ADJ":
                        pos_tag = "NOUN"
                    elif w.pos_ == "PROPN":
                        if "NOUN" in self.morph.lemma_dict[w.text.lower()]:
                            pos_tag = "NOUN"
                        elif "ADJ" in self.morph.lemma_dict[w.text.lower()]:
                            pos_tag = "ADJ"

                    bag_of_words_set.add(self.morph.lemma_dict[w.text.lower()][pos_tag])
                else:
                    # print(w.text.lower())
                    # print(w.pos_)
                    bag_of_words_set.add(self.morph.lemma_dict[w.text.lower()][w.pos_])
        return bag_of_words_set

        def bag_of_words(self, sentence):
            doc = self.nlp(sentence.lower())
        bag_of_words_set = set()
        for w in doc:
            if w.text not in self.stop_words and w.pos_ in self.meaning_tags:
                if w.text.lower() not in self.morph.lemma_dict:
                    bag_of_words_set.add(w.text.lower())
                elif len(self.morph.lemma_dict[w.text.lower()]) == 1:
                    pos_tag = list(self.morph.lemma_dict[w.text.lower()].keys())[0]
                    # print(w.text.lower())
                    # print(pos_tag)
                    bag_of_words_set.add(self.morph.lemma_dict[w.text.lower()][pos_tag])
                elif w.pos_ not in self.morph.lemma_dict[w.text.lower()]: 

                    # print(">", w.text.lower())
                    # print(">", w.pos_)
                    # print(">", self.morph.lemma_dict[w.text.lower()])
                    pos_tag = w.pos_
                    if w.pos_ == "VERB":
                        pos_tag = "NOUN"
                    elif w.pos_ == "NOUN":
                        pos_tag = "ADJ"
                    elif w.pos_ == "ADJ":
                        pos_tag = "NOUN"
                    elif w.pos_ == "PROPN":
                        if "NOUN" in self.morph.lemma_dict[w.text.lower()]:
                            pos_tag = "NOUN"
                        elif "ADJ" in self.morph.lemma_dict[w.text.lower()]:
                            pos_tag = "ADJ"

                    bag_of_words_set.add(self.morph.lemma_dict[w.text.lower()][pos_tag])
                else:
                    # print(w.text.lower())
                    # print(w.pos_)
                    bag_of_words_set.add(self.morph.lemma_dict[w.text.lower()][w.pos_])
        return bag_of_words_set
