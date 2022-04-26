from utils import Tokenizer, look_ahead, cocol_definitions, id_regex, add_or_opperator, add_parenthesis, remove_plus, remove_except, token
from Automata.direct_construction import Tree 
from Automata.functions import epsilon

#Basic regular expresions that will help while reading the file 

class Scanner():
    def __init__(self, file_path):
        self.file_path = file_path
        self.reserved_words = ["COMPILER", "CHARACTERS", "KEYWORDS","TOKENS","PRODUCTIONS", "END"]
        self.curr_index = 0
        self.keywords = {}
        self.tokens = {}
        self.character_definitions = {}
        self.tokens_tokenized = {}
        self.character_definitions_tokenized = {}
        self.tokenizer = Tokenizer(cocol_definitions)
        self.extractFileContent()
        self.removeComments()
        self.scan()
        self.tokenize_chars()
        self.tokenize_tokens()
        self.remove_except_tonkens()
        self.build_character_regexes()
        self.build_token_regexes()
        self.clean_keywords_definitions()
    
    #Save file content in the buffer self.file_content
    def extractFileContent(self):
        file = open(self.file_path, 'r')
        self.file_content = file.read()
        file.close()
    
    #Iterate through the file to find and delete comments since they are not used
    
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
        

    def get_file_data(self):
        return self.character_definitions, self.keywords, self.tokens
    
    def clean_keywords_definitions(self):  
        for key in self.keywords.keys():         
            self.keywords[key] = add_parenthesis(self.keywords[key])

    def tokenize_chars(self):
        for key in self.character_definitions.keys():
            self.character_definitions_tokenized[key] = self.tokenizer.find_tokens(self.character_definitions[key])
    
    def tokenize_tokens(self):
        for key in self.tokens.keys():
            self.tokens_tokenized[key] = self.tokenizer.find_tokens(self.tokens[key])
    
    def build_character_regexes(self):
        for key in self.character_definitions_tokenized.keys():
            regex = ''
            for token in self.character_definitions_tokenized[key]:
                if token.token_name == 'set':
                    regex += add_parenthesis(add_or_opperator(token.value))
                elif token.token_name == 'id':
                    regex += self.character_definitions[token.value]
                elif token.token_name == 'opp':
                    if token.value == '+':
                        regex += '|'
                    elif token.value == '{' or token.value == '}' or token.value == '[' or token.value == ']':
                        regex += token.value
            self.character_definitions[key] = regex
    
    def remove_except_tonkens(self):
        for key in self.tokens_tokenized.keys():
            i = 0
            while i < len(self.tokens_tokenized[key]):
                if self.tokens_tokenized[key][i].value == "EXCEPT":
                    break
                i+=1
            self.tokens_tokenized[key] = self.tokens_tokenized[key][0:i]


    def build_token_regexes(self):
        character_keys = self.character_definitions.keys()
        for key in self.tokens_tokenized.keys():
            regex = ''
            for token in self.tokens_tokenized[key]:
                if token.token_name == 'set':
                    regex += add_parenthesis(add_or_opperator(token.value))
                elif token.token_name == 'id':
                    if token.value in character_keys:
                        regex += self.character_definitions[token.value]
                    elif token.value == "EXCEPT":
                        pass
                elif token.token_name == 'opp':
                    if token.value == '+':
                        regex += '|'
                    elif token.value == '{' or token.value == '}' or token.value == '[' or token.value == ']':
                        regex += token.value
            self.tokens[key] = regex


    def build_tokens(self):
        found_tokens = []
        for i in self.keywords.keys():
            found_token = token(i, self.keywords[i])
            found_tokens.append(found_token)
        for i in self.tokens.keys():
            found_token = token(i, self.tokens[i])
            found_tokens.append(found_token)
        return found_tokens

file_input = input("Archivo con las definiciones ->")
scanner = Scanner(file_input)
print(scanner.character_definitions_tokenized)
print(scanner.tokens_tokenized)
print(scanner.character_definitions)
tokens = scanner.build_tokens()
print(tokens)
