import math
import pandas as pd

class NFAtoDFA:
    def __init__(self, autom_states, input_values, final_state, transitions=None) -> None:

        # Initialize the NFA attributes
        self.set_of_states =autom_states
        self.input_alphabet = input_values
        self.final_state = final_state
        self.transitions = transitions
        self.dict_transitions = {}

        # Initialize the DFA attributes
        self.dict_transitions_dfa = {}
        self.set_of_states_dfa = []

    # Function for DFA transformation process.
    def __init_transformation(self):
        self.set_of_states_dfa = self.set_of_states.copy()
        for state in self.set_of_states:
            for value in self.input_alphabet:
                if (state, value) in self.dict_transitions:
                    if isinstance(self.dict_transitions[(state, value)], list):
                        self.set_of_states_dfa.append(self.dict_transitions[(state, value)])

        self.dict_transitions_dfa = self.dict_transitions.copy()
        for i in range(len(self.set_of_states_dfa)):
            if isinstance(self.set_of_states_dfa[i], list):
                for value in self.input_alphabet:
                    new_state = set()
                    for state in self.set_of_states_dfa[i]:
                        if (state, value) in self.dict_transitions:
                            if isinstance(self.dict_transitions[(state, value)], list):
                                new_state.update(set(self.dict_transitions[(state, value)]))
                            else:
                                new_state.update(set([self.dict_transitions[(state, value)]]))
                    if new_state:
                        self.dict_transitions_dfa[(''.join(self.set_of_states_dfa[i]), value)] = sorted(new_state) if len(new_state) > 1 else new_state.pop()
    
    def get_transitions(self):
        if self.transitions is None:
            self.transitions = []
            while True:
                transition = input().split()
                if not transition:
                    break
                self.transitions.append([tuple([transition[0], transition[1]]), transition[2]])
        
        for transition in self.transitions:
            self.dict_transitions[transition[0]] = [state[1]
                                                    for state in self.transitions if transition[0] == state[0]]
            if len(self.dict_transitions[transition[0]]) == 1:
                self.dict_transitions[transition[0]] = self.dict_transitions[transition[0]][0]

    def __update_states(self):
        for transition in self.dict_transitions_dfa:
            if self.dict_transitions_dfa[transition] not in self.set_of_states_dfa:
                self.set_of_states_dfa.append(self.dict_transitions_dfa[transition])

    def __update_transitions(self):
        for i in range(len(self.set_of_states_dfa)):
            if isinstance(self.set_of_states_dfa[i], list):
                for value in self.input_alphabet:
                    temp = set()
                    for state in self.set_of_states_dfa[i]:
                        if (state, value) in self.dict_transitions_dfa:
                            if isinstance(self.dict_transitions_dfa[(state, value)], list):
                                temp.update(set(self.dict_transitions_dfa[(state, value)]))
                            else:
                                temp.update(set([self.dict_transitions_dfa[(state, value)]]))
                    if temp:
                        self.dict_transitions_dfa[(''.join(self.set_of_states_dfa[i]), value)] = sorted(temp) if len(temp) > 1 else temp.pop()

    def __update_final_states(self):
        for i in range(len(self.set_of_states_dfa)):
            self.set_of_states_dfa[i] = ''.join(self.set_of_states_dfa[i])

        for state in self.set_of_states_dfa:
            if self.final_state[0] in state and state not in self.final_state:
                self.final_state.append(state)

    def transform_to_dfa(self):
        self.__init_transformation()
        for i in range(math.factorial(len(self.set_of_states))):
            self.__update_states()
            self.__update_transitions()
        self.__update_final_states()

    #Transition table as visualization
    def display_table(self):
        transition_table = []
        for state in self.set_of_states_dfa:
            transition_table.append([])
            for value in self.input_alphabet:
                if (state, value) in self.dict_transitions_dfa:
                    transition_table[-1].append(self.dict_transitions_dfa[(state, value)])

        transition_df = pd.DataFrame(
            transition_table,
            columns=self.input_alphabet,
            index=self.set_of_states_dfa
        )

        return transition_df


set_of_states = ['q0', 'q1', 'q2']
alphabet = ['a', 'b']
final_state = ['q2']
transitions = [
    [('q0', 'a'), 'q0'],
    [('q1', 'b'), 'q2'],
    [('q0', 'a'), 'q1'],
    [('q2', 'a'), 'q2'],
    [('q2', 'b'), 'q3'],
    [('q2', 'c'), 'q0'],
]

nfa = NFAtoDFA(set_of_states, alphabet, final_state, transitions)

nfa.get_transitions()
nfa.transform_to_dfa()
nfa.dict_transitions_dfa
nfa.display_table()
nfa.final_state
table = nfa.display_table()
print(table)
