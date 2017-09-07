
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

#Dateframe=pd.read_csv(fin)
Dateframe=pd.read_excel(fin_xlsx)

df=Dateframe
#print(df.shape)
#print(df.columns)

Pass_count=0  #取 DHCP_Chr_Event为 -1 的个数
fail_count=0  #取 DHCP_Chr_Event为  1 的个数
#DHCP=df.groupby(df["DHCP_Chr_Event"])
DHCP=df['DHCP_Chr_Event'].groupby(df['DHCP_Chr_Event'])#取DHCP_Chr_Event列数据作为待处理数据  分组统计根据groupby(df['DHCP_Chr_Event'])

DHCP_CNT=list(DHCP.sum())
print(list(DHCP.sum()))
Pass_count=math.fabs(DHCP_CNT[0])
fail_count=DHCP_CNT[1]
print(Pass_count,fail_count)
horizontal_axial=['-1','1']   #横坐标取值

#AP_rssi=list(df['AP_RSSI'])
#print AP_rssi[0:10]





time.sleep(10)

# df_timestamp=df.set_index('TimeStamp')   #时间为横坐标
# df_timestamp.DHCP_Chr_Event.plot(color='g')
# df_timestamp.AP_RSSI.plot(color='r')
# plt.show()



#plt.figure()
# plt.plot()
#plt.legend(loc='best')
#plt.show()
#df.to_save(fout)
