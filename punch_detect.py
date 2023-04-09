from collections import deque
import time
import math
class punch_detect:
    X = deque(maxlen = 5)
    
    def punch_detect(self,mobj):
        r = 0
        if mobj.visibility > 0.5:
            self.X.append(mobj.z)
            r = abs(max(self.X) - min(self.X))
            if r > 0.8 and len(self.X)==5:
                #print(self.X)
                self.X.clear()
                return True,math.ceil(r/0.8)
        return False, math.ceil(r/0.8)
        

