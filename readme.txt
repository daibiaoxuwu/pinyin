文件:
list1.py 产生:dict2c文件.
        来源:原始的文本文件.title和html.
        格式:{'安':{'安全':10,'安稳':5},...}

list2.py 来源:dict2c文件
            产生:dict2ctotal文件.
            格式:1) 内部的voicedict格式:{'安':'an',...}
                2) pointset,最后dump到了errorverse里.是记录所有不再拼音汉字表voicedict里的字的set.
                3) 文件格式:{'安':{'quan':{'全':10,'权':1,...},'wen':
                '安quan':'全'+'权'+...合为1.

list4.py 生成dict2ctotal2文件.
        和list2区别在:
                '安':'全'+'稳'+...和为1.

list5.py 来源:dict2c. 
        产生取过log的dict2clog

run1.py 利用dict2c的
run2.py 利用ditc2ctotal2的(也可以改成total,效果并不好)
