from collections import namedtuple

token = namedtuple('token', ['token_name','value'])
def look_ahead(buffer, index):
        try:
            return buffer[index + 1]
        except:
            return -1