from xml.dom.minidom import Identified
from Automata.direct_construction import Tree
from Scanner import tokens
from utils import token, pi

class Parser():
    def __init__(self, definitions):
        self.definitions = definitions
        self.build_regex()
        self.tree = Tree(self.regex)
        self.dfa = self.tree.generate_DFA()
        self.simple_regexes = dict((x,Tree(y).generate_DFA()) for x,y in definitions)
    
    def build_regex(self):
        final_regex = ''
        i = 0
        while i < len(self.definitions):
            if i +1 >=len(self.definitions):
                final_regex += self.definitions[i].value 
            else:
                final_regex += self.definitions[i].value + '|'
            i+=1
        self.regex = final_regex

    def identify_token(self,string):
        for key in self.simple_regexes:
            if self.simple_regexes[key].simulate(string)[0]:
                return key

    def find_tokens(self,string):
        buffer = ''       
        simulation_results = [] 
        Identified_tokens = []
        while string != '':
            position_of_last_true = -1
            #fill the simulation results array with the result of simulating the chars of the strings 
            i = 0
            while i < len(string):
                buffer += string[i]
                result = self.dfa.simulate(buffer)
                simulation_results.append(result[0])
                i += 1
            #find the position of the last and first true
            j =0
            while j < len(simulation_results):
                if simulation_results[j]:
                    position_of_last_true = j
                j+=1
            # check if position_of_last_true is -1, if this is true remove the first char of the string
            if position_of_last_true == -1:
                string_list = list(string)
                string_list.pop(0)
                string = ''.join([str(item) for item in string_list])
            else:
                token_name = self.identify_token(string[0:position_of_last_true+1])
                Identified_tokens.append(token(token_name,string[0:position_of_last_true+1]))
                string = string[position_of_last_true+1:]
            buffer = ''
            simulation_results = []
        return Identified_tokens

             
parser = Parser(tokens)