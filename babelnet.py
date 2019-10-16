
import urllib.parse as parse
import requests
import sys

class Babelnet:

    def __init__(self, key:str, lang:str):
        self.key = key
        self.url = "https://babelnet.io/v5"
        self.lang = lang
        self.API_call_number = 0
        self.cached_synsets = dict()
        self.cached_synset_ids = dict()
        self.cached_outgoing_edges = dict()

    def get_version(self):
        return self.babelnet_http_request("getVersion")['version']
    
    def get_synset_ids(self,lemma: str, lang:str =None):
        if lang is None:
            lang=self.lang
        if str(lemma+lang) not in self.cached_synset_ids:
            synset_id  = self.babelnet_http_request("getSynsetIds", {"lemma": lemma, "searchLang": lang})
            self.cached_synset_ids[str(lemma+lang)] = synset_id
        else:
            synset_id = self.cached_synset_ids[str(lemma+lang)]

        return synset_id
    
    def get_synset(self,synset_id: str):
        if synset_id not in self.cached_synsets:
            synset = self.babelnet_http_request("getSynset", {"id": synset_id, "targetLang": self.lang})
            self.cached_synsets[synset_id] = synset
        else:
            synset = self.cached_synsets[synset_id]
        return synset

    def get_outgoing_edges(self,synset_id: str):
        if synset_id not in self.cached_outgoing_edges:
            outgoing_edges = self.babelnet_http_request("getOutgoingEdges", {"id": synset_id})
            self.cached_outgoing_edges[synset_id] = outgoing_edges
        else:
            outgoing_edges = self.cached_outgoing_edges[synset_id]
        return outgoing_edges
    

    def babelnet_http_request(self, url:str, params: dict = dict()):
        params["key"] = self.key
        try:
            resp = requests.get(url=self.url + "/" + url, params=params)
        except requests.exceptions.HTTPError as e:  # This is the correct syntax
            print(e)
            sys.exit(1)
        if resp.status_code is not 200:
            print(resp._content)
            print(url, params)
            print("Error code", resp.status_code)
            sys.exit(1)
        if 'message' in resp.json() and str(resp.json()['message']).startswith('Your key is not valid'):
            print("ERROR:", resp.json()['message'])
            sys.exit(1)
        self.API_call_number += 1
        return resp.json()
    
    def get_all_definitions(self, word):
        definitions = dict()
        synset_ids = self.get_synset_ids(word)
        for synset_id in synset_ids:
            definitions[synset_id['id']] = self.get_synset_definition(synset_id['id'])
        return definitions

    def get_all_synonyms(self, synset_id):
        synset = self.get_synset(synset_id)
        synonyms_lemma = list()
        if len(synset['senses']) > 0: 
            for sense in synset['senses']:
                synonyms_lemma.append(sense['properties']['fullLemma'])
        return synonyms_lemma

    def get_synset_definition(self, synset_id):
        synset = self.get_synset(synset_id)
        if len(synset['glosses']) > 0: 
            return synset['glosses'][0]['gloss']
        return None
