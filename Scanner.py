from dataclasses import replace

from sklearn import tree
from utils import *
from Automata.direct_construction import Tree
from Automata.functions import epsilon

#Basic regular expresions that will help while reading the file 
letter_regex = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)"
digit_regex = "(0|1|2|3|4|5|6|7|8|9)"
id_regex = letter_regex + "(" + letter_regex + "|" + digit_regex + ")*"
letter_or_numbers =letter_regex + "*|" + digit_regex + "*"
class Scanner():
    def __init__(self, file_path):
        self.file_path = file_path
        self.reserved_words = ["COMPILER", "CHARACTERS", "KEYWORDS","TOKENS","PRODUCTIONS", "END"]
        self.curr_index = 0
        self.keywords = {}
        self.tokens = {}
        self.character_definitions = {}
        self.extractFileContent()
        self.removeComments()
        self.scan()
        self.clean_char_definitions()
        self.clean_keywords_definitions()
        self.clean_tokens()
    
    #Save each line of the file in list self.file_content
    def extractFileContent(self):
        file = open(self.file_path, 'r')
        self.file_content = file.read()
        file.close()
    """
    Iterate through the file to find and delete comments since they are not used
    """
    def removeComments(self):
        comments_removed= ""
        comentStarted = False
        while self.curr_index < len(self.file_content):
            if self.file_content[self.curr_index] == "(" and look_ahead(self.file_content, self.curr_index)==".":
                comentStarted = True
            elif self.file_content[self.curr_index] =="." and look_ahead(self.file_content, self.curr_index)==")":
                comentStarted = False
                self.curr_index +=2
            if comentStarted:
                pass
            else:
                comments_removed += self.file_content[self.curr_index]
            self.curr_index +=1
        self.file_content = comments_removed
        self.curr_index = 0

    
    def check_if_word_is_reserved(self,word):
        if word in self.reserved_words:
            return True
        return False

    def expect(self, pattern):
        tree = Tree(pattern)
        dfa = tree.generate_DFA()
        found_first_coincidence = False
        found_last_coincidence = False
        content = self.file_content
        buffer = ''
        while not found_last_coincidence:
            try:
                buffer += content[self.curr_index]
            except:
                return False
            found_coincidence = dfa.simulate(buffer)[0]
            if found_coincidence and not found_first_coincidence:
                found_first_coincidence = True
            elif found_coincidence and found_first_coincidence:
                pass
            elif not found_coincidence and found_first_coincidence:
                found_last_coincidence = True
                buffer= buffer[:-1]
            self.curr_index += 1
        return buffer

    def read_blank_spaces(self):
        while(self.file_content[self.curr_index] == ' ' or self.file_content[self.curr_index]== "\n" ):
            self.curr_index +=1
    
    def read_section(self, section_name):
        expression_id = self.expect(id_regex)
        while expression_id:
            equals_char= self.expect("=")
            if equals_char:
                expression_value = ''
                while self.file_content[self.curr_index] != ".":
                    expression_value += self.file_content[self.curr_index]
                    self.curr_index += 1
                if section_name == "CHARACTERS":
                    self.character_definitions[expression_id] = expression_value
                elif section_name == "KEYWORDS":
                    self.keywords[expression_id] = expression_value
                elif section_name == "TOKENS":
                    self.tokens[expression_id] = expression_value
            else:
                raise ValueError("Expected = between id and value ")
            if self.file_content[self.curr_index] ==".":
                self.curr_index +=1
                self.read_blank_spaces()
                expression_id = self.expect(id_regex)
            else:
                raise ValueError("Expected period")
            if(self.check_if_word_is_reserved(expression_id)):
                print("Keyword:", expression_id, "found section ended")
                return expression_id
    
    def scan(self):
        next_section = "CHARACTERS"
        found_compiler_keyword = self.expect("COMPILER")
        if found_compiler_keyword:
            print("Compiler keyword was found in header")
        else:
            raise ValueError("Compiler keyword not found")
        found_compiler_name = self.expect(id_regex)
        if found_compiler_name:
            print("Compiler name: ", found_compiler_name)
        self.read_blank_spaces()
        found_characters_key_word = self.expect("CHARACTERS")
        if found_characters_key_word:
            self.read_blank_spaces()
            next_section = self.read_section(next_section)
        self.read_blank_spaces()
        next_section = self.read_section(next_section)
        self.read_blank_spaces()
        next_section = self.read_section(next_section)
        self.read_blank_spaces()
        end = self.expect("END")
        if end:
            compiler_name = self.expect(found_compiler_name)
            if compiler_name:
                print("File read successfull")
            else:
                raise ValueError("Exptected", found_compiler_name, "at end line")
        else:
            raise ValueError("Expected END statement")

    def get_file_data(self):
        return self.character_definitions, self.keywords, self.tokens

    def clean_char_definitions(self):
        char_definitions = sorted(self.character_definitions.keys(),reverse=True ,key=len)
        for key in self.character_definitions.keys():
            self.character_definitions[key] = add_or_opperator(self.character_definitions[key])           
            for i in char_definitions:
                if i in self.character_definitions[key]:
                    self.character_definitions[key] = self.character_definitions[key].replace(i, self.character_definitions[i])
            self.character_definitions[key] = add_parenthesis(self.character_definitions[key])
            self.character_definitions[key] = remove_plus(self.character_definitions[key])
    
    def clean_keywords_definitions(self):  
        for key in self.keywords.keys():         
            self.keywords[key] = add_parenthesis(self.keywords[key])

    def clean_tokens(self):   
        character_definitions =sorted(self.character_definitions.keys(),reverse=True ,key=len)
        for key in self.tokens.keys():          
            for i in character_definitions:
                if i in self.tokens[key]:
                    self.tokens[key] = self.tokens[key].replace(i, self.character_definitions[i])
            self.tokens[key] = add_parenthesis(self.tokens[key])
            self.tokens[key] = remove_plus(self.tokens[key])
            self.tokens[key] = remove_except(self.tokens[key])
    
    def build_tokens(self):
        found_tokens = []
        for i in self.keywords.keys():
            found_token = token(i, self.keywords[i])
            found_tokens.append(found_token)
        for i in self.tokens.keys():
            found_token = token(i, self.tokens[i])
            found_tokens.append(found_token)
        return found_tokens

scanner = Scanner('test.cocol')
tokens = scanner.build_tokens()