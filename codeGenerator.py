class codeGenerator():
    def __init__(self, path):
        self.path = path
        self.tab = '    '
        self.line_end = '\n'
        self.write_program()
    
    def write_program(self):
        file = open(self.path, 'w')
        file.write(
'''from Parser import parser
import sys

if len(sys.argv) == 0:
    sys.exit("input file missing")
file_path = sys.argv[1]
file = open(file_path, 'r')
file_content = file.read()
file.close()
identified_tokens = parser.find_tokens(file_content)
for i in identified_tokens:
    print(i)
''')
        file.close()

code_generator = codeGenerator('generated_code.py')

