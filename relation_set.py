from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset, Lemma

class RelationSet():
    """
    This class is a set of all Wordnet Synsets and sub-Synsets of a given word
    within a user-defined amount of layers. In order to create a RelationSet
    instance, the user must pass a word as a string as well as an integer
    which represents the layer of sub-relations to be retrieved.

    When an instance is created, the related terms are immediately retrieved by calling the
    private methods within the class. The user can call the public method "includes" with another
    word as an argument to return a Boolean value: True if the RelationSet includes any Synset of
    this word, False if it doesn't.
    """
    
    def __init__(self, current_word: str, layers: int):
        self.word = current_word
        self.layers = layers
        self.related = self.__related_terms()

    # Returns a set of functions for relations that are defined for the current synset
    def __get_valid_methods(current_term):
        valid_methods = []
        methods = [method for method in dir(current_term) if method[0] != "_"]
        for method_name in methods:
            method = getattr(current_term, method_name)
            if callable(method):
                try:
                    result = method()
                    if isinstance(result, list) and len(result) > 0 and (isinstance(result[0], (Synset, Lemma))):
                        valid_methods.append(method_name)
                except TypeError:
                    pass
        return valid_methods

    # Flattens an embedded list completely with recursion
    def __flatten_sub_list(maybe_list):
        try:
            flattened_list = [y for x in maybe_list for y in x]
            if any(isinstance(item, list) for item in flattened_list):
                return RelationSet.__flatten_sub_list(flattened_list)
            else:
                return flattened_list
        except TypeError:
            return maybe_list  # If maybe_list is not iterable, return it as is
        
    # Checks current method for current term
    def __check_method(term, method):
        related_terms = getattr(term, method)()

        # If the current term is a synset and we're checking its lemmas, the check_terms method
        # is called recursively since certain relationships are defined only for Lemmas by WordNet

        if isinstance(term, Synset) and method == 'lemmas':
            result = RelationSet.__check_terms(related_terms)
            return result
        elif isinstance(related_terms[0], Lemma):
            result = [lemma.synset() for lemma in related_terms]
            return result
        else:
            return related_terms
        
    # Checks all methods for current Synset/Lemma
    def __check_all_methods(term):
        all_related= []
        methods = RelationSet.__get_valid_methods(term)
        for method in methods:
            result = RelationSet.__check_method(term, method)
            if len(result) > 0:
                all_related.append(result)
        return all_related

    # Checks each Synset/Lemma and gets its sub-Synsets
    def __check_terms(all_terms):
        sub_syns = [item for term in all_terms for item in RelationSet.__check_all_methods(term)]
        flattened_sub_syns = set(RelationSet.__flatten_sub_list(sub_syns))
        return flattened_sub_syns

    # Checks each Synset for related words
    def __get_all_terms(self, all_syns, sub_status): # Sub status tracks whether the function is checking moves or sub-moves
        result = RelationSet.__check_terms(all_syns)
        return RelationSet.__get_all_terms(self, result, sub_status+1) if sub_status < self.layers else result
                
    # Gets synsets for instance word
    def __get_synsets(self):
        self.all_syns = wn.synsets(self.word)

    # Gets all terms related to the instance word
    def __related_terms(self):
        self.synsets = self.__get_synsets()
        self.result = self.__get_all_terms(self.all_syns, sub_status=1)
        return self.result
    
    # Checks if a word is in current RelationSet
    def __check_if_related(self, maybe_related):
        for synset in wn.synsets(maybe_related):
            if synset in self.related:
                return True
        return False
    
    # Public method to check if a given word is in the RelationSet instance. Returns a boolean value
    def includes(self, maybe_related):
        return self.__check_if_related(maybe_related)