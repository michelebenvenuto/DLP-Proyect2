from collections import namedtuple
from Automata.direct_construction import Tree


ANY = []
for i in range(0,256):
    ANY.APPEND(chr(i))
i = 0
result = ''
while i < len(ANY):
    result+= ANY[i]
    if i +1 < len(ANY):
        result += "¦"
    i +=1

letter_regex = "(a¦b¦c¦d¦e¦f¦g¦h¦i¦j¦k¦l¦m¦n¦o¦p¦q¦r¦s¦t¦u¦v¦w¦x¦y¦z¦A¦B¦C¦D¦E¦F¦G¦H¦I¦J¦K¦L¦M¦N¦O¦P¦Q¦R¦S¦T¦U¦V¦W¦X¦Y¦Z)"
digit_regex = "(0¦1¦2¦3¦4¦5¦6¦7¦8¦9)"
id_regex = letter_regex + "(" + letter_regex + "¦" + digit_regex + ")*"
number = digit_regex + "(" + digit_regex + ")*"
simboles = "(+¦-¦{¦}¦[¦]¦|¦(..))"
opp_ass_string = '"' + simboles + '"'
char_opp = "CHR"
set_regex = '"'+ "(" + "(" + letter_regex +"("+letter_regex+")*"+")" + "¦" + "("+ digit_regex+ "("+digit_regex+")*" + ")" + ")" +'"'
char_regex = "'" +"(" + letter_regex +"¦"+ digit_regex+ "¦"+ simboles + ")" + "'"
letter_or_numbers =letter_regex + "*¦" + digit_regex + "*"
token = namedtuple('token', ['token_name','value'])

cocol_definitions= [
    token('opp', simboles),
    token('char_opp', char_opp),
    token('id', id_regex),
    token('number', number),
    token('opp_string', opp_ass_string),
    token('char', char_regex),
    token('set', set_regex),
]

def look_ahead(buffer, index, positons_ahead = 1):
        try:
            return buffer[index + positons_ahead]
        except:
            return -1

def remove_plus(string):
    new_string = string.replace("+",'¦')
    return new_string


def add_parenthesis(string):
    i = 0 
    new_string = ''
    set_positions = find_sets(string)
    while i < len(string):
        if i in set_positions and (set_positions.index(i) ) %2 == 0:
            new_string += '('
        elif i in set_positions and (set_positions.index(i)) %2 == 1:
            new_string += ')'
        else:
            new_string += string[i]
        i += 1
    return  new_string 

def add_or_opperator(string):
    i = 0
    new_string ='' 
    found_quote = False
    set_positions = find_sets(string)
    while i < len(string):
        new_string += string[i]
        if i  in  set_positions:
            found_quote = not found_quote
        elif found_quote:
            if i + 1 < len(string) and string[i + 1 ] != '"': 
                new_string += "¦"
        i += 1
    return new_string
        
def find_sets(string):
    positions = []
    i = 0
    while i < len(string):
        if string[i] == '"':
            positions.append(i)
        i += 1
    return positions

class Tokenizer():
    def __init__(self, definitions):
        self.definitions = definitions
        self.build_regex()
        self.tree = Tree(self.regex, True)
        self.dfa = self.tree.generate_DFA()
        self.simple_regexes = dict((x,Tree(y,True).generate_DFA()) for x,y in definitions)
    
    def build_regex(self):
        final_regex = ''
        i = 0
        while i < len(self.definitions):
            if i +1 >=len(self.definitions):
                final_regex += self.definitions[i].value 
            else:
                final_regex += self.definitions[i].value + '¦'
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