# Laboratory Work Nr.2 Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy
## Course: Formal Languages & Finite Automata
## Author: Mihaela Cușnir
## Variant 15
****
## Theory
Some notions I found important and useful: <br>

**Automaton** - mathematical model for finite-state machines.
<br>

**Determinism** (in automata theory) - when the result of the transition from one state to another depends on the input. 
<br>

**Finite Automata** - machine that recognize patterns within input taken from alphabet and accept it or reject it.
<br>

**Deterministic finite automaton (DFA)** - type of finite state machine that accepts or rejects an input string based on a set of states and transitions between those states.
<br>

**Non-Deterministic finite automaton (NDFA)** - type of finite state machine, but unlike DFA, it can transition to multiple states at the same time for a given input symbol.
<br>

**Chomsky hierarchy** - a hierarchy of four types of formal grammars (Type 0, Type 1, Type 2 and Type 3).
****
## Objectives

1. Understand what an automaton is and what it can be used for.

2. Continuing the work in the same repository and the same project, the following need to be added:

    a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
    
    b. For this you can use the variant from the previous lab.

3. According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:

    a. Implement conversion of a finite automaton to a regular grammar.
    
    b. Determine whether your FA is deterministic or non-deterministic.

    c. Implement some functionality that would convert an NDFA to a DFA.

    d. Represent the finite automaton graphically (Optional, and can be considered as a bonus point):
****
## Implementation
This code defines a class NFAtoDFA which transforms a Non-Deterministic Finite Automaton (NFA) into a Deterministic Finite Automaton (DFA). The code initializes the NFA with its attributes including a set of states, input alphabet, a final state, and transition function. It then initializes the DFA attributes with an empty transition function and an empty set of states. The code also provides methods to update the DFA attributes for the transformation process and to display the resulting transition table.
<br>

The __init_transformation() method is called to perform the transformation process. It updates the set of states and transition function for the DFA based on the NFA transition function. It then updates the final states of the DFA. The get_transitions() method is used to get the NFA transition function if it is not already provided during initialization.
```
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
```
The __update_states(), __update_transitions(), and __update_final_states() methods are used to update the DFA attributes during the transformation process. The transform_to_dfa() method performs the transformation process by calling the __init_transformation() method and then updating the DFA attributes until no more new states are added to the DFA set of states.
```
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
```
The __update_final_states() method checks which states in the DFA contain the original final state from the NFA and adds them to the final states of the DFA. The transform_to_dfa() method converts the NFA to a DFA by looping through all possible combinations of states in the DFA and updating the set of states and transitions until no more changes occur.
<br>
```
def transform_to_dfa(self):
        self.__init_transformation()
        for i in range(math.factorial(len(self.set_of_states))):
            self.__update_states()
            self.__update_transitions()
        self.__update_final_states()
```
The display_table() method is used to display the resulting DFA transition table as a Pandas DataFrame.
```       
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
```
****
## Results
Results for the 15th Variant:
```
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
```
is:

|             | a           | b        |
| ----------- | ----------- |----------|
| q0          | [q0, q1]    |  None    |
| q1          | q2          |  None    |
| q2          | q2          |   q3     |
| q0q1        | [q0, q1]    |   q2     |
| q3          | None        |  None    |

****
## References
1. Lecture Presentations
2. Is (desperately) googling and my collegue patience to help a reference?
