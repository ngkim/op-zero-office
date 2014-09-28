# -*- coding: utf-8 -*-

class StringUtil:
    
    # 문자열을 int 배열로 만들어줌
    # 예) "1-4,7,9" ==> [1,2,3,4,7,9] 
    def list_str_to_int(self, list_str):
        lstr = list_str.split(",")
        
        lint = []
        for str in lstr:
            lstr1 = str.split("-")
            
            if len(lstr1) == 2:
                min = int(lstr1[0])
                max = int(lstr1[1]) + 1 # range함수에서 max 값을 포함할 수 있도록 1을 더함 
            
                for i in range(min, max):
                    lint.append(i)
            else:
                lint.append(int(str))
        
        return lint
        
 
class Console:
    
    def __init__(self):
        self.INFO = '\033[94m'
        self.DBG = '\033[93m'        
        self.WARN = '\033[92m'
        self.ERR = '\033[91m'
        
        self.ENDC = '\033[0m'
            
    def log(self, msg, type = "" ):
        if type == "info":
            print self.INFO + "%s" % msg + self.ENDC
        elif type == "debug":
            print self.DBG + "%s" % msg + self.ENDC
        elif type == "warn":
            print self.WARN + "%s" % msg + self.ENDC
        elif type == "error":
            print self.ERR + "%s" % msg + self.ENDC
        else:
            print "%s" % msg
    
    def info(self, msg):
        self.log(msg, "info") 
            
    def debug(self, msg):
        self.log(msg, "debug")
        
    def error(self, msg):
        self.log(msg, "error")        