# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 18:56:11 2020

@author: Rich
"""

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import copy
import pymysql
from sqlalchemy import create_engine
import time



cname={}
cname['joints']=['questionsymbol','jointnum','x','y','jointconnection']
cname['elements']=['questionsymbol','elementnum','jointi','jointj','EA','EI']
cname['restraints']=['questionsymbol','jointnum','restrainttype','alp']
cname['concentrated_load']=['questionsymbol','elementnum','loadmag','loaddirection','loadposition']
cname['distributed_load']=['questionsymbol','elementnum','loadmag','loaddirection','loadstartposition','loadendposition']
cname['jointload']=['questionsymbol','jointnum','Fx','Fy','M']
cname['settlements']=['questionsymbol','elementnum','dxi','dyi','thetai','dxj','dyj','thetaj']
cname['spring']=['questionsymbol','jointnum','restrainttype','alp','k']
cname['temperature_load']=['questionsymbol','elementnum','alpt','temperatureupside','temperaturedownside','sectionheight']
cname['basic_questioninfor']=['questionsymbol','nickname','generaldescription','languagesource','state','drawingtype','modetype','tishitype','difficulty','thumbs','frequency','filetime','filetimenum','badpost']
cname['detailtips']=['questionsymbol','tipappearnum','tipobject','objectnum','tipcondition','tiptext']
cname['generaltip']=['questionsymbol','tiptext']
global language
language='中文'


global userID,nickname,school
userID='z373072096'

#nickname='周毅华'
#school='123'
#nickname='0'
#userID='0' 
global timunum,timustate,timuhuizhi,timuyingyong
global timumiaoshu,timutishifangshi,timunandu

def qualifymanageshangchuan():
    conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
    cursor = conn.cursor()
    sql="delete from detailtips where questionsymbol=%s"
    cursor.execute(sql,[questionsymbol])
    conn.commit()
    cursor.close()
    conn.close()
    conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
    cursor = conn.cursor()
    sql="delete from generaltip where questionsymbol=%s"
    cursor.execute(sql,[questionsymbol])
    conn.commit()
    cursor.close()
    conn.close()
    ZDYTISHI.sortzdytishi()
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    if len(zdytishi)!=0:
        d=[]
        for i in range(len(zdytishi)):
            d.append(questionsymbol)
        uploadmatrix=pd.concat([pd.DataFrame(d),zdytishi],axis=1)
        uploadmatrix.columns=cname['detailtips']
        uploadmatrix.to_sql('detailtips', engine, index= False,if_exists='append')
    if len(zhengtitishi)>1:
        d=[]
        d.append(questionsymbol)
        uploadmatrix=pd.concat([pd.DataFrame(d),pd.DataFrame([zhengtitishi])],axis=1)
        uploadmatrix.columns=cname['generaltip']
        uploadmatrix.to_sql('generaltip', engine, index= False,if_exists='append')
    
    
def qualifyshangchuan():
    global timunum,timustate,timuhuizhi,timuyingyong
    global timumiaoshu,timutishifangshi,userID,zdytishi,timunandu
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    sql="select count(*) from basic_questioninfor where questionsymbol like('%%%%%s%%%%')"%(userID)
    df = pd.read_sql_query(sql, engine)
    num=int(df.loc[0,'count(*)'])
    
    
    df=pd.DataFrame(np.zeros((1,14)))
    df.iloc[0,0]=userID+'_'+str(num+1)
    df.iloc[0,1]=nickname
    df.iloc[0,2]=timumiaoshu
    df.iloc[0,3]=language
    df.iloc[0,4]=timustate
    df.iloc[0,5]=timuhuizhi
    df.iloc[0,6]=timuyingyong
    df.iloc[0,7]=timutishifangshi
    df.iloc[0,8]=timunandu
    df.iloc[0,9]=0
    df.iloc[0,10]=0
    df.iloc[0,11]=time.strftime("%Y/%m/%d", time.localtime(time.time()))
    df.iloc[0,12]=int(time.time())
    df.iloc[0,13]=0

    df.columns=cname['basic_questioninfor']
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    df.to_sql('basic_questioninfor', engine, index= False,if_exists='append')
    questionsymbol=userID+'_'+str(num+1)
    
    
    def upload(x,y):
        d=[]
        if len(informatrixs[x])==0:
            return
        for i in range(len(informatrixs[x])):
            d.append(userID+'_'+str(num+1))
        uploadmatrix=pd.concat([pd.DataFrame(d),informatrixs[x]],axis=1)
        uploadmatrix.columns=cname[y]
        uploadmatrix.to_sql(y, engine, index= False,if_exists='append')
    upload(0,'joints')
    upload(1,'elements')
    upload(2,'restraints')
    upload(3,'jointload')
    upload(4,'concentrated_load')
    upload(5,'distributed_load')
    upload(6,'temperature_load')
    upload(7,'settlements')
    upload(8,'spring')
    ZDYTISHI.sortzdytishi()
    if len(zdytishi)!=0:
        d=[]
        for i in range(len(zdytishi)):
            d.append(userID+'_'+str(num+1))
        uploadmatrix=pd.concat([pd.DataFrame(d),zdytishi],axis=1)
        uploadmatrix.columns=cname['detailtips']
        uploadmatrix.to_sql('detailtips', engine, index= False,if_exists='append')
    if len(zhengtitishi)>1:
        d=[]
        d.append(userID+'_'+str(num+1))
        uploadmatrix=pd.concat([pd.DataFrame(d),pd.DataFrame([zhengtitishi])],axis=1)
        uploadmatrix.columns=cname['generaltip']
        uploadmatrix.to_sql('generaltip', engine, index= False,if_exists='append')

 
    conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='answering_process',charset='utf8')
    cursor = conn.cursor()
    sql="create table moment%s (questionsymbol varchar(50),userID varchar(50),starttime varchar(50),answertime varchar(50),primary key(questionsymbol,userID,starttime,answertime))"%(userID+'_'+str(num+1))
    print(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='answering_process',charset='utf8')
    cursor = conn.cursor()
    for i in range(len(a)):
        for j in range(len(a[i])):
            tempcname=str(i+1)+'_'+str(j+1)
            sql="alter table moment%s add %s varchar(50)"%(questionsymbol,tempcname)
            cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='answering_process',charset='utf8')
    cursor = conn.cursor()
    sql="alter table moment%s add %s varchar(50)"%(questionsymbol,"提示或错误")
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return 1
    
def momentanswer_record():
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    df=pd.DataFrame(np.zeros((1,3)))
    df.iloc[0,0]=userID
    df.iloc[0,1]=questionsymbol
    df.iloc[0,2]=starttime
    df.columns=['userID','questionsymbol','starttime']
    df.to_sql('momentanswer_record', engine, index= False,if_exists='append')
    
    conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
    cursor = conn.cursor()
    sql="select frequency from basic_questioninfor where questionsymbol='%s'"%questionsymbol
    cursor.execute(sql)
    result=cursor.fetchone()[0]
    result=int(result)+1
    cursor.close()
    conn.close()
    
    conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
    cursor = conn.cursor()
    sql="update basic_questioninfor set frequency='%d' where questionsymbol='%s'"%(result,questionsymbol)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


global informatrixs
informatrixs=[]
global zdytishi
zdytishi=pd.DataFrame(np.full((15,5),np.nan))
global zdytishinum
zdytishinum=0
zhengtitishi=''
class ZDYTISHI():
    @staticmethod
    def initzdytishinum():
        global zdytishinum,zdytishi
        zdytishinum=0
        zdytishi=pd.DataFrame(np.full((15,5),np.nan))
    @staticmethod
    def updatezdytishi(x1,x2,x3,x4):
        global zdytishinum,zdytishi
        zdytishi.iloc[zdytishinum,0]=zdytishinum+1
        zdytishi.iloc[zdytishinum,1]=x1
        zdytishi.iloc[zdytishinum,2]=x2
        zdytishi.iloc[zdytishinum,3]=x3
        zdytishi.iloc[zdytishinum,4]=x4
        zdytishinum=zdytishinum+1
        print(zdytishi)
    @staticmethod
    def sortzdytishi():
        global zdytishi
        zdytishi=zdytishi.dropna()
    @staticmethod
    def exchangezdytishi(x,y):
        global zdytishi
        temp1=zdytishi.iloc[x]
        temp2=zdytishi.iloc[y]
        zdytishi.iloc[x]=temp2
        zdytishi.iloc[y]=temp1
        for i in range(len(zdytishi)):
            if pd.isnull(zdytishi.iloc[i,0])==False:
                zdytishi.iloc[i,0]=i+1
        print(zdytishi)
    @staticmethod
    def shanchutishi(x):
        global zdytishi,zdytishinum
        zdytishinum=zdytishinum-1
        zdytishi=zdytishi.drop(x)
        zdytishi=zdytishi.append([np.NaN],ignore_index=True)
        for i in range(len(zdytishi)):
            if pd.isnull(zdytishi.iloc[i,0])==False:
                zdytishi.iloc[i,0]=i+1
        print(zdytishi)
def updatezhengtitishi(x):
    global zhengtitishi
    zhengtitishi=x
#zdytishi.iloc[0,0]="单个杆件"
#zdytishi.iloc[0,1]="1"
#zdytishi.iloc[0,2]="自动判断"
#zdytishi.iloc[0,3]="测试ing"


def offerzdytishi():
    global zdytishi,zdycuowunum
    zdytishi=zdytishi.dropna()
    state=1
    print(zdytishi)
    for i in range(len(zdytishi)):
        if zdytishi[1][i]=='单个节点':
            x=zdytishi[2][i].split(',')
            print(x)
            state=zdybiduileixing(x)
            if state==0:
                zdycuowunum=i
                return i
            state=zdybiduizf(x)
            if state==0:
                zdycuowunum=i
                return i
            state=zdybiduixddx(x)
            if state==0:
                zdycuowunum=i
                return i
            state=zdybiduijdfp(x)
            if state==0:
                zdycuowunum=i
                return i
        else:
            x=zdytishi[2][i].split(',')
            state=zdybiduileixing(x)
            if state==0:
                zdycuowunum=i
                return i
            state=zdybiduizf(x)
            if state==0:
                zdycuowunum=i
                return i
            state=zdybiduixddx(x)
            if state==0:
                zdycuowunum=i
                return i
    zdycuowunum=-1
    return -1







      
for i in range(0,9):
    informatrixs.append(pd.DataFrame())
def initinformatrixs():
    global informatrixs
    informatrixs=[]
    for i in range(0,9):
        informatrixs.append(pd.DataFrame())
def getmanagequestion(x):
    global questionsymbol
    questionsymbol=x
    global informatrixs,zdytishi,zhengtitishi
    global timunum,timustate,timuhuizhi,timuyingyong
    global timumiaoshu,timutishifangshi,timunandu,zdytishinum
    informatrixs[0]=pd.DataFrame(np.full((15,4),np.nan))
    informatrixs[1]=pd.DataFrame(np.full((15,5),np.nan))
    informatrixs[2]=pd.DataFrame(np.full((15,3),np.nan))
    informatrixs[3]=pd.DataFrame(np.full((15,4),np.nan))
    informatrixs[4]=pd.DataFrame(np.full((15,4),np.nan))
    informatrixs[5]=pd.DataFrame(np.full((15,5),np.nan))
    informatrixs[6]=pd.DataFrame(np.full((15,5),np.nan))
    informatrixs[7]=pd.DataFrame(np.full((15,7),np.nan))
    informatrixs[8]=pd.DataFrame(np.full((15,4),np.nan))
    zdytishi=pd.DataFrame(np.full((15,5),np.nan))
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    def getmatrixs(x1,x2):
        sql = "select * from %s where questionsymbol='"%x2+questionsymbol+"'"
        infor=pd.read_sql_query(sql, engine)
        informatrixs[x1]=infor.drop('questionsymbol',axis=1)
        lieshu=informatrixs[x1].shape[1]
        columns=[]
        for i in range(lieshu):
            columns.append(i)
        informatrixs[x1].columns=columns
    getmatrixs(0,'joints')
    getmatrixs(1,'elements')
    getmatrixs(2,'restraints')
    getmatrixs(3,'jointload')
    getmatrixs(4,'concentrated_load')
    getmatrixs(5,'distributed_load')
    getmatrixs(6,'temperature_load')
    getmatrixs(7,'settlements')
    getmatrixs(8,'spring')
    sql = "select * from detailtips where questionsymbol='"+questionsymbol+"'"
    infor=pd.read_sql_query(sql, engine)
    if len(infor)>0:
        zdytishi=infor.drop('questionsymbol',axis=1)
        lieshu=zdytishi.shape[1]
        columns=[]
        for i in range(lieshu):
            columns.append(i)
        zdytishi.columns=columns
        zdytishinum=len(zdytishi)
    else:
        zdytishi=pd.DataFrame(np.zeros((1,5)))
        zdytishi.iloc[0,0]=np.NaN
        zdytishi.iloc[0,1]=np.NaN
        zdytishi.iloc[0,2]=np.NaN
        zdytishi.iloc[0,3]=np.NaN
        zdytishi.iloc[0,4]=np.NaN
        zdytishinum=0
    for i in range(15):
        if len(zdytishi)<15:
            zdytishi=zdytishi.append([np.NaN],ignore_index=True)
    sql = "select * from generaltip where questionsymbol='"+questionsymbol+"'"
    infor=pd.read_sql_query(sql, engine)
    if len(infor)>0:
        zhengtitishi=infor.iloc[0,1]
    else:
        zhengtitishi=''
    sql = "select * from basic_questioninfor where questionsymbol='"+questionsymbol+"'"
    infor=pd.read_sql_query(sql, engine)
    timustate=infor.iloc[0,4]
    timuhuizhi=infor.iloc[0,5]
    timuyingyong=infor.iloc[0,6]
    timutishifangshi=infor.iloc[0,7]
    timunandu=infor.iloc[0,8]

  
def getquestion(x):
    global questionsymbol
    questionsymbol=x
    c1=time.time()
    global informatrixs,zdytishi,zhengtitishi
    global timunum,timustate,timuhuizhi,timuyingyong
    global timumiaoshu,timutishifangshi,timunandu
    informatrixs[0]=pd.DataFrame(np.full((15,4),np.nan))
    informatrixs[1]=pd.DataFrame(np.full((15,5),np.nan))
    informatrixs[2]=pd.DataFrame(np.full((15,3),np.nan))
    informatrixs[3]=pd.DataFrame(np.full((15,4),np.nan))
    informatrixs[4]=pd.DataFrame(np.full((15,4),np.nan))
    informatrixs[5]=pd.DataFrame(np.full((15,5),np.nan))
    informatrixs[6]=pd.DataFrame(np.full((15,5),np.nan))
    informatrixs[7]=pd.DataFrame(np.full((15,7),np.nan))
    informatrixs[8]=pd.DataFrame(np.full((15,4),np.nan))
    zdytishi=pd.DataFrame(np.full((15,5),np.nan))
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    def getmatrixs(x1,x2):
        sql = "select * from %s where questionsymbol='"%x2+questionsymbol+"'"
        infor=pd.read_sql_query(sql, engine)
        informatrixs[x1]=infor.drop('questionsymbol',axis=1)
        lieshu=informatrixs[x1].shape[1]
        columns=[]
        for i in range(lieshu):
            columns.append(i)
        informatrixs[x1].columns=columns
    getmatrixs(0,'joints')
    getmatrixs(1,'elements')
    getmatrixs(2,'restraints')
    getmatrixs(3,'jointload')
    getmatrixs(4,'concentrated_load')
    getmatrixs(5,'distributed_load')
    getmatrixs(6,'temperature_load')
    getmatrixs(7,'settlements')
    getmatrixs(8,'spring')
    sql = "select * from detailtips where questionsymbol='"+questionsymbol+"'"
    infor=pd.read_sql_query(sql, engine)
    if len(infor)>0:
        zdytishi=infor.drop('questionsymbol',axis=1)
        lieshu=zdytishi.shape[1]
        columns=[]
        for i in range(lieshu):
            columns.append(i)
        zdytishi.columns=columns
    else:
        zdytishi=pd.DataFrame()
    sql = "select * from generaltip where questionsymbol='"+questionsymbol+"'"
    infor=pd.read_sql_query(sql, engine)
    if len(infor)>0:
        zhengtitishi=infor.iloc[0,1]
    else:
        zhengtitishi=''
    sql = "select * from basic_questioninfor where questionsymbol='"+questionsymbol+"'"
    infor=pd.read_sql_query(sql, engine)
    timustate=infor.iloc[0,4]
    timuhuizhi=infor.iloc[0,5]
    timuyingyong=infor.iloc[0,6]
    timutishifangshi=infor.iloc[0,7]
    timunandu=infor.iloc[0,8]
    c2=time.time()
    print(c2-c1)
    #df = pd.read_sql_query(sql, engine)
#informatrixs[0]=pd.DataFrame(np.full((15,4),np.nan))
#informatrixs[1]=pd.DataFrame(np.full((15,5),np.nan))
#informatrixs[2]=pd.DataFrame(np.full((15,3),np.nan))
#informatrixs[3]=pd.DataFrame(np.full((15,4),np.nan))
#informatrixs[4]=pd.DataFrame(np.full((15,4),np.nan))
#informatrixs[5]=pd.DataFrame(np.full((15,5),np.nan))
#informatrixs[6]=pd.DataFrame(np.full((15,5),np.nan))
#informatrixs[7]=pd.DataFrame(np.full((15,7),np.nan))
#informatrixs[8]=pd.DataFrame(np.full((15,4),np.nan))
##1
#informatrixs[0][0][0]=1
#informatrixs[0][1][0]=0
#informatrixs[0][2][0]=0
#informatrixs[0][3][0]=1
#informatrixs[0][0][1]=2
#informatrixs[0][1][1]=0
#informatrixs[0][2][1]=1
#informatrixs[0][3][1]=1
#informatrixs[0][0][2]=3
#informatrixs[0][1][2]=1
#informatrixs[0][2][2]=1
#informatrixs[0][3][2]=1
#informatrixs[0][0][3]=4
#informatrixs[0][1][3]=1
#informatrixs[0][2][3]=0
#informatrixs[0][3][3]=1
##2
#informatrixs[1][0][0]=1
#informatrixs[1][1][0]=1
#informatrixs[1][2][0]=2
#informatrixs[1][3][0]=1
#informatrixs[1][4][0]=1
#
#informatrixs[1][0][1]=2
#informatrixs[1][1][1]=2
#informatrixs[1][2][1]=3
#informatrixs[1][3][1]=1
#informatrixs[1][4][1]=1
#
#informatrixs[1][0][2]=3
#informatrixs[1][1][2]=3
#informatrixs[1][2][2]=4
#informatrixs[1][3][2]=1
#informatrixs[1][4][2]=1
##3
#informatrixs[2][0][0]=1
#informatrixs[2][1][0]=4
#informatrixs[2][2][0]=0
#
#informatrixs[2][0][1]=4
#informatrixs[2][1][1]=2
#informatrixs[2][2][1]=0
##4
#informatrixs[3][0][0]=2
#informatrixs[3][1][0]=10
#informatrixs[3][2][0]=10
#informatrixs[3][3][0]=10
##5
#informatrixs[4][0][0]=2
#informatrixs[4][1][0]=10
#informatrixs[4][2][0]=-90
#informatrixs[4][3][0]=0.5

#！！!
#6
#informatrixs[5][0][0]=3
#informatrixs[5][1][0]=10
#informatrixs[5][2][0]=90
#informatrixs[5][3][0]=0
#informatrixs[5][4][0]=1
##7
#informatrixs[6][0][0]=1
#informatrixs[6][1][0]=0.0001
#informatrixs[6][2][0]=10
#informatrixs[6][3][0]=20
#informatrixs[6][4][0]=0.1
#8
#informatrixs[7][0][0]=1
#informatrixs[7][1][0]=0
#informatrixs[7][2][0]=0
#informatrixs[7][3][0]=1
#informatrixs[7][4][0]=0
#informatrixs[7][5][0]=0
#informatrixs[7][6][0]=0
#9
#informatrixs[8][0][0]=2
#informatrixs[8][1][0]=2
#informatrixs[8][2][0]=45
#informatrixs[8][3][0]=1

#for i in range(0,9):
#    informatrixs[i]=informatrixs[i].dropna()
    
    
global choosetab
choosetab=0

def setbasicinfor(x,y):
    global nickname
    global userID
    nickname=x
    userID=y
    
def updateinformatrixs(x,y):
    informatrixs[x]=y


def sortinformatrixs():
    for i in range(0,9):
        informatrixs[i]=informatrixs[i].dropna()
        if len(informatrixs[i])>0:
            informatrixs[i]=informatrixs[i].sort_values(by=0)


def updatenum(x):
    global choosetab
    choosetab=x
    print("choosetab="+str(choosetab))
    
#jys角约束，xys线约束、scxys删除线约束
global jys,xys,scxys
jys=[]
xys=[]
scxys=[]
#daduan打断状态，duandian断点
global daduan,duandian
daduan=0
duandian=[]
#ps起始点，pe终止点（一根杆件上的相对位置）
ps=0
pe=1
#是否显示跨中荷载
global switchmidspan
switchmidspan=0
#是否取半结构
global switchbjg
switchbjg=0
#正对称、反对称
global zdc,fdc
zdc=0
fdc=0
global switchEAI
switchEAI=1






#从question1.xlsx录入信息
def fileinelements():
    global switchEAI
    switchEAI=1
    global zdc,fdc,dcz
    joint={}
    element={}
    global joints,joints_,elements
    joints=[]
    joints_=[]
    elements=[]
    global xflim,xzlim,yflim,yzlim

    for i in range(len(informatrixs[0])):
        joint['num']=int(informatrixs[0].iloc[i,0])
        joint['x']=informatrixs[0].iloc[i,1]
        joint['y']=informatrixs[0].iloc[i,2]
        joint['connection']=informatrixs[0].iloc[i,3]
        joint['restraint']=0
        #supportalp支座转角
        joint['salp']=0
        #弹性支座转角
        joint['esupport']=0
        joint['ealp']=0
        joint['k']=0
        joints.append(joint.copy())
    
    
    #去掉重复的节点
    for i in joints:
        if i  not in joints_:
            joints_.append(i)
    #节点按编号排序
    for j in range(len(joints_)):
        for k in range(len(joints_)):
            t={}
            if joints_[j]['num']<joints_[k]['num']:
                t=joints_[j]
                joints_[j]=joints_[k]
                joints_[k]=t.copy()
    for i in range(len(informatrixs[8])):
        joints_[int(informatrixs[8].iloc[i,0]-1)]['esupport']=int(informatrixs[8].iloc[i,1])
        joints_[int(informatrixs[8].iloc[i,0]-1)]['ealp']=int(informatrixs[8].iloc[i,2])
        joints_[int(informatrixs[8].iloc[i,0]-1)]['k']=int(informatrixs[8].iloc[i,3])

    #读取，将节点放入杆件中
    for i in range(len(informatrixs[1])):
       element['num']=informatrixs[1].iloc[i,0]
       element['pi']=joints_[int(informatrixs[1].iloc[i,1]-1)]
       element['pj']=joints_[int(informatrixs[1].iloc[i,2]-1)]
       if (element['pj']['x']-element['pi']['x'])!=0:
           element['alp']=int(np.arctan2((element['pj']['y']-element['pi']['y']),(element['pj']['x']-element['pi']['x']))/3.14159*180)
       else:
           if (element['pj']['y']-element['pi']['y'])>=0:
               element['alp']=90
           else:
               element['alp']=-90
       element['l']=np.sqrt((element['pj']['y']-element['pi']['y'])**2+(element['pj']['x']-element['pi']['x'])**2)
       elements.append(element.copy())
    for i in range(len(informatrixs[2])):
        joints_[int(informatrixs[2].iloc[i,0]-1)]['restraint']=int(informatrixs[2].iloc[i,1])
        joints_[int(informatrixs[2].iloc[i,0]-1)]['salp']=int(int(informatrixs[2].iloc[i,2]))
        
    #确定最长和最短的杆件，取一个均值
    if len(elements)!=0:
        minl=elements[0]['l']
        maxl=0
        for i in range(len(elements)):
            if elements[i]['l']>maxl:
                maxl=elements[i]['l']
            if elements[i]['l']<minl:
                minl=elements[i]['l']
    else:
        minl=0
        maxl=0
        for i in range(len(joints_)):
            if abs(joints_[i]['x'])>maxl or abs(joints_[i]['y'])>maxl :
                maxl=max(abs(joints_[i]['x']),abs(joints_[i]['y']))
    #r控制圆的板件，s控制支座直线的长度
    if maxl==0:
        maxl=1
    global r,s
    s=0.06*(maxl+minl)/2
    print(s)
    r=s/3
    #c就是用户作答的答案
    global c
    c=[]
    for i in range(len(elements)):
        c_=[]
        c.append(c_)
    #x负界限，x正界限，y负界限，y正界限
    global xflim,xzlim,yflim,yzlim
    xflim=joints_[0]['x']
    xzlim=joints_[0]['x']
    yflim=joints_[0]['y']
    yzlim=joints_[0]['y']
    for i in range(len(joints_)):
        if joints_[i]['x']<=xflim:
            xflim=joints_[i]['x']
        if joints_[i]['x']>=xzlim:
            xzlim=joints_[i]['x']
        if joints_[i]['y']<=yflim:
            yflim=joints_[i]['y']
        if joints_[i]['y']>=yzlim:
            yzlim=joints_[i]['y']
    #res四周留白的大小
    global res,xrange,yrange,xlong
    res=6*s
    #图幅比例1：1.6，需要确定长边与短边
    if xzlim-xflim+2*res>=1.6*(yzlim-yflim+2*res):
        xrange=[xflim-res,xzlim+res]
        yrange=[0,0]
#        yrange=[(xflim-res)/1.6,(xzlim+res)/1.6]
        yrange[0]=0.5*(yflim+yzlim)-(xzlim-xflim+2*res)/3.2
        yrange[1]=0.5*(yflim+yzlim)+(xzlim-xflim+2*res)/3.2
        xlong=1
    else:
        yrange=[yflim-res,yzlim+res]
        xrange=[0,0]
        xrange[0]=xflim-0.8*(yzlim-yflim)-1.6*res+0.5*xzlim-0.5*xflim
        xrange[1]=xzlim+0.8*(yzlim-yflim)+1.6*res-0.5*xzlim+0.5*xflim
        xlong=0


#filedc，用户选择半结构情况下导入
#默认只考虑对称轴是沿着x方向的



#辨别题型
def bianbietixing():
    global lxl,xflim,xzlim,informatrixs
    #lxl连续梁，判断条件，所有杆件的角度均为0度
    lxl=0
    alplist=[]
    for i in range(len(elements)):
        if elements[i]['alp']==0:
            alplist.append(0)
    if len(alplist)==len(elements):
        lxl=1

    #wcygj，无侧移刚架，判断条件，非支座的角位移最大值的5倍，小于最大线位移
    global wcygj
    wcygj=0
    #cy侧移，jwy角位移，qgj全刚架
    cy=-1
    jwy=-1
    qgj=1
    #排除支座的位移
    global maxweiyi,maxzhuanjiao
    maxweiyi=0
    maxzhuanjiao=0
    for i in range(len(elements)):
        if abs(calelements[i]['pi']['displacement'][0])>maxweiyi and calelements[i]['pi']['restraint']==0:
            maxweiyi=abs(calelements[i]['pi']['displacement'][0])
        if abs(calelements[i]['pi']['displacement'][1])>maxweiyi and calelements[i]['pi']['restraint']==0:
            maxweiyi=abs(calelements[i]['pi']['displacement'][1])
        if abs(calelements[i]['pi']['displacement'][2])>maxzhuanjiao and calelements[i]['pi']['restraint']==0 and calelements[i]['pi']['connection']!=0:
            maxzhuanjiao=abs(calelements[i]['pi']['displacement'][2])
        if abs(calelements[i]['pj']['displacement'][0])>maxweiyi and calelements[i]['pj']['restraint']==0:
            maxweiyi=abs(calelements[i]['pj']['displacement'][0])
        if abs(calelements[i]['pj']['displacement'][1])>maxweiyi and calelements[i]['pj']['restraint']==0:
            maxweiyi=abs(calelements[i]['pj']['displacement'][1])
        if abs(calelements[i]['pj']['displacement'][2])>maxzhuanjiao and calelements[i]['pj']['restraint']==0 and calelements[i]['pj']['connection']!=0:
            maxzhuanjiao=abs(calelements[i]['pj']['displacement'][2])
#    for i in range(len(elements)):
#        if close0(calelements[i]['pi']['displacement'][0])==False and calelements[i]['pi']['restraint']==0:
#            cy=1
#        if close0(calelements[i]['pi']['displacement'][1])==False and calelements[i]['pi']['restraint']==0:
#            cy=1
#        if close0(calelements[i]['pj']['displacement'][0])==False and calelements[i]['pj']['restraint']==0:
#            cy=1
#        if close0(calelements[i]['pj']['displacement'][1])==False and calelements[i]['pj']['restraint']==0:
#            cy=1
    #存在铰则不是全刚架
    for i in range(len(elements)):
#        if close0(calelements[i]['pi']['displacement'][2])==False or close0(calelements[i]['pj']['displacement'][2])==False:
#            jwy=1
        if calelements[i]['pi']['restraint']==0 and calelements[i]['pi']['connection']==0:
            qgj=0
        if calelements[i]['pj']['restraint']==0 and calelements[i]['pj']['connection']==0:
            qgj=0
    if maxweiyi>5*maxzhuanjiao:
        cy=1
        jwy=0
    if maxzhuanjiao>5*maxweiyi:
        cy=0
        jwy=1
    if cy==0 and qgj==1:
        wcygj=1
    #框架，杆件不是垂直就是水平
    global kuangjia
    kuangjia=1
    for i in range(len(elements)):
        if elements[i]['alp']%90!=0:
            kuangjia=0
    #jdjlfpf简单剪力分配法，cygj侧移刚架，fzjlfpf
    global jdjlfpf,cygj,fzjlfpf
    jdjlfpf=0
    cygj=0
    fzjlfpf=0
    #满足线位移是角位移5倍，就可定义为复杂的建立分配法
    if cy==1 and jwy==0:
        if len(elements)>=3:
            fzjlfpf=1
    #如果满足框架，且具有多层标准框架的样式，即可定义为简单的剪力分配法
    #判断条件，竖杆与横杆的个数满足数学关系
    #且每根竖杆只在自己那一层中，不会跨越层
    if kuangjia==1 and jwy==0 :
        yfanwei=[]
        for i in range(len(joints_)):
            if joints_[i]['y'] not in yfanwei:
                yfanwei.append(joints_[i]['y'])
      
        henggan=0
        shugan=0
        for i in range(len(elements)):
            if abs(elements[i]['alp'])%180==90:
                shugan=shugan+1
            if elements[i]['alp']%180==0:
                henggan=henggan+1
        if shugan-len(yfanwei)+1==henggan:
            jdjlfpf=1
            fzjlfpf=0
        yfanwei.sort()
        deltay=0
        for i in range(len(yfanwei)-1):
            if abs(yfanwei[i+1]-yfanwei[i])>deltay:
                deltay=abs(yfanwei[i+1]-yfanwei[i])
        for i in range(len(elements)):
            if abs(elements[i]['pi']['y']-elements[i]['pj']['y'])>deltay:
                jdjlfpf=0
                fzjlfpf=1
    
    
    
    if len(elements)==3 and kuangjia==1 and qgj==1:
        cygj=1
    
    #支座沉降，温度变化，存在此类荷载即是    
    global zzcj,wdbh
    zzcj=0
    wdbh=0
#    file2 = xlrd.open_workbook('excel/FIN.xlsx')
#    table2 = file2.sheet_by_index(Qnum)
    class Settlement():
        pass
    class Temperature():
        pass
    global Settlements,Temperatures
    Settlements=[]
    Temperatures=[]
    for i in range(len(calelements)):
        if len(informatrixs[6])>0:
                    if i+1 in list(informatrixs[6][0]):
                        for j in range(len(informatrixs[6])):
                            if i+1==informatrixs[6][0][j]:
                                wdbh=1
                                cy=-1
                                jwy=-1
                                Temperature_=Temperature()
                                Temperature_.t1=informatrixs[6].iloc[j,2]
                                Temperature_.t2=informatrixs[6].iloc[j,3]
                                Temperatures.append(copy.copy(Temperature_))
        if len(informatrixs[7])>0:
            if i+1 in list(informatrixs[7][0]):
                for j in range(len(informatrixs[7])):
                    if i+1==informatrixs[7][0][j]:
                        zzcj=1
                        lxl=0
                        Settlement_=Settlement()
                        Settlement.num=i
                        delta=[]
                        delta.append(informatrixs[7].iloc[j,1])
                        delta.append(informatrixs[7].iloc[j,2])
                        delta.append(informatrixs[7].iloc[j,3])
                        delta.append(informatrixs[7].iloc[j,4])
                        delta.append(informatrixs[7].iloc[j,5])
                        delta.append(informatrixs[7].iloc[j,6])
                        Settlement_.delta=delta
                        Settlements.append(copy.copy(Settlement_)) 
#    for i in range(table2.nrows):
#        for j in range(table2.ncols):
#            if table2.cell(i,j).value=='S':
#                zzcj=1
#                lxl=0
#                Settlement_=Settlement()
#                Settlement.num=i
#                delta=[]
#                delta.append(table2.cell(i,j+1).value)
#                delta.append(table2.cell(i,j+2).value)
#                delta.append(table2.cell(i,j+3).value)
#                delta.append(table2.cell(i,j+4).value)
#                delta.append(table2.cell(i,j+5).value)
#                delta.append(table2.cell(i,j+6).value)
#                Settlement_.delta=delta
#                Settlements.append(copy.copy(Settlement_))
#            if table2.cell(i,j).value=='T':
#                wdbh=1
#                cy=-1
#                jwy=-1
#                Temperature_=Temperature()
#                Temperature_.t1=table2.cell(i,j+2).value
#                Temperature_.t2=table2.cell(i,j+3).value
#                Temperatures.append(copy.copy(Temperature_))
                



#辨别对称性，不论是否对称，假想一个对称轴
#杆件都是垂直的，且ymax，ymin相同，则对称轴是两个x的平均值
def bianbiedcx():
#    file1 = xlrd.open_workbook('excel/results.xls')
#    table = file1.sheet_by_index(0)
    global dcz
    dcz=0
    for i in range(len(elements)):
        for j in range(len(elements)):
                if i!=j:
                    if abs(elements[i]['alp'])==90:
                        if abs(elements[i]['alp'])==abs(elements[j]['alp']):
                            if max(elements[i]['pi']['y'],elements[i]['pj']['y'])==max(elements[j]['pi']['y'],elements[j]['pj']['y']):
                                if min(elements[i]['pi']['y'],elements[i]['pj']['y'])==min(elements[j]['pi']['y'],elements[j]['pj']['y']):
                                    dcz=(elements[i]['pi']['x']+elements[j]['pi']['x'])/2
    global zdc,fdc
    zdc=1
    fdc=1
    #不在对称轴上的竖杆，第一步查找是否有在对称轴另一半的杆件
    #若存在，根据弯矩图确定是否有对称性
    for i in range(len(elements)):
        if abs(elements[i]['alp'])==90 and elements[i]['pi']['x']!=dcz:
            dcgj=0
            for j in range(len(elements)):
                if elements[j]['pi']['x']==(2*dcz-elements[i]['pi']['x']) and abs(elements[j]['alp'])%180!=0:
                    dcgj=1
                    M1i=abs(calelements[i]['MI'])
                    M1j=abs(calelements[i]['MJ'])
                    M2i=abs(calelements[j]['MI'])
                    M2j=abs(calelements[j]['MJ'])
#                    M1i=abs(table.cell(i+1,38).value)
#                    M1j=abs(table.cell(i+1,41).value)
#                    M2i=abs(table.cell(j+1,38).value)
#                    M2j=abs(table.cell(j+1,41).value)
                    if close(max(M1i,M1j),max(M2i,M2j))==False and close(min(M1i,M1j),min(M2i,M2j))==False:
                        zdc=0
                        fdc=0
            if dcgj==0:
                zdc=0
                fdc=0
        print('zdc=%s'%zdc)
        #看横杆，横杆两端弯矩同号且相等，为正对称，异号但绝对值相等为反对称
        if abs(elements[i]['alp'])%180==0:
            if close(a[i][0].Mi,a[i][-1].Mj)==False:
                zdc=0
            if close(a[i][0].Mi*-1,a[i][-1].Mj)==False:
                fdc=0
            if close0(a[i][0].Mi) and a[i][0].Mmid!=0:
                fdc=0
    #是否可分解为正对称和反对称两张图结合，zfjh
    #判断方式，反对称情况下，是否在有节点荷载的节点关于对称轴对称的那一点上有荷载
    #有则就是反对称，无则是正负结合
    global zfjh
    zfjh=0
    if fdc==1:
        for i in range(len(caljoints_)):
            if caljoints_[i]['Fx']!=0:
                for j in range(len(caljoints_)):
                    if close(caljoints_[j]['x'],2*dcz-caljoints_[i]['x']) and caljoints_[i]['y']==caljoints_[j]['y']:
                        if caljoints_[j]['Fx']==0:
                            zfjh=1
                        else:
                            zfjh=0
    
    
    
    print('zdc=%s'%zdc)
    print('fdc=%s'%fdc)







#改变支座，线约束
def changerestraint():
    global joints_,scxys
    for xys_ in xys:
        num=xys_.num
        alp=xys_.alp
        if joints_[num-1]['restraint']==0:
            joints_[num-1]['restraint']=1
            joints_[num-1]['salp']=alp
    for i in scxys:
        if joints_[i-1]['restraint']==1:
            joints_[i-1]['restraint']=0
        
#改变支座，线约束（计算方面的）        
def changecalrestraint():
    global caljoints_,scxys
    for xys_ in xys:
        num=xys_.num
        alp=xys_.alp
        if caljoints_[num-1]['restraint']==0:
            caljoints_[num-1]['restraint']=1
            caljoints_[num-1]['salp']=alp
    for i in scxys:
        if caljoints_[i-1]['restraint']==1:
            caljoints_[i-1]['restraint']=0


def shanchuuserM(smallest_index):
    if len(c[smallest_index])>=1:
        for i in range(len(c[smallest_index])):
            if c[smallest_index][i].ns==ps and c[smallest_index][i].ne==pe:
                del c[smallest_index][i]
            
    







#ddzt断点状态
def ddzt():
    global daduan
    daduan=1


#录入用户的作答，若对应位置已经有一个答案，先删除，再添加，最后按相对位置排序    
def changec(x):
    global c
    shanchu=0
    for i in range(len(c[x.num-1])):
        if c[x.num-1][i].ns==ps and c[x.num-1][i].ne==pe:
            deli=i
            shanchu=1
    if shanchu==1:
        del c[x.num-1][deli]
    c[x.num-1].append(x)
    for i in range(len(c[x.num-1])):
        for j in range(len(c[x.num-1])-1):
            if c[x.num-1][j].ns>c[x.num-1][j+1].ns:
                t=c[x.num-1][j]
                c[x.num-1][j]=c[x.num-1][j+1]
                c[x.num-1][j+1]=t

            
    



#画跨中荷载和节点荷载
def drawmidspan():
    global zdjh
    #所有杆件的跨中荷载放在FIN里面，每个杆件的跨中荷载放在FINE里面，FINED是具体的每一个跨中力
    global zdc,fdc,switchbjg
    FIN=[]
    if (zdc!=1 and fdc!=1) or switchbjg==0:
        for i in range(len(elements)):
            FINE=[]
            FIN.append(FINE)
        for i in range(len(informatrixs[4])):
            FINED={}
            FINED['Ftype']='F'
            FINED['F']=informatrixs[4].iloc[i,1]
            FINED['alp']=informatrixs[4].iloc[i,2]
            FINED['p']=informatrixs[4].iloc[i,3]
            FIN[int(informatrixs[4].iloc[i,0]-1)].append(FINED.copy())
        for i in range(len(informatrixs[5])):
            FINED={}
            FINED['Ftype']='Q'
            FINED['Q']=informatrixs[5].iloc[i,1]
            FINED['alp']=informatrixs[5].iloc[i,2]
            FINED['ps']=informatrixs[5].iloc[i,3]
            FINED['pe']=informatrixs[5].iloc[i,4]
            FIN[int(informatrixs[5].iloc[i,0]-1)].append(FINED.copy())
        for i in range(len(informatrixs[6])):
            FINED={}
            FINED['Ftype']='T'
            FINED['alpt']=informatrixs[6].iloc[i,1]
            FINED['t1']=informatrixs[6].iloc[i,2]
            FINED['t2']=informatrixs[6].iloc[i,3]
            FINED['h']=informatrixs[6].iloc[i,4]
            FIN[int(informatrixs[6].iloc[i,0]-1)].append(FINED.copy())
        for i in range(len(informatrixs[7])):
            FINED={}
            FINED['Ftype']='S'
            FINED['dxi']=informatrixs[7].iloc[i,1]
            FINED['dyi']=informatrixs[7].iloc[i,2]
            FINED['dalpi']=informatrixs[7].iloc[i,3]
            FINED['dxj']=informatrixs[7].iloc[i,4]
            FINED['dyj']=informatrixs[7].iloc[i,5]
            FINED['dalpj']=informatrixs[7].iloc[i,6]
            FIN[int(informatrixs[7].iloc[i,0]-1)].append(FINED.copy())
#        for i in range(table2.nrows):
#            FINE=[]
#            FINED={}
#            for j in range(table2.ncols):
#                if table2.cell(i,j).value=='F':
#                    FINED={}
#                    FINED['Ftype']='F'
#                    FINED['F']=table2.cell(i,j+1).value
#                    FINED['alp']=table2.cell(i,j+2).value
#                    FINED['p']=table2.cell(i,j+3).value
#                    FINE.append(FINED.copy())
#                if table2.cell(i,j).value=='Q'
#                    FINED={}
#                    FINED['Ftype']='Q'
#                    FINED['Q']=table2.cell(i,j+1).value
#                    FINED['alp']=table2.cell(i,j+2).value
#                    FINED['ps']=table2.cell(i,j+3).value
#                    FINED['pe']=table2.cell(i,j+4).value
#                    FINE.append(FINED.copy())
#                if table2.cell(i,j).value=='S':
#                    FINED={}
#                    FINED['Ftype']='S'
#                    FINED['dxi']=table2.cell(i,j+1).value
#                    FINED['dyi']=table2.cell(i,j+2).value
#                    FINED['dalpi']=table2.cell(i,j+3).value
#                    FINED['dxj']=table2.cell(i,j+4).value
#                    FINED['dyj']=table2.cell(i,j+5).value
#                    FINED['dalpj']=table2.cell(i,j+6).value
#                    FINE.append(FINED.copy())
#                if table2.cell(i,j).value=='T':
#                    FINED={}
#                    FINED['Ftype']='T'
#                    FINED['alpt']=table2.cell(i,j+1).value
#                    FINED['t1']=table2.cell(i,j+2).value
#                    FINED['t2']=table2.cell(i,j+3).value
#                    FINED['h']=table2.cell(i,j+4).value
#                    FINE.append(FINED.copy())
#            FIN.append(FINE)
#        for i in range(table2.nrows+1,table.nrows):
#            FINE=[]
#            FIN.append(FINE)
        numT=1
        for i in range(len(elements)):
            xi=elements[i]['pi']['x']
            yi=elements[i]['pi']['y']
            xj=elements[i]['pj']['x']
            yj=elements[i]['pj']['y']
            for j in range(len(FIN[i])):
                if FIN[i][j]['Ftype']=='F':
                    alpz=(elements[i]['alp']+FIN[i][j]['alp'])/180*3.14159
                    sin=np.sin(alpz)
                    cos=np.cos(alpz)
                    xif=xi+FIN[i][j]['p']*(xj-xi)
                    yif=yi+FIN[i][j]['p']*(yj-yi)
                    #画出带箭头的直线用annotate
                    plt.annotate('',xytext=(xif,yif),xy=(xif+5*s*cos,yif+5*s*sin),
                                 arrowprops=dict(facecolor='black',width=3,headwidth=18,frac=0.2))
                    plt.scatter(x=xif+5*s*cos,y=yif+5*s*sin,edgecolor='',color='')
                    plt.text(xif+5*s*cos+0.015,yif+5*s*sin+0.015,'F'+'='+str(FIN[i][j]['F']),fontsize=35)
                if FIN[i][j]['Ftype']=='Q':
                    alpz=(elements[i]['alp']+FIN[i][j]['alp'])/180*3.14159
                    sin=np.sin(alpz)
                    cos=np.cos(alpz)
                    ps=FIN[i][j]['ps']
                    pe=FIN[i][j]['pe']
                    plt.plot([xi+ps*(xj-xi)+2*s*cos,xi+pe*(xj-xi)+2*s*cos],
                             [yi+ps*(yj-yi)+2*s*sin,yi+pe*(yj-yi)+2*s*sin],'k--')
                    pmid=ps+(pe-ps)*0.4
                    while(ps+0.05<=pe+0.01):
                        xif=xi+ps*(xj-xi)
                        yif=yi+ps*(yj-yi)
                        plt.annotate('',xytext=(xif,yif),xy=(xif+2*s*cos,yif+2*s*sin),
                                 arrowprops=dict(facecolor='black',width=3,headwidth=12))
                        ps=ps+0.05
                    xif=xi+pmid*(xj-xi)
                    yif=yi+pmid*(yj-yi)
                    plt.text(xif+3.5*s*cos,yif+3.5*s*sin,'Q'+'='+str(FIN[i][j]['Q']),fontsize=35)
                    plt.scatter(x=xif+3.5*s*cos,y=yif+3.5*s*sin,edgecolor='',color='')
                if FIN[i][j]['Ftype']=='S':
                    alp=elements[i]['alp']/180*3.14159
                    sin=np.sin(alp)
                    cos=np.cos(alp)
                    dxi=FIN[i][j]['dxi']
                    dyi=FIN[i][j]['dyi']
                    dalpi=np.round(FIN[i][j]['dalpi'],2)
                    dxj=FIN[i][j]['dxj']
                    dyj=FIN[i][j]['dyj']
                    dalpj=np.round(FIN[i][j]['dalpj'],2)
                    if dxi!=0 or dyi!=0 or dalpi!=0:
                        if dxi!=0:
                            plt.annotate(r'$settlement:\Delta x=%s$'%(dxi),
                                     xy=(xi,yi),xytext=(xi-2*s*cos+3*s*sin,yi-2*s*sin-3*s*cos),fontsize=35,
                                     color='b',weight='bold',
                                     bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='k', lw=1,alpha=0.7))
                        elif dyi!=0:
                            plt.annotate(r'$settlement:\Delta y=%s$'%(dyi),
                                     xy=(xi,yi),xytext=(xi-2*s*cos+3*s*sin,yi-2*s*sin-3*s*cos),fontsize=35,
                                     color='b',weight='bold',
                                     bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='k', lw=1,alpha=0.7))
                        elif dalpi!=0:
                            plt.annotate(r'$settlement:\Delta \theta =%s$'%(dalpi),
                                     xy=(xi,yi),xytext=(xi-2*s*cos+3*s*sin,yi-2*s*sin-3*s*cos),fontsize=35,
                                     color='b',weight='bold',
                                     bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='k', lw=1,alpha=0.7))
                        else:
                            plt.annotate(r'$settlement:\Delta x=%s,\Delta y=%s,\Delta \theta =%s$'%(dxi,dyi,dalpi),
                                         xy=(xi,yi),xytext=(xi-2*s*cos+3*s*sin,yi-2*s*sin-3*s*cos),fontsize=35,
                                         color='b',weight='bold',
                                         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='k', lw=1,alpha=0.7))
                            plt.scatter(xi-5*s*cos+5*s*sin,yi-5*s*sin-5*s*cos,c='',edgecolor='')
                    if dxj!=0 or  dyj!=0 or dalpj!=0:
                        if dxj!=0:
                            plt.annotate(r'$settlement:\Delta x=%s$'%(dxj),
                                     xy=(xj,yj),xytext=(xj+2*s*cos+3*s*sin,yj+2*s*sin-3*s*cos),fontsize=35,
                                     color='b',weight='bold',
                                     bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='k', lw=1,alpha=0.7))
                        elif dyj!=0:
                            plt.annotate(r'$settlement:\Delta y=%s$'%(dyj),
                                     xy=(xj,yj),xytext=(xj+2*s*cos+3*s*sin,yj+2*s*sin-3*s*cos),fontsize=35,
                                     color='b',weight='bold',
                                     bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='k', lw=1,alpha=0.7))
                        elif dalpj!=0:
                            plt.annotate(r'$settlement:\Delta \theta=%s$'%(dalpj),
                                     xy=(xj,yj),xytext=(xj+2*s*cos+3*s*sin,yj+2*s*sin-3*s*cos),fontsize=35,
                                     color='b',weight='bold',
                                     bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='k', lw=1,alpha=0.7))
                        else:
                            plt.annotate(r'$settlement:\Delta x=%s,\Delta y=%s,\Delta \theta =%s$'%(dxj,dyj,dalpj),
                                         xy=(xj,yj),xytext=(xj+2*s*cos+3*s*sin,yj+2*s*sin-3*s*cos),fontsize=35,
                                         color='b',weight='bold',
                                         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='k', lw=1,alpha=0.7))
                            plt.scatter(xj+5*s*cos+5*s*sin,yj+5*s*sin-5*s*cos,c='',edgecolor='')
                if FIN[i][j]['Ftype']=='T':
                    alp=elements[i]['alp']/180*3.14159
                    sin=np.sin(alp)
                    cos=np.cos(alp)
                    alpt=FIN[i][j]['alpt']
                    h=FIN[i][j]['h']
                    t1=FIN[i][j]['t1']
                    t2=FIN[i][j]['t2']
                    xmid=(xi+xj)/2
                    ymid=(yi+yj)/2
                    if t1<=0:
                        plt.annotate(r'$%s$'%t1+r'$^\circ$C',xy=(xmid,ymid),
                                     xytext=(xmid-2.5*s*sin,ymid+2.5*s*cos),color='b',weight='bold',
                                     fontsize=35)
                    if t1>0:
                        plt.annotate(r'$%s$'%t1+r'$^\circ$C',xy=(xmid,ymid),
                                     xytext=(xmid-2.5*s*sin,ymid+2.5*s*cos),color='r',weight='bold',
                                     fontsize=35)
                    plt.scatter(xmid-2.5*s*sin,ymid+2.5*s*cos,c='',edgecolor='')
                    if t2<=0:
                        plt.annotate(r'$%s$'%t2+r'$^\circ$C',xy=(xmid,ymid),
                                     xytext=(xmid+2.5*s*sin,ymid-2.5*s*cos),color='b',weight='bold',
                                     fontsize=35)
                    if t2>0:
                        plt.annotate(r'$%s$'%t2+r'$^\circ$C',xy=(xmid,ymid),
                                     xytext=(xmid+2.5*s*sin,ymid-2.5*s*cos),color='r',weight='bold',
                                     fontsize=35)
                    plt.scatter(xmid+2.5*s*sin,ymid-2.5*s*cos,c='',edgecolor='')
                    if numT>0:
                        plt.annotate(r'$ \alpha t=%s,h=%s$'%(alpt,h),xy=(xi,yi),xytext=(xi+2*s*sin+s*cos,yi-2*s*cos+s*sin),
                                     fontsize=35,color='b',weight='bold',
                                     bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='k', lw=1,alpha=0.7))
                        numT=numT-1
        for i in range(len(elements)):
            xi=elements[i]['pi']['x']
            yi=elements[i]['pi']['y']
            xj=elements[i]['pj']['x']
            yj=elements[i]['pj']['y']
            if len(informatrixs[3])>0:
                if elements[i]['pi']['num'] in list(informatrixs[3][0]):
                    for j in range(len(informatrixs[3])):
                        if informatrixs[3][0][j]==elements[i]['pi']['num'] and informatrixs[3][1][j]>0:
                            plt.annotate('',xytext=(xi,yi),xy=(xi+5*s,yi),
                                             arrowprops=dict(facecolor='red',width=3,headwidth=18))
                            plt.text(xi+5*s,yi+r,'FX'+'='+str(informatrixs[3][1][j]),fontsize=35)
                            plt.scatter(xi+5*s,yi+r,c='',edgecolor='')
                        if informatrixs[3][0][j]==elements[i]['pi']['num'] and informatrixs[3][1][j]<0:
                            plt.annotate('',xytext=(xi,yi),xy=(xi-5*s,yi),
                                     arrowprops=dict(facecolor='red',width=3,headwidth=18))
                            plt.text(xi-5*s,yi+r,'FX'+'='+str(abs(informatrixs[3][1][j])),fontsize=35)
                            plt.scatter(xi-5*s,yi+r,c='',edgecolor='')
                        if informatrixs[3][0][j]==elements[i]['pi']['num'] and informatrixs[3][2][j]>0:
                            plt.annotate('',xytext=(xi,yi),xy=(xi,yi+5*s),
                                     arrowprops=dict(facecolor='red',width=3,headwidth=18))
                            plt.text(xi+r,yi+5*s,'FY'+'='+str(informatrixs[3][2][j]),fontsize=35)
                            plt.scatter(xi+r+s,yi+5*s,c='',edgecolor='')
                        if informatrixs[3][0][j]==elements[i]['pi']['num'] and informatrixs[3][2][j]<0:
                            plt.annotate('',xytext=(xi,yi),xy=(xi,yi-5*s),
                                     arrowprops=dict(facecolor='red',width=3,headwidth=18))
                            plt.text(xi+r,yi-5*s,'FY'+'='+str(abs(informatrixs[3][2][j])),fontsize=35)
                            plt.scatter(xi+r+s,yi-5*s,c='',edgecolor='')
                        if informatrixs[3][0][j]==elements[i]['pi']['num'] and informatrixs[3][3][j]>0:
#                           plt.annotate('',xytext=(xi+0.15,yi+0.15),xy=(xi-0.1,yi-0.1),
#                                     arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.5'),fontsize=75,bbox=dict(lw=4))
#                           plt.text(xi+0.1,yi+0.1,'M'+'='+str(informatrixs[3][3][j]),fontsize=35)
                            plt.annotate('',xytext=(xi+2*s,yi+2*s),xy=(xi-2*s,yi-2*s),
                                     arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.5'),fontsize=75,bbox=dict(lw=4))
                            plt.text(xi+2*r,yi+2*r,'M'+'='+str(informatrixs[3][3][j]),fontsize=35)
                            plt.plot([xi,xi-2*s],[yi,yi-2*s],'k--')
                            
                        if informatrixs[3][0][j]==elements[i]['pi']['num'] and informatrixs[3][3][j]<0:
#                            plt.annotate('',xytext=(xi+0.15,yi+0.15),xy=(xi-0.1,yi-0.1),
#                                     arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-0.5'),fontsize=75,bbox=dict(lw=4))
#                            plt.text(xi+0.1,yi+0.1,'M'+'='+str(abs(informatrixs[3][3][j])),fontsize=35)
#                            plt.plot([xi,xi-0.1],[yi,yi-0.1],'k--')
                            plt.annotate('',xytext=(xi+2*s,yi+2*s),xy=(xi-2*s,yi-2*s),
                                     arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-0.5'),fontsize=75,bbox=dict(lw=4))
                            plt.text(xi+2*r,yi+2*r,'M'+'='+str(abs(informatrixs[3][3][j])),fontsize=35)
                            plt.plot([xi,xi-2*s],[yi,yi-2*s],'k--')
                            
                if elements[i]['pj']['num'] in list(informatrixs[3][0]):
                    for j in range(len(informatrixs[3])):
                        if informatrixs[3][0][j]==elements[i]['pj']['num'] and informatrixs[3][1][j]>0:
                            plt.annotate('',xytext=(xj,yj),xy=(xj+5*s,yj),
                                             arrowprops=dict(facecolor='red',width=3,headwidth=18))
                            plt.text(xj+5*s,yj+r,'FX'+'='+str(informatrixs[3][1][j]),fontsize=35)
                            plt.scatter(xj+5*s,yj+r,c='',edgecolor='')
                        if informatrixs[3][0][j]==elements[i]['pj']['num'] and informatrixs[3][1][j]<0:
                            plt.annotate('',xytext=(xj,yj),xy=(xj-5*s,yj),
                                     arrowprops=dict(facecolor='red',width=3,headwidth=18))
                            plt.text(xj-5*s,yj+r,'FX'+'='+str(abs(informatrixs[3][1][j])),fontsize=35)
                            plt.scatter(xj-5*s,yj+r,c='',edgecolor='')
                        if informatrixs[3][0][j]==elements[i]['pj']['num'] and informatrixs[3][2][j]>0:
                            plt.annotate('',xytext=(xj,yj),xy=(xj,yj+5*s),
                                     arrowprops=dict(facecolor='red',width=3,headwidth=18))
                            plt.text(xj+r,yj+5*s,'FY'+'='+str(informatrixs[3][2][j]),fontsize=35)
                            plt.scatter(xj+r+s,yj+5*s,c='',edgecolor='')
                        if informatrixs[3][0][j]==elements[i]['pj']['num'] and informatrixs[3][2][j]<0:
                            plt.annotate('',xytext=(xj,yj),xy=(xj,yj-5*s),
                                     arrowprops=dict(facecolor='red',width=3,headwidth=18))
                            plt.text(xj+r,yj-5*s,'FY'+'='+str(abs(informatrixs[3][2][j])),fontsize=35)
                            plt.scatter(xj+r+s,yj-5*s,c='',edgecolor='')
                        if informatrixs[3][0][j]==elements[i]['pj']['num'] and informatrixs[3][3][j]>0:
#                           plt.annotate('',xytext=(xj+0.15,yj+0.15),xy=(xj-0.1,yj-0.1),
#                                     arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.5'),fontsize=75,bbox=dict(lw=4))
#                           plt.text(xj+0.1,yj+0.1,'M'+'='+str(informatrixs[3][3][j]),fontsize=35)
#                           plt.plot([xj,xj-0.1],[yj,yj-0.1],'k--') 
                           
                           plt.annotate('',xytext=(xj+2*s,yj+2*s),xy=(xj-2*s,yj-2*s),
                                     arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.5'),fontsize=75,bbox=dict(lw=4))
                           plt.text(xj+2*r,yj+2*r,'M'+'='+str(informatrixs[3][3][j]),fontsize=35)
                           plt.plot([xj,xj-2*s],[yj,yj-2*s],'k--') 
                           
                        if informatrixs[3][0][j]==elements[i]['pj']['num'] and informatrixs[3][3][j]<0:
#                            plt.annotate('',xytext=(xj+0.15,yj+0.15),xy=(xj-0.1,yj-0.1),
#                                     arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-0.5'),fontsize=75,bbox=dict(lw=4))
#                            plt.text(xj+0.1,yj+0.1,'M'+'='+str(abs(informatrixs[3][3][j])),fontsize=35)
#                            plt.plot([xj,xj-0.1],[yj,yj-0.1],'k--')
                            
                            plt.annotate('',xytext=(xj+2*s,yj+2*s),xy=(xj-2*s,yj-2*s),
                                     arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-0.5'),fontsize=75,bbox=dict(lw=4))
                            plt.text(xj+2*r,yj+2*r,'M'+'='+str(abs(informatrixs[3][3][j])),fontsize=35)
                            plt.plot([xj,xj-2*s],[yj,yj-2*s],'k--') 
                            
                
            
            
#            if table.cell(i+1,18).value>0:
#                plt.annotate('',xytext=(xi,yi),xy=(xi,yi+5*s),
#                                 arrowprops=dict(facecolor='red',width=3,headwidth=18))
#                plt.text(xi+r,yi+5*s,'FY'+'='+str(table.cell(i+1,18).value),fontsize=35)
#                plt.scatter(xi+r+s,yi+5*s,c='',edgecolor='')
#            if table.cell(i+1,19).value>0:
#                plt.annotate('',xytext=(xi+0.15,yi+0.15),xy=(xi-0.1,yi-0.1),
#                                 arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.5'),fontsize=75,bbox=dict(lw=4))
#                plt.text(xi+0.1,yi+0.1,'M'+'='+str(table.cell(i+1,19).value),fontsize=35)
#                plt.plot([xi,xi-0.1],[yi,yi-0.1],'k--')
#            if table.cell(i+1,17).value<0:
#                plt.annotate('',xytext=(xi,yi),xy=(xi-5*s,yi),
#                                 arrowprops=dict(facecolor='red',width=3,headwidth=18))
#                plt.text(xi-5*s,yi+r,'FX'+'='+str(abs(table.cell(i+1,17).value)),fontsize=35)
#                plt.scatter(xi-5*s,yi+r,c='',edgecolor='')
#            if table.cell(i+1,18).value<0:
#                plt.annotate('',xytext=(xi,yi),xy=(xi,yi-5*s),
#                                 arrowprops=dict(facecolor='red',width=3,headwidth=18))
#                plt.text(xi+r,yi-5*s,'FY'+'='+str(abs(table.cell(i+1,18).value)),fontsize=35)
#                plt.scatter(xi+r+s,yi-5*s,c='',edgecolor='')
#            if table.cell(i+1,19).value<0:
#                plt.annotate('',xytext=(xi+0.15,yi+0.15),xy=(xi-0.1,yi-0.1),
#                                 arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-0.5'),fontsize=75,bbox=dict(lw=4))
#                plt.text(xi+0.1,yi+0.1,'M'+'='+str(abs(table.cell(i+1,19).value)),fontsize=35)
#                plt.plot([xi,xi-0.1],[yi,yi-0.1],'k--')
#            if table.cell(i+1,20).value>0:
#                plt.annotate('',xytext=(xj,yj),xy=(xj+5*s,yj),
#                                 arrowprops=dict(facecolor='red',width=3,headwidth=18))
#                plt.text(xj+5*s,yj+r,'FX'+'='+str(table.cell(i+1,20).value),fontsize=35)
#                plt.scatter(xj+5*s,yj+r,c='',edgecolor='')
#            if table.cell(i+1,21).value>0:
#                plt.annotate('',xytext=(xj,yj),xy=(xj,yj+5*s),
#                                 arrowprops=dict(facecolor='red',width=3,headwidth=18))
#                plt.text(xj+r,yj+5*s,'FY'+'='+str(table.cell(i+1,21).value),fontsize=35)
#                plt.scatter(xj+r+s,yj+5*s,c='',edgecolor='')
#            if table.cell(i+1,22).value>0:
#                plt.annotate('',xytext=(xj+0.15,yj+0.15),xy=(xj-0.1,yj-0.1),
#                                 arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.5'),fontsize=75,bbox=dict(lw=4))
#                plt.text(xj+0.1,yj+0.1,'M'+'='+str(table.cell(i+1,22).value),fontsize=35)
#                plt.plot([xj,xj-0.1],[yj,yj-0.1],'k--')
#            if table.cell(i+1,20).value<0:
#                plt.annotate('',xytext=(xj,yj),xy=(xj-5*s,yj),
#                                 arrowprops=dict(facecolor='red',width=3,headwidth=18))
#                plt.text(xj-5*s,yj+r,'FX'+'='+str(abs(table.cell(i+1,20).value)),fontsize=35)
#                plt.scatter(xj-5*s,yj+r,c='',edgecolor='')
#            if table.cell(i+1,21).value<0:
#                plt.annotate('',xytext=(xj,yj),xy=(xj,yj-5*s),
#                                 arrowprops=dict(facecolor='red',width=3,headwidth=18))
#                plt.text(xj+r,yj-5*s,'FY'+'='+str(abs(table.cell(i+1,21).value)),fontsize=35)
#                plt.scatter(xj+r+s,yj-5*s,c='',edgecolor='')
#            if table.cell(i+1,22).value<0:
#                plt.annotate('',xytext=(xj+0.15,yj+0.15),xy=(xj-0.1,yj-0.1),
#                                 arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-0.5'),fontsize=75,bbox=dict(lw=4))
#                plt.text(xj+0.1,yj+0.1,'M'+'='+str(abs(table.cell(i+1,22).value)),fontsize=35)
#                plt.plot([xj,xj-0.1],[yj,yj-0.1],'k--')
        


#用颜色显示刚度，先确定有多少种刚度，用颜色表示的最多3种，最小的是绿色，第二大的是蓝色
#若刚度为-1则为红色
def drawEAI():
    global s,r
    EAIlist=[]
    for i in range(len(calelements)):
        if calelements[i]['EI'] not in EAIlist:
            EAIlist.append(calelements[i]['EI'])
    EAIlist.sort()
    print(EAIlist)
    color=['green','blue','red']
    for i in range(len(calelements)):
        xi=calelements[i]['pi']['x']
        yi=calelements[i]['pi']['y']
        xj=calelements[i]['pj']['x']
        yj=calelements[i]['pj']['y']
        cos=np.cos(calelements[i]['alp']/180*3.14159)
        sin=np.sin(calelements[i]['alp']/180*3.14159)
        if calelements[i]['EI']==EAIlist[0] and calelements[i]['EI']<=1e6 :
            if calelements[i]['pi']['connection']==0 and calelements[i]['pj']['connection']==0:
                h1,=plt.plot([xi+2*r*cos,xj-2*r*cos],[yi+2*r*sin,yj-2*r*sin],color=color[0],linestyle='--',linewidth=8,label='EI=%d'%EAIlist[0])
            elif calelements[i]['pi']['connection']==0 and calelements[i]['pj']['connection']!=0:
                h1,=plt.plot([xi+2*r*cos,xj],[yi+2*r*sin,yj],color=color[0],linestyle='--',linewidth=8,label='EI=%d'%EAIlist[0])
            elif calelements[i]['pi']['connection']!=0 and calelements[i]['pj']['connection']==0:
                h1,=plt.plot([xi,xj-2*r*cos],[yi,yj-2*r*sin],color=color[0],linestyle='--',linewidth=8,label='EI=%d'%EAIlist[0])
            else:
                h1,=plt.plot([xi,xj],[yi,yj],color=color[0],linestyle='--',linewidth=8,label='EI=%d'%EAIlist[0])
        if len(EAIlist)>1:
            if calelements[i]['EI']==EAIlist[1] and calelements[i]['EI']<=1e6:
                if calelements[i]['pi']['connection']==0 and calelements[i]['pj']['connection']==0:
                    h2,=plt.plot([xi+2*r*cos,xj-2*r*cos],[yi+2*r*sin,yj-2*r*sin],color=color[1],linestyle='--',linewidth=8,label='EI=%d'%EAIlist[1])
                elif calelements[i]['pi']['connection']==0 and calelements[i]['pj']['connection']!=0:
                    h2,=plt.plot([xi+2*r*cos,xj],[yi+2*r*sin,yj],color=color[1],linestyle='--',linewidth=8,label='EI=%d'%EAIlist[1])
                elif calelements[i]['pi']['connection']!=0 and calelements[i]['pj']['connection']==0:
                    h2,=plt.plot([xi,xj-2*r*cos],[yi,yj-2*r*sin],color=color[1],linestyle='--',linewidth=8,label='EI=%d'%EAIlist[1])
                else:
                    h2,=plt.plot([xi,xj],[yi,yj],color=color[1],linestyle='--',linewidth=8,label='EI=%d'%EAIlist[1])
#                h2,=plt.plot([xi,xj],[yi,yj],color=color[1],linestyle='--',linewidth=8,label='EI=%d'%EAIlist[1])
            if calelements[i]['EI']==EAIlist[-1] and calelements[i]['EI']>=1e6:
                if calelements[i]['pi']['connection']==0 and calelements[i]['pj']['connection']==0:
                    h3,=plt.plot([xi+2*r*cos,xj-2*r*cos],[yi+2*r*sin,yj-2*r*sin],color=color[-1],linestyle='--',linewidth=8,label='EI=%d'%-1)
                elif calelements[i]['pi']['connection']==0 and calelements[i]['pj']['connection']!=0:
                    h3,=plt.plot([xi+2*r*cos,xj],[yi+2*r*sin,yj],color=color[-1],linestyle='--',linewidth=8,label='EI=%d'%-1)
                elif calelements[i]['pi']['connection']!=0 and calelements[i]['pj']['connection']==0:
                    h3,=plt.plot([xi,xj-2*r*cos],[yi,yj-2*r*sin],color=color[-1],linestyle='--',linewidth=8,label='EI=%d'%-1)
                else:
                    h3,=plt.plot([xi,xj],[yi,yj],color=color[-1],linestyle='--',linewidth=8,label='EI=%d'%-1)
            #            h3,=plt.plot([xi,xj],[yi,yj],color=color[-1],linestyle='--',linewidth=8,label='EI=%d'%-1)
    if len(EAIlist)==1:
        if EAIlist[0]>=1e6:
            plt.legend(handles=[h3,],loc='best',fontsize=50)
        else:
            plt.legend(handles=[h1,],loc='best',fontsize=50)
    elif len(EAIlist)==2:
        if EAIlist[-1]>=1e6:
            plt.legend(handles=[h1,h3,],loc='best',fontsize=50)
        else:
            plt.legend(handles=[h1,h2,],loc='best',fontsize=50)
    else:
        if EAIlist[-1]>=1e6:
           plt.legend(handles=[h1,h2,h3,],loc='best',fontsize=50) 
        else:
            plt.legend(handles=[h1,h2],loc='best',fontsize=50) 


#画题目
def drawquestion():
    sortinformatrixs()
    plt.figure(figsize=(32,20))
    fileinelements()
    drawjoints()
    drawelements()
    drawannotation()
    drawmidspan()
    drawjys()
#    print(switchEAI)
    print(switchEAI)
    if switchEAI==1:
        try:
            drawEAI()
        except:
            pass
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/question.png',bbox_inches='tight',pad_inches=0, )
    plt.close()

def drawrestraintquestion():
    plt.figure(figsize=(32,20))
    drawjoints()
    drawelements()
    drawannotation()
    drawmidspan()
    drawjys()
#    print(switchEAI)
    print(switchEAI)
    if switchEAI==1:
        try:
            drawEAI()
        except:
            pass
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/question.png',bbox_inches='tight',pad_inches=0, )
    plt.close()
    






def drawjoints():
    global r
    print('len(joints_)='+str(len(joints_)))
    if len(informatrixs[0])==0:
        return
    
    for i in range(len(joints_)):
        independency=1
        for j in range(len(elements)):
            if elements[j]['pi']['num']==joints_[i]['num']or elements[j]['pj']['num']==joints_[i]['num']:
                independency=0
        if independency==1:
                plt.scatter(x=joints_[i]['x'],y=joints_[i]['y'],color='black',s=250)
                plt.text(joints_[i]['x'],joints_[i]['y'],int(joints_[i]['num']),fontsize=35,c='b',family='fantasy')








#画杆件
def drawelements():    
    #r和s控制铰接点的支座的大小
    #下面三行是画圆的代码，参数方程
    theta = np.arange(0, 2*np.pi, 0.01)
    #x = 1 + r * np.cos(theta)
    #y = 1 + r * np.sin(theta)
    for i in range(len(joints_)):
        joints_[i]['esupportdraw']=True
        joints_[i]['supportdraw']=True
    for i in range(len(elements)):
        #简化表达式
        xi=elements[i]['pi']['x']
        yi=elements[i]['pi']['y']
        xj=elements[i]['pj']['x']
        yj=elements[i]['pj']['y']
        #杆件的角度，t代表了临时temporary
        talp=elements[i]['alp']/180*3.14159
        sin=np.sin(talp)
        cos=np.cos(talp)
        #0铰接，1刚接，由于杆件要一次画出来，所以i端和j端需要同时考虑
        if elements[i]['pi']['connection']==0 and elements[i]['pj']['connection']==0:
            #ni，nj记录铰接点是否有多根杆件相连
            ni=0
            nj=0
            #一个循环，用来检查铰接点有没有多根杆件相连
            for jt in range(len(joints_)):
                     if math.isclose(joints_[jt]['x'], elements[i]['pi']['x'], abs_tol=1e-5):
                         if math.isclose(joints_[jt]['y'], elements[i]['pi']['y'], abs_tol=1e-5):
                             if joints_[jt]['connection']==0:
                                 ni=ni+1
            for jt in range(len(joints_)):
                     if math.isclose(joints_[jt]['x'], elements[i]['pj']['x'], abs_tol=1e-5):
                         if math.isclose(joints_[jt]['y'], elements[i]['pj']['y'], abs_tol=1e-5):
                             if joints_[jt]['connection']==0:
                                 nj=nj+1
            #必会与自身重复所以减去1
            ni=ni-1
            nj=nj-1
            #ni=0意味这个铰接点只有1根杆件，ni！=0意味着这个铰接点有很多杆件，由于这两个的不同，画法也不同
            #ni=0铰接点的圆与其他杆件相切（铰接点的圆的直径与缩短后的杆件长度总和为原杆件长）
            #ni！=0，铰接点不和任何杆件相切，杆件缩短（铰接点的圆与杆件缩短后的长度为原杆件长加上一个半径的长度）
            #nj与ni同理
            #画圆时指定圆心x坐标和y坐标，半径有最上面的r控制
            #由于铰接点实际是有区别的需要加一个参数ht（hinge type）ht=1意思是这是一个由多个杆件相连的铰接点
            #ht=0意思是这是一个只有一根杆件相连的铰接点
            #后面的代码没有很强的逻辑，就是不停的分析各种的情况，代码都是画图的代码
            if ni!=0 and nj!=0:
                plt.plot([xi+r*cos,xj-r*cos],[yi+r*sin,yj-r*sin],'k',linewidth=4)
                x = xi + r * np.cos(theta)
                y = yi + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                x = xj + r * np.cos(theta)
                y = yj + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                elements[i]['pi']['ht']=1
                elements[i]['pj']['ht']=1
                elements[i]['pi']['xc']=xi
                elements[i]['pi']['yc']=yi
                elements[i]['pj']['xc']=xj
                elements[i]['pj']['yc']=yj
            if ni==0 and nj!=0:
                plt.plot([xi+2*r*cos,xj-r*cos],[yi+2*r*sin,yj-r*sin],'k',linewidth=4)
                x=xi+r*cos+r*np.cos(theta)
                y=yi+r*sin+r*np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                x = xj + r * np.cos(theta)
                y = yj + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                elements[i]['pi']['ht']=0
                elements[i]['pj']['ht']=1
                elements[i]['pi']['xc']=xi+r*cos
                elements[i]['pi']['yc']=yi+r*sin
                elements[i]['pj']['xc']=xj
                elements[i]['pj']['yc']=yj
            if ni==0 and nj==0:
                plt.plot([xi+2*r*cos,xj-2*r*cos],[yi+2*r*sin,yj-2*r*sin],'k',linewidth=4)
                x=xi+r*cos+r*np.cos(theta)
                y=yi+r*sin+r*np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                x=xj-r*cos+r*np.cos(theta)
                y=yj-r*sin+r*np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                elements[i]['pi']['ht']=0
                elements[i]['pj']['ht']=0
                elements[i]['pi']['xc']=xi+r*cos
                elements[i]['pi']['yc']=yi+r*sin
                elements[i]['pj']['xc']=xj-r*cos
                elements[i]['pj']['yc']=yj-r*sin
                
            if ni!=0 and nj==0:
                plt.plot([xi+r*cos,xj-2*r*cos],[yi+r*sin,yj-2*r*sin],'k',linewidth=4)
                x = xi + r * np.cos(theta)
                y = yi + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                x=xj-r*cos+r*np.cos(theta)
                y=yj-r*sin+r*np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                elements[i]['pi']['ht']=1
                elements[i]['pj']['ht']=0
                elements[i]['pi']['xc']=xi
                elements[i]['pi']['yc']=yi
                elements[i]['pj']['xc']=xj-r*cos
                elements[i]['pj']['yc']=yj-r*sin
        if elements[i]['pi']['connection']==0 and elements[i]['pj']['connection']==1:
            ni=0
            for jt in range(len(joints_)):
                     if math.isclose(joints_[jt]['x'], elements[i]['pi']['x'], rel_tol=1e-5):
                         if math.isclose(joints_[jt]['y'], elements[i]['pi']['y'], rel_tol=1e-5):
                             if joints_[jt]['connection']==0:
                                 ni=ni+1
            ni=ni-1
            if ni!=0:
                plt.plot([xi+r*cos,xj],[yi+r*sin,yj],'k',linewidth=4)
                x = xi + r * np.cos(theta)
                y = yi + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                elements[i]['pi']['ht']=1
                elements[i]['pi']['xc']=xi
                elements[i]['pi']['yc']=yi
                elements[i]['pj']['xc']=xj
                elements[i]['pj']['yc']=yj
            if ni==0:
                plt.plot([xi+2*r*cos,xj],[yi+2*r*sin,yj],'k',linewidth=4)
                x=xi+r*cos+r*np.cos(theta)
                y=yi+r*sin+r*np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                elements[i]['pi']['ht']=0
                elements[i]['pi']['xc']=xi+r*cos
                elements[i]['pi']['yc']=yi+r*sin
                elements[i]['pj']['xc']=xj
                elements[i]['pj']['yc']=yj
        if elements[i]['pi']['connection']==1 and elements[i]['pj']['connection']==0:
            nj=0
            for jt in range(len(joints_)):
                     if math.isclose(joints_[jt]['x'], elements[i]['pj']['x'], rel_tol=1e-5):
                         if math.isclose(joints_[jt]['y'], elements[i]['pj']['y'], rel_tol=1e-5):
                             if joints_[jt]['connection']==0:
                                 nj=nj+1
            nj=nj-1
            if nj!=0:
                plt.plot([xi,xj-r*cos],[yi,yj-r*sin],'k',linewidth=4)
                x = xj + r * np.cos(theta)
                y = yj + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                elements[i]['pj']['ht']=1
                elements[i]['pi']['xc']=xi
                elements[i]['pi']['yc']=yi
                elements[i]['pj']['xc']=xj
                elements[i]['pj']['yc']=yj
            if nj==0:
                plt.plot([xi,xj-2*r*cos],[yi,yj-2*r*sin],'k',linewidth=4)
                x = xj -r*cos + r * np.cos(theta)
                y = yj -r*sin + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                elements[i]['pj']['ht']=0
                elements[i]['pi']['xc']=xi
                elements[i]['pi']['yc']=yi
                elements[i]['pj']['xc']=xj-r*cos
                elements[i]['pj']['yc']=yj-r*sin
        if elements[i]['pi']['connection']==1 and elements[i]['pj']['connection']==1:   
            plt.plot([xi,xj],[yi,yj],'k',linewidth=4)
    
    
    
    def drawrestraint1(x,y,alp):
        alp=alp/180*3.1415
        sin=np.sin(alp)
        cos=np.cos(alp)
    #    sin_90=-cos
    #    cos_90=sin
        xc=x+r*np.cos(theta)
        yc=y+r*np.sin(theta)
        plt.plot(xc,yc,'r',linewidth=3)
        x1_=x
        y1_=y
        x1_=x1_+r*sin
        y1_=y1_-r*cos
        x2_=x
        y2_=y
        x2_=x2_+(r+s)*sin
        y2_=y2_-(r+s)*cos
        plt.plot([x1_,x2_],[y1_,y2_],'k',linewidth=4)
        xc=x+(2*r+s)*sin+r*np.cos(theta)
        yc=y-(2*r+s)*cos+r*np.sin(theta)
        plt.plot(xc,yc,'r',linewidth=3)
        x1_=x+(2*r+s)*sin-3*r*cos
        y1_=y-(2*r+s)*cos-3*r*sin
        x2_=x+(2*r+s)*sin-r*cos
        y2_=y-(2*r+s)*cos-r*sin
        plt.plot([x1_,x2_],[y1_,y2_],'k',linewidth=4)
        x1_=x+(2*r+s)*sin+3*r*cos
        y1_=y-(2*r+s)*cos+3*r*sin
        x2_=x+(2*r+s)*sin+r*cos
        y2_=y-(2*r+s)*cos+r*sin
        plt.plot([x1_,x2_],[y1_,y2_],'k',linewidth=4)
        
        linspace=np.array([-2.75,-2.25,-1.75,-1.25,1.25,1.75,2.25,2.75])*r
        x1_=x
        x2_=x
        y1_=y
        y2_=y
        x1_=x+(2*r+s)*sin-linspace*cos
        x2_=x+(2*r+s)*sin-linspace*cos+0.5*r*sin
        y1_=y-(2*r+s)*cos-linspace*sin
        y2_=y-(2*r+s)*cos-linspace*sin-0.5*r*cos
        plt.plot([x1_,x2_],[y1_,y2_],'k',linewidth=4)








    def drawrestraint2(x,y,alp):
        alp1=alp/180*3.1415
        sin=np.sin(alp1)
        cos=np.cos(alp1)
        sin45=np.sin((45-alp)/180*3.14159)
        cos45=np.cos((45-alp)/180*3.14159)
        sin45_=np.sin((alp+45)/180*3.14159)
        cos45_=np.cos((alp+45)/180*3.14159)
        xc=x+r*np.cos(theta)
        yc=y+r*np.sin(theta)
        plt.plot(xc,yc,'r',linewidth=3)
        x1_=x-r*sin45
        y1_=y-r*cos45
        x2_=x-(r+s)*sin45
        y2_=y-(r+s)*cos45
        plt.plot([x1_,x2_],[y1_,y2_],'k',linewidth=4)
        x1_=x+r*sin45_
        y1_=y-r*cos45_
        x2_=x+(r+s)*sin45_
        y2_=y-(r+s)*cos45_
        plt.plot([x1_,x2_],[y1_,y2_],'k',linewidth=4)
        xc=x-(2*r+s)*sin45+r*np.cos(theta)
        yc=y-(2*r+s)*cos45+r*np.sin(theta)
        plt.plot(xc,yc,'r',linewidth=3)
        xc=x+(2*r+s)*sin45_+r*np.cos(theta)
        yc=y-(2*r+s)*cos45_+r*np.sin(theta)
        plt.plot(xc,yc,'r',linewidth=3)
        x1_=x-(2*r+s)*sin45+r*cos
        y1_=y-(2*r+s)*cos45+r*sin
        x2_=x+(2*r+s)*sin45_-r*cos
        y2_=y-(2*r+s)*cos45_-r*sin
        plt.plot([x1_,x2_],[y1_,y2_],'k',linewidth=4)

    
    def drawelasticrestraint1(x,y,alp,k):
        alp=alp/180*3.1415
        
        sin=np.sin(alp)
        cos=np.cos(alp)
    #    sin_90=-cos
    #    cos_90=sin
        xc=x+r*np.cos(theta)
        yc=y+r*np.sin(theta)
        plt.plot(xc,yc,'r',linewidth=3)
        x1=np.array([0,-1,1,-1,1,0])*r
        y1=np.array([0,-0.5,-0.5,-1,-1,-1.5])*r
        x_=x1*cos-y1*sin+x+r*sin
        y_=x1*sin+y1*cos+y-r*cos
        plt.plot(x_,y_,'r')
        xc=x+r*np.cos(theta)+3.5*r*sin
        yc=y+r*np.sin(theta)-3.5*r*cos
        plt.plot(xc,yc,'r',linewidth=3)
        x_=np.array([-2.5,-2,-1.5,1.5,2,2.5])*r
        y_=np.array([0,0,0,0,0,0])
        x1=x_*cos-y_*sin+x+3.5*r*sin
        y1=x_*sin+y_*cos+y-3.5*r*cos
        
        x_=np.array([-2.5,-2,-1.5,1.5,2,2.5])*r
        y_=np.array([-1,-1,-1,-1,-1,-1])*r
        x2=x_*cos-y_*sin+x+3.5*r*sin
        y2=x_*sin+y_*cos+y-3.5*r*cos
        plt.plot([x1,x2],[y1,y2],'k')
        
        x1=-3*r*cos+3.5*r*sin+x
        y1=-3*r*sin-3.5*r*cos+y
        x2=-r*cos+3.5*r*sin+x
        y2=-r*sin-3.5*r*cos+y
        plt.plot([x1,x2],[y1,y2],'k')
        x1=3*r*cos+3.5*r*sin+x
        y1=3*r*sin-3.5*r*cos+y
        x2=r*cos+3.5*r*sin+x
        y2=r*sin-3.5*r*cos+y
        plt.plot([x1,x2],[y1,y2],'k')
        
        x1=2.5*r*sin+x+r*cos
        y1=-2.5*r*cos+y+r*sin
    
        plt.text(x1,y1,'k=%d'%k,fontsize=45,c='b',family='fantasy')
        plt.scatter(x=x1,y=y1,color='',edgecolor='')
        print(11111111)
    
    
    
    for i in range(len(elements)):
        xi=elements[i]['pi']['x']
        yi=elements[i]['pi']['y']
        xj=elements[i]['pj']['x']
        yj=elements[i]['pj']['y']
        talp=elements[i]['alp']/180*3.14159
        sin=np.sin(talp)
        cos=np.cos(talp)
        itsalp=(elements[i]['pi']['salp']-90)/180*3.14159
        jtsalp=(elements[i]['pj']['salp']-90)/180*3.14159
        sinsi=np.sin(itsalp)
        cossi=np.cos(itsalp)
        sinsj=np.sin(jtsalp)
        cossj=np.cos(jtsalp)
        
        if elements[i]['pi']['connection']==0 and elements[i]['pi']['restraint']==1 and elements[i]['pi']['supportdraw']:
            drawrestraint1(elements[i]['pi']['xc'],elements[i]['pi']['yc'],elements[i]['pi']['salp'])
            elements[i]['pi']['supportdraw']=False
                
        if elements[i]['pi']['connection']==1 and elements[i]['pi']['restraint']==1 and elements[i]['pi']['supportdraw']:
            if elements[i]['alp']==0 and elements[i]['pi']['salp']==0 :
                x = xi+ r * np.cos(theta)
                y = yi-r + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                plt.plot([xi,xi],[yi-2*r,yi-2*r-s],'k',linewidth=4)
                x=xi+ r * np.cos(theta)
                y = yi-3*r-s + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                plt.plot([xi-s-r,xi-r],[yi-3*r-s,yi-3*r-s],'k',linewidth=2)
                plt.plot([xi+s+r,xi+r],[yi-3*r-s,yi-3*r-s],'k',linewidth=2)
                plt.plot([xi-0.8*s-r,xi-0.8*s-r],[yi-3*r-s,yi-4.5*r-s],'k',linewidth=2)
                plt.plot([xi-0.6*s-r,xi-0.6*s-r],[yi-3*r-s,yi-4.5*r-s],'k',linewidth=2)
                plt.plot([xi-0.4*s-r,xi-0.4*s-r],[yi-3*r-s,yi-4.5*r-s],'k',linewidth=2)
                plt.plot([xi-0.2*s-r,xi-0.2*s-r],[yi-3*r-s,yi-4.5*r-s],'k',linewidth=2)
                plt.plot([xi+0.8*s+r,xi+0.8*s+r],[yi-3*r-s,yi-4.5*r-s],'k',linewidth=2)
                plt.plot([xi+0.6*s+r,xi+0.6*s+r],[yi-3*r-s,yi-4.5*r-s],'k',linewidth=2)
                plt.plot([xi+0.4*s+r,xi+0.4*s+r],[yi-3*r-s,yi-4.5*r-s],'k',linewidth=2)
                plt.plot([xi+0.2*s+r,xi+0.2*s+r],[yi-3*r-s,yi-4.5*r-s],'k',linewidth=2)
                elements[i]['pi']['supportdraw']==False
                
                
            else:
                drawrestraint1(xi-r*cos,yi-r*sin,elements[i]['pi']['salp'])
                elements[i]['pi']['supportdraw']=False

 
        if elements[i]['pj']['connection']==0 and elements[i]['pj']['restraint']==1 and elements[i]['pj']['supportdraw']:
            drawrestraint1(elements[i]['pj']['xc'],elements[i]['pj']['yc'],elements[i]['pj']['salp'])
            elements[i]['pj']['supportdraw']=False

            
        if elements[i]['pj']['connection']==1 and elements[i]['pj']['restraint']==1 and elements[i]['pj']['supportdraw']:
            if elements[i]['alp']==0 and elements[i]['pj']['salp']==0 :
                x = xj+ r * np.cos(theta)
                y = yj-r + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                plt.plot([xj,xj],[yj-2*r,yj-2*r-s],'k',linewidth=4)
                x=xj+ r * np.cos(theta)
                y = yj-3*r-s + r * np.sin(theta)
                plt.plot(x,y,'r',linewidth=3)
                plt.plot([xj-s-r,xj-r],[yj-3*r-s,yj-3*r-s],'k',linewidth=2)
                plt.plot([xj+s+r,xj+r],[yj-3*r-s,yj-3*r-s],'k',linewidth=2)
                plt.plot([xj-0.8*s-r,xj-0.8*s-r],[yj-3*r-s,yj-4.5*r-s],'k',linewidth=2)
                plt.plot([xj-0.6*s-r,xj-0.6*s-r],[yj-3*r-s,yj-4.5*r-s],'k',linewidth=2)
                plt.plot([xj-0.4*s-r,xj-0.4*s-r],[yj-3*r-s,yj-4.5*r-s],'k',linewidth=2)
                plt.plot([xj-0.2*s-r,xj-0.2*s-r],[yj-3*r-s,yj-4.5*r-s],'k',linewidth=2)
                plt.plot([xj+0.8*s+r,xj+0.8*s+r],[yj-3*r-s,yj-4.5*r-s],'k',linewidth=2)
                plt.plot([xj+0.6*s+r,xj+0.6*s+r],[yj-3*r-s,yj-4.5*r-s],'k',linewidth=2)
                plt.plot([xj+0.4*s+r,xj+0.4*s+r],[yj-3*r-s,yj-4.5*r-s],'k',linewidth=2)
                plt.plot([xj+0.2*s+r,xj+0.2*s+r],[yj-3*r-s,yj-4.5*r-s],'k',linewidth=2)
                elements[i]['pj']['supportdraw']=False
            else:
                drawrestraint1(xj+r*cos,yj+r*sin,elements[i]['pj']['salp'])
                elements[i]['pj']['supportdraw']=False

        
        if elements[i]['pi']['connection']==0 and elements[i]['pi']['restraint']==2 and elements[i]['pi']['supportdraw']: 
            drawrestraint2(elements[i]['pi']['xc'],elements[i]['pi']['yc'],elements[i]['pi']['salp'])
            elements[i]['pi']['supportdraw']=False

                
        if elements[i]['pj']['connection']==0 and elements[i]['pj']['restraint']==2 and elements[i]['pj']['supportdraw']: 
            drawrestraint2(elements[i]['pj']['xc'],elements[i]['pj']['yc'],elements[i]['pj']['salp'])
            elements[i]['pj']['supportdraw']=False


        if elements[i]['pi']['connection']==1 and elements[i]['pi']['restraint']==2 and elements[i]['pi']['supportdraw']:
            if elements[i]['alp']==0:
                drawrestraint2(xi,yi-r*sin-r,elements[i]['pi']['salp'])
                elements[i]['pi']['supportdraw']=False
            else:
                drawrestraint2(xi-r*cos,yi-r*sin,elements[i]['pi']['salp'])
                elements[i]['pi']['supportdraw']=False
                
#            x = xi-r*cos + r * np.cos(theta)
#            y = yi-r*sin + r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            plt.plot([xi-r*cos-r*np.sqrt(2)/2,xi-r*cos-(r+s)*np.sqrt(2)/2],[yi-r*sin-r*np.sqrt(2)/2,yi-r*sin-(r+s)*np.sqrt(2)/2],'k',linewidth=4)
#            plt.plot([xi-r*cos+r*np.sqrt(2)/2,xi-r*cos+(r+s)*np.sqrt(2)/2],[yi-r*sin-r*np.sqrt(2)/2,yi-r*sin-(r+s)*np.sqrt(2)/2],'k',linewidth=4)
#            x = xi-r*cos-(2*r+s)*np.sqrt(2)/2 + r * np.cos(theta)
#            y = yi-r*sin -(2*r+s)*np.sqrt(2)/2+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            x = xi-r*cos+(2*r+s)*np.sqrt(2)/2 + r * np.cos(theta)
#            y = yi-r*sin -(2*r+s)*np.sqrt(2)/2+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            plt.plot([xi-r*cos-(2*r+s)*np.sqrt(2)/2+r,xi-r*cos+(2*r+s)*np.sqrt(2)/2-r],[yi-r*sin -(2*r+s)*np.sqrt(2)/2,yi-r*sin -(2*r+s)*np.sqrt(2)/2],'k',linewidth=4)
#            elements[i]['pi']['supportdraw']=False
        if elements[i]['pj']['connection']==1 and elements[i]['pj']['restraint']==2 and elements[i]['pj']['supportdraw']:
            if elements[i]['alp']==0:
                drawrestraint2(xj,yj+r*sin-r,elements[i]['pj']['salp'])
                elements[i]['pj']['supportdraw']=False
            else:
                drawrestraint2(xj+r*cos,yj+r*sin,elements[i]['pj']['salp'])
                elements[i]['pj']['supportdraw']=False
                
        if elements[i]['pi']['connection']==1 and elements[i]['pi']['restraint']==3 and elements[i]['pi']['supportdraw']:
            itsalp=elements[i]['pi']['salp']/180*3.14159
            sinsi=np.sin(itsalp)
            cossi=np.cos(itsalp)
            plt.plot([xi-2*s*cossi,xi+2*s*cossi],[yi-2*s*sinsi,yi+2*s*sinsi],'k',linewidth=4)
            x=xi-s*cossi+r*sinsi+ r * np.cos(theta)
            y=yi-s*sinsi-r*cossi+ r * np.sin(theta)
            plt.plot(x,y,'r',linewidth=3)
            x=xi+s*cossi+r*sinsi+ r * np.cos(theta)
            y=yi+s*sinsi-r*cossi+ r * np.sin(theta)
            plt.plot(x,y,'r',linewidth=3)
            plt.plot([xi-s*cossi+2*r*sinsi,xi-s*cossi+(2*r+s)*sinsi],
                      [yi-s*sinsi-2*r*cossi,yi-s*sinsi-(2*r+s)*cossi],'k',linewidth=3.5)
            plt.plot([xi+s*cossi+2*r*sinsi,xi+s*cossi+(2*r+s)*sinsi],
                      [yi+s*sinsi-2*r*cossi,yi+s*sinsi-(2*r+s)*cossi],'k',linewidth=3.5)
            x=xi-s*cossi+(3*r+s)*sinsi+ r * np.cos(theta)
            y=yi-s*sinsi-(3*r+s)*cossi+ r * np.sin(theta)
            plt.plot(x,y,'r',linewidth=3.5)
            x=xi+s*cossi+(3*r+s)*sinsi+ r * np.cos(theta)
            y=yi+s*sinsi-(3*r+s)*cossi+ r * np.sin(theta)
            plt.plot(x,y,'r',linewidth=3.5)
            plt.plot([xi-(2*s)*cossi+(4*r+s)*sinsi,xi+(2*s)*cossi+(4*r+s)*sinsi],
                      [yi-(2*s)*sinsi-(4*r+s)*cossi,yi+(2*s)*sinsi-(4*r+s)*cossi],'k',linewidth=3.5)
            itsalp=(elements[i]['pi']['salp']-90)/180*3.14159
            sinsi=np.sin(itsalp)
            cossi=np.cos(itsalp)
            elements[i]['pi']['supportdraw']=False
        if elements[i]['pj']['connection']==1 and elements[i]['pj']['restraint']==3 and elements[i]['pj']['supportdraw']:
            jtsalp=elements[i]['pj']['salp']/180*3.14159
            sinsj=np.sin(jtsalp)
            cossj=np.cos(jtsalp)
            plt.plot([xj-2*s*cossj,xj+2*s*cossj],[yj-2*s*sinsj,yj+2*s*sinsj],'k',linewidth=3.5)
            x=xj-s*cossj+r*sinsj+ r * np.cos(theta)
            y=yj-s*sinsj-r*cossj+ r * np.sin(theta)
            plt.plot(x,y,'r',linewidth=3.5)
            x=xj+s*cossj+r*sinsj+ r * np.cos(theta)
            y=yj+s*sinsj-r*cossj+ r * np.sin(theta)
            plt.plot(x,y,'r',linewidth=3.5)
            plt.plot([xj-s*cossj+2*r*sinsj,xj-s*cossj+(2*r+s)*sinsj],
                      [yj-s*sinsj-2*r*cossj,yj-s*sinsj-(2*r+s)*cossj],'k',linewidth=3.5)
            plt.plot([xj+s*cossj+2*r*sinsj,xj+s*cossj+(2*r+s)*sinsj],
                      [yj+s*sinsj-2*r*cossj,yj+s*sinsj-(2*r+s)*cossj],'k',linewidth=3.5)
            x=xj-s*cossj+(3*r+s)*sinsj+ r * np.cos(theta)
            y=yj-s*sinsj-(3*r+s)*cossj+ r * np.sin(theta)
            plt.plot(x,y,'r',linewidth=3.5)
            x=xj+s*cossj+(3*r+s)*sinsj+ r * np.cos(theta)
            y=yj+s*sinsj-(3*r+s)*cossj+ r * np.sin(theta)
            plt.plot(x,y,'r',linewidth=3.5)
#            plt.plot([xj-(2*s-r)*cossj+(4*r+s)*sinsj,xj+(2*s-r)*cossj+(4*r+s)*sinsj],
#                      [yj-(2*s-r)*sinsj-(4*r+s)*cossj,yj+(2*s-r)*sinsj-(4*r+s)*cossj],'k',linewidth=3.5)
            plt.plot([xj-(2*s)*cossj+(4*r+s)*sinsj,xj+(2*s)*cossj+(4*r+s)*sinsj],
                      [yj-(2*s)*sinsj-(4*r+s)*cossj,yj+(2*s)*sinsj-(4*r+s)*cossj],'k',linewidth=3.5)
            jtsalp=(elements[i]['pj']['salp']-90)/180*3.14159
            sinsj=np.sin(jtsalp)
            cossj=np.cos(jtsalp)
            elements[i]['pj']['supportdraw']=False
        if elements[i]['pi']['connection']==1 and elements[i]['pi'] ['restraint']==4 and elements[i]['pi']['supportdraw']:
            itsalp=elements[i]['pi']['salp']/180*3.14159
            sinsi=np.sin(itsalp)
            cossi=np.cos(itsalp)
            plt.plot([xi-2*s*cossi,xi+2*s*cossi],[yi-2*s*sinsi,yi+2*s*sinsi],'k',linewidth=4)
            x=np.array([-1.5*s,-s,-0.5*s,0,0.5*s,s,1.5*s])
            y=np.array([-0.75*s,-0.75*s,-0.75*s,-0.75*s,-0.75*s,-0.75*s,-0.75*s])
            x1=x*cossi+xi
            y1=x*sinsi+yi
            x2=x*cossi-y*sinsi+xi
            y2=x*sinsi+y*cossi+yi
            plt.plot([x1,x2],[y1,y2],'k--',linewidth=2.5)
            itsalp=(elements[i]['pi']['salp']-90)/180*3.14159
            sinsi=np.sin(itsalp)
            cossi=np.cos(itsalp)
            elements[i]['pi']['supportdraw']=False
        if elements[i]['pj']['connection']==1 and elements[i]['pj'] ['restraint']==4 and elements[i]['pj']['supportdraw']:
            jtsalp=elements[i]['pj']['salp']/180*3.14159
            sinsj=np.sin(jtsalp)
            cossj=np.cos(jtsalp)
            plt.plot([xj-2*s*cossj,xj+2*s*cossj],[yj-2*s*sinsj,yj+2*s*sinsj],'k',linewidth=4)
            x=np.array([-1.5*s,-s,-0.5*s,0,0.5*s,s,1.5*s])
            y=np.array([-0.75*s,-0.75*s,-0.75*s,-0.75*s,-0.75*s,-0.75*s,-0.75*s])
            x1=x*cossj+xj
            y1=x*sinsj+yj
            x2=x*cossj-y*sinsj+xj
            y2=x*sinsj+y*cossj+yj
            plt.plot([x1,x2],[y1,y2],'k--',linewidth=2.5)
            jtsalp=(elements[i]['pj']['salp']-90)/180*3.14159
            sinsj=np.sin(jtsalp)
            cossj=np.cos(jtsalp)
            elements[i]['pj']['supportdraw']=False  
    for i in range(len(elements)):
        xi=elements[i]['pi']['x']
        yi=elements[i]['pi']['y']
        xj=elements[i]['pj']['x']
        yj=elements[i]['pj']['y']
        talp=elements[i]['alp']/180*3.14159
        sin=np.sin(talp)
        cos=np.cos(talp)
        itsalp=(elements[i]['pi']['ealp']-90)/180*3.14159
        jtsalp=(elements[i]['pj']['ealp']-90)/180*3.14159
        sinsi=np.sin(itsalp)
        cossi=np.cos(itsalp)
        sinsj=np.sin(jtsalp)
        cossj=np.cos(jtsalp)
        if elements[i]['pi']['esupport']==1 and elements[i]['pi']['connection']==1:
            drawelasticrestraint1(xi +r*cossi,yi +r*sinsi,elements[i]['pi']['ealp'],elements[i]['pi']['k'])
            elements[i]['pi']['esupportdraw']=False
            
#            x = xi +r*cossi+ r * np.cos(theta)
#            y = yi +r*sinsi+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            x = xi +(3*r+s)*cossi+ r * np.cos(theta)
#            y = yi +(3*r+s)*sinsi+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            plt.plot([xi +(3*r+s)*cossi-r*sinsi,xi +(3*r+s)*cossi-s*sinsi],
#                          [yi +(3*r+s)*sinsi+r*cossi,yi +(3*r+s)*sinsi+s*cossi],'k')
#            plt.plot([xi +(3*r+s)*cossi+r*sinsi,xi +(3*r+s)*cossi+s*sinsi],
#                          [yi +(3*r+s)*sinsi-r*cossi,yi +(3*r+s)*sinsi-s*cossi],'k')
#            itsalp=elements[i]['pi']['ealp']/180*3.14159
#            sinsi=np.sin(itsalp)
#            cossi=np.cos(itsalp)
#            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
#            y=np.array([-2*r,-2*r-0.25*s,-2*r-0.25*s,-2*r-0.75*s,-2*r-0.75*s,-2*r-s])
#            x1=x*cossi-y*sinsi+xi
#            y1=x*sinsi+y*cossi+yi
#            plt.plot(x1,y1,'r')
#            x=np.array([-2.75,-2.25,-1.75,-1.25,1.25,1.75,2.25,2.75])*r
#            y=x*0-(3*r+1.3*s)
#            y_=y+0.3*s
#            x1=x*cossi-y*sinsi+xi
#            x2=x*cossi-y_*sinsi+xi
#            y1=x*sinsi+y*cossi+yi
#            y2=x*sinsi+y_*cossi+yi
#            plt.plot([x1,x2],[y1,y2],'k') 
#            plt.text(xis,yis,int(elements[i]['pi']['num']),fontsize=35,c='b',family='fantasy')
#            plt.scatter(x=xis,y=yis,color='',edgecolor='')
        if elements[i]['pj']['esupport']==1 and elements[i]['pj']['connection']==1:
            drawelasticrestraint1(xj +r*cossj,yj +r*sinsj,elements[i]['pj']['ealp'],elements[i]['pj']['k'])
            elements[i]['pj']['esupportdraw']=False
            
#            x = xj +r*cossj+ r * np.cos(theta)
#            y = yj +r*sinsj+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            x = xj +(3*r+s)*cossj+ r * np.cos(theta)
#            y = yj +(3*r+s)*sinsj+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            plt.plot([xj +(3*r+s)*cossj-r*sinsj,xj +(3*r+s)*cossj-s*sinsj],
#                          [yj +(3*r+s)*sinsj+r*cossj,yj +(3*r+s)*sinsj+s*cossj],'k')
#            plt.plot([xj +(3*r+s)*cossj+r*sinsj,xj +(3*r+s)*cossj+s*sinsj],
#                          [yj +(3*r+s)*sinsj-r*cossj,yj +(3*r+s)*sinsj-s*cossj],'k')
#            jtsalp=elements[i]['pj']['ealp']/180*3.14159
#            sinsj=np.sin(jtsalp)
#            cossj=np.cos(jtsalp)
#            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
#            y=np.array([-2*r,-2*r-0.25*s,-2*r-0.25*s,-2*r-0.75*s,-2*r-0.75*s,-2*r-s])
#            x1=x*cossj-y*sinsj+xj
#            y1=x*sinsj+y*cossj+yj
#            plt.plot(x1,y1,'r')
#            x=np.array([-2.75,-2.25,-1.75,-1.25,1.25,1.75,2.25,2.75])*r
#            y=x*0-(3*r+1.3*s)
#            y_=y+0.3*s
#            x1=x*cossj-y*sinsj+xj
#            x2=x*cossj-y_*sinsj+xj
#            y1=x*sinsj+y*cossj+yj
#            y2=x*sinsj+y_*cossj+yj
#            plt.plot([x1,x2],[y1,y2],'k')
            
        if elements[i]['pi']['esupport']==1 and elements[i]['pi']['connection']==0 and elements[i]['pi']['ht']==0:
            drawelasticrestraint1(elements[i]['pi']['xc'],elements[i]['pi']['yc'],elements[i]['pi']['ealp'],elements[i]['pi']['k'])
            elements[i]['pi']['esupportdraw']=False
            
#            x = xi +(r+s)*cossi+ r * np.cos(theta)
#            y = yi +(r+s)*sinsi+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            plt.plot([xi +(r+s)*cossi-r*sinsi,xi +(r+s)*cossi-s*sinsi],
#                          [yi +(r+s)*sinsi+r*cossi,yi +(r+s)*sinsi+s*cossi],'k')
#            plt.plot([xi +(r+s)*cossi+r*sinsi,xi +(r+s)*cossi+s*sinsi],
#                          [yi +(r+s)*sinsi-r*cossi,yi +(r+s)*sinsi-s*cossi],'k')
#            itsalp=elements[i]['pi']['ealp']/180*3.14159
#            sinsi=np.sin(itsalp)
#            cossi=np.cos(itsalp)
#            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
#            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-s])
#            x1=x*cossi-y*sinsi+xi
#            y1=x*sinsi+y*cossi+yi
#            plt.plot(x1,y1,'r')
#            x=np.array([-2.75,-2.25,-1.75,-1.25,1.25,1.75,2.25,2.75])*r
#            y=x*0-(r+1.3*s)
#            y_=y+0.3*s
#            x1=x*cossi-y*sinsi+xi
#            x2=x*cossi-y_*sinsi+xi
#            y1=x*sinsi+y*cossi+yi
#            y2=x*sinsi+y_*cossi+yi
#            plt.plot([x1,x2],[y1,y2],'k')    
        if elements[i]['pj']['esupport']==1 and elements[i]['pj']['connection']==0 and elements[i]['pj']['ht']==0:
            drawelasticrestraint1(elements[i]['pj']['xc'],elements[i]['pj']['yc'],elements[i]['pj']['ealp'],elements[i]['pj']['k'])
            elements[i]['pj']['esupportdraw']=False
            
            
#            x = xj +(r+s)*cossj+ r * np.cos(theta)
#            y = yj +(r+s)*sinsj+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            plt.plot([xj +(r+s)*cossj-r*sinsj,xj +(r+s)*cossj-s*sinsj],
#                          [yj +(r+s)*sinsj+r*cossj,yj +(r+s)*sinsj+s*cossj],'k')
#            plt.plot([xj +(r+s)*cossj+r*sinsj,xj +(r+s)*cossj+s*sinsj],
#                          [yj +(r+s)*sinsj-r*cossj,yj +(r+s)*sinsj-s*cossj],'k')
#            jtsalp=elements[i]['pj']['ealp']/180*3.14159
#            sinsj=np.sin(jtsalp)
#            cossj=np.cos(jtsalp)
#            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
#            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-s])
#            x1=x*cossj-y*sinsj+xj
#            y1=x*sinsj+y*cossj+yj
#            plt.plot(x1,y1,'r')
#            x=np.array([-2.75,-2.25,-1.75,-1.25,1.25,1.75,2.25,2.75])*r
#            y=x*0-(r+1.3*s)
#            y_=y+0.3*s
#            x1=x*cossj-y*sinsj+xj
#            x2=x*cossj-y_*sinsj+xj
#            y1=x*sinsj+y*cossj+yj
#            y2=x*sinsj+y_*cossj+yj
#            plt.plot([x1,x2],[y1,y2],'k')
#            x=np.array([-2.75,-2.25,-1.75,-1.25,1.25,1.75,2.25,2.75])*r
#            y=x*0-(r+1.3*s)
#            y_=y+0.3*s
#            x1=x*cossj-y*sinsj+xj
#            x2=x*cossj-y_*sinsj+xj
#            y1=x*sinsj+y*cossj+yj
#            y2=x*sinsj+y_*cossj+yj
#            plt.plot([x1,x2],[y1,y2],'k')
        if elements[i]['pi']['esupport']==1 and elements[i]['pi']['connection']==0 and elements[i]['pi']['ht']==1:
            drawelasticrestraint1(elements[i]['pi']['xc'],elements[i]['pi']['yc'],elements[i]['pi']['ealp'],elements[i]['pi']['k'])
            elements[i]['pi']['esupportdraw']=False
            
#            
#            x = xi +(2*r+s)*cossi+ r * np.cos(theta)
#            y = yi +(2*r+s)*sinsi+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            plt.plot([xi +(2*r+s)*cossi-r*sinsi,xi +(2*r+s)*cossi-s*sinsi],
#                          [yi +(2*r+s)*sinsi+r*cossi,yi +(2*r+s)*sinsi+s*cossi],'k')
#            plt.plot([xi +(2*r+s)*cossi+r*sinsi,xi +(2*r+s)*cossi+s*sinsi],
#                          [yi +(2*r+s)*sinsi-r*cossi,yi +(2*r+s)*sinsi-s*cossi],'k')
#            itsalp=elements[i]['pi']['ealp']/180*3.14159
#            sinsi=np.sin(itsalp)
#            cossi=np.cos(itsalp)
#            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
#            y=np.array([-r,-r-0.25*s,-r-0.25*s,-r-0.75*s,-r-0.75*s,-r-s])
#            x1=x*cossi-y*sinsi+xi
#            y1=x*sinsi+y*cossi+yi
#            plt.plot(x1,y1,'r')
#            x=np.array([-2.75,-2.25,-1.75,-1.25,1.25,1.75,2.25,2.75])*r
#            y=x*0-(2*r+1.3*s)
#            y_=y+0.3*s
#            x1=x*cossi-y*sinsi+xi
#            x2=x*cossi-y_*sinsi+xi
#            y1=x*sinsi+y*cossi+yi
#            y2=x*sinsi+y_*cossi+yi
#            plt.plot([x1,x2],[y1,y2],'k') 
        if elements[i]['pj']['esupport']==1 and elements[i]['pj']['connection']==0 and elements[i]['pj']['ht']==1:
            drawelasticrestraint1(elements[i]['pj']['xc'],elements[i]['pj']['yc'],elements[i]['pj']['ealp'],elements[i]['pj']['k'])
            elements[i]['pj']['esupportdraw']=False 
            
#            x = xj +(2*r+s)*cossj+ r * np.cos(theta)
#            y = yj +(2*r+s)*sinsj+ r * np.sin(theta)
#            plt.plot(x,y,'r',linewidth=3)
#            plt.plot([xj +(2*r+s)*cossj-r*sinsj,xj +(2*r+s)*cossj-s*sinsj],
#                          [yj +(2*r+s)*sinsj+r*cossj,yj +(2*r+s)*sinsj+s*cossj],'k')
#            plt.plot([xj +(2*r+s)*cossj+r*sinsj,xj +(2*r+s)*cossj+s*sinsj],
#                          [yj +(2*r+s)*sinsj-r*cossj,yj +(2*r+s)*sinsj-s*cossj],'k')
#            jtsalp=elements[i]['pj']['ealp']/180*3.14159
#            sinsj=np.sin(jtsalp)
#            cossj=np.cos(jtsalp)
#            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
#            y=np.array([-r,-r-0.25*s,-r-0.25*s,-r-0.75*s,-r-0.75*s,-r-s])
#            x1=x*cossj-y*sinsj+xj
#            y1=x*sinsj+y*cossj+yj
#            plt.plot(x1,y1,'r')
#            x=np.array([-2.75,-2.25,-1.75,-1.25,1.25,1.75,2.25,2.75])*r
#            y=x*0-(2*r+1.3*s)
#            y_=y+0.3*s
#            x1=x*cossj-y*sinsj+xj
#            x2=x*cossj-y_*sinsj+xj
#            y1=x*sinsj+y*cossj+yj
#            y2=x*sinsj+y_*cossj+yj
#            plt.plot([x1,x2],[y1,y2],'k') 
            
        if elements[i]['pi']['esupport']==2 and elements[i]['pi']['connection']==1 and elements[i]['pi']['restraint']==0:
            
            itsalp=elements[i]['pi']['ealp']/180*3.14159
            sinsi=np.sin(itsalp)
            cossi=np.cos(itsalp)
            plt.plot([xi-2*s*cossi,xi+2*s*cossi],[yi-2*s*sinsi,yi+2*s*sinsi],'k')
            plt.plot([xi-2*s*cossi+1.5*s*sinsi,xi+2*s*cossi+1.5*s*sinsi],
                     [yi-2*s*sinsi-1.5*s*cossi,yi+2*s*sinsi-1.5*s*cossi],'k')
            
            k=elements[i]['pi']['k']
            plt.text(xi+2*s*cossi+1.5*s*sinsi,yi+2*s*sinsi-1.5*s*cossi,'k=%d'%k,fontsize=45,c='b',family='fantasy')
            plt.scatter(x=xi+2*s*cossi+1.5*s*sinsi,y=yi+2*s*sinsi-1.5*s*cossi,color='',edgecolor='')
            
            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-1.25*s,-1.25*s,-1.5*s])
            x1=x*cossi-y*sinsi+xi-2*s*cossi
            y1=x*sinsi+y*cossi+yi-2*s*sinsi
            plt.plot(x1,y1,'r') 
            x1=x*cossi-y*sinsi+xi+2*s*cossi
            y1=x*sinsi+y*cossi+yi+2*s*sinsi
            plt.plot(x1,y1,'r')
            
        if elements[i]['pi']['esupport']==2 and elements[i]['pi']['connection']==1 and elements[i]['pi']['restraint']!=0:
            itsalp=elements[i]['pi']['ealp']/180*3.14159
            sinsi=np.sin(itsalp)
            cossi=np.cos(itsalp)
            plt.plot([xi-2*s*cossi,xi+2*s*cossi],[yi-2*s*sinsi,yi+2*s*sinsi],'k')
            plt.plot([xi-2*s*cossi+1.5*s*sinsi,xi+2*s*cossi+1.5*s*sinsi],
                     [yi-2*s*sinsi-1.5*s*cossi,yi+2*s*sinsi-1.5*s*cossi],'k')
            
            k=elements[i]['pi']['k']
            plt.text(xi+2*s*cossi+1.5*s*sinsi,yi+2*s*sinsi-1.5*s*cossi,'k=%d'%k,fontsize=45,c='b',family='fantasy')
            plt.scatter(x=xi+2*s*cossi+1.5*s*sinsi,y=yi+2*s*sinsi-1.5*s*cossi,color='',edgecolor='')
            
            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-1.25*s,-1.25*s,-1.5*s])
            x1=x*cossi-y*sinsi+xi-2*s*cossi
            y1=x*sinsi+y*cossi+yi-2*s*sinsi
            plt.plot(x1,y1,'r') 
            x1=x*cossi-y*sinsi+xi+2*s*cossi
            y1=x*sinsi+y*cossi+yi+2*s*sinsi
            plt.plot(x1,y1,'r')
        if elements[i]['pj']['esupport']==2 and elements[i]['pj']['connection']==1 and elements[i]['pj']['restraint']==0:
            
            jtsalp=elements[i]['pj']['ealp']/180*3.14159
            sinsj=np.sin(jtsalp)
            cossj=np.cos(jtsalp)
            plt.plot([xj-2*s*cossj,xj+r*cossi+2*s*cossj],[yj-2*s*sinsj,yj+2*s*sinsj],'k')
            plt.plot([xj-2*s*cossj+1.5*s*sinsj,xj+2*s*cossj+1.5*s*sinsj],
                     [yj-2*s*sinsj-1.5*s*cossj,yj+2*s*sinsj-1.5*s*cossj],'k')
            
            k=elements[i]['pj']['k']
            plt.text(xj+2*s*cossj+1.5*s*sinsj,yj+2*s*sinsj-1.5*s*cossj,'k=%d'%k,fontsize=45,c='b',family='fantasy')
            plt.scatter(x=xj+2*s*cossj+1.5*s*sinsj,y=yj+2*s*sinsj-1.5*s*cossj,color='',edgecolor='')
            
            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-1.25*s,-1.25*s,-1.5*s])
            x1=x*cossj-y*sinsj+xj-2*s*cossj
            y1=x*sinsj+y*cossj+yj-2*s*sinsj
            plt.plot(x1,y1,'r')
            x1=x*cossj-y*sinsj+xj+2*s*cossj
            y1=x*sinsj+y*cossj+yj+2*s*sinsj
            plt.plot(x1,y1,'r') 
        if elements[i]['pj']['esupport']==2 and elements[i]['pj']['connection']==1 and elements[i]['pj']['restraint']!=0:
            
            
            jtsalp=elements[i]['pj']['ealp']/180*3.14159
            sinsj=np.sin(jtsalp)
            cossj=np.cos(jtsalp)
            plt.plot([xj-2*s*cossj,xj+2*s*cossj],[yj-2*s*sinsj,yj+2*s*sinsj],'k')
            plt.plot([xj-2*s*cossj+1.5*s*sinsj,xj+2*s*cossj+1.5*s*sinsj],
                     [yj-2*s*sinsj-1.5*s*cossj,yj+2*s*sinsj-1.5*s*cossj],'k')
            
            k=elements[i]['pj']['k']
            plt.text(xj+2*s*cossj+1.5*s*sinsj,yj+2*s*sinsj-1.5*s*cossj,'k=%d'%k,fontsize=45,c='b',family='fantasy')
            plt.scatter(x=xj+2*s*cossj+1.5*s*sinsj,y=yj+2*s*sinsj-1.5*s*cossj,color='',edgecolor='')
            
            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-1.25*s,-1.25*s,-1.5*s])
            x1=x*cossj-y*sinsj+xj-2*s*cossj
            y1=x*sinsj+y*cossj+yj-2*s*sinsj
            plt.plot(x1,y1,'r')
            x1=x*cossj-y*sinsj+xj+2*s*cossj
            y1=x*sinsj+y*cossj+yj+2*s*sinsj
            plt.plot(x1,y1,'r') 
        if elements[i]['pi']['esupport']==2 and elements[i]['pi']['connection']==0 and elements[i]['pi']['ht']==0:
            itsalp=elements[i]['pi']['ealp']/180*3.14159
            sinsi=np.sin(itsalp)
            cossi=np.cos(itsalp)
            plt.plot([xi+2*r*cos-2*s*cossi,xi+2*r*cos+2*s*cossi],[yi+2*r*sin-2*s*sinsi,yi+2*r*sin+2*s*sinsi],'k')
            plt.plot([xi+2*r*cos-2*s*cossi+2*s*sinsi,xi+2*r*cos+2*s*cossi+2*s*sinsi],
                     [yi+2*r*sin-2*s*sinsi-2*s*cossi,yi+2*r*sin+2*s*sinsi-2*s*cossi],'k')
            
            k=elements[i]['pi']['k']
            plt.text(xi+2*r*cos+2*s*cossi+2*s*sinsi,yi+2*r*sin+2*s*sinsi-2*s*cossi,'k=%d'%k,fontsize=45,c='b',family='fantasy')
            plt.scatter(x=xi+2*r*cos+2*s*cossi+2*s*sinsi,y=yi+2*r*sin+2*s*sinsi-2*s*cossi,color='',edgecolor='')
            
            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-1.25*s,-1.25*s,-1.75*s,-1.75*s,-2*s])
            x1=x*cossi-y*sinsi+xi-2*s*cossi+2*r*cos
            y1=x*sinsi+y*cossi+yi-2*s*sinsi+2*r*sin
            plt.plot(x1,y1,'r') 
            x1=x*cossi-y*sinsi+xi+2*s*cossi+2*r*cos
            y1=x*sinsi+y*cossi+yi+2*s*sinsi+2*r*sin
            plt.plot(x1,y1,'r')
        if elements[i]['pj']['esupport']==2 and elements[i]['pj']['connection']==0 and elements[i]['pj']['ht']==0:
            jtsalp=elements[i]['pj']['ealp']/180*3.14159
            sinsj=np.sin(jtsalp)
            cossj=np.cos(jtsalp)
            plt.plot([xj-2*r*cos-2*s*cossj,xj-2*r*cos+2*s*cossj],[yj-2*r*sin-2*s*sinsj,yj-2*r*sin+2*s*sinsj],'k')
            plt.plot([xj-2*r*cos-2*s*cossj+2*s*sinsj,xj-2*r*cos+2*s*cossj+2*s*sinsj],
                     [yj-2*r*sin-2*s*sinsj-2*s*cossj,yj-2*r*sin+2*s*sinsj-2*s*cossj],'k')
            
            k=elements[i]['pj']['k']
            plt.text(xj-2*r*cos+2*s*cossj+2*s*sinsj,yj-2*r*sin+2*s*sinsj-2*s*cossj,'k=%d'%k,fontsize=45,c='b',family='fantasy')
            plt.scatter(x=xj-2*r*cos+2*s*cossj+2*s*sinsj,y=yj-2*r*sin+2*s*sinsj-2*s*cossj,color='',edgecolor='')
            
            
            
            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-1.25*s,-1.25*s,-1.75*s,-1.75*s,-2*s])
            x1=x*cossj-y*sinsj+xj-2*s*cossj-2*r*cos
            y1=x*sinsj+y*cossj+yj-2*s*sinsj-2*r*sin
            plt.plot(x1,y1,'r')
            x1=x*cossj-y*sinsj+xj+2*s*cossj-2*r*cos
            y1=x*sinsj+y*cossj+yj+2*s*sinsj-2*r*sin
            plt.plot(x1,y1,'r')
        if elements[i]['pi']['esupport']==2 and elements[i]['pi']['connection']==0 and elements[i]['pi']['ht']==1:
            itsalp=elements[i]['pi']['ealp']/180*3.14159
            sinsi=np.sin(itsalp)
            cossi=np.cos(itsalp)
            plt.plot([xi+r*cos-2*s*cossi,xi+r*cos+2*s*cossi],[yi+r*sin-2*s*sinsi,yi+r*sin+2*s*sinsi],'k')
            plt.plot([xi+r*cos-2*s*cossi+2*s*sinsi,xi+r*cos+2*s*cossi+2*s*sinsi],
                     [yi+r*sin-2*s*sinsi-2*s*cossi,yi+r*sin+2*s*sinsi-2*s*cossi],'k')
            
            k=elements[i]['pi']['k']
            plt.text(xi+2*r*cos+2*s*cossi+2*s*sinsi,yi+2*r*sin+2*s*sinsi-2*s*cossi,'k=%d'%k,fontsize=45,c='b',family='fantasy')
            plt.scatter(x=xi+2*r*cos+2*s*cossi+2*s*sinsi,y=yi+2*r*sin+2*s*sinsi-2*s*cossi,color='',edgecolor='')
            
            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-1.25*s,-1.25*s,-1.75*s,-1.75*s,-2*s])
            x1=x*cossi-y*sinsi+xi-2*s*cossi+r*cos
            y1=x*sinsi+y*cossi+yi-2*s*sinsi+r*sin
            plt.plot(x1,y1,'r') 
            x1=x*cossi-y*sinsi+xi+2*s*cossi+r*cos
            y1=x*sinsi+y*cossi+yi+2*s*sinsi+r*sin
            plt.plot(x1,y1,'r')
        if elements[i]['pj']['esupport']==2 and elements[i]['pj']['connection']==0 and elements[i]['pj']['ht']==1:
            jtsalp=elements[i]['pj']['ealp']/180*3.14159
            sinsj=np.sin(jtsalp)
            cossj=np.cos(jtsalp)
            plt.plot([xj-r*cos-2*s*cossj,xj-r*cos+2*s*cossj],[yj-r*sin-2*s*sinsj,yj-r*sin+2*s*sinsj],'k')
            plt.plot([xj-r*cos-2*s*cossj+2*s*sinsj,xj-r*cos+2*s*cossj+2*s*sinsj],
                     [yj-r*sin-2*s*sinsj-2*s*cossj,yj-r*sin+2*s*sinsj-2*s*cossj],'k')
            
            k=elements[i]['pj']['k']
            plt.text(xj-2*r*cos+2*s*cossj+2*s*sinsj,yj-2*r*sin+2*s*sinsj-2*s*cossj,'k=%d'%k,fontsize=45,c='b',family='fantasy')
            plt.scatter(x=xj-2*r*cos+2*s*cossj+2*s*sinsj,y=yj-2*r*sin+2*s*sinsj-2*s*cossj,color='',edgecolor='')
            
            
            x=np.array([0,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,-1/4*s,1/4*s,0])
            y=np.array([0,-0.25*s,-0.25*s,-0.75*s,-0.75*s,-1.25*s,-1.25*s,-1.75*s,-1.75*s,-2*s])
            x1=x*cossj-y*sinsj+xj-2*s*cossj-r*cos
            y1=x*sinsj+y*cossj+yj-2*s*sinsj-r*sin
            plt.plot(x1,y1,'r')
            x1=x*cossj-y*sinsj+xj+2*s*cossj-r*cos
            y1=x*sinsj+y*cossj+yj+2*s*sinsj-r*sin
            plt.plot(x1,y1,'r') 
















#画杆件号和节点号的标注
def drawannotation():
    for i in range(len(joints_)):
        joints_[i]['dj']=0
    for i in range(len(elements)):
        xi=elements[i]['pi']['x']
        yi=elements[i]['pi']['y']
        xj=elements[i]['pj']['x']
        yj=elements[i]['pj']['y']
        #xmid和ymid是放杆件编号的位置（相对位置）
        xmid=xi+(xj-xi)*0.45
        ymid=yi+(yj-yi)*0.45
        #找到杆件的角度，正方向旋转90，根据这个角度把各种标注进行适当移动
        alpz=(elements[i]['alp']+90)/180*3.14159
        sin=np.sin(alpz)
        cos=np.cos(alpz)
        #写杆件编号
        plt.text(xmid+1.5*s*cos,ymid+1.5*s*sin,'('+str(i+1)+')',fontsize=35,family='fantasy') 
        plt.scatter(x=xmid+1.5*s*cos,y=ymid+1.5*s*sin,color='',edgecolor='')          
        if xi!=xj:
            #参数方程来表达一条直线，那么每个比例点都可以找到相应的X，Y坐标
            kl=(yj-yi)/(xj-xi)
            b=yi
            xis=s+xi+0.02*cos
            yis=kl*s+b+0.02*sin
            xjs=(xj-xi)-s+xi+0.02*cos
            yjs=kl*(xj-xi-s)+b+0.02*sin
            #写点的编号
            if elements[i]['pi']['dj']<1:
                plt.text(xis,yis,int(elements[i]['pi']['num']),fontsize=35,c='b',family='fantasy')
                plt.scatter(x=xis,y=yis,color='',edgecolor='')    
                elements[i]['pi']['dj']+=1
            if elements[i]['pj']['dj']<1:
                plt.text(xjs,yjs,int(elements[i]['pj']['num']),fontsize=35,c='b',family='fantasy')
                plt.scatter(x=xjs,y=yjs,color='',edgecolor='')
                elements[i]['pj']['dj']+=1
        else:
            xis=xi+s*cos
            yis=yi+0.07*np.sin(elements[i]['alp']/180*3.14159)
            xjs=xj-s*cos
            yjs=(yj-yi)+yi-0.07*np.sin(elements[i]['alp']/180*3.14159)
            if elements[i]['pi']['dj']<1:
                plt.text(xis,yis,int(elements[i]['pi']['num']),fontsize=35,c='b',family='fantasy')
                plt.scatter(x=xis,y=yis,color='',edgecolor='')
                elements[i]['pi']['dj']+=1
            if elements[i]['pj']['dj']<1:
                plt.text(xjs,yjs,int(elements[i]['pj']['num']),fontsize=35,c='b',family='fantasy')
                plt.scatter(x=xjs,y=yjs,color='',edgecolor='')
                elements[i]['pj']['dj']+=1




#在力学计算方面信息的导入
def file():
    caljoints=[]
    #中间项，有重复的节点
    global caljoints_,calelements
    caljoints_=[]
    #无重复项
    caljoint={}
    #杆件存储在一个列表里
    calelements=[]
    element={}
    for i in range(len(informatrixs[0])):
        caljoint['num']=int(informatrixs[0][0][i])
        caljoint['x']=informatrixs[0][1][i]
        caljoint['y']=informatrixs[0][2][i]
        caljoint['connection']=informatrixs[0][3][i]
        caljoint['restraint']=0
        caljoint['r']=[0,0,0]
        caljoint['displacement']=[0,0,0]
        caljoint['Fx']=0
        caljoint['Fy']=0
        caljoint['M']=0
        caljoint['PEx']=0
        caljoint['PEy']=0
        caljoint['PEM']=0
        caljoint['salp']=0
        #弹性支座的转角ealp
        caljoint['esupport']=0
        caljoint['ealp']=0
        caljoint['k']=0
        caljoints.append(caljoint.copy())
    #去重，去掉重复的节点
    for i in caljoints:
        if i  not in caljoints_:
            caljoints_.append(i)
    #将节点按照编号排序
    for j in range(len(caljoints_)):
        for k in range(len(caljoints_)):
            t={}
            if caljoints_[j]['num']<caljoints_[k]['num']:
                t=caljoints_[j]
                caljoints_[j]=caljoints_[k]
                caljoints_[k]=t.copy()
    for i in range(len(informatrixs[8])):
        caljoints_[int(informatrixs[8][0][i]-1)]['esupport']=int(informatrixs[8][1][i])
        caljoints_[int(informatrixs[8][0][i]-1)]['ealp']=int(informatrixs[8][2][i])
        caljoints_[int(informatrixs[8][0][i]-1)]['k']=int(informatrixs[8][3][i])
    for i in range(len(informatrixs[2])):
        caljoints_[int(informatrixs[2][0][i]-1)]['restraint']=int(informatrixs[2][1][i])
        caljoints_[int(informatrixs[2][0][i]-1)]['salp']=int(int(informatrixs[2][2][i]))
    for i in range(len(informatrixs[3])):
        caljoints_[int(informatrixs[3][0][i]-1)]['Fx']=int(informatrixs[3][1][i])
        caljoints_[int(informatrixs[3][0][i]-1)]['Fy']=int(informatrixs[3][2][i])
        caljoints_[int(informatrixs[3][0][i]-1)]['M']=int(informatrixs[3][3][i])
    #存储杆件信息
    for i in range(len(informatrixs[1])):
       element['num']=informatrixs[1][0][i]
       element['pi']=caljoints_[int(informatrixs[1][1][i]-1)]
       element['pj']=caljoints_[int(informatrixs[1][2][i]-1)]
       if (element['pj']['x']-element['pi']['x'])!=0:
           element['alp']=int(np.arctan2((element['pj']['y']-element['pi']['y']),(element['pj']['x']-element['pi']['x']))/3.14159*180)
       else:
           if (element['pj']['y']-element['pi']['y'])>=0:
               element['alp']=90
           else:
               element['alp']=-90
       element['l']=np.sqrt((element['pj']['y']-element['pi']['y'])**2+(element['pj']['x']-element['pi']['x'])**2)
       if informatrixs[1][3][i]==-1:
           element['EA']=1e8
       else:
           element['EA']=informatrixs[1][3][i]
       if informatrixs[1][4][i]==-1: 
           element['EI']=1e6
       else:
           element['EI']=informatrixs[1][4][i]
       element['PExi']=0
       element['PEyi']=0
       element['PEMi']=0
       element['PExj']=0
       element['PEyj']=0
       element['PEMj']=0
       calelements.append(element.copy())
    #自由度
    #节点编码过程（注释在caljoints noding里）

#改变杆件的刚度，给一个双重列表，每个小列表的第一个参数的杆件编号，后面两个是EA和EI
def changeEAI(infor):
    for i in range((len(infor))):
        if infor[i][1]==-1:
            calelements[infor[i][0]-1]['EA']=1e8
        else:
            calelements[infor[i][0]-1]['EA']=infor[i][1]
        if infor[i][2]==-1:
            calelements[infor[i][0]-1]['EI']=1e6
        else:
            calelements[infor[i][0]-1]['EI']=infor[i][2]

#展示难度，1-5星，在excel题目的最前端添加数字1-5
def shownandu():
    global Qnum
    file1 = xlrd.open_workbook('excel/question1.xlsx')
    sheets = file1.sheet_names()
    nd=sheets[Qnum][0]
    if nd=='1':
        return 1
    elif nd=='2':
        return 2
    elif nd=='3':
        return 3
    elif nd=='4':
        return 4
    elif nd=='5':
        return 5
    else:
        return 0



#显示刚度
def showEAIL():
    global EAIL
    EAIL=[]
    for i in range(len(calelements)):
        EAI_=[]
        EAI_.append(calelements[i]['num'])
        EAI_.append(calelements[i]['l'])
        if calelements[i]['EA']>=1e8:
            EAI_.append(-1)
        else:
            EAI_.append(calelements[i]['EA'])
        if calelements[i]['EI']>=1e6:
            EAI_.append(-1)
        else:
            EAI_.append(calelements[i]['EI'])  
        EAIL.append(EAI_.copy())
    return EAIL

#计算程序
def calculationdof():
        global dof
        dof=1
        for j_ in range(len(calelements)):
            if calelements[j_]['pi']['r'][0]==0 and calelements[j_]['pi']['r'][1]==0 and calelements[j_]['pi']['r'][2]==0 :
                if calelements[j_]['pi']['connection']==1 and calelements[j_]['pi']['restraint']==0:
                    calelements[j_]['pi']['r'][0]=dof
                    dof=dof+1
                    calelements[j_]['pi']['r'][1]=dof
                    dof=dof+1
                    if calelements[j_]['pi']['num'] not in jys:
                        calelements[j_]['pi']['r'][2]=dof
                        dof=dof+1
                    for jt in range(len(caljoints_)):
                         if math.isclose(caljoints_[jt]['x'], calelements[j_]['pi']['x'], abs_tol=1e-5):
                             if math.isclose(caljoints_[jt]['y'], calelements[j_]['pi']['y'], abs_tol=1e-5):
                                 if caljoints_[jt]['r'][0]==0 and caljoints_[jt]['r'][1]==0:
                                     caljoints_[jt]['r'][0]=calelements[j_]['pi']['r'][0]
                                     caljoints_[jt]['r'][1]=calelements[j_]['pi']['r'][1]
                if calelements[j_]['pi']['connection']==1 and calelements[j_]['pi']['restraint']==1:
                        calelements[j_]['pi']['r'][0]=dof
                        dof=dof+1
                        if calelements[j_]['pi']['num'] not in jys:
                            calelements[j_]['pi']['r'][2]=dof
                            dof=dof+1
                if calelements[j_]['pi']['connection']==1 and calelements[j_]['pi']['restraint']==2:
                    if calelements[j_]['pi']['num'] not in jys:
                        calelements[j_]['pi']['r'][2]=dof
                        dof=dof+1
                if calelements[j_]['pi']['connection']==1 and calelements[j_]['pi']['restraint']==3:
                        calelements[j_]['pi']['r'][0]=dof
                        dof=dof+1
                if calelements[j_]['pi']['connection']==0 and calelements[j_]['pi']['restraint']==0 :
                     calelements[j_]['pi']['r'][0]=dof
                     dof=dof+1
                     calelements[j_]['pi']['r'][1]=dof
                     dof=dof+1
                     if calelements[j_]['pi']['num'] not in jys:
                         calelements[j_]['pi']['r'][2]=dof
                         dof=dof+1
                     for jt in range(len(caljoints_)):
                         if math.isclose(caljoints_[jt]['x'], calelements[j_]['pi']['x'], abs_tol=1e-5):
                             if math.isclose(caljoints_[jt]['y'], calelements[j_]['pi']['y'], abs_tol=1e-5):
                                 if caljoints_[jt]['r'][0]==0 and caljoints_[jt]['r'][1]==0:
                                     caljoints_[jt]['r'][0]=calelements[j_]['pi']['r'][0]
                                     caljoints_[jt]['r'][1]=calelements[j_]['pi']['r'][1]
                if calelements[j_]['pi']['connection']==0 and calelements[j_]['pi']['restraint']==1 :
                     calelements[j_]['pi']['r'][0]=dof
                     dof=dof+1
                     if calelements[j_]['pi']['num'] not in jys:
                         calelements[j_]['pi']['r'][2]=dof
                         dof=dof+1
                     for jt in range(len(caljoints_)):
                         if math.isclose(caljoints_[jt]['x'], calelements[j_]['pi']['x'], rel_tol=1e-5):
                             if math.isclose(caljoints_[jt]['y'], calelements[j_]['pi']['y'], rel_tol=1e-5):
                                 if caljoints_[jt]['r'][0]==0 & caljoints_[jt]['r'][1]==0:
                                     caljoints_[jt]['r'][0]=calelements[j_]['pi']['r'][0]
                if calelements[j_]['pi']['connection']==0 and calelements[j_]['pi']['restraint']==2 :
                    if calelements[j_]['pi']['num'] not in jys: 
                        calelements[j_]['pi']['r'][2]=dof
                        dof=dof+1           
            if calelements[j_]['pi']['r'][0]!=0 and calelements[j_]['pi']['r'][1]!=0 and calelements[j_]['pi']['r'][2]==0 :
                if calelements[j_]['pi']['num'] not in jys:
                    calelements[j_]['pi']['r'][2]=dof
                    dof=dof+1
            if calelements[j_]['pj']['r'][0]==0 and calelements[j_]['pj']['r'][1]==0 and calelements[j_]['pj']['r'][2]==0 :
                if calelements[j_]['pj']['connection']==1 and calelements[j_]['pj']['restraint']==0:
                    calelements[j_]['pj']['r'][0]=dof
                    dof=dof+1
                    calelements[j_]['pj']['r'][1]=dof
                    dof=dof+1
                    if calelements[j_]['pj']['num'] not in jys:
                        calelements[j_]['pj']['r'][2]=dof
                        dof=dof+1
                    for jt_ in range(len(caljoints_)):
                         if math.isclose(caljoints_[jt_]['x'], calelements[j_]['pj']['x'], abs_tol=1e-5):
                             if math.isclose(caljoints_[jt_]['y'], calelements[j_]['pj']['y'], abs_tol=1e-5):
                                 if caljoints_[jt_]['r'][0]==0 and caljoints_[jt_]['r'][1]==0:
                                     caljoints_[jt_]['r'][0]=calelements[j_]['pj']['r'][0]
                                     caljoints_[jt_]['r'][1]=calelements[j_]['pj']['r'][1]
                if calelements[j_]['pj']['connection']==1 and calelements[j_]['pj']['restraint']==1:
                        calelements[j_]['pj']['r'][0]=dof
                        dof=dof+1
                        if calelements[j_]['pj']['num'] not in jys:
                            calelements[j_]['pj']['r'][2]=dof
                            dof=dof+1
                if calelements[j_]['pj']['connection']==1 and calelements[j_]['pj']['restraint']==2:
                    if calelements[j_]['pj']['num'] not in jys:
                        calelements[j_]['pj']['r'][2]=dof
                        dof=dof+1
                if calelements[j_]['pj']['connection']==1 and calelements[j_]['pj']['restraint']==3:
                        calelements[j_]['pj']['r'][0]=dof
                        dof=dof+1
                if calelements[j_]['pj']['connection']==0 and calelements[j_]['pj']['restraint']==0 :
                     calelements[j_]['pj']['r'][0]=dof
                     dof=dof+1
                     calelements[j_]['pj']['r'][1]=dof
                     dof=dof+1
                     if calelements[j_]['pj']['num'] not in jys:
                         calelements[j_]['pj']['r'][2]=dof
                         dof=dof+1
                     for jt_ in range(len(caljoints_)):
                         if math.isclose(caljoints_[jt_]['x'], calelements[j_]['pj']['x'], abs_tol=1e-5):
                             if math.isclose(caljoints_[jt_]['y'], calelements[j_]['pj']['y'], abs_tol=1e-5):
                                 if caljoints_[jt_]['r'][0]==0 and caljoints_[jt_]['r'][1]==0:
                                     caljoints_[jt_]['r'][0]=calelements[j_]['pj']['r'][0]
                                     caljoints_[jt_]['r'][1]=calelements[j_]['pj']['r'][1]
                if calelements[j_]['pj']['connection']==0 and calelements[j_]['pj']['restraint']==1 :
                     calelements[j_]['pj']['r'][0]=dof
                     dof=dof+1
                     if calelements[j_]['pj']['num'] not in jys:
                         calelements[j_]['pj']['r'][2]=dof
                         dof=dof+1
                     for jt in range(len(caljoints_)):
                         if math.isclose(caljoints_[jt]['x'], calelements[j_]['pj']['x'], abs_tol=1e-5):
                             if math.isclose(caljoints_[jt]['y'], calelements[j_]['pj']['y'], abs_tol=1e-5):
                                 if caljoints_[jt]['r'][0]==0 & caljoints_[jt]['r'][1]==0:
                                     caljoints_[jt]['r'][0]=calelements[j_]['pj']['r'][0]
                if calelements[j_]['pj']['connection']==0 and calelements[j_]['pj']['restraint']==2 :
                     if calelements[j_]['pj']['num'] not in jys:
                        calelements[j_]['pj']['r'][2]=dof
                        dof=dof+1           
            if calelements[j_]['pj']['r'][0]!=0 and calelements[j_]['pj']['r'][1]!=0 and calelements[j_]['pj']['r'][2]==0 :
                if calelements[j_]['pj']['num'] not in jys:
                    calelements[j_]['pj']['r'][2]=dof
                    dof=dof+1
        dof=dof-1
    
def calculation():    
    global jys,oldelementnums
    calculationdof()
    jhfx()
    if duoyuyueshu<0:
        return 0
    #T,和T_为局部坐标系和x，y方向的转换矩阵
    #当支座有转角时，需要将局部坐标转换到支座方向和其垂直方向进行运算，Ts和Ts_这这种情况的转换矩阵
    T=[]   
    T_=[]
    Ts=[]
    Ts_=[]
    #Ttan和Ttan_可以把弹簧方向的刚度转换到整体坐标系下
    Ttan=[]
    Ttan_=[]
    #存储每个杆件刚度矩阵的列表
    #Ke存储整体坐标系下的刚度矩阵，删除不需要的行与列，Ke_为局部坐标系下的刚度矩阵
    Ke=[]
    Ke_=[]
    Kee=[]
    #kz存储整体坐标系下的每个杆件的刚度矩阵（不删除编号为0的行与列）
    kz=[]
    for i in range(len(calelements)):
        alp12=calelements[i]['alp']/180*3.141592653
        sin=round(np.sin(alp12),4)
        cos=round(np.cos(alp12),4)
        t=pd.DataFrame(np.zeros((6,6)))
        t.loc[0,0]=cos
        t.loc[0,1]=sin
        t.loc[1,0]=sin*-1
        t.loc[1,1]=cos
        t.loc[2,2]=1
        t.loc[3,3]=cos
        t.loc[3,4]=sin
        t.loc[4,3]=sin*-1
        t.loc[4,4]=cos
        t.loc[5,5]=1
        T.append(t.copy())
        T_.append(t.T.copy())
    for i in range(len(calelements)):
        alp1=calelements[i]['pi']['ealp']/180*3.1415926
        sini=round(np.sin(alp1),4)
        cosi=round(np.cos(alp1),4)
        alp2=calelements[i]['pj']['ealp']/180*3.1415926
        sinj=round(np.sin(alp2),4)
        cosj=round(np.cos(alp2),4)
        t=pd.DataFrame(np.zeros((6,6)))
        t.loc[0,0]=cosi
        t.loc[0,1]=sini
        t.loc[1,0]=sini*-1
        t.loc[1,1]=cosi
        t.loc[2,2]=1
        t.loc[3,3]=cosj
        t.loc[3,4]=sinj
        t.loc[4,3]=sinj*-1
        t.loc[4,4]=cosj
        t.loc[5,5]=1
        Ttan.append(t.copy())
        Ttan_.append(t.T.copy())
    #print(calelements[0]['pi']['restraint'])
    #编写Ts和Ts_
    for i in range(len(calelements)):
        ts=np.eye(6)
        if calelements[i]['pi']['restraint']==1:
            th=calelements[i]['pi']['salp']/180*3.141592653
            sin=np.sin(th)
            cos=np.cos(th)
            ts[0][0]=cos
            ts[0][1]=sin
            ts[1][0]=-1*sin
            ts[1][1]=cos
        if calelements[i]['pi']['restraint']==3:
            th=calelements[i]['pi']['salp']/180*3.1415953
            sin=np.sin(th)
            cos=np.cos(th)
            ts[0][0]=cos
            ts[0][1]=sin
            ts[1][0]=-1*sin
            ts[1][1]=cos
        if calelements[i]['pj']['restraint']==1:
            th=calelements[i]['pj']['salp']/180*3.141592653
            sin=np.sin(th)
            cos=np.cos(th)
            ts[3][3]=cos
            ts[3][4]=sin
            ts[4][3]=-1*sin
            ts[4][4]=cos   
        if calelements[i]['pj']['restraint']==3:
            th=calelements[i]['pj']['salp']/180*3.141592653
            sin=np.sin(th)
            cos=np.cos(th)
            ts[3][3]=cos
            ts[3][4]=sin
            ts[4][3]=-1*sin
            ts[4][4]=cos
        Ts.append(ts.copy())
        Ts_.append(ts.T.copy())
    #刚度矩阵
    for i in range(len(calelements)):
        EA=calelements[i]['EA']
        EI=calelements[i]['EI']
        L=calelements[i]['l']
        k=pd.DataFrame([[EA/L,0,0,-EA/L,0,0],
                   [0,12*EI/np.power(L,3),6*EI/np.power(L,2),0,
                    -12*EI/np.power(L,3),6*EI/np.power(L,2)],
                   [0,6*EI/L**2,4*EI/L,0,-6*EI/L**2,2*EI/L],
                   [-EA/L,0,0,EA/L,0,0],
                   [0,-12*EI/(L**3),-6*EI/L**2,0,12*EI/L**3,-6*EI/L**2],
                   [0,6*EI/L**2,2*EI/L,0,-6*EI/L**2,4*EI/L]],
                   index=calelements[i]['pi']['r']+calelements[i]['pj']['r'],
                   columns=calelements[i]['pi']['r']+calelements[i]['pj']['r'])
        Ke_.append(k.copy())
    #ktan存储整体坐标系下由弹性支座的刚度组成的矩阵，ktan_存储局部坐标系下弹性支座的刚度组成的矩阵
    ktan_=[]
    ktan=[]
    for i in range(len(calelements)):
        kt=np.zeros((6,6))
#        if table.cell(i+1,13).value==1:
#            kt[1][1]=table.cell(i+1,14).value
#        if table.cell(i+1,13).value==2:
#            kt[2][2]=table.cell(i+1,14).value
#        if table.cell(i+1,15).value==1:
#            kt[4][4]=table.cell(i+1,16).value
#        if table.cell(i+1,15).value==2:
#            kt[5][5]=table.cell(i+1,16).value
        if calelements[i]['pi']['esupport']==1:
            kt[1][1]=calelements[i]['pi']['k']
        if calelements[i]['pi']['esupport']==2:
            kt[2][2]=calelements[i]['pi']['k']
        if calelements[i]['pj']['esupport']==1:
            kt[4][4]=calelements[i]['pj']['k']
        if calelements[i]['pj']['esupport']==2:
            kt[5][5]=calelements[i]['pj']['k']
        ktan_.append(kt.copy())
    
    #将节点荷载转换坐标，以整体坐标的形式交给节点
    def tfiy(t1,t2):
        t1=0.5*(t1**4)-t1**3+t1
        t2=0.5*(t2**4)-t2**3+t2
        return(t2-t1)
        #temporary fiy 
    def tfjy(t1,t2):
        t1=t1**3-0.5*t1**4
        t2=t2**3-0.5*t2**4
        return(t2-t1)
    def tfix(t1,t2):
        t1=t1-0.5*t1**2
        t2=t2-0.5*t2**2
        return(t2-t1)
    def tfjx(t1,t2):
        t1=0.5*t1**2
        t2=0.5*t2**2
        return(t2-t1)
    def tmi(t1,t2):
        t1=1/12*(6*t1**2-8*t1**3+3*t1**4)
        t2=1/12*(6*t2**2-8*t2**3+3*t2**4)
        return(t2-t1)
    def tmj(t1,t2):
        t1=1/12*(4*t1**3-3*t1**4)
        t2=1/12*(4*t2**3-3*t2**4)
        return(t2-t1)
    if (zdc!=1 and fdc!=1) or switchbjg==0:
        for i in range(len(calelements)):
            fix=0
            fiy=0
            mi=0
            fjx=0
            fjy=0
            mj=0
            EA=calelements[i]['EA']
            EI=calelements[i]['EI']
            l=calelements[i]['l']
            if len(informatrixs[4])>0:
                if i+1 in list(informatrixs[4][0]):
                    for j in range(len(informatrixs[4])):
                        if i+1==informatrixs[4][0][j]:
                            f=informatrixs[4][1][j]
                            alg=informatrixs[4][2][j]
                            positions=informatrixs[4][3][j]
                            #position+start简写posintions，开始点
                            sin=round(np.sin(alg/180*np.pi),4)
                            cos=round(np.cos(alg/180*np.pi),4)
                            fiy+=-1*f*sin*(1-positions)**2*(1+2*positions)
                            fjy+=-1*f*sin*positions**2*(3-2*positions)
                            fix+=-1*f*cos*(1-positions)
                            fjx+=-1*f*cos*positions
                            mi+=-1*f*l*sin*positions*(1-positions)**2
                            mj+=f*sin*positions**2*(1-positions)*l
            if len(informatrixs[5])>0:
                if i+1 in list(informatrixs[5][0]):
                    for j in range(len(informatrixs[5])):
                        if i+1==informatrixs[5][0][j]:
                            q=informatrixs[5][1][j]
                            alg=informatrixs[5][2][j]
                            ps=informatrixs[5][3][j]
                            pe=informatrixs[5][4][j]
                            #position+start简写posintions，开始点
                            sin=round(np.sin(alg/180*np.pi),4)
                            cos=round(np.cos(alg/180*np.pi),4)
                            #tt开头均为中间值，得到一个Q下的值
                            ttfiy=tfiy(ps,pe)*q*sin*l*-1
                            ttfjy=tfjy(ps,pe)*q*sin*l*-1
                            ttfix=tfix(ps,pe)*q*cos*l*-1
                            ttfjx=tfjx(ps,pe)*q*cos*l*-1
                            ttmi=tmi(ps,pe)*q*sin*l*l*-1
                            ttmj=tmj(ps,pe)*q*sin*l*l
                            #累加
                            fiy+=ttfiy
                            fjy+=ttfjy
                            fix+=ttfix
                            fjx+=ttfjx
                            mi+=ttmi
                            mj+=ttmj

            if len(informatrixs[6])>0:
                if i+1 in list(informatrixs[6][0]):
                    for j in range(len(informatrixs[6])):
                        if i+1==informatrixs[6][0][j]:
                            alpt=informatrixs[6][1][j]
                            t1=informatrixs[6][2][j]
                            t2=informatrixs[6][3][j]
                            h=informatrixs[6][4][j]
                            t0=(t1+t2)/2
                            dt=t1-t2
                            fix+=EA*alpt*t0
                            fjx+=-EA*alpt*t0
                            mi+=-1*EI*alpt/h*dt
                            mj+=EI*alpt/h*dt
            if len(informatrixs[7])>0:
                if i+1 in list(informatrixs[7][0]):
                    for j in range(len(informatrixs[7])):
                        if i+1==informatrixs[7][0][j]:
                            delta=[]
                            delta.append(informatrixs[7][1][j])
                            delta.append(informatrixs[7][2][j])
                            delta.append(informatrixs[7][3][j])
                            delta.append(informatrixs[7][4][j])
                            delta.append(informatrixs[7][5][j])
                            delta.append(informatrixs[7][6][j])
                            delta=np.array(delta)
                            delta=delta[:,np.newaxis]
                            k1=np.dot(T_[i],Ke_[i])
                            k=np.dot(k1,T[i])
                            Fs=np.dot(k,delta)
                            Fs=np.dot(T[i],Fs)
                            #如果支座有转角会转化为支座方向的刚度矩阵，没有的话，杆件整体刚度矩阵不会变
                            fix+=float(Fs[0])
                            fiy+=float(Fs[1])
                            mi+=float(Fs[2])
                            fjx+=float(Fs[3])
                            fjy+=float(Fs[4])
                            mj+=float(Fs[5])

            fff=np.array([fix,fiy,mi,fjx,fjy,mj])
            fff=fff[:,np.newaxis]
            #将力转化为整体坐标，再写入另一个表格
            fff=np.dot(T_[i],fff)
            calelements[i]['PExi']+=-1*float(fff[0])
            calelements[i]['PEyi']+=-1*float(fff[1])
            calelements[i]['PEMi']+=-1*float(fff[2])
            calelements[i]['PExj']+=-1*float(fff[3])
            calelements[i]['PEyj']+=-1*float(fff[4])
            calelements[i]['PEMj']+=-1*float(fff[5])
    
    for i in range(len(calelements)):
        calelements[i]['pi']['PEx']+=calelements[i]['PExi']
        calelements[i]['pi']['PEy']+=calelements[i]['PEyi']
        calelements[i]['pi']['PEM']+=calelements[i]['PEMi']
        calelements[i]['pj']['PEx']+=calelements[i]['PExj']
        calelements[i]['pj']['PEy']+=calelements[i]['PEyj']
        calelements[i]['pj']['PEM']+=calelements[i]['PEMj']

        
    for i in range(len(calelements)):
        Ft=[]
        Ft.append(calelements[i]['pi']['Fx'])
        Ft.append(calelements[i]['pi']['Fy'])
        Ft.append(calelements[i]['pi']['M'])
        Ft.append(calelements[i]['pj']['Fx'])
        Ft.append(calelements[i]['pj']['Fy'])
        Ft.append(calelements[i]['pj']['M'])
        Ft=np.array(Ft)
        Ft=Ft[:,np.newaxis]
        Ft=np.dot(Ts[i],Ft)

        calelements[i]['pi']['Fx']=float(Ft[0])
        calelements[i]['pi']['Fy']=float(Ft[1])
        calelements[i]['pi']['M']=float(Ft[2])
        calelements[i]['pj']['Fx']=float(Ft[3])
        calelements[i]['pj']['Fy']=float(Ft[4])
        calelements[i]['pj']['M']=float(Ft[5])
        Ft=[]
        Ft.append(calelements[i]['pi']['PEx'])
        Ft.append(calelements[i]['pi']['PEy'])
        Ft.append(calelements[i]['pi']['PEM'])
        Ft.append(calelements[i]['pj']['PEx'])
        Ft.append(calelements[i]['pj']['PEy'])
        Ft.append(calelements[i]['pj']['PEM'])
        Ft=np.array(Ft)
        Ft=Ft[:,np.newaxis]
        Ft=np.dot(Ts[i],Ft)

        calelements[i]['pi']['PEx']=float(Ft[0])
        calelements[i]['pi']['PEy']=float(Ft[1])
        calelements[i]['pi']['PEM']=float(Ft[2])
        calelements[i]['pj']['PEx']=float(Ft[3])
        calelements[i]['pj']['PEy']=float(Ft[4])
        calelements[i]['pj']['PEM']=float(Ft[5])
    #局部坐标的刚度矩阵转换变为整体坐标的刚度矩阵
    for i in range(len(calelements)):
        #局部坐标的刚度矩阵转换变为整体坐标的刚度矩阵
        k1=np.dot(T_[i],Ke_[i])
        k=np.dot(k1,T[i])
        kz.append(k.copy())
        #如果支座有转角会转化为支座方向的刚度矩阵，没有的话，杆件整体刚度矩阵不会变
        k=np.dot(Ts[i],k)
        k=np.dot(k,Ts_[i])
        k_=pd.DataFrame(k,index=calelements[i]['pi']['r']+calelements[i]['pj']['r'],
                        columns=calelements[i]['pi']['r']+calelements[i]['pj']['r'])
        #去掉自由度编号为0的行与列
        if 0 in k_.index:
            k_=k_.drop([0],axis=1).drop([0])
        Ke.append(k_.copy())
    #大的刚度矩阵，按照自由度个数来设置行与列
    for i in range(len(calelements)):
        k2=np.dot(Ttan_[i],ktan_[i])
        k2=np.dot(k2,Ttan[i])
        k2=np.dot(Ts[i],k2)
        k2=np.dot(k2,Ts_[i])
        k3=pd.DataFrame(k2,index=calelements[i]['pi']['r']+calelements[i]['pj']['r'],
                        columns=calelements[i]['pi']['r']+calelements[i]['pj']['r'])
        if 0 in k3.index:
            k3=k3.drop([0],axis=1).drop([0])
        ktan.append(k3.copy())    
    K=pd.DataFrame(np.zeros((dof,dof)),index=range(1,dof+1),columns=range(1,dof+1))
    #kf为由弹性支座组成的集合大矩阵，先给它附一个值ktan【0】
    kf=ktan[0]
    #刚度矩阵集合
    for k in Ke:
        K=(K.add(k,fill_value=0)).fillna(0)
    #由于弹性支座跟随杆件，因此特殊情况下会被算多次，不可以用杆件的集合方式集合kf
    for k in ktan[1:]:
        #纵向合并，nan的部分填充0,列号会合并
        kf=(pd.concat([kf,k],join='outer')).fillna(0)
        #行号有重复，去掉重复的行（所有重复的行内容是一致的），最终得到大的Kf
        kf=(kf[~kf.index.duplicated(keep='first')]).fillna(0)
    #把K理解成杆件组成的大矩阵和弹性支座组成的大矩阵的和
    K=(K.add(kf,fill_value=0)).fillna(0)
    P=np.zeros((dof,1))

    #按照自由度，和节点荷载，和等效荷载分别放入
    for i in range(len(caljoints_)):
        if caljoints_[i]['r'][0]!=0:
            P[caljoints_[i]['r'][0]-1][0]=caljoints_[i]['Fx']
        if caljoints_[i]['r'][1]!=0:
            P[caljoints_[i]['r'][1]-1][0]=caljoints_[i]['Fy']
        if caljoints_[i]['r'][2]!=0:
            P[caljoints_[i]['r'][2]-1][0]=caljoints_[i]['M']
    for i in range(len(caljoints_)):
        if caljoints_[i]['r'][0]!=0:
            P[caljoints_[i]['r'][0]-1][0]+=caljoints_[i]['PEx']
        if caljoints_[i]['r'][1]!=0:
            P[caljoints_[i]['r'][1]-1][0]+=caljoints_[i]['PEy']
        if caljoints_[i]['r'][2]!=0:
            P[caljoints_[i]['r'][2]-1][0]+=caljoints_[i]['PEM']
    x=np.dot(np.linalg.inv(K),P)
    print(x)
    #放位移给节点
    for i in range(len(caljoints_)):
        if caljoints_[i]['r'][0]!=0:
            caljoints_[i]['displacement'][0]+=x[caljoints_[i]['r'][0]-1][0]
        if caljoints_[i]['r'][1]!=0:
            caljoints_[i]['displacement'][1]+=x[caljoints_[i]['r'][1]-1][0]
        if caljoints_[i]['r'][2]!=0:
            caljoints_[i]['displacement'][2]+=x[caljoints_[i]['r'][2]-1][0]
    #放位移给杆件（通过节点）
    for i in range(len(calelements)):
        tdisplacement=[]
        tdisplacement.append(calelements[i]['pi']['displacement'][0])
        tdisplacement.append(calelements[i]['pi']['displacement'][1])
        tdisplacement.append(calelements[i]['pi']['displacement'][2])
        tdisplacement.append(calelements[i]['pj']['displacement'][0])
        tdisplacement.append(calelements[i]['pj']['displacement'][1])
        tdisplacement.append(calelements[i]['pj']['displacement'][2])
        tdisplacement=np.array(tdisplacement)
        tdisplacement=tdisplacement[:,np.newaxis]
        tdisplacement=np.dot(Ts_[i],tdisplacement)
        calelements[i]['pi']['displacement'][0]=float(tdisplacement[0])
        calelements[i]['pi']['displacement'][1]=float(tdisplacement[1])
        calelements[i]['pi']['displacement'][2]=float(tdisplacement[2])
        calelements[i]['pj']['displacement'][0]=float(tdisplacement[3])
        calelements[i]['pj']['displacement'][1]=float(tdisplacement[4])
        calelements[i]['pj']['displacement'][2]=float(tdisplacement[5])    
#    new_excel=xlwt.Workbook()
#    new_sheet=new_excel.add_sheet('0')
#    new_sheet.write(0,table.ncols,'Pix')
#    new_sheet.write(0,table.ncols+1,'Piy')
#    new_sheet.write(0,table.ncols+2,'PMi')
#    new_sheet.write(0,table.ncols+3,'Pjx')
#    new_sheet.write(0,table.ncols+4,'Pjy')
#    new_sheet.write(0,table.ncols+5,'PMj')
#    new_sheet.write(0,36,'NI')
#    new_sheet.write(0,37,'FYI')
#    new_sheet.write(0,38,'MI')
#    new_sheet.write(0,39,'NJ')
#    new_sheet.write(0,40,'FYJ')
#    new_sheet.write(0,41,'MJ')
    for i in range(len(calelements)):
        ttdisplacement=[]
        ttdisplacement.append(float(calelements[i]['pi']['displacement'][0]))
        ttdisplacement.append(float(calelements[i]['pi']['displacement'][1]))
        ttdisplacement.append(float(calelements[i]['pi']['displacement'][2]))
        ttdisplacement.append(float(calelements[i]['pj']['displacement'][0]))
        ttdisplacement.append(float(calelements[i]['pj']['displacement'][1]))
        ttdisplacement.append(float(calelements[i]['pj']['displacement'][2]))
        ttdisplacement=np.array(ttdisplacement)
        ttdisplacement=ttdisplacement[:,np.newaxis]
        Fresult=np.dot(kz[i],ttdisplacement)
        Fresult[0]=float(Fresult[0])-calelements[i]['PExi']
        Fresult[1]=float(Fresult[1])-calelements[i]['PEyi']
        Fresult[2]=float(Fresult[2])-calelements[i]['PEMi']
        Fresult[3]=float(Fresult[3])-calelements[i]['PExj']
        Fresult[4]=float(Fresult[4])-calelements[i]['PEyj']
        Fresult[5]=float(Fresult[5])-calelements[i]['PEMj']
        Fresult=np.dot(T[i],Fresult)
        calelements[i]['NI']=float(Fresult[0])*-1
        calelements[i]['FYI']=float(Fresult[1])
        calelements[i]['MI']=float(Fresult[2])*-1
        calelements[i]['NJ']=float(Fresult[3])
        calelements[i]['FYJ']=float(Fresult[4])*-1
        calelements[i]['MJ']=float(Fresult[5])
    global displace
    displace=[]
    for i in range(len(calelements)):
        tdisplacement=[]
        tdisplacement.append(calelements[i]['pi']['displacement'][0])
        tdisplacement.append(calelements[i]['pi']['displacement'][1])
        tdisplacement.append(calelements[i]['pi']['displacement'][2])
        tdisplacement.append(calelements[i]['pj']['displacement'][0])
        tdisplacement.append(calelements[i]['pj']['displacement'][1])
        tdisplacement.append(calelements[i]['pj']['displacement'][2])
        tdisplacement=np.array(tdisplacement)
        tdisplacement=tdisplacement[:,np.newaxis]
        tdisplacement=np.dot(T[i],tdisplacement)
        tt=[]
        tt.append(float(tdisplacement[0]))
        tt.append(float(tdisplacement[1]))
        tt.append(float(tdisplacement[2]))
        tt.append(float(tdisplacement[3]))
        tt.append(float(tdisplacement[4]))
        tt.append(float(tdisplacement[5]))
        displace.append(tt)
    for i in range(len(informatrixs[7])):
        if i+1 in list(informatrixs[7][0]):
            for j in range(len(informatrixs[7])):
                if i+1==informatrixs[7][0][j]:
                        delta=[]
                        delta.append(informatrixs[7][1][j])
                        delta.append(informatrixs[7][2][j])
                        delta.append(informatrixs[7][3][j])
                        delta.append(informatrixs[7][4][j])
                        delta.append(informatrixs[7][5][j])
                        delta.append(informatrixs[7][6][j])
                        delta=np.array(delta)
                        delta=np.dot(T[i],delta)
                        displace[i][0]+=float(delta[0])
                        displace[i][1]+=float(delta[1])
                        displace[i][2]+=float(delta[2])
                        displace[i][3]+=float(delta[3])
                        displace[i][4]+=float(delta[4])
                        displace[i][5]+=float(delta[5])
    return 1




#jhfx几何分析确定是不是静定结构
def jhfx():
    global dof,duoyuyueshu
    G=pd.DataFrame(np.zeros((len(elements)*3,dof)),index=range(1,len(elements)*3+1),columns=range(1,dof+1))
    for i in range(len(elements)):
        xi=elements[i]['pi']['x']
        yi=elements[i]['pi']['y']
        xj=elements[i]['pj']['x']
        yj=elements[i]['pj']['y']
        if calelements[i]['pi']['r'][0]!=0:
            G.loc[i*3+1,calelements[i]['pi']['r'][0]]=1
        if calelements[i]['pi']['r'][1]!=0:
            G.loc[i*3+2,calelements[i]['pi']['r'][1]]=1
        if calelements[i]['pi']['r'][2]!=0:
            G.loc[i*3+3,calelements[i]['pi']['r'][2]]=1
            G.loc[i*3+1,calelements[i]['pi']['r'][2]]=yi-yj
        if calelements[i]['pj']['r'][0]!=0:
            G.loc[i*3+1,calelements[i]['pj']['r'][0]]=-1
        if calelements[i]['pj']['r'][1]!=0:
            G.loc[i*3+2,calelements[i]['pj']['r'][1]]=-1
        if calelements[i]['pj']['r'][2]!=0:
            G.loc[i*3+3,calelements[i]['pj']['r'][2]]=-1
            G.loc[i*3+2,calelements[i]['pj']['r'][2]]=xj-xi
    allzeros=1
    for j in range(G.shape[1]):
        for k in range(G.shape[0]):
            if G.iloc[k,j]!=0:
                allzeros=0

    if allzeros:
        rankG=0
        
    else:
        rankG=np.linalg.matrix_rank(G)
    print(rankG)
    duoyuyueshu=3*len(elements)-rankG
    if duoyuyueshu>0:
        print('多余约束='+'%d'%(duoyuyueshu))
    if duoyuyueshu==0:
        print('静定结构')
    global jdjg
    jdjg=0
    if duoyuyueshu==0:
        jdjg=1






#ad放大变形图的倍数
ad=5
def amplifydeformation(a):
    global ad
    ad=a*ad


#将杆件标准化，不存在跨中力且全跨可以存在分布力
#带公式，每一段的相关信息，Mi，Mj，F，N，Q都记录下来，以便以后使用，绘制内力图    
def fileinforces():
    global FIN,oldelementnums
    FIN=[]
    if (zdc!=1 and fdc!=1) or switchbjg==0:
        for i in range(len(calelements)):
            FINE=[]
            FIN.append(FINE)
        for i in range(len(informatrixs[4])):
            FINED={}
            FINED['Ftype']='F'
            FINED['Mag']=informatrixs[4][1][i]
            FINED['alp']=informatrixs[4][2][i]
            FINED['p']=informatrixs[4][3][i]
            FIN[int(informatrixs[4][0][i]-1)].append(FINED.copy())
        for i in range(len(informatrixs[5])):
            FINED={}
            FINED['Ftype']='Qs'
            FINED['Mag']=informatrixs[5][1][i]
            FINED['alp']=informatrixs[5][2][i]
            FINED['p']=informatrixs[5][3][i]
            FIN[int(informatrixs[5][0][i]-1)].append(FINED.copy())
            FINED={}
            FINED['Ftype']='Qe'
            FINED['Mag']=informatrixs[5][1][i]
            FINED['alp']=informatrixs[5][2][i]
            FINED['p']=informatrixs[5][4][i]
            FIN[int(informatrixs[5][0][i]-1)].append(FINED.copy())
#        for i in range(len(elements)):
#            FINE=[]
#            FINED={}
#            for j in range(table2.ncols):
#                if table2.cell(i,j).value=='F':
#                    FINED={}
#                    FINED['Ftype']='F'
#                    FINED['Mag']=table2.cell(i,j+1).value
#                    FINED['alp']=table2.cell(i,j+2).value
#                    FINED['p']=table2.cell(i,j+3).value
#                    FINE.append(FINED.copy())
#                if table2.cell(i,j).value=='Q':
#                    FINED={}
#                    FINED['Ftype']='Qs'
#                    FINED['Mag']=table2.cell(i,j+1).value
#                    FINED['alp']=table2.cell(i,j+2).value
#                    FINED['p']=table2.cell(i,j+3).value
#                    FINE.append(FINED.copy())
#                    FINED={}
#                    FINED['Ftype']='Qe'
#                    FINED['Mag']=table2.cell(i,j+1).value
#                    FINED['alp']=table2.cell(i,j+2).value
#                    FINED['p']=table2.cell(i,j+4).value
#                    FINE.append(FINED.copy())
#            FIN.append(FINE)
        t={}
        for i in range(len(FIN)):
            for j in range(len(FIN[i])):
                for k in range(len(FIN[i])-1):
                    if FIN[i][k]['p']>FIN[i][k+1]['p']:
                        t=FIN[i][k]
                        FIN[i][k]=FIN[i][k+1]
                        FIN[i][k+1]=t
#    else:
#        minus=0
#        for i in range(table2.nrows):
#            if i+1 not in oldelementnums:
#                minus=minus+1
#                continue
#            FINE=[]
#            FINED={}
#            for j in range(table2.ncols):
#                if table2.cell(i,j).value=='F':
#                    if abs(elements[i-minus]['alp'])%180==0:
#                        if zdc==1 and table2.cell(i,j+3).value<0.5:
#                            FINED={}
#                            FINED['Ftype']='F'
#                            FINED['Mag']=table2.cell(i,j+1).value
#                            FINED['alp']=table2.cell(i,j+2).value
#                            FINED['p']=table2.cell(i,j+3).value*2
#                            FINE.append(FINED.copy())
#                        if zdc==1 and table2.cell(i,j+3).value==0.5:
#                            FINED={}
#                            FINED['Ftype']='F'
#                            FINED['Mag']=table2.cell(i,j+1).value/2
#                            FINED['alp']=table2.cell(i,j+2).value
#                            FINED['p']=table2.cell(i,j+3).value*2
#                            FINE.append(FINED.copy())
#                        if fdc==1 and table2.cell(i,j+3).value<0.5:
#                            FINED={}
#                            FINED['Ftype']='F'
#                            FINED['Mag']=table2.cell(i,j+1).value
#                            FINED['alp']=table2.cell(i,j+2).value
#                            FINED['p']=table2.cell(i,j+3).value*2
#                            FINE.append(FINED.copy())
#                    else:
#                        FINED={}
#                        FINED['Ftype']='F'
#                        FINED['Mag']=table2.cell(i,j+1).value
#                        FINED['alp']=table2.cell(i,j+2).value
#                        FINED['p']=table2.cell(i,j+3).value
#                        FINE.append(FINED.copy())
#                if table2.cell(i,j).value=='Q':
#                    FINED={}
#                    FINED['Ftype']='Qs'
#                    FINED['Mag']=table2.cell(i,j+1).value
#                    FINED['alp']=table2.cell(i,j+2).value
#                    FINED['p']=table2.cell(i,j+3).value
#                    FINE.append(FINED.copy())
#                    FINED={}
#                    FINED['Ftype']='Qe'
#                    FINED['Mag']=table2.cell(i,j+1).value
#                    FINED['alp']=table2.cell(i,j+2).value
#                    FINED['p']=table2.cell(i,j+4).value
#                    FINE.append(FINED.copy())
#            FIN.append(FINE)
#        file1 = xlrd.open_workbook('excel/results.xls')
#        table = file1.sheet_by_index(0)
#        for i in range(table2.nrows+1-minus,table.nrows-minus):
#            FINE=[]
#            FIN.append(FINE)
#        t={}
#        for i in range(len(FIN)):
#            for j in range(len(FIN[i])):
#                for k in range(len(FIN[i])-1):
#                    if FIN[i][k]['p']>FIN[i][k+1]['p']:
#                        t=FIN[i][k]
#                        FIN[i][k]=FIN[i][k+1]
#                        FIN[i][k+1]=t
        
    global M
    M=[]
    for i in range(len(calelements)):
        Me=[]
        l=calelements[i]['l']
        ns=0
        ne=0
        Mi=calelements[i]['MI']
        F=calelements[i]['FYI']
        N=calelements[i]['NI']
        Q=0
        Qn=0
        if FIN[i]==[]:
            ne=1
            Mj=calelements[i]['MJ']
            M_=[Mi,Mj,ns,ne,F,Q,N,Qn]
            Me.append(M_.copy())
            M.append(Me.copy())
        else:
            ne=FIN[i][0]['p']
            if math.isclose(ne,0,abs_tol=1e-5)==False:
                Mj=Mi+F*l*ne
                M_=[Mi,Mj,ns,ne,F,Q,N,Qn]
                Me.append(M_.copy())
                ns=ne
                Mi=Mj
            for j in range(len(FIN[i])-1):
                if FIN[i][j]['Ftype']=='Qs':
                    Q=FIN[i][j]['Mag']*np.sin(FIN[i][j]['alp']/180*3.14159)
                    Qn=FIN[i][j]['Mag']*np.cos(FIN[i][j]['alp']/180*3.14159)
                if FIN[i][j]['Ftype']=='Qe':
                    Q=0
                    Qn=0
                if FIN[i][j]['Ftype']=='F':
                    F=F+FIN[i][j]['Mag']*np.sin(FIN[i][j]['alp']/180*3.14159)
                    N=N-FIN[i][j]['Mag']*np.cos(FIN[i][j]['alp']/180*3.14159)
                ns=FIN[i][j]['p']
                ne=FIN[i][j+1]['p']
                Mj=Mi+F*l*(ne-ns)+0.5*Q*((ns-ne)*l)**2
                M_=[Mi,Mj,ns,ne,F,Q,N,Qn]
                Me.append(M_.copy())
                F=F+Q*(ne-ns)*l
                N=N-Qn*(ne-ns)*l
                Mi=Mj
                ns=ne
            if math.isclose(ns,1,abs_tol=1e-5)==False:
                if FIN[i][-1]['Ftype']=='F':
                    F=F+FIN[i][-1]['Mag']*np.sin(FIN[i][-1]['alp']/180*3.14159)
                    N=N-FIN[i][-1]['Mag']*np.cos(FIN[i][-1]['alp']/180*3.14159)                 
                ne=1
                Q=0
                Mj=Mi+F*l*(ne-ns)
                M_=[Mi,Mj,ns,ne,F,Q,N,Qn]
                Me.append(M_.copy())
            M.append(Me.copy())
            

#创造答案
def createanswers():
    fileinforces()
    class A():
        pass
    global a
    a=[]
    for i in range(len(elements)):
        a.append([])
    for i in range(len(M)):
        for j in range(len(M[i])):
            a_=A()
            a_.Mi=M[i][j][0]
            a_.Mj=M[i][j][1]
            ns=M[i][j][2]
            ne=M[i][j][3]
            F=M[i][j][4]
            Q=M[i][j][5]
            l=elements[i]['l']
            a_.Mmid=M[i][j][0]+F*l*(ne-ns)/2+0.5*Q*((ne-ns)/2*l)**2
            a_.num=i+1
            if close0(M[i][j][5]):
                a_.type='l'
            else:
                a_.type='p'
            a_.ns=M[i][j][2]
            a_.ne=M[i][j][3]
            a[i].append(copy.copy(a_))
#    for i in range(len(a)):
#        for j in range(len(a[i])):
#            print('len=%d'%len(a[i]))
#            print(a[i][j].ns)
#            print(a[i][j].ne)
            

    



#画变形图，注意支座沉降以及温度变化对于变形图的影响，用变形图三次曲线拟合        
def drawdeformation():
    fileinforces()
    plt.figure(figsize=(32,20))
    maxdeform=0
    n=1
    switch=0
    
    
    
    class STANARD_DEFORMATION_ANSWER():
        pass
    global stanard_deformation_answer
    stanard_deformation_answer=[]
    for t in range(len(elements)):
        stanard_deformation_answer.append([])
    
    
    def fx(x):
        dis=dey+th*x+0.5*x**2*Mi/EI+1/6*x**3*F/EI+1/24*x**4*Q/EI
        return dis
    def ft(x):
        dis=dey+th*x+0.5*x**2*(Mi/EI-alpt*(t1-t2)/h)+1/6*x**3*F/EI+1/24*x**4*Q/EI
        return dis
    for i in range(len(M)):
        switch=0
        dex=displace[i][0]
        dey=displace[i][1]
        th=displace[i][2]
        EI=calelements[i]['EI']
        EA=calelements[i]['EA']
        l=calelements[i]['l']
        if len(informatrixs[6])>0:
            for j in range(len(informatrixs[6])):
                if i+1 ==informatrixs[6][0][j]:
                    switch=1
                    alpt=informatrixs[6][1][j]
                    t1=informatrixs[6][2][j]
                    t2=informatrixs[6][3][j]
                    h=informatrixs[6][4][j]
                    break
#            if i<table2.nrows:
#                if table2.cell(i,j).value=='T':
#                    switch=1
#                    alpt=table2.cell(i,j+1).value
#                    t1=table2.cell(i,j+2).value
#                    t2=table2.cell(i,j+3).value
#                    h=table2.cell(i,j+4).value
#                    break
#                else:
#                    switch=0
        for j in range(len(M[i])):
            Mi=M[i][j][1]
            ns=M[i][j][2]
            ne=M[i][j][3]
            F=M[i][j][4]
            Q=M[i][j][5]
            N=M[i][j][6]
            Qn=M[i][j][7]
            tl=(ne-ns)*l
            x=np.linspace(0,(ne-ns)*l,30)
            if switch==0:
#                if abs(fx(0))>maxdeform:
#                    maxdeform=abs(fx(0))
#                if abs(fx(0.5*tl))>maxdeform:
#                    maxdeform=abs(fx(0.5*tl))
#                if abs(fx(tl))>maxdeform:
#                    maxdeform=abs(fx(tl))
#                if abs(dex)>maxdeform:
#                    maxdeform=abs(dex)
                dey=fx(tl)
                dex=dex+N*tl/EA-Qn*0.5*(tl)**2/EA
                th=th+tl*Mi/EI+0.5*(tl)**2*F/EI+1/6*(tl)**3*Q/EI
                if max(abs(fx(x)))>maxdeform:
                    maxdeform=max(abs(fx(x)))
                if abs(th)>maxdeform:
                    maxdeform=abs(th)
            if switch==1:
#                if abs(ft(0))>maxdeform:
#                    maxdeform=abs(fx(0))
#                if abs(ft(0.5*tl))>maxdeform:
#                    maxdeform=abs(fx(0.5*tl))
#                if abs(ft(tl))>maxdeform:
#                    maxdeform=abs(fx(tl))
#                if abs(dex)>maxdeform:
#                    maxdeform=abs(dex)
                dey=ft(tl)
                dex=dex+N*tl/EA-Qn*0.5*(tl)**2/EA+alpt*(t1+t2)/2*tl
                th=th+tl*(Mi/EI-alpt*(t1-t2)/h)+0.5*(tl)**2*F/EI+1/6*(tl)**3*Q/EI
                if max(abs(ft(x)))>maxdeform:
                    maxdeform=max(abs(fx(x)))
    print('maxdeforma=%f'%maxdeform)
    #控制变形图大小，如果最大位移都很小，说明这个结构刚度太大有无限刚度的存在，无变形
    while maxdeform<=1.5*s:
        if maxdeform<1e-4:
            break
        else:
            maxdeform=maxdeform*2
            n=n/2
    while maxdeform>=3*s:
        maxdeform=maxdeform/2
        n=n*2
    n=n/ad
    for i in range(len(calelements)):
        switch=0
        l=calelements[i]['l']
        alp=calelements[i]['alp']/180*3.14159
        sin=np.sin(alp)
        cos=np.cos(alp)
        xi=calelements[i]['pi']['x']
        yi=calelements[i]['pi']['y']
        dex=displace[i][0]
        dey=displace[i][1]
        th=displace[i][2]
        EI=calelements[i]['EI']
        EA=calelements[i]['EA']
        if len(informatrixs[6])>0:
            for j in range(len(informatrixs[6])):
                if i+1 ==informatrixs[6][0][j]:
                    switch=1
                    alpt=informatrixs[6][1][j]
                    t1=informatrixs[6][2][j]
                    t2=informatrixs[6][3][j]
                    h=informatrixs[6][4][j]
                    break
#        for j in range(table2.ncols):
#            if i<table2.nrows:
#                if table2.cell(i,j).value=='T':
#                    switch=1
#                    alpt=table2.cell(i,j+1).value
#                    t1=table2.cell(i,j+2).value
#                    t2=table2.cell(i,j+3).value
#                    h=table2.cell(i,j+4).value
#                    break
#                else:
#                    switch=0
        for j in range(len(M[i])):
            Mi=M[i][j][0]
            ns=M[i][j][2]
            ne=M[i][j][3]
            F=M[i][j][4]
            Q=M[i][j][5]
            N=M[i][j][6]
            Qn=M[i][j][7]
            tl=(ne-ns)*l
            x=np.linspace(0,tl,20)
            
            
            stanard_deformation_answer_=STANARD_DEFORMATION_ANSWER()
            stanard_deformation_answer_.num=i+1
            stanard_deformation_answer_.ns=ns
            stanard_deformation_answer_.ne=ns
            if switch==0:
                stanard_deformation_answer_.A=dey
                stanard_deformation_answer_.B=th
                stanard_deformation_answer_.C=0.5*Mi/EI
                stanard_deformation_answer_.D=1/6*F
                stanard_deformation_answer_.E=1/24*Q
                stanard_deformation_answer_.dex=dex
                stanard_deformation_answer[i].append(copy.copy(stanard_deformation_answer_))
            else:
                stanard_deformation_answer_.A=dey
                stanard_deformation_answer_.B=th
                stanard_deformation_answer_.C=0.5*(Mi/EI-alpt*(t1-t2)/h)
                stanard_deformation_answer_.D=1/6*F/EI
                stanard_deformation_answer_.E=1/24*Q/EI
                stanard_deformation_answer_.dex=dex
                stanard_deformation_answer[i].append(copy.copy(stanard_deformation_answer_))
            
            
            
            
            
            
            
            
            
            if switch==0:
                y=fx(x)
                x_=np.linspace(0,tl+(N*tl/EA-Qn*0.5*(tl)**2/EA)/n,20)
            if switch==1:
                y=ft(x)
                print(dey)
                print(y)
                x_=np.linspace(0,tl+(N*tl/EA-Qn*0.5*(tl)**2/EA+alpt*(t1+t2)/2*tl)/n,20)
            x1=xi+(l*ns+dex/n)*cos+x_*cos-y*sin/n
            y1=yi+(l*ns+dex/n)*sin+x_*sin+y*cos/n
            plt.plot(x1,y1,'g--',linewidth=4)
            if switch==0:
                dey=fx(tl)
                dex=dex+N*tl/EA-Qn*0.5*(tl)**2/EA
                th=th+tl*Mi/EI+0.5*(tl)**2*F/EI+1/6*(tl)**3*Q/EI
            if switch==1:
                dey=ft(tl)
                dex=dex+N*tl/EA-Qn*0.5*(tl)**2/EA+alpt*(t1+t2)/2*tl
                th=th+tl*(Mi/EI-alpt*(t1-t2)/h)+0.5*(tl)**2*F/EI+1/6*(tl)**3*Q/EI
                
#    print(stanard_deformation_answer)
#    
#    pickle.dump(stanard_deformation_answer,open('123.pkl','wb'))
    
#    pickle.dump(stanard_deformation_answer,open('stanard_deformation_answer.pkl', 'wb'))
    

    drawelements()
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/deformation.png',bbox_inches='tight')
    plt.close()
    
    





    
    
    
    
    
    
    
#amplify放大系数，aM,aF,aN分别控制放大弯矩，剪力，轴力
aM=1
aF=1
aN=1

def drawM():
    fileinforces()
    plt.figure(figsize=(32,20))
    maxM=0
    n=1
    for i in range(len(M)):
        for j in range(len(M[i])):
            ns=M[i][j][2]
            ne=M[i][j][3]
            F=M[i][j][4]
            Q=M[i][j][5]
            l=elements[i]['l']
            Mmid=abs(M[i][j][0]+F*l*(ne-ns)/2+0.5*Q*((ne-ns)/2*l)**2)
            if abs(M[i][j][0])>maxM:
                maxM=abs(M[i][j][0])
            if abs(M[i][j][1])>maxM:
                maxM=abs(M[i][j][1])
            if Mmid>maxM:
                maxM=Mmid
    while maxM>=8*s:
        maxM=maxM/2
        n=n*2
    n=n/aM
    #print(n)
    for i in range(len(elements)):
        l=elements[i]['l']
        alp=elements[i]['alp']/180*3.14159
        sin=np.sin(alp)
        cos=np.cos(alp)
        xi=elements[i]['pi']['x']
        yi=elements[i]['pi']['y']
        xj=elements[i]['pj']['x']
        yj=elements[i]['pj']['y']
        for j in range(len(M[i])):
            Mi=M[i][j][0]
            Mj=M[i][j][1]
            ns=M[i][j][2]
            ne=M[i][j][3]
            F=M[i][j][4]
            Q=M[i][j][5]
            Mmid=np.round(Mi+F*l*(ne-ns)/2+0.5*Q*((ne-ns)/2*l)**2,2)
            if abs(Q)>0:
                plt.annotate(np.round(Mmid,2),xy=(xi+l*(ns+ne)/2*cos+Mmid*sin/n-s*sin*Mmid/abs(Mmid)*-1,
                                      yi+l*(ns+ne)/2*sin-Mmid*cos/n+s*cos*Mmid/abs(Mmid)*-1),
                                     fontsize=30,color='black',weight='bold')
                plt.scatter(x=xi+l*(ns+ne)/2*cos+Mmid*sin/n-s*sin*Mmid/abs(Mmid)*-1,
                            y=yi+l*(ns+ne)/2*sin-Mmid*cos/n+s*cos*Mmid/abs(Mmid)*-1,edgecolor='',color='')
            if math.isclose(Mi,0,abs_tol=1e-4):
                Mi=0
            if Mi!=0:
                plt.annotate(np.round(Mi,2),xy=(xi+l*ns*cos+Mi*sin/n-s*sin*Mi/abs(Mi)*-1,
                                      yi+l*ns*sin-Mi*cos/n+s*cos*Mi/abs(Mi)*-1),
                                     fontsize=30,color='black',weight='bold')
                plt.scatter(x=xi+l*ns*cos+Mi*sin/n-s*sin*Mi/abs(Mi)*-1,
                            y=yi+l*ns*sin-Mi*cos/n+s*cos*Mi/abs(Mi)*-1,edgecolor='',color='')
                
            #if Mi==0:
                #plt.annotate(np.round(Mi,2),xy=(xi+l*ns*cos,yi+l*ns*sin),
                         #fontsize=12,color='black',weight='bold')
            Mmid=np.round(Mi+F*l*(ne-ns)/2+0.5*Q*((ne-ns)/2*l)**2,2)
            xmid=xi+(ne+ns)/2*l*cos
            ymid=yi+(ne+ns)/2*l*sin
            if math.isclose(Mmid,0,abs_tol=1e-4):
                 Mmid=0
            else:
                if math.isclose(np.round(Mi,2),0,abs_tol=1e-4) and math.isclose(np.round(Mi,2),0,abs_tol=1e-4):
                    plt.annotate(Mmid,xy=(xmid+Mmid*sin/n-s*sin*Mmid/abs(Mmid)*-1,
                                          ymid-Mmid*cos/n+s*cos*Mmid/abs(Mmid)*-1),
                                 fontsize=30,color='black',weight='bold')
                    plt.scatter(x=xmid+Mmid*sin/n-s*sin*Mmid/abs(Mmid)*-1,
                            y=ymid-Mmid*cos/n+s*cos*Mmid/abs(Mmid)*-1,edgecolor='',color='')
            x=np.linspace(0,l*(ne-ns),20)
            y=-(Mi+F*x+0.5*Q*x**2)
            x1=xi+l*ns*cos+x*cos-y*sin/n
            y1=yi+l*ns*sin+x*sin+y*cos/n
            x2=xi+l*ns*cos+x*cos
            y2=yi+l*ns*sin+x*sin
            plt.plot(x1,y1,'r')
            plt.plot([x1,x2],[y1,y2],'r')
        if  math.isclose(Mj,0,abs_tol=1e-4):
            Mj=0
            #plt.annotate(Mj,xy=(xj,yj),fontsize=12,color='black',weight='bold')
        else:
            plt.annotate(np.round(Mj,2),xy=(xj+Mj*sin/n-s*sin*Mj/abs(Mj)*-1,
                                  yj-Mj*cos/n+s*cos*Mj/abs(Mj)*-1),
                         fontsize=30,color='black',weight='bold')
            plt.scatter(x=xj+Mj*sin/n-s*sin*Mj/abs(Mj)*-1,
                            y=yj-Mj*cos/n+s*cos*Mj/abs(Mj)*-1,edgecolor='',color='')
    drawelements()        
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/M.png',bbox_inches='tight')
    plt.close()
def drawshearforce():
    fileinforces()
    plt.figure(figsize=(32,20))
    maxF=0
    n=1
    for i in range(len(M)):
        for j in range(len(M[i])):
            l=elements[i]['l']
            ns=M[i][j][2]
            ne=M[i][j][3]
            F=M[i][j][4]
            Q=M[i][j][5]
            Fe=F+Q*(ne-ns)*l
            if abs(M[i][j][4])>maxF:
                maxF=abs(M[i][j][4])
            if abs(Fe)>maxF:
                maxF=abs(Fe) 
    while maxF>=8*s:
        maxF=maxF/2
        n=n*2
    n=n/aF
    for i in range(len(elements)):
        l=elements[i]['l']
        alp=elements[i]['alp']/180*3.14159
        sin=np.sin(alp)
        cos=np.cos(alp)
        xi=elements[i]['pi']['x']
        yi=elements[i]['pi']['y']
        xj=elements[i]['pj']['x']
        yj=elements[i]['pj']['y']
        for j in range(len(M[i])):
            ns=M[i][j][2]
            ne=M[i][j][3]
            F=M[i][j][4]
            Q=M[i][j][5]
            Fe=F+Q*(ne-ns)*l
            if math.isclose(F,0,abs_tol=1e-5):
                F=0
            if math.isclose(Fe,0,abs_tol=1e-5):
                Fe=0
            if F!=0:
                plt.annotate(np.round(abs(F),2),xy=(xi+l*ns*cos-F*sin/n-0.04*sin*F/abs(F),
                        yi+l*ns*sin+F*cos/n+0.04*cos*F/abs(F)),
                         fontsize=30,color='black',weight='bold')
            #if F==0:
                #plt.annotate(np.round(F,2),xy=(xi+l*ns*cos-F*sin/n-0.02*sin,
                             #yi+l*ns*sin+F*cos/n+0.02*cos),
                         #fontsize=12,color='black',weight='bold')
            if Fe!=0:
                plt.annotate(np.round(abs(Fe),2),xy=(xi+l*ne*cos-Fe*sin/n-0.04*sin*Fe/abs(Fe),
                                      yi+l*ne*sin+Fe*cos/n+0.04*cos*Fe/abs(Fe)),
                         fontsize=30,color='black',weight='bold')
            #if Fe==0:
                #plt.annotate(np.round(Fe,2),xy=(xi+l*ne*cos+Fe*sin/n-0.02*sin,
                             #yi+l*ne*sin+Fe*cos/n+0.02*cos),
                         #fontsize=12,color='black',weight='bold')

            x=np.linspace(0,l*(ne-ns),20)
            y=F+Q*x
            x1=xi+l*ns*cos+x*cos-y*sin/n
            y1=yi+l*ns*sin+x*sin+y*cos/n
            x2=xi+l*ns*cos+x*cos
            y2=yi+l*ns*sin+x*sin
            plt.plot(x1,y1,'b')
            plt.plot([x1,x2],[y1,y2],'b')
    drawelements()
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/shearforce.png',bbox_inches='tight')
    plt.close()
def drawN():
    fileinforces()
    plt.figure(figsize=(32,20))
    maxN=0
    n=1
    for i in range(len(M)):
        l=elements[i]['l']
        for j in range(len(M[i])):
            ns=M[i][j][2]
            ne=M[i][j][3]
            N=M[i][j][6]
            Qn=M[i][j][7]
            Ne=N-Qn*(ne-ns)*l
            if abs(M[i][j][6])>maxN:
                maxN=abs(M[i][j][6])
            if abs(Ne)>maxN:
                maxN=abs(Ne)
    while maxN>=8*s:
        maxN=maxN/2
        n=n*2
    n=n/aN
    for i in range(len(elements)):
        l=elements[i]['l']
        alp=elements[i]['alp']/180*3.14159
        sin=np.sin(alp)
        cos=np.cos(alp)
        xi=elements[i]['pi']['x']
        yi=elements[i]['pi']['y']
        xj=elements[i]['pj']['x']
        yj=elements[i]['pj']['y']
        for j in range(len(M[i])):
            ns=M[i][j][2]
            ne=M[i][j][3]
            N=M[i][j][6]
            Qn=M[i][j][7]
            Ne=N-Qn*(ne-ns)*l
            if math.isclose(N,0,abs_tol=1e-3):
                N=int(0)
            if math.isclose(Ne,0,abs_tol=1e-3):
                Ne=int(0)
            if N!=0:
                plt.annotate(np.round(N,2),xy=(xi+l*ns*cos-N*sin/n-s*sin*N/abs(N),
                        yi+l*ns*sin+N*cos/n+s*cos*N/abs(N)),
                         fontsize=30,color='black',weight='bold')
            #if N==0:
                #plt.annotate(N,xy=(xi+l*ns*cos,
                             #yi+l*ns*sin),
                         #fontsize=12,color='black',weight='bold')
                
            if Ne!=0:
                plt.annotate(np.round(Ne,2),xy=(xi+l*ne*cos-Ne*sin/n-s*sin*Ne/abs(Ne),
                                      yi+l*ne*sin+Ne*cos/n+s*cos*Ne/abs(Ne)),
                         fontsize=30,color='black',weight='bold')
            #if Ne==0:
                #plt.annotate(Ne,xy=(xi+l*ne*cos,
                             #yi+l*ne*sin),
                         #fontsize=12,color='black',weight='bold')
            x=np.linspace(0,l*(ne-ns),20)
            y=N-Qn*x
            x1=xi+l*ns*cos+x*cos-y*sin/n
            y1=yi+l*ns*sin+x*sin+y*cos/n
            x2=xi+l*ns*cos+x*cos
            y2=yi+l*ns*sin+x*sin
            plt.plot(x1,y1,'b')
            plt.plot([x1,x2],[y1,y2],'b')
    drawelements()
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/N.png',bbox_inches='tight')
    plt.close()
    
    
def amplifyM(a):
    global aM
    aM=a*aM
    
    
def amplifyF(a):
    global aF
    aF=a*aF
    
def amplifyN(a):
    global aN
    aN=a*aN

def recordansweringprocess(x):
    '''x=0是通过自定义提示进来的，x=1是通过系统自带的提示进来的，x=2是通过比对进来的'''
    global questionsymbol,a,df
    global starttime
    columns=[]
    columns.append('questionsymbol')
    columns.append('userID')
    columns.append('starttime')
    ts = time.time()
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    columns.append('answertime')
    for i in range(len(a)):
        for j in range(len(a[i])):
            columns.append(str(i+1)+'_'+str(j+1))
    df=pd.DataFrame(np.full((1,len(columns)),'0'))
    df.columns=columns
    df.loc[0,'answertime']=dt
    df.loc[0,'userID']=userID
    df.loc[0,'starttime']=starttime
    df.loc[0,'questionsymbol']=questionsymbol
    for i in range(len(a)):
        if len(c[i])>0:
            for j in range(len(c[i])):
                for k in range(len(a[i])):
                    if c[i][j].ns==a[i][k].ns and c[i][j].ne==a[i][k].ne:
                        column=str(i+1)+'_'+str(k+1)
                        context=str(c[i][j].num)+','+str(c[i][j].type)+','+str(c[i][j].Mi)+','
                        context=context+str(c[i][j].Mj)+','+str(c[i][j].Mmid)+','+str(c[i][j].ns)+','+str(c[i][j].ne)
#                        if x==0:
#                            weizuoda=1
#                            for l in range(len(a)):
#                                if len(a[i])==len(c[i]):
#                                        weizuoda=0
#                            if weizuoda==1:
#                                if len(zhengtitishi)>1:
#                                    context=context+","+str(zhengtitishi)
#                                else:
#                                    context=context+",请先尝试作答"
#                            else:
#                                if zdycuowunum<0:
#                                    context=context+",特征点作答正确"
#                                else:
#                                    context=context+','+zdytishi.iloc[zdycuowunum,4]
#                        if x==1:
#                            if tishi!='':
#                                context=context+','+tishi
#                            else:
#                                context=context+',特征点作答正确'
#                        if x==2:
#                            if jys!=[] or len(xys)!=len(scxys):
#                                context=context+',请先去除约束'
#                                return
#                            elif timutishifangshi!='自定义提示':
#                                if tishiright==0:
#                                    context=context+',请点击分析与提示，修改作答'
#                            
#                            else:
#                                weizuoda=1
#                                for l in range(len(a)):
#                                    if len(a[i])==len(c[i]):
#                                            weizuoda=0
#                                if weizuoda==1:
#                                    context=context+',请先完成作答，再比对'
#                                if weizuoda==0:
#                                    context=context+','+cuowu
                        df.loc[0,column]=context
                        #print(df)
    df.loc[0,"提示或错误"]='0'
    if x==0:
        weizuoda=1
        for l in range(len(a)):
            if len(a[i])==len(c[i]):
                    weizuoda=0
        if weizuoda==1:
            if len(zhengtitishi)>1:
                df.loc[0,"提示或错误"]=str(zhengtitishi)
            else:
                df.loc[0,"提示或错误"]="请先尝试作答"
        else:
            if zdycuowunum<0:
                df.loc[0,"提示或错误"]="特征点作答正确"
            else:
                df.loc[0,"提示或错误"]=zdytishi.iloc[zdycuowunum,4]
    if x==1:
        if tishi!='':
            df.loc[0,"提示或错误"]=tishi
        else:
            df.loc[0,"提示或错误"]='特征点作答正确'
    if x==2:
        if jys!=[] or len(xys)!=len(scxys):
            df.loc[0,"提示或错误"]='请先去除约束'
        elif timutishifangshi!='自定义提示':
            if tishiright==0:
                df.loc[0,"提示或错误"]='请点击分析与提示，修改作答'
        
        else:
            weizuoda=1
            for l in range(len(a)):
                if len(a[i])==len(c[i]):
                        weizuoda=0
            if weizuoda==1:
                df.loc[0,"提示或错误"]=='请先完成作答，再比对'
            if weizuoda==0:
                df.loc[0,"提示或错误"]=cuowu
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/answering_process')
    df.to_sql('moment'+str(questionsymbol), engine, index= False,if_exists='append')
    df2=pd.DataFrame(np.zeros((1,5)))
    columns=[]
    columns.append('questionsymbol')
    columns.append('userID')
    columns.append('starttime')
    columns.append('answertime')
    columns.append('提示或错误')
    df2.columns=columns
    df2.loc[0,'answertime']=dt
    df2.loc[0,'userID']=userID
    df2.loc[0,'starttime']=starttime
    df2.loc[0,'questionsymbol']=questionsymbol
    df2.loc[0,'提示或错误']=df.loc[0,'提示或错误']
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    df2.to_sql('tishi', engine, index= False,if_exists='append')
    
#绘制用户作答的结果
def userM():
    global s
    for ctt in c:
        for ct in ctt:
            num=ct.num
            Mi=ct.Mi*2*s/1.5
            Mj=ct.Mj*2*s/1.5
            Mmid=ct.Mmid*2*s/1.5
            ns=ct.ns
            ne=ct.ne
            cos=np.cos(elements[num-1]['alp']/180*3.14159)
            sin=np.sin(elements[num-1]['alp']/180*3.14159)
            xi=elements[num-1]['pi']['x']
            yi=elements[num-1]['pi']['y']
            xj=elements[num-1]['pj']['x']
            yj=elements[num-1]['pj']['y']
            l=elements[num-1]['l']
            if ct.type=='l':
                x_=np.linspace(0,l*(ne-ns),20)
                y_=(Mj-Mi)/l*x_/(ne-ns)+Mi
                y_=y_*-1
                x0=(x_+ns*l)*cos+xi
                y0=(x_+ns*l)*sin+yi
                x1=(x_+ns*l)*cos-y_*sin+xi
                y1=(x_+ns*l)*sin+y_*cos+yi
                plt.plot(x1,y1,'darkgreen')
                plt.plot([x0,x1],[y0,y1],'darkgreen')
                if Mi==0 and Mj==0:
                    plt.plot([xi,xj],[yi,yj],'darkgreen',linewidth=6)
            if ct.type=='p':
                y_=[Mi,Mmid,Mj]
                y_=np.array(y_)
                y_=y_*-1
#                x_=[0,0.5*l*(ne-ns),l*(ne-ns)]
                x_=[0,0.5*l*(ne-ns),l*(ne-ns)]
                x_=np.array(x_)
                f1 = np.polyfit(x_, y_,2)
                x_=np.linspace(0,l*(ne-ns),20)
                y_=f1[0]*x_**2+f1[1]*x_+f1[2]
                x0=x_*cos+xi+ns*l*cos
                y0=x_*sin+yi+ns*l*sin
                x1=x_*cos-y_*sin+xi+ns*l*cos
                y1=x_*sin+y_*cos+yi+ns*l*sin
                plt.plot(x1,y1,'darkgreen')
                plt.plot([x0,x1],[y0,y1],'darkgreen')
#                y_=[Mi,Mmid,Mj]
#                y_=np.array(y_)
#                y_=y_*-1
#                x_=[0,0.5*l,l]
#                x_=np.array(x_)
#                f1 = np.polyfit(x_, y_,2)
#                x_=np.linspace(0,l,20)
#                y_=f1[0]*x_**2+f1[1]*x_+f1[2]
#                x0=x_*cos+xi
#                y0=x_*sin+yi
#                x1=x_*cos-y_*sin+xi
#                y1=x_*sin+y_*cos+yi
#                plt.plot(x1,y1,'darkgreen')
#                plt.plot([x0,x1],[y0,y1],'darkgreen')
    

#画角约束         
def drawjys():
    for i in jys:
        x0=joints_[i-1]['x']
        y0=joints_[i-1]['y']
        cos=np.cos(22.5/180*3.14159)
        sin=np.sin(22.5/180*3.14159)
        plt.plot([x0,x0+2*s*cos],[y0,y0+2*s*sin],'k',linewidth=5)
        plt.plot([x0,x0+2*s*sin],[y0,y0+2*s*cos],'k',linewidth=5)
        plt.plot([x0+2*s*cos,x0+2*s*sin],[y0+2*s*sin,y0+2*s*cos],'k',linewidth=5)




#userM，加上杆件、支座等内容
def drawuserM(smallest_index):

    plt.figure(figsize=(32,20))
    drawelements()
    drawannotation()
#    userM()
    if smallest_index!=-1 and daduan==0:
        i=smallest_index
        xi=elements[i]['pi']['x']
        yi=elements[i]['pi']['y']
        xj=elements[i]['pj']['x']
        yj=elements[i]['pj']['y']
        plt.plot([xi+ps*(xj-xi),xi+pe*(xj-xi)],[yi+ps*(yj-yi),yi+pe*(yj-yi)],linewidth=15,
                  color='orange',linestyle='--')       
    for i in range(len(duandian)):
        for j in duandian[i]:
            xi=elements[i]['pi']['x']
            yi=elements[i]['pi']['y']
            xj=elements[i]['pj']['x']
            yj=elements[i]['pj']['y']
            if j!=0 and j!=1:
                plt.scatter(x=xi+j*(xj-xi),y=yi+j*(yj-yi),s=500,color='red')
    if daduan==1:
        drawmidspan()
    drawjys()
    plt.xlim((xrange[0],xrange[1]))
    plt.ylim((yrange[0],yrange[1]))
    #print(xrange,yrange,xlong)
    plt.xticks(())
    plt.yticks(())
    plt.savefig('drawing/userM.png',bbox_inches='tight',pad_inches=0)
    plt.close()
    








#自定义函数，是否靠近0，以及是否靠近
def close0(x):
    return(math.isclose(x,0,abs_tol=1e-2))

def close(x,y):
    return(math.isclose(x,y,abs_tol=1e-2))

#def biduizf():
#    global zf,rp2
#    rp2=1
#    zf=[]
#    for i in range(len(elements)):
#        zf.append(1)
#    for i in range(len(elements)):
#        if close0(a[i]['Mi']==False) and a[i]['Mi']*c[i]['Mi']<0:
#            zf[i]=0
#        if close0(a[i]['Mi']) and close0(c[i]['Mi'])==False:
#            zf[i]=0
#        if close0(a[i]['Mj']==False) and a[i]['Mj']*c[i]['Mj']<0:
#            zf[i]=0
#        if close0(a[i]['Mj']) and close0(c[i]['Mj'])==False:
#            zf[i]=0
#        if c[i]['type']=='d' or c[i]['type']=='p':
#            if close0(a[i]['Mmid']==False) and a[i]['Mmid']*c[i]['Mmid']<0:
#                zf[i]=0
#            if close0(a[i]['Mmid']) and close0(c[i]['Mmid'])==False:
#                zf[i]=0
#    for i in range(len(elements)):
#        if zf[i]==0:
#            print(' 杆件 %s 正负有误' %(i+1))
#            rp2=0
#
#    
#    return rp2
#    
#def biduileixing():
#    global leixing,rp1
#    rp1=1
#    leixing=[]
#    for i in range(len(elements)):
#        leixing.append(1)
#    for i in range(len(elements)):
#        if a[i]['type']!=c[i]['type']:
#            leixing[i]=0
#    for i in range(len(elements)):
#        if leixing[i]==0:
#            print(' 杆件 %s 类型有误' %(i+1))
#            rp1=0
#
#
#    return rp1
#def biduixddx():
#    global xddx,rp3
#    rp3=1
#    xddx=[]
#    for i in range(len(elements)):
#        xddx.append(1)
#    for i in range(len(elements)):
#        if close(abs(a[i]['Mi']),abs(a[i]['Mj'])) and close(abs(c[i]['Mi']),abs(c[i]['Mj']))==False:
#            xddx[i]=0
#        if close(abs(a[i]['Mi']),abs(a[i]['Mj']))==False:
#            if abs(a[i]['Mi'])>abs(a[i]['Mj']) and abs(c[i]['Mi'])<=abs(c[i]['Mj']):
#                xddx[i]=0
#            if abs(a[i]['Mi'])<abs(a[i]['Mj']) and abs(c[i]['Mi'])>=abs(c[i]['Mj']):
#                xddx[i]=0    
#        if a[i]['type']=='p' or a[i]['type']=='d':
#              if close(abs(a[i]['Mi']),abs(a[i]['Mmid'])) and close(abs(c[i]['Mi']),abs(c[i]['Mmid']))==False:
#                  xddx[i]=0
#              if close(abs(a[i]['Mi']),abs(a[i]['Mmid']))==False:
#                  if abs(a[i]['Mi'])>abs(a[i]['Mmid']) and abs(c[i]['Mi'])<=abs(c[i]['Mmid']):
#                      xddx[i]=0
#                  if abs(a[i]['Mi'])<abs(a[i]['Mmid']) and abs(c[i]['Mi'])>=abs(c[i]['Mmid']):
#                      xddx[i]=0              
#             
#              if close(abs(a[i]['Mj']),abs(a[i]['Mmid'])) and close(abs(c[i]['Mj']),abs(c[i]['Mmid']))==False:  
#                  xddx[i]=0
#              if close(abs(a[i]['Mj']),abs(a[i]['Mmid']))==False:
#                  if abs(a[i]['Mj'])>abs(a[i]['Mmid']) and abs(c[i]['Mj'])<=abs(c[i]['Mmid']):
#                      xddx[i]=0
#                  if abs(a[i]['Mj'])<abs(a[i]['Mmid']) and abs(c[i]['Mj'])>=abs(c[i]['Mmid']):
#                      xddx[i]=0 
#    
#    
#    
#    
#    for i in range(len(elements)):
#        if xddx[i]==0:
#            print(' 杆件 %s 杆端相对大小有误' %(i+1))
#            rp3=0
#    
#
#
#    return rp3    
#def biduijdfp():
#    global jdfp,rp4
#    rp4=1
#    jdfp=[]
#    for i in range(len(joints_)):
#        jdfp.append(1)
#    class JD():
#        def __init__(self,num,p):
#            self.num=num
#            self.p=p
#    
#    for i in range(len(joints_)):
#        jiedian=[]
#        for j in range(len(elements)):
#            if elements[j]['pi']['num']==i+1:
#                jdt=JD(j,'i')
#                jiedian.append(jdt)
#            if elements[j]['pj']['num']==i+1:
#                jdt=JD(j,'j')
#                jiedian.append(jdt)
#        if len(jiedian)>=2:
#            Mc=[]
#            Ma=[]
#            sumM=0
#            sumM=-1*caljoints_[i]['M']
#            for k in range(len(jiedian)): 
#                num=jiedian[k].num
#                p=jiedian[k].p
#                if p=='i':
#                    Mc.append(c[num]['Mi'])
#                    Ma.append(a[num]['Mi'])
#                    sumM=sumM+c[num]['Mi']
#                if p=='j':
#                    Mc.append(c[num]['Mj'])
#                    Ma.append(a[num]['Mj'])
#                    sumM=sumM-c[num]['Mj']
#            if close0(sumM)==False:
#                jdfp[i]=0
#            if len(jiedian)>2:
#                Ma_=[]
#                Mc_=[]
#                for t in range(len(Ma)):
#                    cf=0
#                    for q in range(len(Ma_)):
#                        if close(abs(Ma_[q]),abs(Ma[t])):
#                            cf=1
#                    if cf==0:
#                        Ma_.append(Ma[t])
#                Ma=Ma_
#                
#                for t in range(len(Mc)):
#                    cf=0
#                    for q in range(len(Mc_)):
#                        if close(abs(Mc_[q]),abs(Mc[t])):
#                            cf=1
#                    if cf==0:
#                        Mc_.append(Mc[t])
#                Mc=Mc_
#                if len(Mc)!=len(Ma):
#                    jdfp[i]=0
#                else:    
#                    sorta=np.argsort(Ma)
#                    sorta=np.argsort(sorta)
#                    sortc=np.argsort(Mc)
#                    sortc=np.argsort(sortc)
#                    if any(sorta !=sortc):
#                        jdfp[i]=0
#    for i in range(len(jdfp)):
#        if jdfp[i]==0:
#            print('节点%s分配错误'%(i+1))
#            rp4=0
#    return rp4

#给予提示
def jiyutishi():
    createanswers()
    global tishi,zdc,fdc,zfjh,tishiright
    tishiright=0
    tishi=''
    global M
    global wcygj,jdjlfpf,cygj,lxl,zzcj,Settlements,wdbh,fzjlfpf,Temperatures
    global yflim,yzlim
    if lxl==1 and len(elements)>=2 and jdjg!=1:
        weizuoda=1
        for i in range(len(a)):
            if len(a[i])==len(c[i]):
                weizuoda=0
        if weizuoda==1:
            tishi='连续梁问题，可增加角约束，采用弯矩分配法'
        if weizuoda==0:
            zdq=-1
            for i in range(len(a)):
                if len(a[i])>1:
                    zdq=i
            for i in range(len(M)):
                for j in range(len(M[i])):
                    if close0(M[i][j][5])==False:
                        zdq=i
            global sgi,sgj
            sgi=0
            sgj=0
            ilj=-1
            ilj=-1
            ilj2=-1
            jlj2=-1
            if zdq!=-1:
                for i in range(len(elements)):
                    if elements[i]['pj']['num']==elements[zdq]['pi']['num']:
                        ilj=i
                    if elements[i]['pi']['num']==elements[zdq]['pj']['num']:
                        jlj=i
                if len(elements)>=2:
                    if elements[ilj]['pi']['restraint']==1 or elements[ilj]['pi']['restraint']==2:
                        sgi=3*calelements[ilj]['EI']/elements[ilj]['l']
                    if elements[ilj]['pi']['restraint']==3:
                        if abs(elements[ilj]['pi']['salp']-elements[ilj]['alp'])%180==90:
                            sgi=calelements[ilj]['EI']/elements[ilj]['l']
                        else:
                            sgi=4*calelements[ilj]['EI']/elements[ilj]['l']
                    if elements[ilj]['pi']['restraint']==4:
                        sgi=3*calelements[ilj]['EI']/elements[ilj]['l']
                    if elements[jlj]['pj']['restraint']==1 or elements[jlj]['pj']['restraint']==2:
                        sgj=3*calelements[jlj]['EI']/elements[jlj]['l']
                    if elements[jlj]['pj']['restraint']==3:
                        if abs(elements[ilj]['pj']['salp']-elements[jlj]['alp'])%180==90:
                            sgj=calelements[jlj]['EI']/elements[jlj]['l']
                        else:
                            sgj=4*calelements[jlj]['EI']/elements[jlj]['l']
                    if elements[jlj]['pj']['restraint']==4:
                        sgj=4*calelements[jlj]['EI']/elements[jlj]['l']
                    if len(elements)>=3:
                        for i in range(len(elements)):
                            if elements[i]['pj']['num']==elements[ilj]['pi']['num']:
                                ilj2=i
                            if elements[i]['pi']['num']==elements[jlj]['pj']['num']:
                                jlj2=i
                        if ilj2>=0:
                            if elements[ilj2]['pi']['restraint']==1 or elements[ilj2]['pi']['restraint']==2 :
                                sgi=(3*calelements[ilj2]['EI']/1e6/12+1)*sgi
                            if elements[ilj2]['pi']['restraint']==3:
                                if abs(elements[ilj2]['pi']['salp']-elements[ilj2]['alp'])%180==90:
                                    sgi=(calelements[ilj2]['EI']/1e6/12+1)*sgi
                                else:
                                    sgi=(4*calelements[ilj2]['EI']/1e6/12+1)*sgi
                            if elements[ilj2]['pi']['restraint']==4:
                                sgi=(4*calelements[ilj2]['EI']/1e6/12+1)*sgi
                        if jlj2>=0:
                            if elements[jlj2]['pj']['restraint']==1 or elements[jlj2]['pj']['restraint']==2:
                                sgj=(3*calelements[jlj2]['EI']/1e6/12+1)*sgj
                            if elements[jlj2]['pj']['restraint']==3:
                                if abs(elements[jlj2]['pj']['salp']-elements[jlj2]['alp'])%180==90:
                                    sgj=(calelements[jlj2]['EI']/1e6/12+1)*sgj
                                else:
                                    sgj=(4*calelements[jlj2]['EI']/1e6/12+1)*sgj
                            if elements[jlj2]['pj']['restraint']==4:
                                sgj=(4*calelements[jlj2]['EI']/1e6/12+1)*sgj
                    if len(c[zdq])!=len(a[zdq]):
                        if sgi>sgj:
                            tishi='杆件%d，左端刚度大于右端刚度'%(zdq+1)+'\n杆件左端弯矩大于右端'
                        if sgi<sgj:
                            tishi='杆件%d，左端刚度小于右端刚度'%(zdq+1)+'\n杆件左端弯矩小于右端'
                        if sgi==sgj: 
                             tishi='杆件%d，右端刚度等于左端刚度'%(zdq+1)+'\n杆件左端弯矩等于右端'
                        return 0
        
                    elif ((c[zdq][0].Mi-c[zdq][-1].Mj)*(a[zdq][0].Mi-a[zdq][-1].Mj)<=0 and sgi!=sgj) or (close(c[zdq][0].Mi,c[zdq][-1].Mj)==False and sgi==sgj):
                        if sgi>sgj:
                            tishi='杆件%d，左端刚度大于右端刚度'%(zdq+1)+'\n杆件左端弯矩大于右端'
                        if sgi<sgj:
                            tishi='杆件%d，左端刚度小于右端刚度'%(zdq+1)+'\n杆件左端弯矩小于右端'
                        if sgi==sgj: 
                             tishi='杆件%d，右端刚度等于左端刚度'%(zdq+1)+'\n杆件左端弯矩等于右端'
                        return 0
        
                if len(elements)>=3:
                    if len(c[ilj])!=len(a[ilj]):
                        if elements[ilj]['pi']['restraint']==2:
                            tishi='杆件%d，铰支座位置弯矩为0' %(ilj+1)
                            return 0
                        if elements[ilj]['pi']['restraint']==3:
                            if abs(elements[ilj]['pi']['salp']-elements[ilj]['alp'])%180==90:
                                tishi='杆件%d,滑动铰支座与杆件垂直，杆上无剪力\n弯矩为一直线'%(ilj+1)
                            else:
                                tishi='杆件%d,滑动铰支座与杆件不垂直，可看作固定端\n两端弯矩比为2：1'%(ilj+1)
                            return 0
                        if elements[ilj]['pi']['restraint']==4:
                            tishi='杆件%d,两端弯矩比为2：1'%(ilj+1)
                            return 0
                    else:
                        if elements[ilj]['pi']['restraint']==2:
                            if close0(c[ilj][0].Mi)==False:
                                tishi='杆件%d，铰支座位置弯矩为0'%(ilj+1)
                                return 0
                        if elements[ilj]['pi']['restraint']==3:
                            if abs(elements[ilj]['pi']['salp']-elements[ilj]['alp'])%180==90:
                                if close(abs(c[ilj][0].Mi),abs(c[ilj][0].Mj))==False:
                                    tishi='杆件%d,滑动铰支座与杆件垂直，杆上无剪力\n弯矩为一直线'%(ilj+1)
                                    return 0
                            else:
                                if max(abs(c[ilj][0].Mi),abs(c[ilj][0].Mj))!=2*min(abs(c[ilj][0].Mi),abs(c[ilj][0].Mj)):
                                    tishi='杆件%d,滑动铰支座与杆件不垂直，可看作固定端\n两端弯矩比为2：1'%(ilj+1)
                                    return 0
                        if elements[ilj]['pi']['restraint']==4:
                            if max(abs(c[ilj][0].Mi),abs(c[ilj][0].Mj))!=2*min(abs(c[ilj][0].Mi),abs(c[ilj][0].Mj)):
                                tishi='杆件%d,两端弯矩比为2：1'%(ilj+1)
                                return 0
                        
                    if len(c[jlj])!=len(a[jlj]):
                        if  elements[jlj]['pj']['restraint']==2:
                            tishi='杆件%d，铰支座位置弯矩为0'%(jlj+1)
                            return 0
                        if elements[jlj]['pj']['restraint']==3:
                            if abs(elements[jlj]['pj']['salp']-elements[jlj]['alp'])%180==90:
                                tishi='杆件%d,滑动铰支座与杆件垂直，杆上无剪力\n弯矩为一直线'%(jlj+1)
                                return 0
                            else:
                                tishi='杆件%d,滑动铰支座与杆件不垂直，可看作固定端\n两端弯矩比为2：1'%(jlj+1)
                            return 0
                            
                        if elements[jlj]['pj']['restraint']==4:
                            tishi='杆件%d,两端弯矩比为2：1'%(jlj+1)
                            return 0
                    else:
                        if elements[jlj]['pj']['restraint']==2:
                            if close0(c[jlj][0].Mi)==False:
                                tishi='杆件%d，铰支座位置弯矩为0'%(jlj+1)
                                return 0
                        if elements[jlj]['pj']['restraint']==3:
                            if abs(elements[jlj]['alp'])-abs(elements[jlj]['pj']['salp'])%180==90:
                                if close(abs(c[jlj][0].Mi),abs(c[jlj][0].Mj))==False:
                                    tishi='杆件%d,滑动铰支座与杆件垂直，杆上无剪力\n弯矩为一直线'%(jlj+1)
                                    return 0
                            else:
                                if max(abs(c[jlj][0].Mi),abs(c[jlj][0].Mj))!=2*min(abs(c[jlj][0].Mi),abs(c[jlj][0].Mj)):
                                    tishi='杆件%d,滑动铰支座与杆件不垂直，可看作固定端\n两端弯矩比为2：1'%(jlj+1)
                                    return 0
                        if elements[jlj]['pj']['restraint']==4:
                            if max(abs(c[jlj][0].Mi),abs(c[jlj][0].Mj))!=2*min(abs(c[jlj][0].Mi),abs(c[jlj][0].Mj)):
                                tishi='杆件%d,两端弯矩比为2：1'%(jlj+1)
                                return 0
                        
                        
                    if len(elements)>=3:
                        for i in range(len(elements)):
                            if elements[i]['pj']['num']==elements[ilj]['pi']['num']:
                                ilj2=i
                            if elements[i]['pi']['num']==elements[jlj]['pj']['num']:
                                jlj2=i
                        if ilj2>=0:
                            if len(c[ilj])!=len(a[ilj]):
                                tishi='杆件%d,两端弯矩比大于2'%(ilj+1)
                                return 0
                            else:
                                if max(abs(c[ilj][0].Mi),abs(c[ilj][0].Mj))<=2*min(abs(c[ilj][0].Mi),abs(c[ilj][0].Mj)):
                                   tishi='杆件%d,两端弯矩比大于2'%(ilj+1) 
                                   return 0
                            if len(c[ilj2])!=len(a[ilj2]):
                                if elements[ilj2]['pi']['restraint']==2:
                                    tishi='杆件%d，铰支座位置弯矩为0'%(ilj2+1)
                                    return 0
                                if elements[ilj2]['pi']['restraint']==3:
                                    if abs(elements[ilj2]['pi']['salp']-elements[ilj2]['alp'])%180==90:
                                        tishi='杆件%d,滑动铰支座与杆件垂直，杆上无剪力\n弯矩为一直线'%(ilj2+1)
                                    else:
                                        tishi='杆件%d,滑动铰支座与杆件不垂直，可看作固定端\n两端弯矩比为2：1'%(ilj2+1)
                                    return 0
                                if elements[ilj2]['pi']['restraint']==4:
                                    tishi='杆件%d,两端弯矩比为2：1'%(ilj2+1)
                                    return 0
                            else:
                                if elements[ilj2]['pi']['restraint']==2:
                                    if close0(c[ilj2][0].Mi)==False:
                                        tishi='杆件%d，铰支座位置弯矩为0'%(ilj2+1)
                                        return 0
                                if elements[ilj2]['pi']['restraint']==3:
                                    if abs(elements[ilj2]['pi']['salp']-elements[ilj2]['alp'])%180==90:
                                        if close(abs(c[ilj2][0].Mi),abs(c[ilj2][0].Mj))==False:
                                            tishi='杆件%d,滑动铰支座与杆件垂直，杆上无剪力\n弯矩为一直线'%(ilj2+1)
                                            return 0
                                    else:
                                        if max(abs(c[ilj2][0].Mi),abs(c[ilj2][0].Mj))!=2*min(abs(c[ilj2][0].Mi),abs(c[ilj2][0].Mj)):
                                            tishi='杆件%d,滑动铰支座与杆件不垂直，可看作固定端\n两端弯矩比为2：1'%(ilj2+1)
                                            return 0
                                if elements[ilj2]['pi']['restraint']==4:
                                    if max(abs(c[ilj2][0].Mi),abs(c[ilj2][0].Mj))!=2*min(abs(c[ilj2][0].Mi),abs(c[ilj2][0].Mj)):
                                        tishi='杆件%d,两端弯矩比为2：1'%(ilj2+1)
                                        return 0
                        if jlj2>=0:
                            if len(c[jlj])!=len(a[jlj]):
                                tishi='杆件%d,两端弯矩比大于2'%(jlj+1)
                                return 0
                            else:
                                if max(abs(c[jlj][0].Mi),abs(c[jlj][0].Mj))<=2*min(abs(c[jlj][0].Mi),abs(c[jlj][0].Mj)):
                                   tishi='杆件%d,两端弯矩比大于2'%(jlj+1) 
                                   return 0
                            if len(c[jlj2])!=len(a[jlj2]):
                                if elements[jlj2]['pj']['restraint']==2:
                                    tishi='杆件%d，铰支座位置弯矩为0'%(jlj2+1)
                                    return 0
                                if elements[jlj2]['pj']['restraint']==3:
                                    if abs(elements[jlj2]['pj']['salp']-elements[jlj2]['alp'])%180==90:
                                        tishi='杆件%d,滑动铰支座与杆件垂直，杆上无剪力\n弯矩为一直线'%(jlj2+1)
                                    else:
                                        tishi='杆件%d,滑动铰支座与杆件不垂直，可看作固定端\n两端弯矩比为2：1'%(jlj2+1)
                                    return 0
                                if elements[jlj2]['pj']['restraint']==4:
                                    tishi='杆件%d,两端弯矩比为2：1'%(jlj2+1)
                                    return 0
                            else:
                                if elements[jlj2]['pj']['restraint']==2:
                                    if close0(c[jlj2][0].Mi)==False:
                                        tishi='杆件%d，铰支座位置弯矩为0'%(jlj2+1)
                                        return 0
                                if elements[jlj2]['pj']['restraint']==3:
                                    if abs(elements[jlj2]['pj']['salp']-elements[jlj2]['alp'])%180==90:
                                        if close(abs(c[jlj2][0].Mi),abs(c[jlj2][0].Mj))==False:
                                            tishi='杆件%d,滑动铰支座与杆件垂直，杆上无剪力\n弯矩为一直线'%(jlj2+1)
                                            return 0
                                    else:
                                        if max(abs(c[jlj2][0].Mi),abs(c[jlj2][0].Mj))!=2*min(abs(c[jlj2][0].Mi),abs(c[jlj2][0].Mj)):
                                            tishi='杆件%d,滑动铰支座与杆件不垂直，可看作固定端\n两端弯矩比为2：1'%(jlj2+1)
                                            return 0
                                if elements[jlj2]['pj']['restraint']==4:
                                    if max(abs(c[jlj2][0].Mi),abs(c[jlj2][0].Mj))!=2*min(abs(c[jlj2][0].Mi),abs(c[jlj2][0].Mj)):
                                        tishi='杆件%d,两端弯矩比为2：1'%(jlj2+1)
                                        return 0       
    
    if wcygj==1 and lxl==0: 
        weizuoda=1
        zdq=-1
        zdqs=[]
        Q=0
        for i in range(len(a)):
            if len(a[i])>1:
                zdqs.append(i)
        for i in range(len(M)):
            for j in range(len(M[i])):
                if close0(M[i][j][5])==False:
                    zdqs.append(i)
                    Q=1
        for i in range(len(a)):
            if len(a[i])==len(c[i]):
                weizuoda=0
        if weizuoda==1 and len(zdqs)==1:
            tishi='角位移为主要因素，考虑增加角约束,采用弯矩分配法'
        if weizuoda==1 and len(zdqs)==2:
            if elements[zdqs[0]]['pi']['num']==elements[zdqs[1]]['pj']['num']:
                tishi='在节点%d处加角约束，计算固端弯矩大小，判断转角'%(elements[zdqs[0]]['pi']['num'])
            if elements[zdqs[0]]['pi']['num']==elements[zdqs[1]]['pi']['num']:
                tishi='在节点%d处加角约束，计算固端弯矩大小，判断转角'%(elements[zdqs[0]]['pi']['num'])
            if elements[zdqs[0]]['pj']['num']==elements[zdqs[1]]['pj']['num']:
                tishi='在节点%d处加角约束，计算固端弯矩大小，判断转角'%(elements[zdqs[0]]['pj']['num'])
            if elements[zdqs[0]]['pj']['num']==elements[zdqs[1]]['pi']['num']:
                tishi='在节点%d处加角约束，计算固端弯矩大小，判断转角'%(elements[zdqs[0]]['pj']['num'])
        if weizuoda==0:
            iljlist=[]
            jljlist=[]
            class Ljd():
                        pass
            
            if len(zdqs)==1:
                zdq=zdqs[0]
            if len(zdqs)==2:
                for zdq in zdqs:
                    iljlist=[]
                    for i in range(len(calelements)):
                        if i not in zdqs:
                            if calelements[i]['pj']['num']==calelements[zdq]['pi']['num']:
                                Ljd_=Ljd()
                                Ljd_.p='j'
                                Ljd_.num=i
                                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                                iljlist.append(copy.copy(Ljd_))
                            if calelements[i]['pi']['num']==calelements[zdq]['pi']['num'] and calelements[i]['pj']['num']!=calelements[zdq]['pj']['num']:
                                Ljd_=Ljd()
                                Ljd_.p='i'
                                Ljd_.num=i
                                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                                iljlist.append(copy.copy(Ljd_))
                    jljlist=[]
                    for i in range(len(calelements)):
                        if i not in zdqs:
                            if calelements[i]['pi']['num']==calelements[zdq]['pj']['num']:
                                Ljd_=Ljd()
                                Ljd_.p='i'
                                Ljd_.num=i
                                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                                jljlist.append(copy.copy(Ljd_))
                            if calelements[i]['pj']['num']==calelements[zdq]['pj']['num'] and calelements[i]['pi']['num']!=calelements[zdq]['pi']['num']:
                                Ljd_=Ljd()
                                Ljd_.p='j'
                                Ljd_.num=i
                                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                                jljlist.append(copy.copy(Ljd_))
                    if len(iljlist)!=0:
                        for i in range(len(iljlist)):
                            num=iljlist[i].num
                            if iljlist[i].p=='j':
                                if elements[iljlist[i].num]['pi']['restraint']==1 :
                                    if abs(elements[iljlist[i].num]['pi']['salp']-elements[iljlist[i].num]['alp'])%90==0:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) :
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                            return 0
                                        elif c[iljlist[i].num][0].Mi!=0 or c[iljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mi!=0:
                                            tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                            return 0
                                if elements[iljlist[i].num]['pi']['restraint']==2 :
                                    if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mi!=0:
                                        tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                        return 0
                                if elements[iljlist[i].num]['pi']['restraint']==3:
                                    if abs(calelements[iljlist[i].num]['pi']['salp']-calelements[iljlist[i].num]['alp'])%180!=90:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(iljlist[i].num+1)
                                            return 0
                                        if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))!=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(iljlist[i].num+1)
                                            return 0
                                        if abs(c[iljlist[i].num][0].Mi)!=abs(c[iljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(iljlist[i].num+1)
                                            return 0
                                if elements[iljlist[i].num]['pi']['restraint']==4:
                                    if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(iljlist[i].num+1)
                                        return 0
                                    if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))!=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(iljlist[i].num+1)
                                        return 0
                                if elements[iljlist[i].num]['pi']['restraint']==0:
                                    jxlj=0
                                    for k in range(len(elements)):
                                        if elements[k]['pj']['num']==elements[num]['pi']['num']:
                                            jxlj=1
                                        if elements[k]['pi']['num']==elements[num]['pi']['num'] and elements[k]['pj']['num']!=elements[num]['pj']['num']:
                                            jxlj==1
                                    if jxlj==1:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
                                            return 0
                                        if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))<=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                            tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        pass
                            
                            if iljlist[i].p=='i':
                                if elements[iljlist[i].num]['pj']['restraint']==1 :
                                    if abs(elements[iljlist[i].num]['pj']['salp']-elements[iljlist[i].num]['alp'])%90==0:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) :
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                            return 0
                                        elif c[iljlist[i].num][0].Mi!=0 or c[iljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                            return 0
                                            
                                if  elements[iljlist[i].num]['pj']['restraint']==2 :
                                     if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mj!=0:
                                        tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                        return 0
                                if elements[iljlist[i].num]['pj']['restraint']==3:
                                    if abs(calelements[iljlist[i].num]['pj']['salp']-calelements[iljlist[i].num]['alp'])%180!=90:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(iljlist[i].num+1)
                                            return 0
                                            print(tishi)
                                        if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))!=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(iljlist[i].num+1)
                                            return 0
                                            print(tishi)
                                        if abs(c[iljlist[i].num][0].Mi)!=abs(c[iljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(iljlist[i].num+1)
                                            return 0
                                if elements[iljlist[i].num]['pj']['restraint']==4:
                                    if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(iljlist[i].num+1)
                                        return 0
                                    if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))!=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(iljlist[i].num+1)
                                        return 0
                                if elements[iljlist[i].num]['pj']['restraint']==0:
                                    jxlj=0
                                    for k in range(len(elements)):
                                        if elements[k]['pi']['num']==elements[num]['pj']['num']:
                                            jxlj=1
                                        if elements[k]['pj']['num']==elements[num]['pj']['num'] and elements[k]['pi']['num']!=elements[num]['pi']['num']:
                                            jxlj==1
                                    if jxlj==1:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
                                            return 0
                                        if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))<=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                            tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        pass
                        
                        
                        
                    if len(jljlist)!=0:
                        for i in range(len(jljlist)):
                            num=jljlist[i].num
                            if jljlist[i].p=='j':
                                if elements[jljlist[i].num]['pi']['restraint']==1 :
                                    if abs(elements[jljlist[i].num]['pi']['salp']-elements[jljlist[i].num]['alp'])%90==0:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) :
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(jljlist[i].num+1)
                                            return 0
                                        elif c[jljlist[i].num][0].Mi!=0 or c[jljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) or c[jljlist[i].num][0].Mi!=0:
                                            tishi='杆件%d，铰支座弯矩为0'%(jljlist[i].num+1)
                                            return 0
                                if elements[jljlist[i].num]['pi']['restraint']==2 :
                                    if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) or c[jljlist[i].num][0].Mi!=0:
                                        tishi='杆件%d，铰支座弯矩为0'%(jljlist[i].num+1)
                                        return 0
                                if elements[jljlist[i].num]['pi']['restraint']==3:
                                    if abs(calelements[jljlist[i].num]['pi']['salp']-calelements[jljlist[i].num]['alp'])%180!=90:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(jljlist[i].num+1)
                                            return 0
                                        if max(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj)!=2*min(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(jljlist[i].num+1)
                                            return 0
                                        if abs(c[jljlist[i].num][0].Mi)!=abs(c[jljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(jljlist[i].num+1)
                                            return 0
                                if elements[jljlist[i].num]['pi']['restraint']==4:
                                    if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(jljlist[i].num+1)
                                        return 0
                                    if max(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj)!=2*min(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(jljlist[i].num+1)
                                        return 0
                                if elements[jljlist[i].num]['pi']['restraint']==0:
                                    jxlj=0
                                    for k in range(len(elements)):
                                        if elements[k]['pj']['num']==elements[num]['pi']['num']:
                                            jxlj=1
                                        if elements[k]['pi']['num']==elements[num]['pi']['num'] and elements[k]['pj']['num']!=elements[num]['pj']['num']:
                                            jxlj==1
                                    if jxlj==1:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d,两端弯矩比大于2'%(jljlist[i].num+1)
                                            return 0
                                        if max(abs(c[jljlist[i].num][0].Mi),abs(c[jljlist[i].num][0].Mj))<=2*min(abs(c[jljlist[i].num][0].Mi),abs(c[jljlist[i].num][0].Mj)):
                                            tishi='杆件%d,两端弯矩比大于2'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        pass
                            
                            if jljlist[i].p=='i':
                                if elements[jljlist[i].num]['pj']['restraint']==1 :
                                    if abs(elements[jljlist[i].num]['pj']['salp']-elements[jljlist[i].num]['alp'])%90==0:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) :
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(jljlist[i].num+1)
                                            return 0
                                        elif c[jljlist[i].num][0].Mi!=0 or c[jljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) or c[jljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d，铰支座弯矩为0'%(jljlist[i].num+1)
                                            return 0
                                            
                                if  elements[jljlist[i].num]['pj']['restraint']==2 :
                                     if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) or c[jljlist[i].num][0].Mj!=0:
                                        tishi='杆件%d，铰支座弯矩为0'%(jljlist[i].num+1)
                                        return 0
                                if elements[jljlist[i].num]['pj']['restraint']==3:
                                    if abs(calelements[jljlist[i].num]['pj']['salp']-calelements[jljlist[i].num]['alp'])%180!=90:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(jljlist[i].num+1)
                                            return 0
                                            print(tishi)
                                        if max(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj)!=2*min(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(jljlist[i].num+1)
                                            return 0
                                            print(tishi)
                                        if abs(c[jljlist[i].num][0].Mi)!=abs(c[jljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(jljlist[i].num+1)
                                            return 0
                                if elements[jljlist[i].num]['pj']['restraint']==4:
                                    if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(jljlist[i].num+1)
                                        return 0
                                    if max(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj)!=2*min(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(jljlist[i].num+1)
                                        return 0
                                if elements[jljlist[i].num]['pj']['restraint']==0:
                                    jxlj=0
                                    for k in range(len(elements)):
                                        if elements[k]['pi']['num']==elements[num]['pj']['num']:
                                            jxlj=1
                                        if elements[k]['pj']['num']==elements[num]['pj']['num'] and elements[k]['pi']['num']!=elements[num]['pi']['num']:
                                            jxlj==1
                                    if jxlj==1:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d,两端弯矩比大于2'%(jljlist[i].num+1)
                                            return 0
                                        if max(abs(c[jljlist[i].num][0].Mi),abs(c[jljlist[i].num][0].Mj))<=2*min(abs(c[jljlist[i].num][0].Mi),abs(c[jljlist[i].num][0].Mj)):
                                            tishi='杆件%d,两端弯矩比大于2'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        pass

                    
    
            if len(zdqs)==1:
                if zdq!=-1:  
                    if calelements[zdq]['pi']['restraint']==1 or calelements[zdq]['pi']['restraint']==2:
                        sgi=0
                    if calelements[zdq]['pi']['restraint']==4:
                        sgi=4
                    if calelements[zdq]['pi']['restraint']==0:
                        iljlist=[]
                        for i in range(len(calelements)):
                            if calelements[i]['pj']['num']==calelements[zdq]['pi']['num']:
                                Ljd_=Ljd()
                                Ljd_.p='j'
                                Ljd_.num=i
                                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                                iljlist.append(copy.copy(Ljd_))
                            if calelements[i]['pi']['num']==calelements[zdq]['pi']['num'] and calelements[i]['pj']['num']!=calelements[zdq]['pj']['num']:
                                Ljd_=Ljd()
                                Ljd_.p='i'
                                Ljd_.num=i
                                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                                iljlist.append(copy.copy(Ljd_))
                        sumsi=0
                        for j in iljlist:
                            sumsi=sumsi+j.s
                        sgi=(sumsi/1e6/3+1)*3
                    if calelements[zdq]['pj']['restraint']==1 or calelements[zdq]['pj']['restraint']==2:
                        sgj=0
                    if calelements[zdq]['pj']['restraint']==4:
                        sgj=4
                    if calelements[zdq]['pj']['restraint']==0 :
                        jljlist=[]
                        for i in range(len(calelements)):
                            if calelements[i]['pi']['num']==calelements[zdq]['pj']['num']:
                                Ljd_=Ljd()
                                Ljd_.p='i'
                                Ljd_.num=i
                                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                                jljlist.append(copy.copy(Ljd_))
                            if calelements[i]['pj']['num']==calelements[zdq]['pj']['num'] and calelements[i]['pi']['num']!=calelements[zdq]['pi']['num']:
                                Ljd_=Ljd()
                                Ljd_.p='j'
                                Ljd_.num=i
                                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                                jljlist.append(copy.copy(Ljd_))
                        sumsj=0
                        for j in jljlist:
                            sumsj=sumsj+j.s
                        sgj=(sumsj/1e6/3+1)*3
                    if calelements[zdq]['pi']['restraint']==3:
                        if abs((calelements[zdq]['pi']['salp']-calelements[zdq]['alp']))%180!=90:
                            sgi=4
                        else:
                            sgi=1
                    if calelements[zdq]['pj']['restraint']==3:
                        if abs((calelements[zdq]['pj']['salp']-calelements[zdq]['alp']))%180!=90:
                            sgj=4
                        else:
                            sgj=1
                    print('sgi=%f'%sgi,'sgj=%f'%sgj)
                    if sgi<sgj:
                        if sgi==1:
                            if len(c[zdq])!=len(a[zdq]):
                                if Q==0 and close0(a[i][0].Mi,a[i][0].Mj)==False:
                                    tishi='杆件%d，存在滑动铰支座与杆件垂直不提供剪力，\n弯矩图一部分为直线'%(zdq+1)
                                    return 0
                                if Q==1:
                                   tishi='杆件%d，滑动铰支座端刚度小于另一端，\n因此滑动铰支座端弯矩小于另一端弯矩'%(zdq+1)
                                   return 0 
                            elif (abs(a[zdq][0].Mi)-abs(a[zdq][-1].Mj))*(abs(c[zdq][0].Mi)-abs(c[zdq][-1].Mj))<=0:
                                tishi='杆件%d，滑动铰支座端刚度小于另一端，\n因此滑动铰支座端弯矩小于另一端弯矩'%(zdq+1)
                                return 0
                        else:
                            if len(c[zdq])!=len(a[zdq]) or (a[zdq][0].Mi-a[zdq][-1].Mj)*(c[zdq][0].Mi-c[zdq][-1].Mj)<=0:
                                if elements[zdq]['pi']['restraint']==1 :
                                    if abs(calelements[zdq]['pi']['salp']-calelements[zdq]['alp'])%180==90 and len(iljlist)==0:
                                        tishi='杆件%d，铰支座弯矩为0，受拉侧判断有误'%(zdq+1)
                                        return 0
                                    else:
                                        if elements[zdq]['alp']==90:
                                            tishi='杆件%d下端刚度小于上端刚度，\n因此下端弯矩小于上端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['alp']==-90:
                                            tishi='杆件%d上端端刚度小于下端刚度，\n因此上端弯矩小于下端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['pi']['x']<elements[zdq]['pj']['x']:
                                            tishi='杆件%d左端刚度小于右端刚度，\n因此左端弯矩小于右端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['pi']['x']>elements[zdq]['pj']['x']:
                                            tishi='杆件%d右端刚度小于左端刚度，\n因此右端弯矩小于左端弯矩'%(zdq+1)
                                            return 0
                                if elements[zdq]['pi']['restraint']==2 :
                                    tishi='杆件%d，铰支座弯矩为0，受拉侧判断有误'%(zdq+1)
                                    return 0
                                if elements[zdq]['pj']['restraint']==1 :
                                    if abs(calelements[zdq]['pj']['salp']-calelements[zdq]['alp'])%180==90 and len(jljlist)==0:
                                        tishi='杆件%d，铰支座弯矩为0，受拉侧判断有误'%(zdq+1)
                                        return 0
                                    else:
                                        if elements[zdq]['alp']==90:
                                            tishi='杆件%d下端刚度小于上端刚度，\n因此下端弯矩小于上端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['alp']==-90:
                                            tishi='杆件%d上端端刚度小于下端刚度，\n因此上端弯矩小于下端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['pi']['x']<elements[zdq]['pj']['x']:
                                            tishi='杆件%d左端刚度小于右端刚度，\n因此左端弯矩小于右端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['pi']['x']>elements[zdq]['pj']['x']:
                                            tishi='杆件%d右端刚度小于左端刚度，\n因此右端弯矩小于左端弯矩'%(zdq+1)
                                            return 0
                                if elements[zdq]['pj']['restraint']==2 :
                                    tishi='杆件%d，铰支座弯矩为0，受拉侧判断有误'%(zdq+1)
                                    return 0
                                if elements[zdq]['pj']['restraint']==3:
                                    if abs(elements[zdq]['pj']['salp']-elements[zdq]['alp'])%180!=90:
                                        tishi='滑动铰支座与杆件不垂直，相当于固定端，刚度大于另一端'%(zdq+1)
                                        return 0 
                                if elements[zdq]['pi']['restraint']==0:
                                    if elements[zdq]['alp']==90:
                                        tishi='杆件%d下端刚度小于上端刚度，\n因此下端弯矩小于上端弯矩'%(zdq+1)
                                        return 0
                                    elif elements[zdq]['alp']==-90:
                                        tishi='杆件%d上端端刚度小于下端刚度，\n因此上端弯矩小于下端弯矩'%(zdq+1)
                                        return 0
                                    elif elements[zdq]['pi']['x']<elements[zdq]['pj']['x']:
                                        tishi='杆件%d左端刚度小于右端刚度，\n因此左端弯矩小于右端弯矩'%(zdq+1)
                                        return 0
                                    elif elements[zdq]['pi']['x']>elements[zdq]['pj']['x']:
                                        tishi='杆件%d右端刚度小于左端刚度，\n因此右端弯矩小于左端弯矩'%(zdq+1)
                                        return 0
                    if sgi>sgj:
                        if sgj==1:
                            if len(c[zdq])!=len(a[zdq]):
                                if Q==0 and close(c[zdq][0].Mi,c[zdq][0].Mj)==False:
                                    tishi='杆件%d，存在滑动铰支座与杆件垂直，不提供剪力，\n弯矩图一部分为直线'%(zdq+1)
                                    return 0
                                if Q==1:
                                    tishi='杆件%d，滑动铰支座端于杆件垂直刚度小于另一端，\n因此滑动铰支座端弯矩小于另一端弯矩'%(zdq+1)
                                    return 0
                            elif (abs(a[zdq][0].Mi)-abs(a[zdq][-1].Mj))*(abs(c[zdq][0].Mi)-abs(c[zdq][-1].Mj))<=0:
                                tishi='杆件%d，滑动铰支座端于杆件垂直刚度小于另一端，\n因此滑动铰支座端弯矩小于另一端弯矩'%(zdq+1)
                                return 0
                        else:
                            if len(c[zdq])!=len(a[zdq]) or (a[zdq][0].Mi-a[zdq][-1].Mj)*(c[zdq][0].Mi-c[zdq][-1].Mj)<=0:
                                if elements[zdq]['pi']['restraint']==1 :
                                    if abs(calelements[zdq]['pi']['salp']-calelements[zdq]['alp'])%180==90 and len(iljlist)==0:
                                        tishi='杆件%d，铰支座弯矩为0，受拉侧判断有误'%(zdq+1)
                                        return 0
                                    else:
                                        if elements[zdq]['alp']==90:
                                            tishi='杆件%d上端端刚度小于下端刚度，\n因此上端弯矩小于下端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['alp']==-90:
                                            tishi='杆件%d下端刚度小于上端刚度，\n因此下端弯矩小于上端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['pi']['x']<elements[zdq]['pj']['x']:
                                            tishi='杆件%d右端刚度小于左端刚度，\n因此右端弯矩小于左端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['pi']['x']>elements[zdq]['pj']['x']:
                                            tishi='杆件%d左端刚度小于右端刚度，\n因此左端弯矩小于右端弯矩'%(zdq+1)
                                            return 0
                                if elements[zdq]['pi']['restraint']==2 :
                                    tishi='杆件%d，铰支座弯矩为0，受拉侧判断有误'%(zdq+1)
                                    return 0
                                if elements[zdq]['pj']['restraint']==1 :
                                    if abs(calelements[zdq]['pj']['salp']-calelements[zdq]['alp'])%180==0 and len(jljlist)==0:
                                        tishi='杆件%d，铰支座弯矩为0，受拉侧判断有误'%(zdq+1)
                                        return 0
                                    else:
                                        if elements[zdq]['alp']==90:
                                            tishi='杆件%d上端端刚度小于下端刚度，\n因此上端弯矩小于下端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['alp']==-90:
                                            tishi='杆件%d下端刚度小于上端刚度，\n因此下端弯矩小于上端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['pi']['x']<elements[zdq]['pj']['x']:
                                            tishi='杆件%d右端刚度小于左端刚度，\n因此右端弯矩小于左端弯矩'%(zdq+1)
                                            return 0
                                        elif elements[zdq]['pi']['x']>elements[zdq]['pj']['x']:
                                            tishi='杆件%d左端刚度小于右端刚度，\n因此左端弯矩小于右端弯矩'%(zdq+1)
                                            return 0
                                if elements[zdq]['pj']['restraint']==2 :
                                    tishi='杆件%d，铰支座弯矩为0，受拉侧判断有误'%(zdq+1)
                                    return 0
                                if elements[zdq]['pi']['restraint']==3 :
                                    if abs(elements[zdq]['pi']['salp']-elements[zdq]['alp'])%180!=90:
                                        tishi='滑动铰支座与杆件不垂直，相当于固定端，刚度大于另一端'%(zdq+1)
                                        return 0 
                                if elements[zdq]['pi']['restraint']==0 or elements[zdq]['pi']['restraint']==4:
                                    if elements[zdq]['alp']==90:
                                        tishi='杆件%d上端端刚度小于下端刚度，\n因此上端弯矩小于下端弯矩'%(zdq+1)
                                        return 0
                                    elif elements[zdq]['alp']==-90:
                                        tishi='杆件%d下端刚度小于上端刚度，\n因此下端弯矩小于上端弯矩'%(zdq+1)
                                        return 0
                                    elif elements[zdq]['pi']['x']<elements[zdq]['pj']['x']:
                                        tishi='杆件%d右端刚度小于左端刚度，\n因此右端弯矩小于左端弯矩'%(zdq+1)
                                        return 0
                                    elif elements[zdq]['pi']['x']>elements[zdq]['pj']['x']:
                                        tishi='杆件%d左端刚度小于右端刚度，\n因此左端弯矩小于右端弯矩'%(zdq+1)
                                        return 0
                    if sgi==sgj:
                        if len(c[zdq])!=len(a[zdq])  or c[zdq][0].Mi!=c[zdq][0].Mj:
                            tishi='杆件%d两端刚度相等，\n因此两端弯矩相等'%(zdq+1)
                            return 0
                    if len(iljlist)!=0:
                        for i in range(len(iljlist)):
                            num=iljlist[i].num
                            if iljlist[i].p=='j':
                                if elements[iljlist[i].num]['pi']['restraint']==1 :
                                    if abs(elements[iljlist[i].num]['pi']['salp']-elements[iljlist[i].num]['alp'])%90==0:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) :
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                            return 0
                                        elif c[iljlist[i].num][0].Mi!=0 or c[iljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mi!=0:
                                            tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                            return 0
                                if elements[iljlist[i].num]['pi']['restraint']==2 :
                                    if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mi!=0:
                                        tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                        return 0
                                if elements[iljlist[i].num]['pi']['restraint']==3:
                                    if abs(calelements[iljlist[i].num]['pi']['salp']-calelements[iljlist[i].num]['alp'])%180!=90:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(iljlist[i].num+1)
                                            return 0
                                        if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))!=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(iljlist[i].num+1)
                                            return 0
                                        if abs(c[iljlist[i].num][0].Mi)!=abs(c[iljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(iljlist[i].num+1)
                                            return 0
                                if elements[iljlist[i].num]['pi']['restraint']==4:
                                    if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(iljlist[i].num+1)
                                        return 0
                                    if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))!=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(iljlist[i].num+1)
                                        return 0
                                if elements[iljlist[i].num]['pi']['restraint']==0:
                                    jxlj=0
                                    for k in range(len(elements)):
                                        if elements[k]['pj']['num']==elements[num]['pi']['num']:
                                            jxlj=1
                                        if elements[k]['pi']['num']==elements[num]['pi']['num'] and elements[k]['pj']['num']!=elements[num]['pj']['num']:
                                            jxlj==1
                                    if jxlj==1:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
                                            return 0
                                        if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))<=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                            tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        pass
                            
                            if iljlist[i].p=='i':
                                if elements[iljlist[i].num]['pj']['restraint']==1 :
                                    if abs(elements[iljlist[i].num]['pj']['salp']-elements[iljlist[i].num]['alp'])%90==0:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) :
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                            return 0
                                        elif c[iljlist[i].num][0].Mi!=0 or c[iljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                            return 0
                                            
                                if  elements[iljlist[i].num]['pj']['restraint']==2 :
                                     if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mj!=0:
                                        tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                        return 0
                                if elements[iljlist[i].num]['pj']['restraint']==3:
                                    if abs(calelements[iljlist[i].num]['pj']['salp']-calelements[iljlist[i].num]['alp'])%180!=90:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(iljlist[i].num+1)
                                            return 0
                                            print(tishi)
                                        if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))!=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(iljlist[i].num+1)
                                            return 0
                                            print(tishi)
                                        if abs(c[iljlist[i].num][0].Mi)!=abs(c[iljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(iljlist[i].num+1)
                                            return 0
                                if elements[iljlist[i].num]['pj']['restraint']==4:
                                    if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(iljlist[i].num+1)
                                        return 0
                                    if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))!=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(iljlist[i].num+1)
                                        return 0
                                if elements[iljlist[i].num]['pj']['restraint']==0:
                                    jxlj=0
                                    for k in range(len(elements)):
                                        if elements[k]['pi']['num']==elements[num]['pj']['num']:
                                            jxlj=1
                                        if elements[k]['pj']['num']==elements[num]['pj']['num'] and elements[k]['pi']['num']!=elements[num]['pi']['num']:
                                            jxlj==1
                                    if jxlj==1:
                                        if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                            tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
                                            return 0
                                        if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))<=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
                                            tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
                                            return 0
                                    else:
                                        pass
                        
                        
                        
                    if len(jljlist)!=0:
                        for i in range(len(jljlist)):
                            num=jljlist[i].num
                            if jljlist[i].p=='j':
                                if elements[jljlist[i].num]['pi']['restraint']==1 :
                                    if abs(elements[jljlist[i].num]['pi']['salp']-elements[jljlist[i].num]['alp'])%90==0:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) :
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(jljlist[i].num+1)
                                            return 0
                                        elif c[jljlist[i].num][0].Mi!=0 or c[jljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) or c[jljlist[i].num][0].Mi!=0:
                                            tishi='杆件%d，铰支座弯矩为0'%(jljlist[i].num+1)
                                            return 0
                                if elements[jljlist[i].num]['pi']['restraint']==2 :
                                    if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) or c[jljlist[i].num][0].Mi!=0:
                                        tishi='杆件%d，铰支座弯矩为0'%(jljlist[i].num+1)
                                        return 0
                                if elements[jljlist[i].num]['pi']['restraint']==3:
                                    if abs(calelements[jljlist[i].num]['pi']['salp']-calelements[jljlist[i].num]['alp'])%180!=90:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(jljlist[i].num+1)
                                            return 0
                                        if max(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj)!=2*min(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(jljlist[i].num+1)
                                            return 0
                                        if abs(c[jljlist[i].num][0].Mi)!=abs(c[jljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(jljlist[i].num+1)
                                            return 0
                                if elements[jljlist[i].num]['pi']['restraint']==4:
                                    if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(jljlist[i].num+1)
                                        return 0
                                    if max(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj)!=2*min(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(jljlist[i].num+1)
                                        return 0
                                if elements[jljlist[i].num]['pi']['restraint']==0:
                                    jxlj=0
                                    for k in range(len(elements)):
                                        if elements[k]['pj']['num']==elements[num]['pi']['num']:
                                            jxlj=1
                                        if elements[k]['pi']['num']==elements[num]['pi']['num'] and elements[k]['pj']['num']!=elements[num]['pj']['num']:
                                            jxlj==1
                                    if jxlj==1:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d,两端弯矩比大于2'%(jljlist[i].num+1)
                                            return 0
                                        if max(abs(c[jljlist[i].num][0].Mi),abs(c[jljlist[i].num][0].Mj))<=2*min(abs(c[jljlist[i].num][0].Mi),abs(c[jljlist[i].num][0].Mj)):
                                            tishi='杆件%d,两端弯矩比大于2'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        pass
                            
                            if jljlist[i].p=='i':
                                if elements[jljlist[i].num]['pj']['restraint']==1 :
                                    if abs(elements[jljlist[i].num]['pj']['salp']-elements[jljlist[i].num]['alp'])%90==0:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) :
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(jljlist[i].num+1)
                                            return 0
                                        elif c[jljlist[i].num][0].Mi!=0 or c[jljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) or c[jljlist[i].num][0].Mj!=0:
                                            tishi='杆件%d，铰支座弯矩为0'%(jljlist[i].num+1)
                                            return 0
                                            
                                if  elements[jljlist[i].num]['pj']['restraint']==2 :
                                     if len(a[jljlist[i].num])!=len(c[jljlist[i].num]) or c[jljlist[i].num][0].Mj!=0:
                                        tishi='杆件%d，铰支座弯矩为0'%(jljlist[i].num+1)
                                        return 0
                                if elements[jljlist[i].num]['pj']['restraint']==3:
                                    if abs(calelements[jljlist[i].num]['pj']['salp']-calelements[jljlist[i].num]['alp'])%180!=90:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(jljlist[i].num+1)
                                            return 0
                                            print(tishi)
                                        if max(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj)!=2*min(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n弯矩比为2：1'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(jljlist[i].num+1)
                                            return 0
                                            print(tishi)
                                        if abs(c[jljlist[i].num][0].Mi)!=abs(c[jljlist[i].num][0].Mj):
                                            tishi='杆件%d滑动铰支座与杆件垂直，弯矩为一直线'%(jljlist[i].num+1)
                                            return 0
                                if elements[jljlist[i].num]['pj']['restraint']==4:
                                    if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(jljlist[i].num+1)
                                        return 0
                                    if max(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj)!=2*min(c[jljlist[i].num][0].Mi,c[jljlist[i].num][0].Mj):
                                        tishi='杆件%d固定端与另一端弯矩大小比为1：2'%(jljlist[i].num+1)
                                        return 0
                                if elements[jljlist[i].num]['pj']['restraint']==0:
                                    jxlj=0
                                    for k in range(len(elements)):
                                        if elements[k]['pi']['num']==elements[num]['pj']['num']:
                                            jxlj=1
                                        if elements[k]['pj']['num']==elements[num]['pj']['num'] and elements[k]['pi']['num']!=elements[num]['pi']['num']:
                                            jxlj==1
                                    if jxlj==1:
                                        if len(a[jljlist[i].num])!=len(c[jljlist[i].num]):
                                            tishi='杆件%d,两端弯矩比大于2'%(jljlist[i].num+1)
                                            return 0
                                        if max(abs(c[jljlist[i].num][0].Mi),abs(c[jljlist[i].num][0].Mj))<=2*min(abs(c[jljlist[i].num][0].Mi),abs(c[jljlist[i].num][0].Mj)):
                                            tishi='杆件%d,两端弯矩比大于2'%(jljlist[i].num+1)
                                            return 0
                                    else:
                                        pass

                
            
#        if len(jljlist)!=0:
#            for i in range(len(jljlist)):
#                num=jljlist[i].num
#                if jljlist[i].p=='j':
#                    if elements[jljlist[i].num]['pi']['restraint']==1 or elements[jljlist[i].num]['pi']['restraint']==2 :
#                        pass
#                    if elements[jljlist[i].num]['pi']['restraint']==3:
#                        if (calelements[jljlist[i].num]['pi']['salp']-calelements[jljlist[i].num]['alp'])%90!=0:
#                            pass
#                        else:
#                            pass
#                    if elements[jljlist[i].num]['pi']['restraint']==4:
#                        pass
#                    if elements[jljlist[i].num]['pi']['restraint']==0:
#                        jxlj=0
#                        for k in range(len(elements)):
#                            if elements[k]['pj']['num']==elements[num]['pi']['num']:
#                                jxlj=1
#                            if elements[k]['pi']['num']==elements[num]['pi']['num'] and elements[k]['pj']['num']!=elements[num]['pj']['num']:
#                                jxlj==1
#                        if jxlj==1:
#                            pass
#                        else:
#                            pass
#                
#                if jljlist[i].p=='i':
#                    if elements[jljlist[i].num]['pj']['restraint']==1 or elements[jljlist[i].num]['pj']['restraint']==2 :
#                        pass
#                    if elements[jljlist[i].num]['pj']['restraint']==3:
#                        if (calelements[jljlist[i].num]['pi']['salp']-calelements[jljlist[i].num]['alp'])%90!=0:
#                            pass
#                        else:
#                            pass
#                    if elements[jljlist[i].num]['pj']['restraint']==4:
#                        pass
#                    if elements[jljlist[i].num]['pj']['restraint']==0:
#                        jxlj=0
#                        for k in range(len(elements)):
#                            if elements[k]['pi']['num']==elements[num]['pj']['num']:
#                                jxlj=1
#                            if elements[k]['pj']['num']==elements[num]['pj']['num'] and elements[k]['pi']['num']!=elements[num]['pi']['num']:
#                                jxlj==1
#                        if jxlj==1:
#                            pass
#                        else:
#                            pass
        
    if fzjlfpf==1 and zzcj==0 and jdjg!=1:
        Q=0
        weizuoda=1
        for i in range(len(calelements)):
            if abs(calelements[i]['alp'])%180==90:
                if calelements[i]['pi']['Fx']!=0 or calelements[i]['pj']['Fx']!=0:
                    zdq=i
        for i in range(len(a)):
            if len(a[i])>1:
                zdq=i
        for i in range(len(M)):
            for j in range(len(M[i])):
                if close0(M[i][j][5])==False:
                    zdq=i
                    Q=1
        for i in range(len(a)):
            if len(a[i])==len(c[i]):
                weizuoda=0
        if weizuoda==1:
            tishi='线位移为主要因素，需先判断整体结构线位移的方向，\n再结合剪力分配法'
            tishi+='做出主要受力区,杆件%d的弯矩图'%(zdq+1)
            return 0
            
        if weizuoda==0:
            if len(a[zdq])!=len(c[zdq]):
                tishi='尝试先做出主要受力区,杆件%d的弯矩图'%(zdq+1)
                return 0
            if close0(a[zdq][0].Mi)==True : 
                if close0(c[zdq][0].Mi)==False:
                    tishi='节点%d弯矩应该为0'%(calelements[zdq]['pi']['num'])
                    return 0
                if a[zdq][0].Mj*c[zdq][0].Mj<0:
                    tishi='杆件%d受拉侧判断错误'%(zdq+1)
                    return 0
            if close0(a[zdq][0].Mj)==True :
                if close0(c[zdq][0].Mj)==False:
                    tishi='节点%d弯矩应该为0'%(calelements[zdq]['pj']['num'])
                    return 0
                if a[zdq][0].Mi*c[zdq][0].Mi<0:
                    tishi='杆件%d受拉侧判断错误'%(zdq+1)
                    return 0
            if close(abs(a[zdq][0].Mi),abs(a[zdq][0].Mj))==True and close(abs(c[zdq][0].Mi),abs(c[zdq][0].Mj))==False:
                tishi='杆件%d两端弯矩大小应相等'%(zdq+1)
                return 0
            if abs(a[zdq][0].Mi)>abs(a[zdq][0].Mj) and abs(c[zdq][0].Mi)<abs(c[zdq][0].Mj):
                if len(a[zdq])>1 or Q>0:
                    tishi='杆件%d作答有误，尝试增减线约束，并采用夹逼法'
                    return 0
            for i in range(len(elements)):
                if abs(calelements[i]['alp'])%180==90:
                    if i!=zdq:
                        if len(a[i])!=len(c[i]):
                            if abs(calelements[i]['pi']['displacement'][0])>abs(calelements[i]['pj']['displacement'][0]):
                                tishi='杆件%d的节点%d更靠近主动区，线位移更大'%(i+1,calelements[i]['pi']['num'])
                                tishi+='根据线位移方向，画出杆件%d的弯矩图'%(i+1)
                                return 0
                            if abs(calelements[i]['pi']['displacement'][0])<abs(calelements[i]['pj']['displacement'][0]):
                                tishi='杆件%d的节点%d更靠近主动区，线位移更大'%(i+1,calelements[i]['pj']['num'])
                                tishi+='根据线位移方向，画出杆件%d弯矩图'%(i+1)
                                return 0
                            if close(calelements[i]['pi']['displacement'][0],calelements[i]['pj']['displacement'][0]):
                                tishi='杆件%d，两端位移相等，无弯矩'%(i+1)
                                return 0
                        if calelements[i]['pi']['connection']==1 and calelements[i]['pj']['connection']==1 and calelements[i]['pi']['restraint']!=2 and calelements[i]['pj']['restraint']!=2:
                            if a[i][0].Mi*c[i][0].Mi<0 or close(abs(c[i][0].Mi),abs(c[i][0].Mj))==False:
                                if abs(calelements[i]['pi']['displacement'][0])>abs(calelements[i]['pj']['displacement'][0]):
                                    tishi='杆件%d受拉侧判断有误，节点%d更靠近主动区，线位移更大'%(i+1,calelements[i]['pi']['num'])
                                    return 0
                                if abs(calelements[i]['pi']['displacement'][0])<abs(calelements[i]['pj']['displacement'][0]):
                                    tishi='杆件%d受拉侧判断有误，节点%d更靠近主动区，线位移更大'%(i+1,calelements[i]['pj']['num'])
                                    return 0
                        else:
                            if a[i][0].Mi*c[i][0].Mi<0 and close0(a[i][0].Mi)==False:
                                if abs(calelements[i]['pi']['displacement'][0])>abs(calelements[i]['pj']['displacement'][0]):
                                    tishi='杆件%d受拉侧判断有误，节点%d更靠近主动区，线位移更大'%(i+1,calelements[i]['pi']['num'])
                                    return 0
                                if abs(calelements[i]['pi']['displacement'][0])<abs(calelements[i]['pj']['displacement'][0]):
                                    tishi='杆件%d受拉侧判断有误，节点%d更靠近主动区，线位移更大'%(i+1,calelements[i]['pj']['num'])
                                    return 0
                            if a[i][0].Mj*c[i][0].Mj<0 and close0(a[i][0].Mj)==False:
                                if abs(calelements[i]['pi']['displacement'][0])>abs(calelements[i]['pj']['displacement'][0]):
                                    tishi='杆件%d受拉侧判断有误，节点%d更靠近主动区，线位移更大'%(i+1,calelements[i]['pi']['num'])
                                    return 0
                                if abs(calelements[i]['pi']['displacement'][0])<abs(calelements[i]['pj']['displacement'][0]):
                                    tishi='杆件%d受拉侧判断有误，节点%d更靠近主动区，线位移更大'%(i+1,calelements[i]['pj']['num'])
                                    return 0
    
    
    
    
    if jdjlfpf==1 and jdjg!=1:
        weizuoda=1
        for i in range(len(a)):
            if len(a[i])==len(c[i]):
                weizuoda=0
        if weizuoda==1:
            tishi='线位移为主要因素，考虑剪力分配法\n可将两端固结的竖杆看作一端固定和一端滑动的杆件'
            tishi+='\n将一端铰接，一端固结的竖杆看作悬臂梁'
        if weizuoda==0: 
            yfanwei=[]
            for i in range(len(joints_)):
                if joints_[i]['y'] not in yfanwei:
                    yfanwei.append(joints_[i]['y'])
            yfanwei.sort(reverse=True)
            jianli=0
            global xielv
            xielv=[]
            for i in range(len(yfanwei)-1):
                zxielv=0
                for j in range(len(caljoints_)):
                    if caljoints_[j]['y']==yfanwei[i]:
                        jianli=jianli+caljoints_[j]['Fx']
                if i!=0:
                    sygj=shouliganjian[0]
                shouliganjian=[]
                class Ganjian():
                    pass
                sumEI=0
                for k in range(len(calelements)):
                    if (calelements[k]['pi']['y']==yfanwei[i] or calelements[k]['pj']['y']==yfanwei[i]) and abs(calelements[k]['alp'])%180==90: 
                        if max(calelements[k]['pi']['y'] ,calelements[k]['pj']['y'])<=yfanwei[i]:
                            if calelements[k]['pi']['connection']==1 and calelements[k]['pj']['connection']==1 and calelements[k]['pj']['restraint']!=2 and calelements[k]['pi']['restraint']!=2:
                                Ganjian_=Ganjian()
                                Ganjian_.ceng=len(yfanwei)-1-i
                                Ganjian_.zongjianli=jianli
                                Ganjian_.num=k
                                Ganjian_.EI=calelements[k]['EI']*12
                                Ganjian_.lianjie='g'
                                shouliganjian.append(copy.copy(Ganjian_))
                                sumEI=sumEI+Ganjian_.EI
                            else:
                                Ganjian_=Ganjian()
                                Ganjian_.ceng=len(yfanwei)-1-i
                                Ganjian_.zongjianli=jianli
                                Ganjian_.num=k
                                Ganjian_.EI=calelements[k]['EI']*3
                                Ganjian_.lianjie='j'
                                shouliganjian.append(copy.copy(Ganjian_))
                                sumEI=sumEI+Ganjian_.EI
                for gj in shouliganjian:
                    if gj.lianjie=='g':
                        if len(c[gj.num])!=len(a[gj.num]) or abs(c[gj.num][0].Mi)!=abs(c[gj.num][0].Mj):
                            tishi='竖杆%d，两端弯矩大小相等'%(gj.num+1)
                            return 0
                    if gj.lianjie=='j':
                        if len(c[gj.num])!=len(a[gj.num]):
                            tishi='将竖杆%d，看作悬臂梁'%(gj.num+1)
                            return 0
                print('len=%d'%(len(shouliganjian)))
                for gj in shouliganjian:
                    for gj2 in shouliganjian:
                        print('gj.EI=%d'%gj.EI)
                        print('gj2.EI=%d'%gj2.EI)
                        if gj.lianjie=='g' and gj2.lianjie=='g':
                            if abs(c[gj.num][0].Mi)/abs(c[gj2.num][0].Mi)!=gj.EI/gj2.EI:
                                tishi='第%d层，剪力分配有误，请注意刚度差异'%(gj.ceng)
                                tishi+='\n有铰的竖杆，抗剪刚度系数为3，无铰的竖杆，抗剪刚度系数为12'
                                return 0
                        if gj.lianjie=='j' and gj2.lianjie=='g':
                            if max(abs(c[gj.num][0].Mi),abs(c[gj.num][0].Mj))/abs(c[gj2.num][0].Mi)!=2*gj.EI/gj2.EI:
                                tishi='第%d层，剪力分配有误，请注意刚度差异'%(gj.ceng)
                                tishi+='\n有铰的竖杆，抗剪刚度系数为3，无铰的竖杆，抗剪刚度系数为12'
                                return 0
                        if gj.lianjie=='g' and gj2.lianjie=='j':
                            if max(abs(c[gj2.num][0].Mi),abs(c[gj2.num][0].Mj))/abs(c[gj.num][0].Mi)!=2*gj2.EI/gj.EI:
                                tishi='第%d层，剪力分配有误，请注意刚度差异'%(gj.ceng)
                                tishi+='\n有铰的竖杆，抗剪刚度系数为3，无铰的竖杆，抗剪刚度系数为12'
                                return 0
                        if gj.lianjie=='j' and gj2.lianjie=='j':
                            if max(abs(c[gj.num][0].Mi),abs(c[gj.num][0].Mj))/max(abs(c[gj2.num][0].Mi),abs(c[gj2.num][0].Mj))!=gj.EI/gj2.EI:
                                tishi='第%d层，剪力分配有误，请注意刚度差异'%(gj.ceng)
                                tishi+='\n有铰的竖杆，抗剪刚度系数为3，无铰的竖杆，抗剪刚度系数为12'
                                return 0
                for l in range(len(shouliganjian)):
                    zxielv=abs(c[shouliganjian[l].num][0].Mi)+zxielv
                    print(zxielv)
                print(zxielv)
                xielv.append(zxielv)
                if shouliganjian[0].ceng!=len(yfanwei)-1:
#                    if close(abs(c[sygj.num][0].Mi)/abs(c[shouliganjian[0].num][0].Mi),abs(a[sygj.num][0].Mi)/abs(a[shouliganjian[0].num][0].Mi))==False
                    print('sygj.zongjianli=%f'%sygj.zongjianli)
                    print('shouliganjian[0].zongjianli=%f'%shouliganjian[0].zongjianli)
                    print(xielv[i])
                    print(xielv[i-1])
                    if sygj.zongjianli<shouliganjian[0].zongjianli:
                         if xielv[i]<=xielv[i-1]:
                             tishi='注意剪力应逐层叠加，不断向下传递'
                             return 0
     
    if wdbh==1:
        if len(elements)==2:
            wdjy=1
            zxbb=1
            for t in Temperatures:
                if t.t1!=t.t2:
                    wdjy=0
                if t.t1+t.t2!=0:
                    zxbb=0
            if wdjy==1:
                tishi='两杆的连接处增加角约束，绘出变形图，弯矩图'
                if len(a[0])==len(c[0]):
                    tishi='连接处增加的角约束不提供弯矩，可直接去除'
            if zxbb==1:
                tishi='将两杆在连接处断开，观察变形图'
                tishi+='\n可在连接处，增加一对相反的弯矩，从而达到平衡'


    if zzcj==1 and jdjg!=1:
        if abs(elements[Settlements[0].num]['alp']%180)==0:
            if Settlements[0].delta[0]!=0:
                tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pj']['num'])
                fjointnum=elements[Settlements[0].num]['pj']['num']
            if Settlements[0].delta[1]!=0:
                ilj=0
                jlj=0
                for i in range(len(elements)):
                    if elements[i]['pj']['num']==elements[Settlements[0].num]['pi']['num']:
                        ilj=1
                    if elements[i]['pi']['num']==elements[Settlements[0].num]['pj']['num']:
                        jlj=1
                if ilj==1 and jlj==1:
                    tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pi']['num'])
                    fjointnum=elements[Settlements[0].num]['pi']['num']
                else:
                    tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pj']['num'])
                    fjointnum=elements[Settlements[0].num]['pj']['num']
            if Settlements[0].delta[2]!=0:
                tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pj']['num'])
                fjointnum=elements[Settlements[0].num]['pj']['num']
            if Settlements[0].delta[3]!=0:
                tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pj']['num'])
                fjointnum=elements[Settlements[0].num]['pj']['num']
            if Settlements[0].delta[4]!=0:
                ilj=0
                jlj=0
                for i in range(len(elements)):
                    if elements[i]['pj']['num']==elements[Settlements[0].num]['pi']['num']:
                        ilj=1
                    if elements[i]['pi']['num']==elements[Settlements[0].num]['pj']['num']:
                        jlj=1
                if ilj==1 and jlj==1:
                    tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pj']['num'])
                    fjointnum=elements[Settlements[0].num]['pj']['num']
                else:
                    tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pi']['num'])
                    fjointnum=elements[Settlements[0].num]['pi']['num']
            if Settlements[0].delta[5]!=0:
                tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pi']['num'])
                fjointnum=elements[Settlements[0].num]['pi']['num']
        if abs(elements[Settlements[0].num]['alp']%180)==90:
            if Settlements[0].delta[0]!=0 or Settlements[0].delta[1]!=0  or Settlements[0].delta[2]!=0 :
                tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pj']['num'])
                fjointnum=elements[Settlements[0].num]['pj']['num']
            if Settlements[0].delta[3]!=0 or Settlements[0].delta[4]!=0  or Settlements[0].delta[5]!=0 :
                tishi='先锁住节点%d处的角约束，尝试绘制弯矩图'%(elements[Settlements[0].num]['pi']['num'])
                fjointnum=elements[Settlements[0].num]['pi']['num']
        class Ljd():
                    pass
        iljlist=[]
        for i in range(len(calelements)):
            if calelements[i]['pj']['num']==fjointnum:
                Ljd_=Ljd()
                Ljd_.p='j'
                Ljd_.num=i
                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                iljlist.append(copy.copy(Ljd_))
            if calelements[i]['pi']['num']==fjointnum:
                Ljd_=Ljd()
                Ljd_.p='i'
                Ljd_.num=i
                Ljd_.s=calelements[i]['EI']/calelements[i]['l']
                iljlist.append(copy.copy(Ljd_))
        if len(iljlist)!=0:
            weizuoda=1
            for i in range(len(c)):
                if len(c[i])!=0:
                    weizuoda=0
            if weizuoda==0:
                for i in range(len(iljlist)):
                    num=iljlist[i].num
                    if iljlist[i].p=='j':
                        if elements[iljlist[i].num]['pi']['restraint']==1 :
                            if abs(elements[iljlist[i].num]['pi']['salp']-elements[iljlist[i].num]['alp'])%90==0:
                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) :
                                    tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                    return 0
                                elif c[iljlist[i].num][0].Mi!=0 or c[iljlist[i].num][0].Mj!=0:
                                    tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                    return 0
                            else:
                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mi!=0:
                                    tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                    return 0
                        if elements[iljlist[i].num]['pi']['restraint']==2 :
                            if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mi!=0:
                                tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                return 0
                        if elements[iljlist[i].num]['pi']['restraint']==3:
                            if abs(calelements[iljlist[i].num]['pi']['salp']-calelements[iljlist[i].num]['alp'])%180!=90:
                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                    tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n'%(iljlist[i].num+1)
                                    return 0
                                if (c[iljlist[i].num][0].Mi-c[iljlist[i].num][0].Mj)*(a[iljlist[i].num][0].Mi-a[iljlist[i].num][0].Mj)<=0:
                                    tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n'%(iljlist[i].num+1)
                                    return 0
                            else:
                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                    tishi='杆件%d滑动铰支座与杆件垂直，\n支座线位移不引起弯矩，角位移引起弯矩为一直线'%(iljlist[i].num+1)
                                    return 0
                                if abs(c[iljlist[i].num][0].Mi)!=abs(c[iljlist[i].num][0].Mj):
                                    tishi='杆件%d滑动铰支座与杆件垂直，\n支座线位移不引起弯矩，角位移引起弯矩为一直线'%(iljlist[i].num+1)
                                    return 0
                        if elements[iljlist[i].num]['pi']['restraint']==4:
                            if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                tishi='释放角约束后，将角位移和线位移叠加有误'
                                return 0
                            if (c[iljlist[i].num][0].Mi-c[iljlist[i].num][0].Mj)*(a[iljlist[i].num][0].Mi-a[iljlist[i].num][0].Mj)<=0:
                                tishi='释放角约束后，将角位移和线位移叠加有误'
                                return 0
#                        if elements[iljlist[i].num]['pi']['restraint']==0:
#                            jxlj=0
#                            for k in range(len(elements)):
#                                if elements[k]['pj']['num']==elements[num]['pi']['num']:
#                                    jxlj=1
#                                if elements[k]['pi']['num']==elements[num]['pi']['num'] and elements[k]['pj']['num']!=elements[num]['pj']['num']:
#                                    jxlj==1
#                            if jxlj==1:
#                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
#                                    tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
#                                    return 0
#                                if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))<=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
#                                    tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
#                                    return 0
#                            else:
#                                pass
                    
                    if iljlist[i].p=='i':
                        if elements[iljlist[i].num]['pj']['restraint']==1 :
                            if abs(elements[iljlist[i].num]['pj']['salp']-elements[iljlist[i].num]['alp'])%90==0:
                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) :
                                    tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                    return 0
                                elif c[iljlist[i].num][0].Mi!=0 or c[iljlist[i].num][0].Mj!=0:
                                    tishi='杆件%d相当于悬臂梁，两端弯矩均为0'%(iljlist[i].num+1)
                                    return 0
                            else:
                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mj!=0:
                                    tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                    return 0
                                    
                        if  elements[iljlist[i].num]['pj']['restraint']==2 :
                             if len(a[iljlist[i].num])!=len(c[iljlist[i].num]) or c[iljlist[i].num][0].Mj!=0:
                                tishi='杆件%d，铰支座弯矩为0'%(iljlist[i].num+1)
                                return 0
                        if elements[iljlist[i].num]['pj']['restraint']==3:
                            if abs(calelements[iljlist[i].num]['pj']['salp']-calelements[iljlist[i].num]['alp'])%180!=90:
                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                    tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n'%(iljlist[i].num+1)
                                    return 0
                                    print(tishi)
                                if (c[iljlist[i].num][0].Mi-c[iljlist[i].num][0].Mj)*(a[iljlist[i].num][0].Mi-a[iljlist[i].num][0].Mj)<=0:
                                    tishi='杆件%d滑动铰支座与杆件不垂直，可看作固定端\n'%(iljlist[i].num+1)
                                    return 0
                            else:
                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                    tishi='杆件%d滑动铰支座与杆件垂直，\n支座线位移不引起弯矩，角位移引起弯矩为一直线'%(iljlist[i].num+1)
                                    return 0
                                    print(tishi)
                                if abs(c[iljlist[i].num][0].Mi)!=abs(c[iljlist[i].num][0].Mj):
                                    tishi='杆件%d滑动铰支座与杆件垂直，\n支座线位移不引起弯矩，角位移引起弯矩为一直线'%(iljlist[i].num+1)
                                    return 0
                        if elements[iljlist[i].num]['pj']['restraint']==4:
                            if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
                                tishi='释放角约束后，将角位移和线位移叠加有误'
                                return 0
                            if (c[iljlist[i].num][0].Mi-c[iljlist[i].num][0].Mj)*(a[iljlist[i].num][0].Mi-a[iljlist[i].num][0].Mj)<=0:
                                tishi='释放角约束后，将角位移和线位移叠加有误'
                                return 0
#                        if elements[iljlist[i].num]['pj']['restraint']==0:
#                            jxlj=0
#                            for k in range(len(elements)):
#                                if elements[k]['pi']['num']==elements[num]['pj']['num']:
#                                    jxlj=1
#                                if elements[k]['pj']['num']==elements[num]['pj']['num'] and elements[k]['pi']['num']!=elements[num]['pi']['num']:
#                                    jxlj==1
#                            if jxlj==1:
#                                if len(a[iljlist[i].num])!=len(c[iljlist[i].num]):
#                                    tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
#                                    return 0
#                                if max(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj))<=2*min(abs(c[iljlist[i].num][0].Mi),abs(c[iljlist[i].num][0].Mj)):
#                                    tishi='杆件%d,两端弯矩比大于2'%(iljlist[i].num+1)
#                                    return 0
#                            else:
#                                pass
#                
                    
                
            

    
    if jdjg==1:
        weizuoda=1
        for i in range(len(c)):
            if len(a[i])==len(c[i]):
                weizuoda=0
        if weizuoda==1:
            tishi='静定结构,注意区分主体结构和附属结构'
            if zzcj==1:
                tishi+='\n注意支座沉降不引起弯矩'
            if wdbh==1:
                tishi+='\n注意温度变化不引起弯矩'
        if weizuoda==0:
            for i in range(len(elements)):
                if calelements[i]['pi']['restraint']==2:
                    if len(c[i])!=len(a[i]) or close0(c[i][0].Mi)==False:
                        tishi='杆件%d，铰支座弯矩为0'%(i+1)
                if calelements[i]['pi']['restraint']==1:
                    if calelements[i]['pj']['restraint']!=2 or calelements[i]['pj']['restraint']!=3:
                        if calelements[i]['pj']['connection']==0:
                            if len(a[i])==1:
                                tishi='杆件%d为附属结构，主体结构不会传力给附属结构'%(i+1)
                        if calelements[i]['pj']['connection']==1:
                            lj=0
                            for j in range(len(elements)):
                                if elements[j]['pi']['num']==elements[i]['pi']['num'] and elements[j]['pj']['num']!=elements[i]['pj']['num']:
                                    lj=1
                                if elements[j]['pj']['num']==elements[i]['pi']['num']:
                                    lj=1
                            if lj==0:
                                if len(a[i])==1:
                                    tishi='杆件%d为附属结构，主体结构不会传力给附属结构'%(i+1)
                if calelements[i]['pi']['restraint']==1 and abs(calelements[i]['alp']-calelements[i]['pi']['salp'])/180==90:
                    if len(a[i])==1:
                                tishi='杆件%d为附属结构，主体结构不会传力给附属结构'%(i+1)
                if calelements[i]['pi']['restraint']==3:
                    if len(a[i])!=len(c[i]):
                        if abs(calelements[i]['pi']['salp']-calelements[i]['alp'])%180==90:
                            tishi='杆件%d，存在滑动铰支座与杆件垂直\n不提供剪力，弯矩一部分为直线'%(i+1)
                        else:
                            tishi='杆件%d，存在滑动铰支座与杆件不垂直\n可提供建剪力'%(i+1)
                    if abs(calelements[i]['pi']['salp']-calelements[i]['alp'])%180==90:
                        if close(c[i][0].Mi,c[i][0].Mj):
                            tishi='杆件%d，存在滑动铰支座与杆件垂直\n不提供剪力，弯矩一部分为直线'%(i+1)
                    if abs(calelements[i]['pi']['salp']-calelements[i]['alp'])%180!=90:
                        if (c[i][0].Mi-c[i][-1].Mj)*(a[i][0].Mi-a[i][-1].Mj)<=0:
                            tishi='杆件%d，存在滑动铰支座与杆件不垂直\n可提供剪力'%(i+1)
                if calelements[i]['pj']['restraint']==2:
                    if len(c[i])!=len(a[i]) or close0(c[i][-1].Mj)==False:
                        tishi='杆件%d，铰支座弯矩为0'%(i+1)
                if calelements[i]['pj']['restraint']==1:
                    if calelements[i]['pi']['restraint']!=2 or calelements[i]['pi']['restraint']!=3:
                        if calelements[i]['pi']['connection']==0:
                            if len(a[i])==1:
                                tishi='杆件%d为附属结构，主体结构不会传力给附属结构'%(i+1)
                        if calelements[i]['pi']['connection']==1:
                            lj=0
                            for j in range(len(elements)):
                                if elements[j]['pj']['num']==elements[i]['pj']['num'] and elements[j]['pi']['num']!=elements[i]['pi']['num']:
                                    lj=1
                                if elements[j]['pi']['num']==elements[i]['pj']['num']:
                                    lj=1
                            if lj==0:
                                if len(a[i])==1:
                                    tishi='杆件%d为附属结构，主体结构不会传力给附属结构'%(i+1)
                if calelements[i]['pj']['restraint']==1 and abs(calelements[i]['alp']-calelements[i]['pj']['salp'])/180==90:
                    if len(a[i])==1:
                                tishi='杆件%d为附属结构，主体结构不会传力给附属结构'%(i+1)
                if calelements[i]['pj']['restraint']==3:
                    if len(a[i])!=len(c[i]):
                        if abs(calelements[i]['pj']['salp']-calelements[i]['alp'])%180==90:
                            tishi='杆件%d，存在滑动铰支座与杆件垂直\n不提供剪力，弯矩一部分为直线'%(i+1)
                        else:
                            tishi='杆件%d，存在滑动铰支座与杆件不垂直\n可提供建剪力'%(i+1)
                    if abs(calelements[i]['pj']['salp']-calelements[i]['alp'])%180==90:
                        if close(c[i][-1].Mi,c[i][-1].Mj):
                            tishi='杆件%d，存在滑动铰支座与杆件垂直\n不提供剪力，弯矩一部分为直线'%(i+1)
                    if abs(calelements[i]['pj']['salp']-calelements[i]['alp'])%180!=90:
                        if (c[i][0].Mi-c[i][-1].Mj)*(a[i][0].Mi-a[i][-1].Mj)<=0:
                            tishi='杆件%d，存在滑动铰支座与杆件不垂直\n可提供剪力'%(i+1)
    if fdc==1:
      weizuoda=1
      for i in range(len(a)):
          if len(a[i])==len(c[i]):
                weizuoda=0 
      if weizuoda==1 and switchbjg==0 and zfjh==0:
          tishi+='\n反对称结构，可以尝试取半结构作答'
          tishi+='\n按照对称轴取半结构，杆件截断处添加竖向支杆'
          return 0
      if weizuoda==1 and zfjh==1 and switchbjg==0:
          tishi='此结构可分解为正对称+反对称的半结构\n正对称只产生轴力，考虑反对称即可'
          tishi+='\n按照对称轴取半结构，杆件截断处添加竖向支杆'
          return 0
      if switchbjg==1 and zfjh==1 and len(elements)==2:
          for i in range(len(elements)):
              if len(a[i])!=len(c[i]):
                  tishi='注意弯矩分配'
                  tishi+='\n由于竖杆的上端无法提供水平力\n'
                  tishi+='因此竖杆可看作悬臂梁，或两端端可自由滑动的杆件，转动刚度s=1*EI/l'
                  tishi+='\n水平杆件一端为支杆，一端为固接，转动刚度s=3*EI/l'
                  return 0
              if (abs(a[i][0].Mi)-abs(a[i][-1].Mj))*(abs(c[i][0].Mi)-abs(c[i][-1].Mj))<=0:
                  tishi='注意弯矩分配'
                  tishi+='\n由于竖杆的上端无法提供水平力\n'
                  tishi+='因此竖杆可看作悬臂梁，或二端可自由滑动的杆件，转动刚度s=1*EI/l'
                  tishi+='\n水平杆件一端为支杆，一端为固接，转动刚度s=3*EI/l'
                  return 0

    
#    if zdc==1:
#        weizuoda=1
#        for i in range(len(a)):
#            if len(a[i])==len(c[i]):
#                weizuoda=0 
#        if weizuoda==1:
#            tishi+='\n正对称结构，可以尝试取半结构作答'
#            tishi+='\n按照对称轴取半结构，杆件截断处添加垂直于杆件的滑动铰支座'
#            return 0
    
    
    return 1                    



def zdybiduileixing(x):
    global rp1,cuowu,cuowunum
    rp1=1
    break2=0
    weizuoda=1
    print('c=')
    print(len(c))
    for i in range(len(c)):
            if len(a[i])==len(c[i]):
                weizuoda=0
    if weizuoda==1:
        return 0
    for i in x:
        i=int(i)-1
        if len(c[i])<len(a[i]):
            return 0
        for j in range(len(a[i])):
            if c[i][j].type!=a[i][j].type:
                cuowu='杆件%d类型错误'%(i+1)
                cuowunum=i
                rp1=0
                break
                break2=1
        if break2:
            break
    if rp1==1:
        cuowu=''
    return rp1    
    
def biduileixing():
    global rp1,cuowu,cuowunum
    rp1=1
    break2=0
    for i in range(len(a)):
        for j in range(len(a[i])):
            if c[i][j].type!=a[i][j].type:
                cuowu='杆件%d，类型错误'%(i+1)
                cuowunum=i
                rp1=0
                break
                break2=1
        if break2:
            break
    if rp1==1:
        cuowu=''
    return rp1    
        
def zdybiduizf(x):
    global rp2,cuowu,cuowunum
    rp2=1
    break2=0
    weizuoda=1
    for i in range(len(c)):
            if len(a[i])==len(c[i]):
                weizuoda=0
    if weizuoda==1:
        return 0
    for i in x:
        i=int(i)-1
        if len(c[i])<len(a[i]):
            return 0
        for j in range(len(a[i])):
            if close0(a[i][j].Mi) and close0(c[i][j].Mi)==False:
                rp2=0
                if len(a[i])==1:
                    cuowu='杆件%d受拉侧判断错误'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d第%d段，受拉侧判断错误'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if close0(a[i][j].Mj) and close0(c[i][j].Mj)==False:
                rp2=0
                if len(a[i])==1:
                    cuowu='杆件%d受拉侧判断错误'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d，第%d段，受拉侧判断错误'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if close0(a[i][j].Mi)==False and a[i][j].Mi*c[i][j].Mi<0:
                rp2=0
                if len(a[i])==1:
                    cuowu='杆件%d受拉侧判断错误'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d，第%d段，受拉侧判断错误'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if close0(a[i][j].Mj)==False and a[i][j].Mj*c[i][j].Mj<0:
                rp2=0
                if len(a[i])==1:
                    cuowu='杆件%d受拉侧判断错误'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d，第%d段，受拉侧判断错误'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if a[i][j].type=='p':
                if close0(a[i][j].Mmid)==False and (a[i][j].Mmid*c[i][j].Mmid<0):
                    print('a[i][j].Mmid=%s'%(a[i][j].Mmid))
                    print('c[i][j].Mmid=%s'%(c[i][j].Mmid))
                    rp2=0
                    cuowu='杆件%d中点，受拉侧判断错误'%(i+1)
                    cuowunum=i
                    break2=1
                    break
        if break2:
            break
    if rp2==1:
        cuowu=''
    return rp2
        
def biduizf():
    global rp2,cuowu,cuowunum
    rp2=1
    break2=0
    
    for i in range(len(a)):
        i=int(i)
        for j in range(len(a[i])):
            if close0(a[i][j].Mi) and close0(c[i][j].Mi)==False:
                rp2=0
                if len(a[i])==1:
                    cuowu='杆件%d受拉侧判断错误'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d，第%d段，受拉侧判断错误'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if close0(a[i][j].Mj) and close0(c[i][j].Mj)==False:
                rp2=0
                if len(a[i])==1:
                    cuowu='杆件%d受拉侧判断错误'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d，第%d段，受拉侧判断错误'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if close0(a[i][j].Mi)==False and a[i][j].Mi*c[i][j].Mi<0:
                rp2=0
                if len(a[i])==1:
                    cuowu='杆件%d受拉侧判断错误'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d，第%d段，受拉侧判断错误'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if close0(a[i][j].Mj)==False and a[i][j].Mj*c[i][j].Mj<0:
                rp2=0
                if len(a[i])==1:
                    cuowu='杆件%d受拉侧判断错误'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d，第%d段，受拉侧判断错误'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if a[i][j].type=='p':
                if close0(a[i][j].Mmid)==False and (a[i][j].Mmid*c[i][j].Mmid<0):
                    print('a[i][j].Mmid=%s'%(a[i][j].Mmid))
                    print('c[i][j].Mmid=%s'%(c[i][j].Mmid))
                    rp2=0
                    cuowu='杆件%d中点，受拉侧判断错误'%(i+1)
                    cuowunum=i
                    break2=1
                    break
        if break2:
            break
    if rp2==1:
        cuowu=''
    return rp2
    
def zdybiduixddx(x):
    global rp3,cuowu,lxl
    global cuowunum
    rp3=1
    break2=0
    weizuoda=1
    for i in range(len(c)):
            if len(a[i])==len(c[i]):
                weizuoda=0
    if weizuoda==1:
        return 0
    for i in x:
        i=int(i)-1
        if len(c[i])<len(a[i]):
            return 0
        for j in range(len(a[i])):
            if close(abs(a[i][j].Mi),abs(a[i][j].Mj)) and close(abs(c[i][j].Mi),abs(c[i][j].Mj))==False:
                rp3=0
                if len(a[i])==1:
                    cuowu='杆件%d两端弯矩大小应相等'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d，第%d段，两端弯矩大小应相等'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if close(abs(a[i][j].Mi),abs(a[i][j].Mj))==False:
                if abs(a[i][j].Mi)>abs(a[i][j].Mj) and abs(c[i][j].Mi)<=abs(c[i][j].Mj):
                    rp3=0
                    if len(a[i])==1:
                        cuowu='杆件%d两端弯矩相对大小错误'%(i+1)
                        cuowunum=i
                    else:
                        cuowu='杆件%d，第%d段，两端弯矩相对大小错误'%(i+1,j+1)
                        cuowunum=i
                    break2=1
                    break
                
                if abs(a[i][j].Mi)<abs(a[i][j].Mj) and abs(c[i][j].Mi)>=abs(c[i][j].Mj):
                    rp3=0
                    if len(a[i])==1:
                        cuowu='杆件%d两端弯矩相对大小错误'%(i+1)
                        cuowunum=i
                    else:
                        cuowu='杆件%d，第%d段，两端弯矩相对大小错误'%(i+1,j+1)
                        cuowunum=i
                    break2=1
        if break2:
            break
    if len(x)>1:
        i=int(x[0])-1
        for j in x:
            j=int(j)-1
            for k in range(len(a[j])):
                if close(abs(a[j][k].Mi),abs(a[i][0].Mi))==False:
                    if (a[j][k].Mi-a[i][0].Mi)*(c[j][k].Mi-c[i][0].Mi)<=0:
                        rp3=0
                    if (a[j][k].Mj-a[i][0].Mi)*(c[j][k].Mj-c[i][0].Mi)<=0:
                        rp3=0
            for k in range(len(a[j])):
                if close(abs(a[j][k].Mi),abs(a[i][-1].Mj))==False:
                    if (a[j][k].Mi-a[i][-1].Mj)*(c[j][k].Mi-c[i][-1].Mi)<=0:
                        rp3=0
                    if (a[j][k].Mj-a[i][-1].Mj)*(c[j][k].Mj-c[i][-1].Mi)<=0:
                        rp3=0
    if rp3==1:
        cuowu=''
    return rp3

def biduixddx():
    global rp3,cuowu,lxl
    global cuowunum
    rp3=1
    break2=0
    for i in range(len(a)):
        for j in range(len(a[i])):
            if close(abs(a[i][j].Mi),abs(a[i][j].Mj)) and close(abs(c[i][j].Mi),abs(c[i][j].Mj))==False:
                rp3=0
                if len(a[i])==1:
                    cuowu='杆件%d两端弯矩大小应相等'%(i+1)
                    cuowunum=i
                else:
                    cuowu='杆件%d，第%d段，两端弯矩大小应相等'%(i+1,j+1)
                    cuowunum=i
                break2=1
                break
            if close(abs(a[i][j].Mi),abs(a[i][j].Mj))==False:
                if abs(a[i][j].Mi)>abs(a[i][j].Mj) and abs(c[i][j].Mi)<=abs(c[i][j].Mj):
                    rp3=0
                    if len(a[i])==1:
                        cuowu='杆件%d两端弯矩相对大小错误'%(i+1)
                        cuowunum=i
                    else:
                        cuowu='杆件%d，第%d段，两端弯矩相对大小错误'%(i+1,j+1)
                        cuowunum=i
                    break2=1
                    break
                
                if abs(a[i][j].Mi)<abs(a[i][j].Mj) and abs(c[i][j].Mi)>=abs(c[i][j].Mj):
                    rp3=0
                    if len(a[i])==1:
                        cuowu='杆件%d两端弯矩相对大小错误'%(i+1)
                        cuowunum=i
                    else:
                        cuowu='杆件%d，第%d段，两端弯矩相对大小错误'%(i+1,j+1)
                        cuowunum=i
                    break2=1
        if break2:
            break
        
    for i in range(len(zdytishi)):
        if zdytishi[1][i]=='多个杆件':
            x=zdytishi[2][i].split(',')
            if len(x)>1:
                i=int(x[0])-1
                for j in x:
                    j=int(j)-1
                    for k in range(len(a[j])):
                        if close(abs(a[j][k].Mi),abs(a[i][0].Mi))==False:
                            if (a[j][k].Mi-a[i][0].Mi)*(c[j][k].Mi-c[i][0].Mi)<=0:
                                cuowu='杆件%s之间相对大小有误\n请点击分析提示'%x
                                cuowunum=int(x[0])
                                rp3=0
                            if (a[j][k].Mj-a[i][0].Mi)*(c[j][k].Mj-c[i][0].Mi)<=0:
                                cuowu='杆件%s之间相对大小有误\n请点击分析提示'%x
                                cuowunum=int(x[0])
                                rp3=0
                    for k in range(len(a[j])):
                        if close(abs(a[j][k].Mi),abs(a[i][-1].Mj))==False:
                            if (a[j][k].Mi-a[i][-1].Mj)*(c[j][k].Mi-c[i][-1].Mi)<=0:
                                cuowu='杆件%s之间相对大小有误\n请点击分析提示'%x
                                cuowunum=int(x[0])
                                rp3=0
                            if (a[j][k].Mj-a[i][-1].Mj)*(c[j][k].Mj-c[i][-1].Mi)<=0:
                                cuowu='杆件%s之间相对大小有误\n请点击分析提示'%x
                                cuowunum=int(x[0])
                                rp3=0
    if rp3==1:
        cuowu=''
    return rp3


def zdybiduijdfp(x):
    global rp4
    global cuowunum
    global cuowu
    rp4=1
    weizuoda=1
    for i in range(len(c)):
            if len(a[i])==len(c[i]):
                weizuoda=0
    if weizuoda==1:
        return 0
    class JD():
        def __init__(self,num,p):
            self.num=num
            self.p=p
    for i in x:
        i=int(i)-1
        jiedian=[]
        for j in range(len(elements)):
            if elements[j]['pi']['num']==i+1:
                jdt=JD(j,'i')
                jiedian.append(jdt)
                if len(c[j])<len(a[j]):
                    return 0
            if elements[j]['pj']['num']==i+1:
                jdt=JD(j,'j')
                jiedian.append(jdt)
                if len(c[j])<len(a[j]):
                    return 0
        if len(jiedian)>=2:
            Mc=[]
            Ma=[]
            sumM=0
#            sumM=-1*caljoints_[i]['M']
            for k in range(len(jiedian)): 
                num=jiedian[k].num
                p=jiedian[k].p
                if p=='i':
                    Mc.append(c[num][0].Mi)
                    Ma.append(a[num][0].Mi)
                    sumM=sumM+c[num][0].Mi
                if p=='j':
                    Mc.append(c[num][-1].Mj)
                    Ma.append(a[num][-1].Mj)
                    sumM=sumM-c[num][-1].Mj            
            if close0(sumM)==False and (caljoints_[i]['M']==0):
                rp4=0
                cuowunum=i
                cuowu='节点%d，弯矩之和不为0'%(i+1)
                return 0
            if close0(sumM)==False and (caljoints_[i]['M']!=0):
                if -1*caljoints_[i]['M']*sumM<=0:
                    rp4=0
                    cuowunum=i
                    cuowu='节点%d，内外弯矩不平衡'%(i+1)
            if len(jiedian)>2:
                Ma_=[]
                Mc_=[]
                for t in range(len(Ma)):
                    cf=0
                    for q in range(len(Ma_)):
                        if close(abs(Ma_[q]),abs(Ma[t])):
                            cf=1
                    if cf==0:
                        Ma_.append(Ma[t])
                Ma=Ma_
                
                for t in range(len(Mc)):
                    cf=0
                    for q in range(len(Mc_)):
                        if close(abs(Mc_[q]),abs(Mc[t])):
                            cf=1
                    if cf==0:
                        Mc_.append(Mc[t])
                Mc=Mc_
                if len(Mc)!=len(Ma):
                    rp4=0
                    cuowunum=i
                    cuowu='节点%d上的各杆件弯矩相对大小错误'%(i+1)
                    return 0
                else:    
                    sorta=np.argsort(Ma)
                    sorta=np.argsort(sorta)
                    sortc=np.argsort(Mc)
                    sortc=np.argsort(sortc)
                    if any(sorta !=sortc):
                        rp4=0
                        cuowunum=i
                        cuowu='节点%d上的各杆件弯矩相对大小错误'%(i+1)
                        return 0
    return rp4
            
def biduijdfp():
    global rp4
    global cuowunum
    global cuowu
    rp4=1
    class JD():
        def __init__(self,num,p):
            self.num=num
            self.p=p
    for i in range(len(joints_)):
        jiedian=[]
        for j in range(len(elements)):
            if elements[j]['pi']['num']==i+1:
                jdt=JD(j,'i')
                jiedian.append(jdt)
            if elements[j]['pj']['num']==i+1:
                jdt=JD(j,'j')
                jiedian.append(jdt)
        if len(jiedian)>=2:
            Mc=[]
            Ma=[]
            sumM=0
#            sumM=-1*caljoints_[i]['M']
            for k in range(len(jiedian)): 
                num=jiedian[k].num
                p=jiedian[k].p
                if p=='i':
                    Mc.append(c[num][0].Mi)
                    Ma.append(a[num][0].Mi)
                    sumM=sumM+c[num][0].Mi
                if p=='j':
                    Mc.append(c[num][-1].Mj)
                    Ma.append(a[num][-1].Mj)
                    sumM=sumM-c[num][-1].Mj            
            if close0(sumM)==False and (caljoints_[i]['M']==0):
                rp4=0
                cuowunum=i
                cuowu='节点%d，弯矩之和不为0，\n节点不平衡'%(i+1)
                return 0
            if close0(sumM)==False and (caljoints_[i]['M']!=0):
                print(caljoints_[i]['M'])
                print(sumM)
                print('***************')
                if -1*caljoints_[i]['M']*sumM<=0:
                    rp4=0
                    cuowunum=i
                    cuowu='节点%d，内外弯矩不平衡'%(i+1)
            if len(jiedian)>2:
                Ma_=[]
                Mc_=[]
                for t in range(len(Ma)):
                    cf=0
                    for q in range(len(Ma_)):
                        if close(abs(Ma_[q]),abs(Ma[t])):
                            cf=1
                    if cf==0:
                        Ma_.append(Ma[t])
                Ma=Ma_
                
                for t in range(len(Mc)):
                    cf=0
                    for q in range(len(Mc_)):
                        if close(abs(Mc_[q]),abs(Mc[t])):
                            cf=1
                    if cf==0:
                        Mc_.append(Mc[t])
                Mc=Mc_
                if len(Mc)!=len(Ma):
                    rp4=0
                    cuowunum=i
                    cuowu='节点%d上的各杆件弯矩相对大小错误'%(i+1)
                    return 0
                else:    
                    sorta=np.argsort(Ma)
                    sorta=np.argsort(sorta)
                    sortc=np.argsort(Mc)
                    sortc=np.argsort(sortc)
                    if any(sorta !=sortc):
                        rp4=0
                        cuowunum=i
                        cuowu='节点%d上的各杆件弯矩相对大小错误'%(i+1)
                        return 0
    for i in range(len(duandian)):
        if len(duandian[i])>2:
            for j in range(1,len(duandian[i])-1):
                if c[i][j-1].Mj!=c[i][j].Mi:
                    rp4=0
                    cuowu='杆件%d，断点处弯矩不连续'%(i+1)
    return rp4            



        
def showleixing():
    global cuowunum
    biduileixing()
    plt.figure(figsize=(32,20))
    drawelements()
    drawannotation()
    userM()
    xi=elements[cuowunum]['pi']['x']
    yi=elements[cuowunum]['pi']['y']
    xj=elements[cuowunum]['pj']['x']
    yj=elements[cuowunum]['pj']['y']
    plt.plot([xi,xj],[yi,yj],'r',linewidth='3')               
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/userM.png',bbox_inches='tight')
    plt.close()
    
def showzf():
    global cuowunum
    biduizf()
    plt.figure(figsize=(32,20))
    drawelements()
    drawannotation()
    userM()
    xi=elements[cuowunum]['pi']['x']
    yi=elements[cuowunum]['pi']['y']
    xj=elements[cuowunum]['pj']['x']
    yj=elements[cuowunum]['pj']['y']
    plt.plot([xi,xj],[yi,yj],'r',linewidth='3')            
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/userM.png',bbox_inches='tight')
    plt.close()
    
    
def showxddx():
    global cuowunum
    biduixddx()
    plt.figure(figsize=(32,20))
    drawelements()
    drawannotation()
    userM()
    xi=elements[cuowunum]['pi']['x']
    yi=elements[cuowunum]['pi']['y']
    xj=elements[cuowunum]['pj']['x']
    yj=elements[cuowunum]['pj']['y']
    plt.plot([xi,xj],[yi,yj],'r',linewidth='3')              
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/userM.png',bbox_inches='tight')
    plt.close()
    
def showjdfp():
    global cuowunum
    biduijdfp()
    plt.figure(figsize=(32,20))
    drawelements()
    drawannotation()
    userM()
    x=joints_[cuowunum]['x']
    y=joints_[cuowunum]['y']
    plt.scatter(x,y,s=1500,c='',marker='o',edgecolor='red',linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.axis('equal')
    plt.savefig('drawing/userM.png',bbox_inches='tight')
    plt.close()

###
#for i in range(0,9):
#    informatrixs.append(pd.DataFrame())
#    
#    
#    
#informatrixs[0]=pd.DataFrame(np.full((15,4),np.nan))
#informatrixs[1]=pd.DataFrame(np.full((15,5),np.nan))
#informatrixs[2]=pd.DataFrame(np.full((15,3),np.nan))
#informatrixs[3]=pd.DataFrame(np.full((15,4),np.nan))
#informatrixs[4]=pd.DataFrame(np.full((15,4),np.nan))
#informatrixs[5]=pd.DataFrame(np.full((15,5),np.nan))
#informatrixs[6]=pd.DataFrame(np.full((15,5),np.nan))
#informatrixs[7]=pd.DataFrame(np.full((15,7),np.nan))
#informatrixs[8]=pd.DataFrame(np.full((15,4),np.nan))
#informatrixs[0][0][0]=1
#informatrixs[0][1][0]=0
#informatrixs[0][2][0]=0
#informatrixs[0][3][0]=1
#informatrixs[0][0][1]=2
#informatrixs[0][1][1]=1
#informatrixs[0][2][1]=0
#informatrixs[0][3][1]=1
#informatrixs[1][0][0]=1
#informatrixs[1][1][0]=1
#informatrixs[1][2][0]=2
#informatrixs[1][3][0]=1
#informatrixs[1][4][0]=1
#informatrixs[2][0][0]=1
#
#informatrixs[2][1][0]=2
#informatrixs[2][2][0]=90
#informatrixs[2][0][1]=2
#
#informatrixs[2][1][1]=2
#informatrixs[2][2][1]=90
#
#informatrixs[4][0][0]=1
#informatrixs[4][1][0]=10
#informatrixs[4][2][0]=-90
#informatrixs[4][3][0]=0.5
#
#
#
#sortinformatrixs()
#fileinelements()
#file()    
#calculation()
#createanswers()

#drawquestion()
#drawM()
#drawshearforce()
#drawN()
#drawdeformation()