
#coding=UTF-8
import matplotlib.pyplot  as plt
import numpy as np
import pandas as pd
import time
import math

import  os
os.chdir("D:\pythonTest\Pnadas")
BasePath=os.getcwd()
#fin=BasePath+"\hello.csv"
Dukefin=BasePath+"\Duke.xlsx"
fin_xlsx=BasePath+"\hello.xlsx"


fout=BasePath+"\bb.csv"

Dateframe=pd.DataFrame(pd.read_excel(fin_xlsx))

df=Dateframe

lc=pd.DataFrame(Dateframe)


print lc.sort(['SSID'])

print(df['SSID'])

#print(dir(df))




# k_down=list(df['SSID'])
# print (k_down)
#
# k1_down=set(k_down)
# print(k1_down)
# print("---------------")
# for i in k1_down:
#     print(i,"----的个数")
#     print(k_down.count(i))

# k_down=sorted(k_down)


print(df,Dateframe)



