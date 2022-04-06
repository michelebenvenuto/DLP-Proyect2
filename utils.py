from collections import namedtuple

token = namedtuple('token', ['token_name','value'])
def look_ahead(buffer, index, positons_ahead = 1):
        try:
            return buffer[index + positons_ahead]
        except:
            return -1