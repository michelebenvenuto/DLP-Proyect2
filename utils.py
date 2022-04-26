from collections import namedtuple

letter_regex = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)"
digit_regex = "(0|1|2|3|4|5|6|7|8|9)"
id_regex = letter_regex + "(" + letter_regex + "|" + digit_regex + ")*"
letter_or_numbers =letter_regex + "*|" + digit_regex + "*"

token = namedtuple('token', ['token_name','value'])

def look_ahead(buffer, index, positons_ahead = 1):
        try:
            return buffer[index + positons_ahead]
        except:
            return -1

def remove_plus(string):
    new_string = string.replace("+",'|')
    return new_string

def remove_except(string):
    if string.find("EXCEPT") == -1:
        return string
    else:
        new_string = string[0:string.find("EXCEPT")]
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
                new_string += "|"
        i += 1
    return '('+new_string + ')'
        
def find_sets(string):
    positions = []
    i = 0
    while i < len(string):
        if string[i] == '"':
            positions.append(i)
        i += 1
    return positions

