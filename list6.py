import pickle
import json
import math
#import sys
#reload(sys)
#sys.setdefaultencoding('gbk')


if __name__ == "__main__":
    with open('dict2clog','rb') as f:
        smdict=pickle.load(f)
    for i in smdict:
        for j in smdict[i]:
                smdict[i][j]=math.log(smdict[i][j]+1)
    with open('dict2cloglog','wb') as f:
        pickle.dump(smdict,f)

