from utils import *
from Automata.direct_construction import Tree

letter_regex = "(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)"
digit_regex = "(0|1|2|3|4|5|6|7|8|9)"
id_regex = letter_regex + "(" + letter_regex + "|" + digit_regex + ")*"

class Scanner():
    def __init__(self, file_path):
        self.file_path = file_path
        self.reserved_words = ["COMPILER", "CHARACTERS", "KEYWORDS","TOKENS","PRODUCTIONS"]
        self.curr_index = 0
        self.keywords = None
        self.tokens = None
        self.character_definitions = None
        self.extractFileContent()
        self.removeComments()
        print(self.file_content)
        self.scan()
    
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

    def scan(self):
    
        found_compiler_keyword = self.expect("COMPILER")
        if found_compiler_keyword:
            print(found_compiler_keyword)
            print("Compiler keyword was found in header")
        else:
            print("Expected compiler definition")
        found_compiler_name = self.expect(id_regex)
        if found_compiler_name:
            print("Compiler name: ", found_compiler_name)
        
scanner = Scanner('test.cocol')
