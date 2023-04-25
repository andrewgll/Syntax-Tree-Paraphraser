from itertools import permutations, product
from abc import abstractmethod

class Functional:
    @abstractmethod
    def apply(self):
        pass
        
class Pattern:
    @property
    @abstractmethod
    def start(self):
        pass

    @property
    @abstractmethod
    def middle(self):
        pass

    @property
    @abstractmethod
    def label(self):
        pass

    @property
    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def isCorrect(self):
        pass

class CartesianPermutator(Functional):
   
    def apply(self,tree,tree_list, limit): 
        result = []
        original_list = sum(tree_list, [])
        for i,permutation in enumerate(self.__permutate(tree_list)):
            if i == limit:
                break
            tree_copy = tree.copy(deep=True)
            for tree_position, leave in zip(original_list,permutation):
                tree_copy[tree_position.treeposition()] = leave.copy(deep=True)
            result.append(tree_copy)
            tree_copy = None

    
        return result
    
    def __permutate(self,tree_list):
        permutation_list = []
        for tree in tree_list:
            permutation_list.append(list(permutations(tree)))
        cartesian_product = list(product(*permutation_list))
        merged_product = [sum(t, ()) for t in cartesian_product]
        return merged_product

class SimpleSerializator(Functional):
    def apply(self, tree):
        return{"paraphrases": [self.__serialize_tree(tree) for tree in tree]}
        
    def __serialize_tree(self,tree):
        tree_string = str(tree).replace("\n", "")
        return {"tree": tree_string}


class NPPattern(Pattern):

    def __init__(self):
        self._label = "NP"
        self._pattern = ["NP",",","CC"]
    
    def __is_correct(self, tree):
        if len(tree) <= 2:
            return False
        for leave in tree:
            if leave.label() not in self._pattern:
                return False
        return True
    def find(self, tree):
        result = []
        for subtree in tree.subtrees():
            if subtree.label() == self._label and self.__is_correct(subtree):
                labeled_trees = self.__find_trees_by_label(subtree)
                result.append(labeled_trees[1:])
        return result

    def __find_trees_by_label(self, tree):
        return [subtree for subtree in tree.subtrees() if subtree.label() == self._label]
    
    
class Paraphraser(Functional):
    def __init__(self, tree, pattern, serializator, permutator, limit):
        self.tree = tree
        self.limit = limit
        self.pattern = pattern
        self.serializator = serializator 
        self.permutator = permutator 
    def apply(self):
        np_trees = self.pattern.find(self.tree)
        results = self.permutator.apply(self.tree, np_trees, self.limit)
        serialized_result = self.serializator.apply(results)
        return serialized_result
    
