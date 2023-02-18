# Laboratory Work Nr.1 REGULAR GRAMMARS, Variant 16
## Course: Formal Languages & Finite Automata
## Author: Mihaela Cușnir
****
## Theory
Some notions I found important and useful: <br>

**Alphabet** -> symbols, letters, tokens. Strings (words) are made from joining them.

<br>**Formal Language** -> words made from an alphabet and have some specific set of rules.

<br>**Grammar** -> rules for forming strings. It is also an ordered quadruple **G = (VN, VT, P, S)** , where: 
<br>
VN - non-terminal symbols; (finite)
<br>
VT - terminal symbols; (finite)
<br>
S - start symbol;
<br>
p - productions of rules. (finite)

<br>**Regular Grammar** -> grammar that is right-regular or left-regular, meaning the production rules have ***at most*** one ***non-terminal symbol***
<br>Left-regular grammar form:
``` 1. A -> a
    2. A -> Ba
    3. A -> ε
```
<br>Right-regular grammar form:
``` 1. A -> a
    2. A -> aB
    3. A -> ε
```
a - terminal symbol
<br>A, B - non-terminal symbols
<br>ε - empty string
<br>

**Automaton** <br> - mathematical model for finite-state machines.
<br>

**Finite Automata** - machine that recognize patterns within input taken from alphabet and accept it or reject it.

****
## Objectives

1. Understand what a language is and what it needs to have in order to be considered a formal one.

2. Provide the initial setup for the evolving project that you will work on during this semester. I said project because usually at lab works, I encourage/impose students to treat all the labs like stages of development of a whole project. Basically you need to do the following:

    a. Create a local && remote repository of a VCS hosting service (let us all use Github to avoid unnecessary headaches);

    b. Choose a programming language, and my suggestion would be to choose one that supports all the main paradigms;

    c. Create a separate folder where you will be keeping the report. This semester I wish I won't see reports alongside source code files, fingers crossed;

3. According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:

    a. Implement a type/class for your grammar;

    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

    c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

    d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;
****
## Implementation
As adviced, I used two classes: Grammar and FiniteAutomaton. 
In the class Grammar, I declared at the beginning the terminal and non-terminal symbols and production for my variant. The first function, ```generateString```, uses the recursion method for parsing and travers the production rules via iteration. Since in my case, the shortest string/word that can be is db, the first iteration will always be db. In the second part of the function, we use the python random generator for choosing as named a "path" (2 different paths for A and 2 for B). Even if A has 3 different variants in the task, one of them was already include in the result as the word db, remaining two.
```
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
            
```
The function ```toFiniteAutomaton```, using hash table through the built-in dictionary data type, mapping the elements of finite automaton.
```
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
```
In the second class ```FiniteAutomaton```, function ```stringBelongToLanguage```, checks if an input string can be obtained via the state transition from it. The method used here was found in an article (indicated in References), which states that that a minimal automaton has the minimal adjacency matrix rank and the minimal adjacency matrix nullity among all equivalent deterministic automata. So the idea was to use the adjacency matrix. Tranversing it, the string is checked being invalid(has nothing to do with the given production) or valid.
```
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

```
****
## Conclusion/Results
Results on the variant: <br>
![image](https://user-images.githubusercontent.com/74179246/219882668-aca88b67-4c55-402d-9acd-e2fe9756664a.png)

Implementation result on a random word:
```
#CHECKIN FOR SOME RANDOM INVALID WORD
ex_word = 'acdb'
print("example to check", ex_word)
print(automaton_response.stringBelongToLanguage(ex_word))
```
Result:<br>
![image](https://user-images.githubusercontent.com/74179246/219882609-302398d3-6f4a-43c6-aeb3-fc9f87cd5e40.png)

****
## References
1. Joshua Abbott, Phyllis Z. Chinn, Tyler Evans, Allen J. Stewart Humboldt State University, Arcata, California, ***Graph Adjacency Matrix Automata*** <br>
  (https://cocosci.princeton.edu/josh/papers/gama.pdf) <br>
2. Lecture Presentations
