import pickle
import math
with open('dict3c','rb') as f:
    d=pickle.load(f)
    e={}
    for k in d:
        e[k]={}
        for j in d[k]:
            e[k][j]={}
            for r in d[k][j]:
                e[k][j][r]=math.log(d[k][j][r])
with open('dict3c2','wb') as f:
    pickle.dump(e,f)

