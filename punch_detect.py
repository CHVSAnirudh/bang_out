from collections import deque
import time
class punch_detect:
    X = deque(maxlen = 5)
    
    def punch_detect(self,mobj):
        if mobj.visibility > 0.5:
            self.X.append(mobj.z)
            r = abs(max(self.X) - min(self.X))
            if r > 0.8 and len(self.X)==5:
                #print(self.X)
                self.X.clear()
                return True
        return False
        

