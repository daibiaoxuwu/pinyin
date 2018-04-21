import jieba
import jieba.posseg as pseg
import jieba.analyse

str1 = "我来到北京清华大学"
str2 = 'python的正则表达式是好用的'
str3 = "小明硕士毕业于中国科学院计算所，后在日本京都大学深造"

##关键词提取，参数setence对应str1为待提取的文本,topK对应2为返回几个TF/IDF权重最大的关键词，默认值为20
result4 = jieba.cut_for_search(str3)        ##搜索引擎模式
for i in result4:
    print(i)
