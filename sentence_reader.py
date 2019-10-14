
import json


class WSDFileReader:

    def __init__(self, json_file):
        self.filename = json_file
        self.words_dict = dict()

        wsd_list = json.load(open(json_file))['wsd_list']

        for wsd in wsd_list:
            word = wsd['word']
            self.words_dict[word] = list()
            for sentence_obj in wsd['sentences']:
                self.words_dict[word].append((sentence_obj['sentence'], sentence_obj['sense']))
