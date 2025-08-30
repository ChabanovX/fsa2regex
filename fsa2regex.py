# Implement an FSA to RegExp Translator
# Overview: https://codeforces.com/group/CsTlwuSxCL/contest/518189/problem/A

import re
import sys

from collections import defaultdict

class Queue:
    def __init__(self):
        self.elements = []

    def add(self, obj):
        self.elements = [obj] + self.elements

    def pop(self):
        return self.elements.pop()


class Vertex:
    def __init__(self, label):
        self.label = label
        self.neighbours = []
        self.outgoing_labels = []


class Edge:
    def __init__(self, start: str, end: str, transition: str):
        self.start = start
        self.end = end
        self.transition = transition


class Graph:
    def __init__(self):
        self.edges = []
        self.vertices = []
        self.labels = []

    def get_neighbours(self, label: str):
        for vertex in self.vertices:
            if vertex.label == label:
                return vertex.neighbours

    def add_vertex(self, label):
        self.vertices.append(Vertex(label))
        self.labels.append(label)

    def add_edge(self, start_label: str, end_label: str, transition: str):
        for vertex in self.vertices:
            if vertex.label == start_label:
                vertex.neighbours.append(end_label)
                vertex.outgoing_labels.append(transition)

        self.edges.append(Edge(start_label, end_label, transition))

    def check_for_disjointness(self, start_label: str):
        queue = Queue()
        visited = set()
        queue.add(start_label)

        while len(queue.elements) > 0:
            some_label = queue.elements.pop()

            if some_label not in visited:
                visited.add(some_label)
                for label in self.get_neighbours(some_label):
                    if label not in visited:
                        queue.add(label)

        return len(self.vertices) == len(visited)


def get_list_without_duplicates(old_list: list):
    new_list = []
    for obj in old_list:
        if obj not in new_list:
            new_list.append(obj)

    return new_list


def check_input_format(fsa: list):
    # E1 check
    # """Simple format-testing before formatting into dict"""

    # check for empty char
    if not fsa[-1]:
        fsa.pop()

    if len(fsa) != 6:
        return False


    regex = ['type=\[(non-|)deterministic\]',
                'states=\[[a-zA-Z0-9]+(?:,[a-zA-Z0-9]+)*\]',
                'alphabet=\[[a-zA-Z0-9_]+(?:,[a-zA-Z0-9_]+)*\]',
                'initial=\[[^,+]*\]',
                'accepting=\[[a-zA-Z0-9]+(?:,[a-zA-Z0-9]+)*\]|accepting=\[\]',
                'transitions=\[[a-zA-Z0-9_]+(?:>[a-zA-Z0-9_]+){2}(?:,[a-zA-Z0-9_]+(?:>[a-zA-Z0-9_]+){2})*\]']

    # Regex checker
    for i in range(6):
        if not re.fullmatch(regex[i], fsa[i]):
            return False

    return True


def check_input_logic(fsa: dict):
    """E1-4 errors tester"""

    # E1 Transition duplicate-checking
    if len(set(fsa["transitions"])) < len(fsa["transitions"]):
        return "E1: Input file is malformed"

    # E1 Empty-list-checking
    for key, value in fsa.items():
        if not value[0] and (key not in ("accepting", "initial")):
            return "E1: Input file is malformed"

    # E1 Type-checking
    if fsa["type"] not in (["deterministic"], ["non-deterministic"]):
        return "E1: Input file is malformed"

    # E1 States-checking
    for state in fsa["states"]:
        if not re.fullmatch("[a-zA-Z0-9]+", state):
            return "E1: Input file is malformed"

    # E1 Alphabet-checking
    for letter in fsa["alphabet"]:
        if not re.fullmatch("[a-zA-Z0-9_]+", letter):
            return f"E1: Input file is malformed"

    # E1 Initial state length-checking
    if len(fsa["initial"]) != 1:
        return f"E1: Input file is malformed"

    # E2 Initial state-checking check
    if not fsa["initial"][0]:
        return "E2: Initial state is not defined"

    # E3 Accepting state-checking
    if len(fsa["accepting"]) == 1 and not fsa["accepting"][0]:
        return "E3: Set of accepting states is empty"

    # E4 If initial in states
    if fsa["initial"][0] not in fsa["states"]:
        return f"E4: A state '{fsa['initial'][0]}' is not in the set of states"

    # E4 If initial in states
    for obj in fsa["initial"]:
        if obj not in fsa["states"]:
            return f"E4: A state '{obj}' is not in the set of states"

    # E4 If accepting in states
    for obj in fsa["accepting"]:
        if obj not in fsa["states"]:
            return f"E4: A state '{obj}' is not in the set of states"


