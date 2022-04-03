from utils import *
class Scanner():
    def __init__(self, file_path):
        self.file_path = file_path
        self.reserved_words = ["COMPILER", "CHARACTERS", "KEYWORDS","TOKENS","PRODUCTIONS"]
        self.keywords = None
        self.tokens = None
        self.character_definitions = None
        self.extractFileContent()
        self.scan()
    
    #Save each line of the file in list self.file_content
    def extractFileContent(self):
        file = open(self.file_path, 'r')
        self.file_content = list(file)
        file.close()
    
    def check_if_word_is_reserved(self,word):
        if word in self.reserved_words:
            return True
        return False
    """
    Funtion: extract_characters
    Purpose: Get the definitions in the character section of the file
    Inputs: 
        start: Index of the key word CHARACTERS
    Outputs: 
        character_definitions: Tuple of the form (token_name, value)
    """
    def extract_section_data(self, start, section_name):
        print("section {} found extracting {}...".format(section_name, section_name))
        line_counter = start + 1
        buffer = ''
        character_definitions = {}
        sectionContinues = True
        while sectionContinues:
            current_line = self.file_content[line_counter]
            set_name = ''
            set_regex = ''
            index = 0
            for char in current_line:
                #Ignore blank spaces
                if char == " ":
                    pass
                #Empty the buffer ones an equal is found 
                #This will be the name of the token
                elif char == "=":
                    if buffer:
                        set_name = buffer
                        buffer = ''
                
                #If the last character is an end line 
                #Dont add the end line 
                elif char == '\n' and  look_ahead(current_line, index) == -1:
                    pass
                #Expretions end with a period so if the period is followed by the LAST
                #line brake dont add the period 
                elif char == '.' and  look_ahead(current_line, index) == '\n' and look_ahead(current_line, index + 1) ==-1:
                    pass
                else:
                    buffer += char
                index +=1 
            if self.check_if_word_is_reserved(buffer):
                sectionContinues =  False
                print("End of section Found")
            else:
                if set_name !='':
                    set_regex = buffer
                    character_definitions[set_name] = set_regex
            buffer = ''
            line_counter+=1
        return character_definitions

    def scan(self):
        for line in self.file_content:
            if "CHARACTERS" in line and self.character_definitions is None:
                self.character_definitions = self.extract_section_data(self.file_content.index(line),"CHARACTERS")
            elif "KEYWORDS" in line and self.keywords is None:
                self.keywords =self.extract_section_data(self.file_content.index(line), "KEYWORDS")
            elif "TOKENS" in line and self.tokens is None:
                self.tokens =self.extract_section_data(self.file_content.index(line), "TOKENS")

scanner = Scanner('test.cocol')
print('Character Definitions found:', scanner.character_definitions)
print('Keywords Definitons found: ', scanner.keywords)
print('Token Definitions found: ', scanner.tokens)