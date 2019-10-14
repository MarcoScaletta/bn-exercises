
class MorphIT:

    def __init__(self):
        self.lemma_dict = dict()
        f = open("morph-it.txt")
        
        for line in f:
            words = line.split()
            word = words[0].lower()
            lemma = words[1].lower()
            tag = self.spacy_tag(words[2])

            if tag != "X":
                if word not in self.lemma_dict:
                    self.lemma_dict[word] = dict()
                self.lemma_dict[word][tag] = lemma


    def spacy_tag(self, tag: str):
        if tag.startswith("NOUN"):
            return "NOUN"
        elif tag.startswith("VER"):
            return "VERB"
        elif tag.startswith("NPR"):
            return "PROPN"
        elif tag.startswith("ADJ"):
            return "ADJ"
        else:
            return "X"