def check_transitions(fsa: dict):
    """E4+5 checker"""

    # E5 if letter in alphabet
    for transition in fsa["transitions"]:
        start, letter, end = transition.split(">")
        # E5 if letter in alphabet
        if letter not in fsa["alphabet"]:
            return f"E5: A transition '{letter}' is not represented in the alphabet"


def build_graph(fsa: dict):
    graph = Graph()
    for transition in fsa["transitions"]:
        start, letter, end = transition.split(">")
        if start not in graph.labels:
            graph.add_vertex(start)
        if end not in graph.labels:
            graph.add_vertex(end)
        graph.add_edge(start, end, letter)

    return graph


def check_determinism(graph: Graph):
    for vertex in graph.vertices:
        if len(set(vertex.outgoing_labels)) < len(vertex.outgoing_labels):
            return False

    return True


def reformat(fsa: list):
    dict_data = dict()
    for definition in fsa:
        key, value = definition.split('=')
        value = value[1:-1].split(',')

        # Get only unique arguments
        # But Repeated transitions should not be deleted.
        if key != "transitions":
            value = get_list_without_duplicates(value)
        dict_data[key] = value

    # dict_data["accepting"].sort()
    return dict_data


def checker_facade(fsa: dict):

    error_with_logic = check_input_logic(fsa)
    if error_with_logic:
        print(error_with_logic)
        sys.exit(0)

    error_with_transitions = check_transitions(fsa)
    if error_with_transitions:
        print(error_with_transitions)
        sys.exit(0)

    graph = build_graph(fsa)
    if not graph.check_for_disjointness(fsa["initial"][0]):
        print("E6: Some states are disjoint")
        sys.exit(0)

    if fsa["type"][0] == "deterministic":
        if not check_determinism(graph):
            print("E7: FSA is non-deterministic")
            sys.exit(0)

    return fsa


def build_transitions(fsa: dict):
    fsa["transitions_dict"] = {}
    for state in fsa["states"]:
        fsa["transitions_dict"][state] = defaultdict(list)


def find_in_list(some_list: list, obj):
    for i in range(len(some_list)):
        if some_list[i] == obj:
            return i

    return -1000000


def fsa_to_re(fsa: dict):
    """Full transition algorithm"""
    regex_aux_list = [[[0] * len(fsa["states"]) for i in range(len(fsa["states"]))] for i in range(len(fsa["states"]) + 1)]
    regex_answer = ""

    def fsa_to_re_base():
        """Builds base (k=0) re steps"""
        for transition in fsa["transitions"]:
            start, letter, end = transition.split(">")
            fsa["transitions_dict"][start][end].append(letter)

        for i in range(len(fsa["states"])):
            for j in range(len(fsa["states"])):
                st1, st2 = fsa["states"][i], fsa["states"][j]
                if st1 != st2:
                    if fsa["transitions_dict"][st1][st2]:
                        regex_aux_list[0][i][j] = "|".join(fsa["transitions_dict"][st1][st2])
                    else:
                        regex_aux_list[0][i][j] = "{}"
                else:
                    if fsa["transitions_dict"][st1][st2]:
                        regex_aux_list[0][i][j] = "|".join(fsa["transitions_dict"][st1][st2]) + "|eps"
                    else:
                        regex_aux_list[0][i][j] = "eps"

    fsa_to_re_base()

    for k in range(1, len(fsa["states"]) + 1):
        for i in range(len(fsa["states"])):
            for j in range(len(fsa["states"])):
                regex_aux_list[k][i][j] = f"({regex_aux_list[k-1][i][k-1]})({regex_aux_list[k-1][k-1][k-1]})*({regex_aux_list[k-1][k-1][j]})|({regex_aux_list[k-1][i][j]})"

    # Proceeding with the answer
    fsa["accepting"].sort()
    for i in range(len(fsa["accepting"])):
        regex_answer += f'({regex_aux_list[len(fsa["states"])][find_in_list(fsa["states"], fsa["initial"][0])][find_in_list(fsa["states"], fsa["accepting"][i])]})|'

    return regex_answer[:-1]


# Main
with open("input.txt") as file:
    input_data = file.read().split('\n')

# Test 1
if not check_input_format(input_data):
    print("E1: Input file is malformed")
    sys.exit(0)

finite_sa = reformat(input_data)

# Test 2
checker_facade(finite_sa)

# Build transitions network
build_transitions(finite_sa)

regex_result = fsa_to_re(finite_sa)
print(regex_result)

