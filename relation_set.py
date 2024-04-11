from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset, Lemma

class RelationSet():
    """
    This class is a set of all Wordnet Synsets and sub-Synsets related to a given word
    within a user-defined amount of layers. It gathers every Synset related to
    the word (hypernyms, hyponyms, etc.), then every Synset related to any of those
    Synsets, and repeats this process for as many times as specified by the user.
    
    In order to create a RelationSet instance, the user must pass:
    1. A word (as a string)
    2. An integer (which represents the layer of sub-relations to be retrieved)

    When an instance is created, the related terms are immediately retrieved by calling the
    private methods within the class. The user can then call the public method
    "includes", with another word as an argument, to return a Boolean value:
    True if the RelationSet includes any Synset of this word, False if it doesn't.
    """
    
    def __init__(self, current_word: str, layers: int):
        """
        Initializes parameters and calls __related_terms() immediately to build the RelationSet.

        Args:
            current_word (str): The word we want to build a RelationSet for.
            layers (int): The number of layers we want our RelationSet to include.
        """
        self.word = current_word
        self.layers = layers
        self.related = self.__related_terms()

    def __get_valid_methods(current_term: Synset | Lemma):
        """
        Returns a list of methods to be called for the current term. The list
        contains the names of the methods, not the methods themselves.

        The methods that are retained are callable with only one argument, which could
        be either a Synset or a Lemma, and return a list of Synsets or Lemmas.

        Args:
            current_term (Synset, Lemma): The term whose methods are being collected

        Returns:
            list: A list of names of methods defined for the current term.
        """
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

    def __flatten_sub_list(maybe_list: list):
        """
        Flattens any list of lists completely by recursively calling
        itself until none of the items in the list are iterable.

        Args:
            maybe_list (list): The list to be flattened

        Returns:
            list: A completely flattened list
        """
        try:
            flattened_list = [y for x in maybe_list for y in x]
            if any(isinstance(item, list) for item in flattened_list):
                return RelationSet.__flatten_sub_list(flattened_list)
            else:
                return flattened_list
        except TypeError:
            return maybe_list
        
    def __check_method(term: Synset | Lemma, method: str):
        """
        Calls current method and returns related terms.
        
        If the term is a Synset and the method returns a list of Synsets,
        the related terms are simply returned.
        
        If the term is a Synset and the method happens be 'lemmas',
        i.e. it returns that Synset's Lemmas, then the check_terms method is called
        recursively to obtain all Lemma relations for that Synset as well.

        If the term is a Lemma, the method returns the corresponding Synset for all related Lemmas.

        Args:
            term (Synset, Lemma): The term whose method is being checked
            method (string): The name of the method to be checkedd

        Returns:
            list: All terms related to the current term
        """

        related_terms = getattr(term, method)()
        if isinstance(term, Synset) and method == 'lemmas':
            result = RelationSet.__check_terms(related_terms)
            return result
        elif isinstance(term, Lemma):
            result = [lemma.synset() for lemma in related_terms]
            return result
        else:
            return related_terms
        
    def __check_all_methods(term: Synset | Lemma):
        """
        Given a term (Synset or Lemma), returns all terms
        related to that term. It gathers the methods that are defined
        for it, checks each of those methods, and puts whatever they return
        into the list of related terms.

        Args:
            term (Synset, Lemma): The term whose methods are being checked

        Returns:
            list: Every related term that was found
        """
        all_related= []
        methods = RelationSet.__get_valid_methods(term)
        for method in methods:
            result = RelationSet.__check_method(term, method)
            if len(result) > 0:
                all_related.append(result)
        return all_related

    def __check_terms(all_terms: list):
        """
        Checks each term for its related Synsets and puts them in a list.
        The list is then flattened, converted to a set to remove duplicates,
        and returned.

        The word "term" is used here instead of "Synset" because this method
        is called to gather Synsets related to a Lemma as well. This is because
        in WordNet, some relationships are defined only over Lemmas. However,
        the Lemmas themselves are never returned or included in the RelationSet.

        Args:
            all_terms (list): Every term to be checked.

        Returns:
            set: A set of Synsets which were found to be related to the input Synsets.
        """
        sub_syns = [item for term in all_terms for item in RelationSet.__check_all_methods(term)]
        flattened_sub_syns = set(RelationSet.__flatten_sub_list(sub_syns))
        return flattened_sub_syns

    def __get_all_terms(self, all_syns: list, i: int):
        """
        Takes a list of Synsets and collects their related terms. The method
        is called recursively, passing whatever it gets to the next iteration.
        This is repeated as long as the current iteration number is lower than
        the user-defined amount of layers. When the recursion has finished, the
        final result is returned.

        Args:
            all_syns (list): The list of Synsets currently being checked
            i (int): The current iteration of the recursion

        Returns:
            list: All related terms found so far
        """
        result = RelationSet.__check_terms(all_syns)
        return RelationSet.__get_all_terms(self, result, i+1) if i < self.layers else result

    def __related_terms(self):
        """
        Gets all related terms and builds the current instance RelationSet.

        Returns:
            list: The list of related terms gathered.
        """
        self.result = self.__get_all_terms(wn.synsets(self.word),i=1)
        return self.result
    
    def includes(self, maybe_related_word: str):
        """
        Can be used to check if a given word is in the instance RelationSet.
        Iterates over each Synset of the word provided and returns a Boolean value.

        Args:
            maybe_related_word (String): A word that may or may not be in the instance RelationSet

        Returns:
            bool: Returns True if the word is in the instance RelationSet, or False if it isn't
        """
        for synset in wn.synsets(maybe_related_word):
            if synset in self.related:
                return True
        return False