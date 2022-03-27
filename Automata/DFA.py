from FA import FA
from pythomata import SimpleDFA
import time
class DFA(FA):
    def simulate(self,chars):
        start_time = time.time()
        s = self.startState
        for i in range(len(chars)):
            c = chars[i]
            if c not in self.alphabet:
                return False, (time.time() - start_time)
            s = self.move(s,c)
        if s in self.accpetingStates:
            return True, (time.time() - start_time)
        else:
            return False, (time.time() - start_time)