import os
import random


class Grammar:
    
    Vn = ['S', 'A', 'B']
    Vt = ['a', 'b', 'c', 'd']
    P = tuple([
    ('S', 'bS'),
    ('S', 'dA'),
    ('A', 'b'),
    ('A', 'aA'),
    ('A', 'dB'),
    ('B', 'a'),
    ('B', 'cB')
    ])

    def generateString(self, state, iteration):
        word: string 
        if(iteration == 1):
            if(state == "S"):
                word = "db"
            elif(state == "A"):
                word = "b"
            elif(state =="B"):
                word = "a"
            return word
        else:
            if(state =="A"):
                aux = random.randrange(0,1)
                if(aux == 0):
                    word = 'd'+self.generateString("B", iteration-1)
                else:
                    word = 'a'+self.generateString("A", iteration-1);  
            elif(state == "S"):
                aux = random.randrange(0,1)
                if(aux == 0):
                    word = 'd'+self.generateString("A", iteration)
                else:
                    word = 'b'+self.generateString("S", iteration);    
            elif(state == "B"):
                word = 'c'+self.generateString("B", iteration-1)
            return word
            
    def toFiniteAutomaton(self):
        c:int
        c = 0
        dictionary = {}
        
        for input_symbol in self.Vn:
            dictionary[input_symbol] = "q{}".format(c)
            c = c + 1

        dictionary['Q'] = "q{}".format(c + 1)
        __P = {}

        for v_n in self.P:
            __P[v_n[0]] = [p[1]
        for p in self.P if p[0] == v_n[0]]
        
        fa = {}
        for v_n in __P:
            fa[dictionary[v_n]] = []
            for trans in __P[v_n]:
                if len(trans) == 2:
                    fa[dictionary[v_n]].append(
                        (trans[0], dictionary[trans[1]]))
                else:
                    fa[dictionary[v_n]].append((trans, 'Q'))
        return fa
    
    
class FiniteAutomaton:
    graph = {}
    startin_state = 'q0'
    def Finite_Automaton(self,FA):
        self.graph = FA
        
    def stringBelongToLanguage(self, final_string):
        
        curr_state = self.startin_state
        for curr in final_string:
            if curr_state == 'Q':
                return False

            for matrix_weight, matrix_node in self.graph[curr_state]:
                if curr == matrix_weight:
                    curr_state = matrix_node
                    break
            else:
                return False
        if curr_state != 'Q':
            for production in self.graph[curr_state]:
                if production[0] == final_string[-1] and production[1] == 'Q':
                    return True
        return curr_state == 'Q'

pass_grammar = Grammar()
automaton_response = FiniteAutomaton()
temp_autom = pass_grammar.toFiniteAutomaton()
automaton_response.Finite_Automaton(temp_autom)

print('Valid 5 outputs/words:')
for i  in range(5):
    words = pass_grammar.generateString("S", i+1)
    print(words)

#CHECKIN FOR SOME RANDOM INVALID WORD
ex_word = 'acdb'
print("example to check", ex_word)
print(automaton_response.stringBelongToLanguage(ex_word))
