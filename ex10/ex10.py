#######################################################################
# FILE: ex10.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex10 2017-2018
# DESCRIPTION: exercise 10
#######################################################################
import copy
import itertools

INCREASE = 1


class Node:
    """
    A class for all node object of a tree
    """

    def __init__(self, data="", pos=None, neg=None):
        self.data = data
        self.positive_child = pos
        self.negative_child = neg


class Record:
    """
    A class for record object
    """

    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    """
    Get the records from a file
    :param filepath:
    :return:
    """
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        self.__root = root

    def get_root(self):
        return self.__root

    def diagnose_helper(self, node, symptoms):
        """
        A recursive method to get the illness that's correspond to the symptoms
        using the tree beginning by node
        :param node: where to start
        :param symptoms: symptoms list
        :return: the illness om the leaf we reach with the symptoms
        """
        if not node.positive_child or not node.negative_child:  # If we are
            # on a leaf

            return node.data
        elif node.data in symptoms:  # If the symptom on the node is in
            # symptoms list
            return self.diagnose_helper(node.positive_child, symptoms)  # Go to
            # the positive child
        else:
            return self.diagnose_helper(node.negative_child, symptoms)  # Go to
            # negative child

    def diagnose(self, symptoms):
        """
        Get the illness that's corresponds to the symptoms using the root tree
        :param symptoms: list of symptoms
        :return: corresponding illness
        """
        return self.diagnose_helper(self.__root, symptoms)

    def calculate_error_rate(self, records):
        """
        Get the error rate between the excepted illness calling diagnose on the
        records symptoms and the illness in the records
        :param records: records to test
        :return: error rate
        """
        error_count = 0
        for record in records:
            # If diagnose doesn't give the illness in the record
            if self.diagnose(record.symptoms) != record.illness:
                error_count += INCREASE
        return float(error_count) / len(records)

    def all_illnesses_helper(self, node, illnesses_list):
        """
        Recursive function to get a list of the illnesses on a tree beginning
        by node
        :param node: beginning of the tree
        :param illnesses_list: list of illnesses
        :return: list of illnesses in alphabetical order
        """
        if not node.positive_child or not node.negative_child:  # If we are
            # on a leaf
            if node.data not in illnesses_list:
                # Adding it to the list (mutable so it will stay in
                # others calls to the functiond)
                illnesses_list.append(node.data)
        else:
            # Progress with the two children
            self.all_illnesses_helper(node.positive_child, illnesses_list)
            self.all_illnesses_helper(node.negative_child, illnesses_list)
        return sorted(illnesses_list)

    def all_illnesses(self):
        """
        Get a list of all illnesses on the root tree
        :return:
        """
        return self.all_illnesses_helper(self.__root, [])

    def most_common_illness(self, records):
        """
        Return the illness that's appears most often in records
        :param records: records to check
        :return: most common illness
        """
        count = dict()
        illnesses = self.all_illnesses()  # Getting a list of all illnesses
        for illness in illnesses:
            # Initialising the counter for each illness
            count[illness] = 0
        for record in records:
            #  Increasing for each occurrences in record
            count[self.diagnose(record.symptoms)] += INCREASE
        return max(count, key=count.get)  # Return the key with the bigger
        # value

    def paths_to_illness_helper(self, illness, node, path, paths_list):
        """
        Getting a list of different paths to reach the given illness on the
        tree beginning by the node
        :param illness: illness to reach
        :param node: node to begin the path
        :param path: actual path
        :param paths_list: paths list
        :return: paths list
        """
        if node.positive_child and node.negative_child:  # Not on a leaf

            # Calling on the positive with list extended with true
            self.paths_to_illness_helper(illness, node.positive_child,
                                         path + [True], paths_list)
            # Calling on the negative with list extended with false
            self.paths_to_illness_helper(illness, node.negative_child,
                                         path + [False], paths_list)
        elif node.data == illness:  # If we reach the wanted illness
            paths_list.append(path)  # Adding the path to paths list
        return paths_list

    def paths_to_illness(self, illness):
        """
        Getting a list of different paths to reach the given illness
        :param illness: illness to reach
        :return: list of paths, each path as a list of True/False
        """
        return self.paths_to_illness_helper(illness, self.__root, [], [])


def best_illness(records, positive_symptoms, symptoms):
    count = dict()
    for record in records:
        count[record.illness] = 0

    for record in records:
        correspond = True
        for symptom in positive_symptoms:
            if symptom not in record.symptoms:
                correspond = False
        for symptom in symptoms:
            if symptom in record.symptoms and symptom not in positive_symptoms:
                correspond = False
        if correspond:
            count[record.illness] += INCREASE
    return max(count, key=count.get)


def build_tree_helper(symptoms, node, i):
    """
    Building recursively a tree asking on symptoms
    :param symptoms: symptoms to ask on
    :param node: node of the tree
    :param i: iterator
    :return: root of the tree
    """
    # I choose to build the tree beginning by the bottom
    # (more easily to return the root)
    if i == 0:  # If we the node is actually the root of the tree
        return node
    else:
        # The actual node is the child (positive and negative) of the next
        node1 = copy.deepcopy(node)
        node2 = copy.deepcopy(node)
        return build_tree_helper(symptoms, Node(symptoms[i - 1], node1, node2),
                                 i - 1)


def symptoms_list(symptoms, node, positive_symptoms, i, records):
    """
    Adding illness that corresponds to each leaf of the tree
    :param symptoms:list of all tested symptoms
    :param node:node (root at the beginning)
    :param positive_symptoms: symptoms we answer yes to reach this leaf
    :param i: iterator
    :param records: records to find the illness
    :return:
    """
    if i == len(symptoms) - 1:  # When we reach a leaf of the actual tree

        # Adding the illness corresponding with or without the last symptom
        node.negative_child = Node(
            best_illness(records, positive_symptoms, symptoms), None, None)
        node.positive_child = Node(
            best_illness(records, positive_symptoms + symptoms[i:i + 1],
                         symptoms), None, None)

    else:
        # Progress in the tree, increasing the positive
        # list for the positive child
        symptoms_list(symptoms, node.negative_child, positive_symptoms,
                      i + INCREASE, records)

        symptoms_list(symptoms, node.positive_child,
                      positive_symptoms + symptoms[i:i + 1],
                      i + INCREASE, records)


def build_tree(records, symptoms):
    """
    Build the tree asking on the symptom and the most probable illness ont the
    leafs
    :param records: records to find the illness
    :param symptoms: symptoms to test
    :return:root of the tree
    """
    root = build_tree_helper(symptoms, Node(symptoms[-1], None, None),
                             len(symptoms) - 1)

    symptoms_list(symptoms, root, [], 0, records)
    return root


def optimal_tree(records, symptoms, depth):
    """
    Finding the optimal tree for a given depth
    :param records: records to find illnesses
    :param symptoms: list of symptoms from it we choose symptoms to test
    :param depth: depth of the wanted tree
    :return: optimal tree
    """
    trees_count = dict()
    for subset in itertools.combinations(symptoms, depth):  # For each sub set
        # of symptoms with size=depth
        tree = Diagnoser(build_tree(records, list(subset)))
        error_rate = tree.calculate_error_rate(records)  # Compute the error
        # rate of the tree
        trees_count[error_rate] = tree.get_root()

    return trees_count[min(trees_count)]  # Return the tree with minimal error
    # rate
