# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 17:35:31 2021

@author: Rich
"""

import zdyallfunction 
import tkinter
import tkinter.messagebox
from PIL import Image,ImageTk
from tkinter import ttk
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import socket
import time
import pymysql
import copy
import os
import math
import matplotlib.pyplot as plt
import random
# import dill


plt.rcParams['font.sans-serif']=['simhei']



win = tkinter.Tk()
win.title("结构力学概念分析器v2.0")    # #窗口标题
win.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
sw =win.winfo_screenwidth()
sh = win.winfo_screenheight()
xr=(sw-400)/2
yr=(sh-225)/2
height=sh*0.8
width=sh*0.8*1.6
dx=(sw-width)/2
dy=(sh-height*1.05)/2
win.geometry('%dx%d+%d+%d'%(0.4*width,0.8*height,(sw-0.4*width)/2,(sh-height)/2))
win.resizable(0,0)

   
class MESSAGEBOARD(tkinter.Toplevel):
    def __init__(self,master=None,**kw):
        tkinter.Toplevel.__init__(self,master,**kw)
        self.timenow=int(time.time())
        self.title('留言板')
        self.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.geometry('%dx%d+%d+%d'%(0.53*width,0.65*height,dx,dy))
        self.engine=create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        self['bg']='white'
        self.incomingletter_canvas=tkinter.Canvas(self,height=0.1*width,width=0.1*width)
        
        self.replyletter_canvas=tkinter.Canvas(self,height=0.1*width,width=0.1*width)
        
        self.incomingletter_label=tkinter.Label(self,text='请输入您的留言：我们会及时认真地回复您',bg='white',font=('微软雅黑',10,'bold'))
        self.replyletter_label=tkinter.Label(self,text='我们的回复:',bg='white',font=('微软雅黑',10,'bold'))
        
        self.incomeingletter_text=tkinter.Text(self,width=45,height=8,highlightthickness=2,highlightcolor='black',highlightbackground='black')
        self.replyletter_text=tkinter.Text(self,width=45,height=8,highlightthickness=2,highlightcolor='black',highlightbackground='black')
        
        self.incomingletter_button=tkinter.Button(self,text='确认留言',font=('微软雅黑',12,'bold'),command=self.qualifyletter)
        
        self.incomingletter_label.place(x=0.2*width,y=0.05*height)
        self.incomeingletter_text.place(x=0.2*width,y=0.1*height)
        
        self.incomingletter_button.place(x=0.4*width,y=0.35*height,anchor='se')
        
        self.replyletter_label.place(x=0.2*width,y=0.35*height)
        self.replyletter_text.place(x=0.2*width,y=0.4*height)
        
        im=Image.open(f'{os.getcwd()}/infor/comingletter.jpg')
        photo = ImageTk.PhotoImage(im.resize((int(0.1*width),int(0.1*width)),Image.ANTIALIAS))
        self.incomingletter_canvas.create_image(0,0,anchor='nw',image = photo)
        
        im2=Image.open(f'{os.getcwd()}/infor/replyletter.jpg')
        photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*width)),Image.ANTIALIAS))
        self.replyletter_canvas.create_image(0,0,anchor='nw',image = photo2)
        
        self.incomingletter_canvas.place(x=0.05*width,y=0.1*height)
        self.replyletter_canvas.place(x=0.05*width,y=0.4*height)
        
        
        
        sql="select * from letter where userID='%s' order by comingtimenum desc "%zdyallfunction.userID
        self.letter = pd.read_sql_query(sql, self.engine)
        self.num=len(self.letter)
        if len(self.letter)>0:
            self.incomeingletter_text.insert('end',self.letter.loc[0,'comingtext'])
            if self.letter.loc[0,'openstate']!=-1:
                self.replyletter_text.insert('end',self.letter.loc[0,'replytext'])
        print(self.num)
        self.nowletternum=0
        self.formerbutton=tkinter.Button(self,text='前一条留言',font=('微软雅黑',12,'bold'),command=self.formerletter)
        self.nextbutton=tkinter.Button(self,text='后一条留言',font=('微软雅黑',12,'bold'),command=self.nextletter)
        
        self.formerbutton.place(x=0.53*width,y=0.65*height,anchor='se')
        self.nextbutton.place(x=0,y=0.65*height,anchor='sw')
        #        self.protocol("WM_DELETE_WINDOW",self.exitmessageboard)
                    
        #        conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
        #        cursor = conn.cursor()
        #        sql="update letter set openstate=1 where userID='%s'"%zdyallfunction.userID
        #        cursor.execute(sql)
        #        conn.commit()
        #        cursor.close()
        #        conn.close()
        self.resizable(0,0)
        win.mainloop()
        
    def qualifyletter(self):
        ctime=int(time.time())
        df=pd.DataFrame(np.zeros((1,6)))
        df.iloc[0,0]=zdyallfunction.userID
        df.iloc[0,1]=self.incomeingletter_text.get('0.0','end')
        df.iloc[0,2]=''
        df.iloc[0,3]=ctime
        df.iloc[0,4]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))
        df.iloc[0,5]=-1
        
        df.columns=['userID','comingtext','replytext','comingtime','comingtimenum','openstate']
        engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        df.to_sql('letter', engine, index= False,if_exists='append')
        tkinter.messagebox.showinfo(title='', message='感谢您的留言，我们会及时回复！')
        self.replyletter_text.delete(0.0,'end')
    
    def formerletter(self):
        if self.nowletternum+2<=self.num:
            self.nowletternum=self.nowletternum+1
            self.incomeingletter_text.delete('0.0','end')
            self.replyletter_text.delete('0.0','end')
            self.incomeingletter_text.insert('end',self.letter.loc[self.nowletternum,'comingtext'])
            if self.letter.loc[self.nowletternum,'openstate']!=-1:
                self.replyletter_text.insert('end',self.letter.loc[self.nowletternum,'replytext'])
        else:
            tkinter.messagebox.showinfo(title='', message='这是您留言记录的开头')
        
    def nextletter(self):
        if self.nowletternum>0:
            self.nowletternum=self.nowletternum-1
            self.incomeingletter_text.delete('0.0','end')
            self.replyletter_text.delete('0.0','end')
            self.incomeingletter_text.insert('end',self.letter.loc[self.nowletternum,'comingtext'])
            if self.letter.loc[self.nowletternum,'openstate']!=-1:
                self.replyletter_text.insert('end',self.letter.loc[self.nowletternum,'replytext'])
        else:
            tkinter.messagebox.showinfo(title='', message='这是您最新的留言')

















class RECOMMENDATION(tkinter.Toplevel):
    def __init__(self,master=None,**kw):
        tkinter.Toplevel.__init__(self,master,**kw)
        self.timenow=int(time.time())
        self.title('为您推荐')
        self.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.geometry('%dx%d+%d+%d'%(width,height,dx,dy))
        self.engine=create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        
        self.sqlbytime="select *,@rank:=@rank + 1 AS rank_no from basic_questioninfor as a,(SELECT @rank:= 0) as b "
        self.sqlbytime+=" where state='公开' and tishitype='自定义提示'  order by filetimenum desc limit 20"
        
        
        self.sqlbytimeandhotdynamic="select *,a.thumbs/(a.thumbs +a.badpost)*100 as ratio,@rank:=@rank + 1 AS rank_no  from basic_questioninfor as a ,(SELECT @rank:= 0) as b where "
        self.sqlbytimeandhotdynamic+="a.thumbs/(a.thumbs +a.badpost)*100 >60 and %d-filetimenum<2592000 and %d-filetimenum>0 and state='公开' and tishitype='自定义提示' order by a.thumbs/(a.thumbs +a.badpost)*100 desc limit 50"%(self.timenow,self.timenow)
        self.sqlbytimeandhotstatic="select *,a.thumbs/(a.thumbs +a.badpost)*100,@rank:=@rank + 1 AS rank_no  from basic_questioninfor as a ,(SELECT @rank:= 0) as b "
        self.sqlbytimeandhotstatic+=" where state='公开' and tishitype='自定义提示' order by a.thumbs/(a.thumbs +a.badpost)*100 desc limit 50"


        df=pd.read_sql_query(self.sqlbytimeandhotstatic, self.engine)

        
        self.sqlbyselecteddynamic="select * ,a.thumbs/(a.thumbs +a.badpost)*100 as ratio,@rank:=@rank + 1 AS rank_no  from basic_questioninfor as a ,(SELECT @rank:= 0) as b where "
        self.sqlbyselecteddynamic+="a.thumbs/(a.thumbs +a.badpost)*100>80 and  state='公开' and tishitype='自定义提示' order by a.thumbs limit 200"
        self.sqlbyselectedstatic="select * ,a.thumbs/(a.thumbs +a.badpost)*100 as ratio,@rank:=@rank + 1 AS rank_no  from basic_questioninfor as a ,(SELECT @rank:= 0) as b where "
        self.sqlbyselectedstatic+=" state='公开' and tishitype='自定义提示' order by a.thumbs limit 200"
        
        self.df_bytime=pd.read_sql_query(self.sqlbytime, self.engine)
        
        self.random_num_bytime=random.randint(0,len(self.df_bytime)-1)
        
        self.df_bytimeandhot=pd.read_sql_query(self.sqlbytimeandhotdynamic, self.engine)


        if len(self.df_bytimeandhot)<10:
            self.df_bytimeandhot=pd.read_sql_query(self.sqlbytimeandhotstatic, self.engine)
        self.random_num_bytimeandhot1=random.randint(0,len(self.df_bytimeandhot)-1)
        self.random_num_bytimeandhot2=random.randint(0,len(self.df_bytimeandhot)-1)
        while self.random_num_bytimeandhot1==self.random_num_bytimeandhot2:
            self.random_num_bytimeandhot2=random.randint(0,len(self.df_bytimeandhot)-1)
        
        self.df_byselected=pd.read_sql_query(self.sqlbyselecteddynamic, self.engine)
        if len(self.df_byselected)<10:
            self.df_byselected=pd.read_sql_query(self.sqlbyselectedstatic, self.engine)
        self.random_num_byselected=random.randint(0,len(self.df_byselected)-1)
        
#        print(self.df_bytime.iloc[self.random_num_bytime,0])
#        print(self.df_bytimeandhot.iloc[self.random_num_bytimeandhot1,0])
#        print(self.df_bytimeandhot.iloc[self.random_num_bytimeandhot2,0])
#        print(self.df_byselected.iloc[self.random_num_byselected,0])
#        print(self.df_byselected.loc[self.random_num_byselected,'generaldescription'])
        
        self.button_bytime=tkinter.Button(self,text='去作答',font=('微软雅黑',12,'bold'),fg='white',bg='black',command=self.donowbytime)
        self.button_bytimeandhot1=tkinter.Button(self,text='去作答',font=('微软雅黑',12,'bold'),fg='white',bg='black',command=self.donowbytimeandhot1)
        self.button_bytimeandhot2=tkinter.Button(self,text='去作答',font=('微软雅黑',12,'bold'),fg='white',bg='black',command=self.donowbytimeandhot2)
        self.button_byselected=tkinter.Button(self,text='去作答',font=('微软雅黑',12,'bold'),fg='white',bg='black',command=self.donowbyselected)
        self.changebutton=tkinter.Button(self,text='◌换一批,请耐心等待刷新',font=('微软雅黑',12,'bold'),command=self.change_a_batch,fg='white',bg='black')
        self.changebutton.place(x=width,y=height,anchor='se')
        
        self.button_bytime.place(x=0.05*width,y=0.42*height,anchor='nw')
        self.button_bytimeandhot1.place(x=0.5*width,y=0.42*height,anchor='nw')
        self.button_bytimeandhot2.place(x=0.05*width,y=0.92*height,anchor='nw')
        self.button_byselected.place(x=0.5*width,y=0.92*height,anchor='nw')
        
        self.label_bytime=tkinter.Label(self,text='%s'%self.df_bytime.loc[self.random_num_bytime,'generaldescription'],font=('微软雅黑',12,'bold'))
        self.label_bytimeandhot1=tkinter.Label(self,text='%s'%self.df_bytimeandhot.loc[self.random_num_bytimeandhot1,'generaldescription'],font=('微软雅黑',12,'bold'))
        self.label_bytimeandhot2=tkinter.Label(self,text='%s'%self.df_bytimeandhot.loc[self.random_num_bytimeandhot2,'generaldescription'],font=('微软雅黑',12,'bold'))
        self.label_byselected=tkinter.Label(self,text='%s'%self.df_byselected.loc[self.random_num_byselected,'generaldescription'],font=('微软雅黑',12,'bold'))
        
        self.label_bytime.place(x=0.15*width,y=0.42*height,anchor='nw')
        self.label_bytimeandhot1.place(x=0.6*width,y=0.42*height,anchor='nw')
        self.label_bytimeandhot2.place(x=0.15*width,y=0.92*height,anchor='nw')
        self.label_byselected.place(x=0.6*width,y=0.92*height,anchor='nw')
        
        self.canvas_bytime=tkinter.Canvas(self,height=0.4*height,width=0.4*width,bg='white')
        self.canvas_bytimeandhot1=tkinter.Canvas(self,height=0.4*height,width=0.4*width,bg='white')
        self.canvas_bytimeandhot2=tkinter.Canvas(self,height=0.4*height,width=0.4*width,bg='white')
        self.canvas_byselected=tkinter.Canvas(self,height=0.4*height,width=0.4*width,bg='white')
        
        self.canvas_bytime.place(x=0.05*width,y=0.02*height,anchor='nw')
        self.canvas_bytimeandhot1.place(x=0.5*width,y=0.02*height,anchor='nw')
        self.canvas_bytimeandhot2.place(x=0.05*width,y=0.52*height,anchor='nw')
        self.canvas_byselected.place(x=0.5*width,y=0.52*height,anchor='nw')
        self.resizable()
        
    
    def donowbytime(self):
        global questionsymbol
        questionsymbol=self.df_bytime.iloc[self.random_num_bytime,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.chuti()
        
    def donowbytimeandhot1(self):
        global questionsymbol
        questionsymbol=self.df_bytimeandhot.iloc[self.random_num_bytimeandhot1,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.chuti()
    
    def donowbytimeandhot2(self):
        global questionsymbol
        questionsymbol=self.df_bytimeandhot.iloc[self.random_num_bytimeandhot2,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.chuti()
        
    def donowbyselected(self):
        global questionsymbol
        questionsymbol=self.df_byselected.iloc[self.random_num_byselected,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.chuti()
        
    def chuti(self):
        global gangdu,newquestion,questionsymbol,rightanswerquestion,tp2,questionselection
        try:
            questionselection.withdraw()
        except:
            pass
        try:
            tp2.deiconify()
        except:
            pass
        newquestion=1
        rightanswerquestion=0
        ts = time.time()
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        zdyallfunction.starttime=dt
#        questionsymbol='Tongji_11'
        text2.delete('0.0','end')
        zdyallfunction.jys=[]
        zdyallfunction.xys=[]
        zdyallfunction.scxys=[]
        c1.ufocus=0
        zdyallfunction.switchbjg=0
        lb1.delete(0,'end')
        
        gangdu=[]
        zdyallfunction.daduan=0
        zdyallfunction.duandian=[]
        
        

        
        zdyallfunction.getquestion(questionsymbol)
#        print(zdyallfunction.informatrixs[0])
        zdyallfunction.fileinelements()
        zdyallfunction.file()
        zdyallfunction.calculation()
        zdyallfunction.drawquestion()
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        c3.create_image(0,0,anchor='nw',image = photo)
        smallest_index=-1
        
        global gjxx
        gjxx=[]
        for i in range(len(zdyallfunction.calelements)):
            num=zdyallfunction.calelements[i]['num']
            EA=zdyallfunction.calelements[i]['EA']
            l=zdyallfunction.calelements[i]['l']
            if zdyallfunction.calelements[i]['EA']>=1e8:
                EA=-1
            else:
                EA=zdyallfunction.calelements[i]['EA']
            if zdyallfunction.calelements[i]['EI']>=1e6:
                EI=-1
            else:
               EI=zdyallfunction.calelements[i]['EI'] 
            gjxx_='  杆件（%d）L=%d  EA=%d EI=%d'%(num,l,EA,EI)
            gjxx.append(gjxx_)
        lb1.delete(0,'end')
        for information in gjxx:
            lb1.insert('end',information)
        
        
        for i in range(len(zdyallfunction.elements)):
            zdyallfunction.duandian.append([0,1])
        #初始化，角约束jys，线约束xys，删除线约束scxys，半结构switchbjg
        #改变刚度的列表gangdu，断点列表duandian
        zdyallfunction.drawuserM(smallest_index)
        c1.relativeposition()
        zdyallfunction.createanswers()
        if zdyallfunction.timutishifangshi!="自定义提示":
            zdyallfunction.bianbiedcx()
            zdyallfunction.bianbietixing()
        im2=Image.open(f'{os.getcwd()}/drawing/userM.png')
        photo2 = ImageTk.PhotoImage(im2.resize((c1.winfo_width(),c1.winfo_height()),Image.ANTIALIAS))
        c1.create_image(0,0,anchor='nw',image = photo2)
        global evaluation
        try:
            evaluation.destroy()
        except:
            pass
        evaluation=EVALUATION(tp2,height=0.1*height,width=0.35*width)
        evaluation.place(x=0.62*width,y=0.5*height,anchor='nw')
        self.destroy()
#        tp2.deiconify()
        evaluation.bind()
        win.mainloop()
    
    def change_a_batch(self):
        self.random_num_bytime=random.randint(0,len(self.df_bytime)-1)  
        self.random_num_bytimeandhot1=random.randint(0,len(self.df_bytimeandhot)-1)
        self.random_num_bytimeandhot2=random.randint(0,len(self.df_bytimeandhot)-1)
        while self.random_num_bytimeandhot1==self.random_num_bytimeandhot2:
            self.random_num_bytimeandhot2=random.randint(0,len(self.df_bytimeandhot)-1)
        self.random_num_byselected=random.randint(0,len(self.df_byselected)-1)
        
#        print(self.df_bytime.iloc[self.random_num_bytime,0])
#        print(self.df_bytimeandhot.iloc[self.random_num_bytimeandhot1,0])
#        print(self.df_bytimeandhot.iloc[self.random_num_bytimeandhot2,0])
#        print(self.df_byselected.iloc[self.random_num_byselected,0])
        
        self.label_bytime['text']=self.df_bytime.loc[self.random_num_bytime,'generaldescription']
        self.label_bytimeandhot1['text']=self.df_bytimeandhot.loc[self.random_num_bytimeandhot1,'generaldescription']
        self.label_bytimeandhot2['text']=self.df_bytimeandhot.loc[self.random_num_bytimeandhot2,'generaldescription']
        self.label_byselected['text']=self.df_byselected.loc[self.random_num_byselected,'generaldescription']
        self.qualifyrecommendationquestions()
        
    def firstqualifyrecommendationquestions(self):
        global questionsymbol
        questionsymbol=self.df_bytime.iloc[self.random_num_bytime,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.drawrecommendationquestions()
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas_bytime.create_image(0,0,anchor='nw',image = photo)
        
        questionsymbol=self.df_bytimeandhot.iloc[self.random_num_bytimeandhot1,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.drawrecommendationquestions()
        im2=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo2 = ImageTk.PhotoImage(im2.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas_bytimeandhot1.create_image(0,0,anchor='nw',image = photo2)
        questionsymbol=self.df_bytimeandhot.iloc[self.random_num_bytimeandhot2,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.drawrecommendationquestions()
        im3=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo3 = ImageTk.PhotoImage(im3.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas_bytimeandhot2.create_image(0,0,anchor='nw',image = photo3)
        
        questionsymbol=self.df_byselected.iloc[self.random_num_byselected,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.drawrecommendationquestions()
        im4=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo4 = ImageTk.PhotoImage(im4.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas_byselected.create_image(0,0,anchor='nw',image = photo4)
        
    def qualifyrecommendationquestions(self):
        global questionsymbol
        questionsymbol=self.df_bytime.iloc[self.random_num_bytime,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.drawrecommendationquestions()
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas_bytime.create_image(0,0,anchor='nw',image = photo)
        
        questionsymbol=self.df_bytimeandhot.iloc[self.random_num_bytimeandhot1,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.drawrecommendationquestions()
        im2=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo2 = ImageTk.PhotoImage(im2.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas_bytimeandhot1.create_image(0,0,anchor='nw',image = photo2)
        questionsymbol=self.df_bytimeandhot.iloc[self.random_num_bytimeandhot2,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.drawrecommendationquestions()
        im3=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo3 = ImageTk.PhotoImage(im3.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas_bytimeandhot2.create_image(0,0,anchor='nw',image = photo3)
        
        questionsymbol=self.df_byselected.iloc[self.random_num_byselected,0]
        zdyallfunction.questionsymbol=questionsymbol
        self.drawrecommendationquestions()
        im4=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo4 = ImageTk.PhotoImage(im4.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas_byselected.create_image(0,0,anchor='nw',image = photo4)
        win.mainloop()
        
        
        
    def drawrecommendationquestions(self):
        global questionsymbol
        zdyallfunction.getquestion(questionsymbol)
        zdyallfunction.fileinelements()
        zdyallfunction.file()
        zdyallfunction.drawquestion()
        global smallest_index
        smallest_index=-1
        zdyallfunction.duandian=[]





class Showtimutable(ttk.Treeview):
    def __init__(self,master=None,tablename=None,**kw):
        ttk.Treeview.__init__(self,master,**kw)
        self.engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        self.page=0
        self.geshu=10
        self.tablename=tablename
        self.searchway=-1
        s = ttk.Style()
        s.configure('Treeview', rowheight=int(50/1800*sh),font=('微软雅黑',9))

    
    def altergeshu(self,x):
        self.geshu=x
    def delself(self):
        x=self.get_children()
        for item in x:
            self.delete(item)
    def showinfor(self):
        for i in range(len(self.df)):
            tt=[]
            tt.append(self.df.iloc[i,0])
            tt.append(self.df.iloc[i,1])
            tt.append(self.df.iloc[i,2])
            tt.append(self.df.iloc[i,7])
            tt.append(self.df.iloc[i,8])
            tt.append(self.df.iloc[i,9])
            tt.append(self.df.iloc[i,10])
            try:
                int(self.df.iloc[i,14])
                tt.append(int(self.df.iloc[i,14]))
            except:
                tt.append('暂无')
            tt=tuple(tt)
#            self.insert('',i,values=(self.df.iloc[i,0],self.df.iloc[i,1]))    
            self.insert('',i,values=tt)
            
    def getinfor(self):
        sql=self.sql+" limit %d,%d"%(self.page*10,self.geshu)
        self.df=pd.read_sql_query(sql, self.engine)
    
    def getquestionsymbol(self,x):
        self.questionsymbol=x
        
    def getkeyword(self,x,y):
        self.keyword=x
        self.tishitype=y
            
    def addpage(self):
        self.page=self.page+1
        if (self.page)*10>=self.num:
            tkinter.messagebox.showinfo(title='提示', message='已经到尾了')
            return
        self.delself()
        self.getinfor()
        self.showinfor()
    
    def minuspage(self):
        if self.page>0:
            self.page=self.page-1
            self.delself()
            self.getinfor()
            self.showinfor()
        else:
            tkinter.messagebox.showinfo(title='提示', message='已经到头了')
 



           
class FREESEARCH(tkinter.Frame):
    def __init__(self,master=None,**kw):
        tkinter.Frame.__init__(self,master,**kw)
        self.searchframe=tkinter.Frame(self,height=0.5*height,width=0.4*width)
        
        
        self.engine=create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        self.searchentry=tkinter.Entry(self,width=20)
        self.searchbutton=tkinter.Button(self,text='搜索',command=self.search)
        self.sqlstart="select *,a.thumbs/(a.`thumbs` +a.badpost)*100 from basic_questioninfor as a where "

        

        
        self.searchcontentlable=tkinter.Label(self.searchframe,text='搜索内容：     ')
        self.searchcontentcmb= ttk.Combobox(self.searchframe,width=15)
        self.searchcontentcmb['value'] = ('关键词','题号','用户')
        self.searchcontentcmb.current(0)
        
        self.searchwaylable=tkinter.Label(self.searchframe,text='搜索方式：     ')
        self.searchwaycmb= ttk.Combobox(self.searchframe,width=15)
        self.searchwaycmb['value'] = ('最新','最热','最好评')
        self.searchwaycmb.current(0)
        
        self.searchrangelable=tkinter.Label(self.searchframe,text='搜索范围：     ')
        self.searchrangecmb= ttk.Combobox(self.searchframe,width=15)
        self.searchrangecmb['value'] = ('自定义题库')
        self.searchrangecmb.current(0)
        
        self.searchdifficultylable=tkinter.Label(self.searchframe,text='题目难度：     ')
        self.searchdifficultycmb= ttk.Combobox(self.searchframe,width=15)
        self.searchdifficultycmb['value'] = ('无限制','0-1★','1-2★','2-3★','3-4★','4-5★')
        self.searchdifficultycmb.current(0)


        self.searchframe.place(x=0,y=0.05*height,anchor='nw')
        self.searchentry.place(x=0,y=0,anchor='nw')
        self.searchbutton.place(x=0.15*width,y=0,anchor='nw')
        

        self.searchcontentlable.grid(row=0,column=0)
        self.searchcontentcmb.grid(row=0,column=1)
        spacelabel=tkinter.Label(self.searchframe,text='   ')
        spacelabel.grid(row=1,column=0)
        self.searchwaylable.grid(row=2,column=0)
        self.searchwaycmb.grid(row=2,column=1)
        spacelabe2=tkinter.Label(self.searchframe,text='   ')
        spacelabe2.grid(row=3,column=0)
        self.searchrangelable.grid(row=4,column=0)
        self.searchrangecmb.grid(row=4,column=1)
        spacelabe3=tkinter.Label(self.searchframe,text='   ')
        spacelabe3.grid(row=5,column=0)
        self.searchdifficultylable.grid(row=6,column=0)
        self.searchdifficultycmb.grid(row=6,column=1)
        
        
        
        
        
        
        self.questioncanvas=tkinter.Canvas(self,width=0.5*width,height=0.5*height,bg='white')
        self.questioncanvas.place(x=0.3*width,y=0,anchor='nw')
        self.canvasnotice=tkinter.Label(self,text='双击表格中的题目等待几秒后可在右上方预览题目',font=('微软雅黑',12,'bold'))
        self.canvasnotice.place(x=0.3*width,y=0.5*height,anchor='nw')
        
        self.startdobutton=tkinter.Button(self,text='去作答',font=('微软雅黑',12,'bold'),fg='white',bg='black',command=self.chutibyfreesearch)
        self.startdobutton.place(x=0.8*width,y=0.5*height,anchor='ne')
        
        self.treeframe=tkinter.Frame(self,width=0.5*width,height=0.2*height)
        
        

        self.treeframe.place(x=0,y=0.7*height)
        ybar=tkinter.Scrollbar(self.treeframe,orient='vertical')
        self.tree=Showtimutable(self.treeframe,tablename='basic_questioninfor',height=5,columns=('col1','col2','col3','col4','col5','col6','col7','col8'),show='headings',selectmode='browse',yscrollcommand=ybar.set)
        ybar['command']=self.tree.yview
        self.tree.column('#1', width=cellwidth*2, anchor='center')
        self.tree.column('#2', width=cellwidth*2, anchor='center')
        self.tree.column('#3', width=cellwidth*3, anchor='center')
        self.tree.column('#4', width=cellwidth*2, anchor='center')
        self.tree.column('#5', width=cellwidth*2, anchor='center')
        self.tree.column('#6', width=cellwidth, anchor='center')
        self.tree.column('#7', width=cellwidth*2, anchor='center')
        self.tree.column('#8', width=cellwidth, anchor='center')
        self.tree.heading('col1', text='题目编号')
        self.tree.heading('col2', text='出题人')
        self.tree.heading('col3', text='题型描述')
        self.tree.heading('col4', text='提示方式')
        self.tree.heading('col5', text='难度系数')
        self.tree.heading('col6', text='总点赞数')
        self.tree.heading('col7', text='总作答次数')
        self.tree.heading('col8', text='好评率%')
#        self.tree.bind('<Double-Button-1>',qualifyquestionsymbol)
        self.tree.bind('<Double-Button-1>',self.previewquestion)
        self.tree.grid(row=0)
        ybar.grid(row=0,column=1,sticky='ns') 
        
        
        self.nextpagebutton=tkinter.Button(self,text='下一页',font=('微软雅黑',12,'bold'),command=self.tree.addpage)
        self.formerpagebutton=tkinter.Button(self,text='上一页',font=('微软雅黑',12,'bold'),command=self.tree.minuspage)
        
        self.nextpagebutton.place(x=0.5*width,y=0.6*height)
        self.formerpagebutton.place(x=0.2*width,y=0.6*height)
    
    def search(self):
        self.sql=self.sqlstart
        if self.searchcontentcmb.get()=='关键词':
            self.sqlkeywordpart="a.generaldescription like '%%%%%s%%%%' "%self.searchentry.get()
            self.sql+=self.sqlkeywordpart
            if self.searchrangecmb.get()=='自定义题库':
                self.sqlrangepart=" and a.tishitype='自定义提示'"
                self.sql+=self.sqlrangepart
            if len(self.searchdifficultycmb.get())!=3:
                self.sqldifficultypart=" and a.difficulty between %s and %s"%(self.searchdifficultycmb.get()[0],self.searchdifficultycmb.get()[2])
                self.sql+=self.sqldifficultypart
            self.sql+=" and a.state='公开'"
            if self.searchwaycmb.get()=='最新':
                self.sqlwaypart=" order by filetimenum desc"
                self.sql+=self.sqlwaypart
            elif self.searchwaycmb.get()=='最热':
                self.sqlwaypart=" order by frequency desc"
                self.sql+=self.sqlwaypart
        elif self.searchcontentcmb.get()=='题号':
            self.sqlquestionsymbolpart=" a.questionsymbol like '%%%%%s%%%%' and a.state='公开'"%self.searchentry.get()
            self.sql+=self.sqlquestionsymbolpart
        elif self.searchcontentcmb.get()=='用户':
            self.sqluserpart=" a.questionsymbol like '%%%%%s%%%%' and a.state='公开'"%self.searchentry.get()
            self.sql+=self.sqluserpart
        
        
        self.tree.sql=self.sql
        self.sql+=" limit %d,%d"%(self.tree.page*10,self.tree.geshu)
        print(self.sql)
        self.df = pd.read_sql_query(self.sql, self.engine)
        print(self.df)
        self.tree.df=self.df
        self.tree.delself()
        self.tree.showinfor()
        
        
        self.sql="select count(*) from basic_questioninfor as a where "
        if self.searchcontentcmb.get()=='关键词':
            self.sqlkeywordpart="a.generaldescription like '%%%%%s%%%%' "%self.searchentry.get()
            self.sql+=self.sqlkeywordpart
            if self.searchrangecmb.get()=='自定义题库':
                self.sqlrangepart=" and a.tishitype='自定义提示'"
                self.sql+=self.sqlrangepart
            if len(self.searchdifficultycmb.get())!=3:
                self.sqldifficultypart=" and a.difficulty between %s and %s"%(self.searchdifficultycmb.get()[0],self.searchdifficultycmb.get()[2])
                self.sql+=self.sqldifficultypart
            self.sql+=" and a.state='公开'"
            if self.searchwaycmb.get()=='最新':
                self.sqlwaypart=" order by filetimenum desc"
                self.sql+=self.sqlwaypart
            elif self.searchwaycmb.get()=='最热':
                self.sqlwaypart=" order by frequency desc"
                self.sql+=self.sqlwaypart
        elif self.searchcontentcmb.get()=='题号':
            self.sqlquestionsymbolpart=" a.questionsymbol like '%%%%%s%%%%' and a.state='公开'"%self.searchentry.get()
            self.sql+=self.sqlquestionsymbolpart
        elif self.searchcontentcmb.get()=='用户':
            self.sqluserpart=" a.questionsymbol like '%%%%%s%%%%' a.state='公开'"%self.searchentry.get()
            self.sql+=self.sqluserpart
        df=pd.read_sql_query(self.sql, self.engine)
        self.tree.num=df.iloc[0][0]
    
    def previewquestion(self,event):
        item =self.tree.selection()[0]
        global questionsymbol
        questionsymbol=self.tree.item(item, "values")[0]
        zdyallfunction.questionsymbol=self.tree.item(item, "values")[0]
        
        zdyallfunction.getquestion(questionsymbol)
        zdyallfunction.fileinelements()
        zdyallfunction.file()
        zdyallfunction.drawquestion()
        global smallest_index
        smallest_index=-1
        zdyallfunction.duandian=[]
        zdyallfunction.drawuserM(smallest_index)
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.5*width),int(0.5*height)),Image.ANTIALIAS))
        self.questioncanvas.create_image(0,0,anchor='nw',image = photo)
        win.mainloop()
    
    
    

    
    
    
    def chutibyfreesearch(self):
        self.questioncanvas.delete('all')
        self.tree.delself()
        global questionselection
        questionselection.withdraw()
        
        global gangdu,newquestion,questionsymbol,rightanswerquestion,c1,c3
        newquestion=1
        rightanswerquestion=0
        ts = time.time()
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        zdyallfunction.starttime=dt
#        questionsymbol='Tongji_11'
        text2.delete('0.0','end')
        zdyallfunction.jys=[]
        zdyallfunction.xys=[]
        zdyallfunction.scxys=[]
        c1.ufocus=0
        zdyallfunction.switchbjg=0
        lb1.delete(0,'end')
        
        gangdu=[]
        zdyallfunction.daduan=0
        zdyallfunction.duandian=[]
        zdyallfunction.calculation()
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        c3.create_image(0,0,anchor='nw',image = photo)
        
        global gjxx
        gjxx=[]
        for i in range(len(zdyallfunction.calelements)):
            num=zdyallfunction.calelements[i]['num']
            EA=zdyallfunction.calelements[i]['EA']
            l=zdyallfunction.calelements[i]['l']
            if zdyallfunction.calelements[i]['EA']>=1e8:
                EA=-1
            else:
                EA=zdyallfunction.calelements[i]['EA']
            if zdyallfunction.calelements[i]['EI']>=1e6:
                EI=-1
            else:
               EI=zdyallfunction.calelements[i]['EI'] 
            gjxx_='  杆件（%d）L=%d  EA=%d EI=%d'%(num,l,EA,EI)
            gjxx.append(gjxx_)
        lb1.delete(0,'end')
        for information in gjxx:
            lb1.insert('end',information)
        for i in range(len(zdyallfunction.elements)):
            zdyallfunction.duandian.append([0,1])
        c1.relativeposition()
        zdyallfunction.createanswers()
        if zdyallfunction.timutishifangshi!="自定义提示":
            zdyallfunction.bianbiedcx()
            zdyallfunction.bianbietixing()

        global tp2
        try:
            tp2.deiconify()
        except:
            pass
        c1.showuserM()
        win.mainloop()

















global instructionpartexist
instructionpartexist=0
def instructionpart():
    global instructionpartexist
    instructionpartexist=1
    gangdu=[]
    global newquestion,rightanswerquestion
    newquestion=0
    global instructiontp
    instructiontp = tkinter.Toplevel()
    instructiontp.title('引导题目')
    instructiontp.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
    instructiontp.geometry('%dx%d+%d+%d'%(1.1*width,height*1.05,dx,dy))
    instructiontp.resizable(0,0)
    def qdpart():
        smallest_index=c1.smallest_index
#        global varnum
        dangwei=c2.dangwei
        d=c2.d
        choice=c2.choice
        choiceelement=c2.choiceelement
        yli=c2.yli
        ylj=c2.ylj
        xli=c2.xli
        xlj=c2.xlj
        positions=c2.positions
#        yli,ylj,xli,xlj
        #清空显示距离的label
#        varnum.set('')
        class C_():
            pass
        alp=zdyallfunction.elements[choiceelement-1]['alp']
        if alp==180 or alp==-180:
            Mi=yli-positions[2][1]
            Mj=ylj-positions[0][1]
            Mmid=yli-positions[1][1]
            print(1)
        elif -90<alp<90:
            #确定过某一控制点与轴线平行的直线方程式，计算距离,
            #i端，中点，j端都一样，不过控制点坐标不同
            k=(ylj-yli)/(xlj-xli)
            b=yli-k*xli
            Mi=positions[0][1]-k*positions[0][0]-b
            Mj=positions[2][1]-k*positions[2][0]-b
            Mmid=positions[1][1]-k*positions[1][0]-b
            Mi=Mi/np.sqrt(1+k*k)
            Mj=Mj/np.sqrt(1+k*k)
            Mmid=Mmid/np.sqrt(1+k*k)
            print(2)
        elif alp==90:
            Mi=positions[0][0]-xli
            Mj=positions[2][0]-xlj
            print(3)
            Mmid=positions[1][0]-xli
        elif alp==-90:
            Mi=xli-positions[0][0]
            Mj=xlj-positions[2][0]
            Mmid=xli-positions[1][0]
            print(4)
        else:
            k=(ylj-yli)/(xlj-xli)
            b=yli-k*xli
            Mi=positions[2][1]-k*positions[2][0]-b
            Mj=positions[0][1]-k*positions[0][0]-b
            Mmid=positions[1][1]-k*positions[1][0]-b
            Mi=Mi/np.sqrt(1+k*k)*-1
            Mj=Mj/np.sqrt(1+k*k)*-1
            Mmid=Mmid/np.sqrt(1+k*k)*-1
            print(5)
        #不同档位，数值不同
        if dangwei==1:
            Mi=np.round(Mi/d)
            Mj=np.round(Mj/d)
        if dangwei==0.5:
            Mi=np.round(Mi/(0.5*d))/2
            Mj=np.round(Mj/(0.5*d))/2
        if dangwei==0.25:
            Mi=np.round(Mi/(0.25*d))/4
            Mj=np.round(Mj/(0.25*d))/4
        print('Mi=%f'%Mi,'Mj=%f'%Mj)
        Mmid=np.round(Mmid/d)
        c_=C_()
        
        if choice=='s':
    #        c_['num']=choiceelement
    #        c_['type']=choice
    #        c_['Mi']=0
    #        c_['Mj']=0
    #        c_['Mmid']=0
            pass
        else:
            #c_为用户作答的记录
            c_.num=choiceelement
            c_.type=choice
            c_.Mi=Mi
            c_.Mj=Mj
            c_.Mmid=Mmid
            c_.ns=zdyallfunction.ps
            c_.ne=zdyallfunction.pe
        zdyallfunction.changec(c_)
        c1.smallest_index=-1
        zdyallfunction.drawuserM(c1.smallest_index)
        c2.delete(tkinter.ALL)
        c2.b1.place(x=-100,y=0)
        c2.b2.place(x=-100,y=0)
        c2.b3.place(x=-100,y=0)
#        zdyallfunction.recordansweringprocess(-1)
        global instructionpartexist
        if instructionpartexist==1:
            global inshelp1,inshelp2,inshelp3,inshelp4,inshelp5
            try:
                inshelp1.destroy()
            except:
                pass
            try:
                inshelp2.destroy()
            except:
                pass     
            try:
                inshelp3.destroy()
            except:
                pass
            try:
                inshelp4.destroy()
            except:
                pass
            try:
                inshelp5.destroy()
            except:
                pass

        c1.paintline(zdyallfunction.c,c1.relposition)
        c2.delete(tkinter.ALL)
        c2.b1.place(x=-100,y=0)
        c2.b2.place(x=-100,y=0)
        c2.b3.place(x=-100,y=0)
    
    #程序自带的提示方式
    def showtishi():
        if zdyallfunction.jys!=[] or len(zdyallfunction.xys)!=len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='请先去除添加的约束')
            return 0
        zdyallfunction.bianbietixing()
        zdyallfunction.jiyutishi()
        if zdyallfunction.tishi!='':
            tkinter.messagebox.showinfo(title='提示', message='%s'%zdyallfunction.tishi)
        if zdyallfunction.tishi=='':
            tkinter.messagebox.showinfo(title='提示', message='特征点作答正确或此题无提示与分析')
    
    #tishichoice先判断给予提示的方式，是自定义还是程序自带的提示方式
    def tishichoice():
        if zdyallfunction.timutishifangshi=="自定义提示":
            showassistframe()
            buttonropemethod['fg']='red'
            zdytishi()
#            zdyallfunction.recordansweringprocess(0)
            button35['fg']='white'
            
        else:
            showtishi()
#            zdyallfunction.recordansweringprocess(1)
    
    #zdytishi是使用自定义的提示
    def zdytishi():
        if zdyallfunction.jys!=[] or len(zdyallfunction.xys)!=len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='请先去除添加的约束')
            return 0
#        ttt=zdyallfunction.jiyutishi()
#        if ttt==0:
#            tkinter.messagebox.showinfo(title='提示', message='请点击分析与提示，修改作答')
        else:
            weizuoda=1
            for i in range(len(zdyallfunction.a)):
                if len(zdyallfunction.a[i])==len(zdyallfunction.c[i]):
                        weizuoda=0 
            if weizuoda==1:
                if len(zdyallfunction.zhengtitishi)>1:
                    tkinter.messagebox.showinfo(title='提示', message=zdyallfunction.zhengtitishi)
                    return 0
                tkinter.messagebox.showinfo(title='提示', message="请先尝试作答")
                return 0
#            wanchengzuoda=1
#            for i in range(len(zdyallfunction.a)):
#                if len(zdyallfunction.c[i])!=len(zdyallfunction.a[i]):
#                    wanchengzuoda=0
#            if wanchengzuoda==0:
#                tkinter.messagebox.showinfo(title='', message='请先完成作答再比对')
#            else:
            zdycuowunum=zdyallfunction.offerzdytishi()
            zdyallfunction.zdycuowunum=zdycuowunum
            if zdycuowunum!=-1:
                tkinter.messagebox.showinfo(title='提示', message=zdyallfunction.zdytishi.iloc[zdycuowunum,4])
            else:
                tkinter.messagebox.showinfo(title='提示', message="特征点作答正确")
    def zdybidui():
        global Qnum
        global newquestion,rightanswerquestion
        def addlevelcredits():
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="select levelcredits from achievements where userID='%s'"%(zdyallfunction.userID)
            cursor.execute(sql)
            result=cursor.fetchone()
            result=int(result[0])
            conn.commit()
            cursor.close()
            
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update achievements set levelcredits='%d' where userID='%s'"%(result+round(float(zdyallfunction.timunandu),1)*10,zdyallfunction.userID)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            
        if zdyallfunction.jys!=[] or len(zdyallfunction.xys)!=len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='请先去除添加的约束')
            return 0
        if zdyallfunction.timutishifangshi!='自定义提示':
            zdyallfunction.bianbietixing()
            tishiright=zdyallfunction.jiyutishi()
            print(tishiright)
            zdyallfunction.tishiright=tishiright
#            zdyallfunction.recordansweringprocess(2)
            if tishiright==0:
    #            recordcuoti()
                tkinter.messagebox.showinfo(title='提示', message='请点击分析与提示，修改作答')
                if newquestion==1:
#                    zdyallfunction.momentanswer_record()
                    pass
                return 0
        if newquestion==1:
#            zdyallfunction.momentanswer_record()
            pass
        newquestion=0
        wanchengzuoda=1
        for i in range(len(zdyallfunction.a)):
            if len(zdyallfunction.c[i])!=len(zdyallfunction.a[i]):
                wanchengzuoda=0
        if wanchengzuoda==0:
            tkinter.messagebox.showinfo(title='', message='请先完成作答再比对')
            return 0
        else:
            rp1=zdyallfunction.biduileixing()
            if rp1==0:
                showcuowu()
                c1.delete('wrong')
                pix=c1.relposition[zdyallfunction.cuowunum]['pix']
                piy=c1.relposition[zdyallfunction.cuowunum]['piy']
                pjx=c1.relposition[zdyallfunction.cuowunum]['pjx']
                pjy=c1.relposition[zdyallfunction.cuowunum]['pjy']
                c1.create_line(pix, piy,
                  pjx, pjy,
                  fill='red',  # 红色
                  width=5,
                  tag=('wrong')
                  )
#                zdyallfunction.showleixing()
                #                    recordcuoti()
#                c1.showuserM()
            else:
                rp2=zdyallfunction.biduizf()
                if rp2==0:
                    showcuowu()
                    c1.delete('wrong')
                    pix=c1.relposition[zdyallfunction.cuowunum]['pix']
                    piy=c1.relposition[zdyallfunction.cuowunum]['piy']
                    pjx=c1.relposition[zdyallfunction.cuowunum]['pjx']
                    pjy=c1.relposition[zdyallfunction.cuowunum]['pjy']
                    c1.create_line(pix, piy,
                      pjx, pjy,
                      fill='red',  # 红色
                      width=5,
                      tag=('wrong')
                      )
#                    zdyallfunction.showzf()
                    #                        recordcuoti()
#                    c1.showuserM()
                else:
                    rp3=zdyallfunction.biduixddx()
                    if rp3==0:
                        showcuowu()
                        c1.delete('wrong')
                        pix=c1.relposition[zdyallfunction.cuowunum]['pix']
                        piy=c1.relposition[zdyallfunction.cuowunum]['piy']
                        pjx=c1.relposition[zdyallfunction.cuowunum]['pjx']
                        pjy=c1.relposition[zdyallfunction.cuowunum]['pjy']
                        c1.create_line(pix, piy,
                          pjx, pjy,
                          fill='red',  # 红色
                          width=5,
                          tag=('wrong')
                          )
#                        zdyallfunction.showxddx()
#                        #                            recordcuoti()
#                        c1.showuserM()
                    else:
                        rp4=zdyallfunction.biduijdfp()
                        if rp4==0:
                            showcuowu()
                            c1.delete('wrong')
                            for i in range(len(zdyallfunction.elements)):
                                if zdyallfunction.elements[i]['pi']['num']==zdyallfunction.cuowunum:
                                    xc=c1.relposition[zdyallfunction.cuowunum]['pix']
                                    yc=c1.relposition[zdyallfunction.cuowunum]['piy']
                                    break
                                if zdyallfunction.elements[i]['pj']['num']==zdyallfunction.cuowunum:
                                    xc=c1.relposition[zdyallfunction.cuowunum]['pjx']
                                    yc=c1.relposition[zdyallfunction.cuowunum]['pjy']
                                    break
                            print(xc,yc)
                            circle_dimension=int(20/1800*height)
                            c1.create_oval(xc-circle_dimension,yc-circle_dimension,
                             xc+circle_dimension,yc+circle_dimension,tag='wrong',width=5, outline='red')
#                            zdyallfunction.showjdfp()
                            #                                recordcuoti()
#                            c1.showuserM() 
                        else:
                            text2.delete('0.0','end')
                            c1.delete('wrong')
                            c1.delete('choice')
                            showcuowu()
                            if rightanswerquestion==0:
                                addlevelcredits()
                            rightanswerquestion=1
                            global achievement
                            try:
                                achievement.destroy()
                            except:
                                pass
                            showresultframe()
                            achievement=ACHIEVEMENTSFRAME(instructiontp,height=height,width=0.1*width,highlightbackground='black',highlightthickness=4)
                            achievement.place(x=width,y=0,anchor='nw')
                            tkinter.messagebox.showinfo(title='作答结果', message='恭喜！回答正确,您可点击内力图和变形图查看精确结果')
                            tkinter.messagebox.showinfo(title='作答结果', message='您已经完成引导题目,可以继续探索其他功能,并挑战更高难度的题目！')
                            achievement.bind()
#                            tkinter.messagebox.showinfo(title='作答结果', message='恭喜！回答正确')
#                                recordcorrectnum()
    def showquestion():
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        c3.create_image(0,0,anchor='nw',image = photo)
        win.mainloop()
            
            



        

#        
#        def qualifyquestionsymbol(event):
#                item =tree.selection()[0]
#                global questionsymbol
#                questionsymbol=tree.item(item, "values")[0]
#                zdyallfunction.questionsymbol=tree.item(item, "values")[0]
#                chuti()
            

#        global evaluation
#        evaluation=EVALUATION(instructiontp,height=0.1*height,width=0.35*width)
#        evaluation.place(x=0.62*width,y=0.5*height)
#        evaluation.bind()

    
    
    
    
    
    def chuti():
        global gangdu,newquestion,questionsymbol,rightanswerquestion
        newquestion=1
        rightanswerquestion=0
        ts = time.time()
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        zdyallfunction.starttime=dt
#        questionsymbol='Tongji_11'
        text2.delete('0.0','end')
        zdyallfunction.jys=[]
        zdyallfunction.xys=[]
        zdyallfunction.scxys=[]
        c1.ufocus=0
        zdyallfunction.switchbjg=0
        lb1.delete(0,'end')
        
        gangdu=[]
        zdyallfunction.daduan=0
        zdyallfunction.duandian=[]
        questionsymbol="z373072096_9"
        zdyallfunction.questionsymbol=questionsymbol
        zdyallfunction.getquestion(questionsymbol)


        zdyallfunction.fileinelements()
        zdyallfunction.file()
        zdyallfunction.calculation()
        zdyallfunction.drawquestion()
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        c3.create_image(0,0,anchor='nw',image = photo)
        smallest_index=-1
        showinfor()
        for i in range(len(zdyallfunction.elements)):
            zdyallfunction.duandian.append([0,1])
        #初始化，角约束jys，线约束xys，删除线约束scxys，半结构switchbjg
        #改变刚度的列表gangdu，断点列表duandian
        zdyallfunction.drawuserM(smallest_index)

        c1.relativeposition()
        zdyallfunction.createanswers()
        if zdyallfunction.timutishifangshi!="自定义提示":
            zdyallfunction.bianbiedcx()
            zdyallfunction.bianbietixing()
        im2=Image.open(f'{os.getcwd()}/drawing/userM.png')
        photo2 = ImageTk.PhotoImage(im2.resize((wp,hp),Image.ANTIALIAS))
        c1.create_image(0,0,anchor='nw',image = photo2)
        tkinter.messagebox.showinfo(title='提示', message='请点击位于屏幕中央的引导模式介绍')
#        c1.showuserM()
        win.mainloop()
    

#    global c1,c2,c3,wp,hp,text2,lb1
    c1=Xuanzecanvas(master=instructiontp,height=0.5*height,width=0.5*width,bg='white')
    c1.place(x=0,y=0.5*height,anchor='nw')
    c2=Zuodacanvas(master=instructiontp,height=0.4*height,width=0.4*height,bg='white')
    c2.qualifypartner(c1)
    c2.place(x=0,y=0,anchor='nw')
    c1.qualifypartner(c2)
    hp=int(0.5*height)
    wp=int(0.5*width)
    frame1=tkinter.Frame(instructiontp,width=0.3*width,height=0.1*height)
    frame1.place(x=0.52*width,y=0.52*height,anchor='nw')
    def showinstructionnotice():
        buttonzdy31['fg']=['white']
        tkinter.messagebox.showinfo(title='提示', message='通过此题您可快速地熟悉作答模式的操作\n接下来请根据软件的提示一步步地绘制本题的大致概念弯矩图')
        button35['fg']='red'

        inshelp1=HELPTOPLEVEL(name='自定义提示介绍',ratio=1.6,picturename='instructionhelp1.jpg',message='请点击中下方的分析提示按钮')
        inshelp1.bind()
        destroy_inshelp()
        win.mainloop()

    buttonzdy31=tkinter.Button(frame1,text='引导模式介绍',fg='red',bg='black',font=('微软雅黑',12),height=1,command=showinstructionnotice)
#    buttonzdy32=tkinter.Button(frame1,text='结束测试',fg='white',bg='black',font=('微软雅黑',13),width=10,height=1)
#    buttonzdy33=tkinter.Button(frame1,text='保存上传',fg='white',bg='black',font=('微软雅黑',13),width=10,height=1)
    buttonzdy31.grid(row=0,column=0)
#    buttonzdy32.grid(row=0,column=2)
#    buttonzdy33.grid(row=0,column=4)
    button34=tkinter.Button(instructiontp,text='确定',font=('微软雅黑',13),width=5,height=1,command=qdpart)
    button34.place(x=0.4*height,y=0.4*height,anchor='sw')
    frame2=tkinter.Frame(instructiontp,width=0.2*width,height=0.2*height)
    frame2.place(x=0.4*height,y=0.1*height)
    lable31=tkinter.Label(frame2,text='档位选择',font=('微软雅黑',10),width=8,height=1,fg='white',bg='black')
    drawhelplable=tkinter.Label(instructiontp,text='请拖动小绿点绘制选中部分的弯矩图',fg='red',font=('微软雅黑',8,'bold'))
    drawhelplable.place(x=0.4*height,y=0.3*height,anchor='sw')
    
    noticelable=tkinter.Label(instructiontp,text='请绘制弯矩图的大致形状，作答的任意过程可点击分析提示并在完成后提交比对',fg='red',font=('微软雅黑',9,'bold'))
    noticelable.place(x=0,y=0.5*height,anchor='sw')
    cmb1 = ttk.Combobox(frame2,width=6)
    cmb1['value'] = ('整数档','0.5档','0.25档')
    def dw(event):
        if (cmb1.get()=="整数档"):
            c2.dangwei=1
        if (cmb1.get()=="0.5档"):
            c2.dangwei=0.5
        if (cmb1.get()=="0.25档"):
            c2.dangwei=0.25
    cmb1.bind("<<ComboboxSelected>>",dw)
    cmb1.current(0)
    lable31.grid(row=0,column=0)
    cmb1.grid(row=1,column=0)
    text2=tkinter.Text(instructiontp,font=('微软雅黑',10),height=5,width=40)
    text2.place(x=0.8*height,y=height,anchor='sw')
    lb1=tkinter.Listbox(instructiontp,font=('微软雅黑',15),height=10,width=25)
    lb1.place(x=width,y=height,anchor='se')
    def createinfor():
        global gjxx
        gjxx=[]
        for i in range(len(zdyallfunction.calelements)):
            num=zdyallfunction.calelements[i]['num']
            EA=zdyallfunction.calelements[i]['EA']
            l=zdyallfunction.calelements[i]['l']
            if zdyallfunction.calelements[i]['EA']>=1e8:
                EA=-1
            else:
                EA=zdyallfunction.calelements[i]['EA']
            if zdyallfunction.calelements[i]['EI']>=1e6:
                EI=-1
            else:
               EI=zdyallfunction.calelements[i]['EI'] 
            gjxx_='  杆件（%d）L=%d  EA=%d EI=%d'%(num,l,EA,EI)
            gjxx.append(gjxx_)
            
    #显示杆件信息，gjxx
    def showinfor():
        createinfor()
        lb1.delete(0,'end')
        for information in gjxx:
            lb1.insert('end',information)
    def gaibiangangdu():
        #确定改变刚度
        def gangduqd():
              gangdu_=[]
              gangdu_.append(int(entry3.get())) 
              gangdu_.append(int(entry4.get()))
              gangdu_.append(int(entry5.get()))
              gangdu.append(gangdu_.copy())
              entry3.delete(0,'end')
              zdyallfunction.changeEAI(gangdu)
              showinfor()
              zdyallfunction.switchEAI=1
              zdyallfunction.drawquestion()
              showquestion()
        #完成输入后计算
        def gangdujs():
            zdyallfunction.file()
            zdyallfunction.changeEAI(gangdu)
            zdyallfunction.calculation()
            showinfor()
            tp6.destroy()
            #swicthEAI负责是否要用颜色在左上角显示刚度
            zdyallfunction.switchEAI=1
            zdyallfunction.drawquestion()
            showquestion()
            
        def original():
             gangdujs()
    
    
    
        tp6=tkinter.Toplevel()
        tp6.title('改变刚度')
        tp6.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp6.geometry('%dx%d+%d+%d'%(0.3*height,0.3*height,dx,dy))
        frame6=tkinter.Frame(tp6,width=0.64*height,height=0.5*height,)
        frame6.place(x=0,y=0,anchor='nw')
        label3=tkinter.Label(frame6,text='杆件号',font=('微软雅黑',15),width=10,height=1)
        entry3=tkinter.Entry(frame6,font=('微软雅黑',15),width=10)
        label4=tkinter.Label(frame6,text='EA=',font=('微软雅黑',15),width=10,height=1)
        entry4=tkinter.Entry(frame6,font=('微软雅黑',15),width=10)
        label5=tkinter.Label(frame6,text='EI=',font=('微软雅黑',15),width=10,height=1)
        entry5=tkinter.Entry(frame6,font=('微软雅黑',15),width=10)
        button23=tkinter.Button(frame6,text='确定并预览',font=('微软雅黑',15),width=10,height=1,fg='red',command=gangduqd)
        button24=tkinter.Button(frame6,text='关闭',font=('微软雅黑',15),width=10,height=1,fg='red',command=gangdujs)
        label3.grid(row=0,column=0)
        entry3.grid(row=0,column=1)
        label4.grid(row=1,column=0)
        entry4.grid(row=1,column=1)
        label5.grid(row=2,column=0)
        entry5.grid(row=2,column=1)
        button23.grid(row=3,column=0,columnspan=4)
        button24.grid(row=4,column=0,columnspan=4)
        tp6.protocol("WM_DELETE_WINDOW",original)
    def showcuowu():
        text2.delete('0.0','end')
        text2.insert('end',zdyallfunction.cuowu)
        
    
    button35=tkinter.Button(instructiontp,text='分析提示',font=('微软雅黑',13),width=10,height=1,fg='white',bg='black',command=tishichoice)
    button36=tkinter.Button(instructiontp,text='提交比对',font=('微软雅黑',13),width=10,height=1,fg='white',bg='black',command=zdybidui)
    button35.place(x=0.9*height,y=0.65*height,anchor='nw')
    button36.place(x=0.9*height,y=0.75*height,anchor='nw')
    c3=tkinter.Canvas(instructiontp,height=0.5*height,width=0.5*width,bg='white')

    c3.place(x=0.5*width,y=0,anchor='nw')
    
    frame0=tkinter.Frame(win,height=0.5*height,width=0.1*height)
    frame0.place(x=0.8*height,y=0,anchor='ne')
    
    
    def showEAI():
        if zdyallfunction.switchEAI==0:
            zdyallfunction.switchEAI=1
        else: 
            zdyallfunction.switchEAI=0
        zdyallfunction.drawrestraintquestion()
        showquestion()
    def jysjm():
        #增角约束
        def zjys():
             if int(entry4.get())>len(zdyallfunction.joints_) or int(entry4.get())>len(zdyallfunction.joints_)<0:
                 tkinter.messagebox.showinfo(title='提示', message='节点号有误，请重新输入')
                 return
             zdyallfunction.jys.append(int(entry4.get()))
             zdyallfunction.drawrestraintquestion()
             showquestion()
    
        #删除角约束
        def sjys():
            if int(entry4.get()) in zdyallfunction.jys:
                zdyallfunction.jys.remove(int(entry4.get()))
            zdyallfunction.drawrestraintquestion()
            showquestion()
        
        #确定
        def queding():
            zdyallfunction.file()
            zdyallfunction.changecalrestraint()
            zdyallfunction.changeEAI(gangdu)
            zdyallfunction.calculation()
            zdyallfunction.drawuserM(c1.smallest_index)
            tp7.destroy()
            c1.showuserM()
            
            
        def originaljys():
            queding()
        
        tp7=tkinter.Toplevel()
        tp7.title('增加角约束')
        tp7.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp7.geometry('%dx%d+%d+%d'%(0.3*height,0.3*height,dx,dy))
        frame7=tkinter.Frame(tp7,width=0.64*height,height=0.5*height,)
        frame7.place(x=0,y=0,anchor='nw')
        label4=tkinter.Label(frame7,text='节点号',font=('微软雅黑',15),width=10,height=1)
        entry4=tkinter.Entry(frame7,font=('微软雅黑',15),width=10)
        button15=tkinter.Button(frame7,text='增加',font=('微软雅黑',15),width=10,height=1,fg='red',command=zjys)
        button16=tkinter.Button(frame7,text='删去',font=('微软雅黑',15),width=10,height=1,fg='red',command=sjys)
        button17=tkinter.Button(frame7,text='确认',font=('微软雅黑',15),width=10,height=1,fg='red',command=queding)
        
        label4.grid(row=0,column=0)
        entry4.grid(row=0,column=1)
        button15.grid(row=1,column=0,columnspan=2)
        button16.grid(row=2,column=0,columnspan=2)
        button17.grid(row=3,column=0,columnspan=2)
        tp7.protocol("WM_DELETE_WINDOW",originaljys)

    #同理如上
    def xysjm():
        class Yueshup():
            pass
        
        
        def zxys():
            if int(entry4.get())>len(zdyallfunction.joints_) or int(entry4.get())>len(zdyallfunction.joints_)<0:
                 tkinter.messagebox.showinfo(title='提示', message='节点号有误，请重新输入')
                 return
            Yueshup_=Yueshup()
            Yueshup_.num=int(entry4.get())
            Yueshup_.alp=int(entry5.get())
            zdyallfunction.xys.append(copy.copy(Yueshup_))
            zdyallfunction.changerestraint()
            zdyallfunction.changecalrestraint()
            zdyallfunction.drawrestraintquestion()
            showquestion()
        
        def sxys():
            for i in range(len(zdyallfunction.xys)):
                print(zdyallfunction.xys[i].num)
                if zdyallfunction.xys[i].num==int(entry4.get()):
                    zdyallfunction.scxys.append(int(entry4.get()))
                    print(zdyallfunction.scxys)
            zdyallfunction.changerestraint()
            zdyallfunction.changecalrestraint()
            zdyallfunction.drawrestraintquestion()
            showquestion()
            
            
        def queding():
            zdyallfunction.file()
            zdyallfunction.changecalrestraint()
            zdyallfunction.changeEAI(gangdu)
            zdyallfunction.calculation()
            zdyallfunction.drawuserM(c1.smallest_index)
            tp7.destroy()
            c1.showuserM()
            
            
            
        def originalxys():
            queding()
    
        tp7=tkinter.Toplevel()
        tp7.title('增加线约束')
        tp7.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp7.geometry('%dx%d+%d+%d'%(0.3*height,0.3*height,dx,dy))
        frame7=tkinter.Frame(tp7,width=0.64*height,height=0.5*height,)
        frame7.place(x=0,y=0,anchor='nw')
        label4=tkinter.Label(frame7,text='节点号',font=('微软雅黑',15),width=10,height=1)
        entry4=tkinter.Entry(frame7,font=('微软雅黑',15),width=10)
        label5=tkinter.Label(frame7,text='角度',font=('微软雅黑',15),width=10,height=1)
        entry5=tkinter.Entry(frame7,font=('微软雅黑',15),width=10)
        button15=tkinter.Button(frame7,text='增加',font=('微软雅黑',15),width=10,height=1,fg='red',command=zxys)
        button16=tkinter.Button(frame7,text='删去',font=('微软雅黑',15),width=10,height=1,fg='red',command=sxys)
        button17=tkinter.Button(frame7,text='确认',font=('微软雅黑',15),width=10,height=1,fg='red',command=queding)
        label4.grid(row=0,column=0)
        entry4.grid(row=0,column=1)
        label5.grid(row=1,column=0)
        entry5.grid(row=1,column=1)
        button15.grid(row=2,column=0,columnspan=2)
        button16.grid(row=3,column=0,columnspan=2)
        button17.grid(row=4,column=0,columnspan=2)
        tp7.protocol("WM_DELETE_WINDOW",originalxys)
    def showassistframe():
        frame0.place(x=0.8*height,y=0,anchor='ne')
        
    frame0=tkinter.Frame(instructiontp,height=0.5*height,width=0.1*height)
#    frame0.place(x=0.8*height,y=0,anchor='ne')
    
#    button37=tkinter.Button(frame0,text='显示刚度',font=('微软雅黑',12),width=10,height=1,bg='yellow',command=showEAI)
#    button38=tkinter.Button(frame0,text='增减角约束',font=('微软雅黑',12),width=10,height=1,command=jysjm,bg='yellow')
#    button39=tkinter.Button(frame0,text='增减线约束',font=('微软雅黑',12),width=10,height=1,command=xysjm,bg='yellow')
#    button310=tkinter.Button(frame0,text='改变刚度',font=('微软雅黑',12),width=10,height=1,bg='yellow',command=gaibiangangdu)
    
    
    def showropemethod():
        global rope
        rope=Rope(win)
        tkinter.messagebox.showinfo(title='提示', message='请向下拖动绳子中点的黑色节点，模拟简支梁的弯矩图')
        rope.bind()
        def exitrope():
            try:
                rope.destroy()
            except:
                pass
            

            tkinter.messagebox.showinfo(title='提示', message='现在您可以正式开始作答了！')
            buttonropemethod['fg']='black'
            global inshelp2
            inshelp2=HELPTOPLEVEL(name='操作简介',ratio=1.6,picturename='instructionhelp2.jpg')
            inshelp2.bind()
            destroy_inshelp()
        rope.protocol("WM_DELETE_WINDOW",exitrope)
    
    buttonropemethod=tkinter.Button(frame0,text='ropemethod',font=('微软雅黑',12),width=10,height=1,bg='yellow',command=showropemethod)
#    button37.grid(row=0,column=0)
#    button38.grid(row=1,column=0)
#    button39.grid(row=2,column=0)
#    button310.grid(row=3,column=0)
    buttonropemethod.grid(row=4,column=0)
    def wjt():
        global newquestion
        if (newquestion==1 and zdyallfunction.jys==[]) and len(zdyallfunction.xys)==len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='您可在增加约束或提交比对后查看')
            return 0
        def fangdaM():
            zdyallfunction.amplifyM(2)
            zdyallfunction.drawM()
            im=Image.open(f'{os.getcwd()}/drawing/M.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp1, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
        def suoxiaoM():
            zdyallfunction.amplifyM(1/2)
            zdyallfunction.drawM()
            im=Image.open(f'{os.getcwd()}/drawing/M.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp1, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
        
    
    
        zdyallfunction.drawM()
        tp1 = tkinter.Toplevel()
        tp1.title('弯矩图')
        tp1.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp1.geometry('%dx%d+%d+%d'%(0.72*height,0.5*height,dx,dy))
        tp1.resizable(0,0)
        im=Image.open(f'{os.getcwd()}/drawing/M.png')
        hp3=int(0.45*height)
        wp3=int(0.72*height)
        photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
        labelphoto3 = tkinter.Label(tp1, image=photo,width=wp3,height=hp3)
        labelphoto3.place(x=0, y=0,anchor='nw')
        
        
        
        frame5=tkinter.Frame(tp1,width=0.72*height,height=0.055*height,bg='deepskyblue')
        frame5.place(x=0,y=0.445*height,anchor='nw')
    
    
        im=Image.open(f'{os.getcwd()}/infor/zheng.png')
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button21=tkinter.Button(tp1,image=imgBtn,command=fangdaM)
        button21.place(x=0.36*height,y=0.5*height,anchor='se')
        
        im=Image.open(f'{os.getcwd()}/infor/fu.png')
        imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button22=tkinter.Button(tp1,image=imgBtn2,command=suoxiaoM)
        button22.place(x=0.36*height,y=0.5*height,anchor='sw')
        
        win.mainloop()
        
    def jlt():
        if (newquestion==1 and zdyallfunction.jys==[]) and len(zdyallfunction.xys)==len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='您可在增加约束或提交比对后查看')
            return 0
        def fangdaF():
            zdyallfunction.amplifyF(2)
            zdyallfunction.drawshearforce()
            im=Image.open(f'{os.getcwd()}/drawing/shearforce.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(instructiontp, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
        def suoxiaoF():
            zdyallfunction.amplifyF(1/2)
            zdyallfunction.drawshearforce()
            im=Image.open(f'{os.getcwd()}/drawing/shearforce.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(instructiontp, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
    
        zdyallfunction.drawshearforce()
        instructiontp = tkinter.Toplevel()
        instructiontp.title('剪力图')
        instructiontp.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        instructiontp.geometry('%dx%d+%d+%d'%(0.72*height,0.5*height,dx,dy))
        instructiontp.resizable(0,0)
        im=Image.open(f'{os.getcwd()}/drawing/shearforce.png')
        hp3=int(0.45*height)
        wp3=int(0.72*height)
        photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
        labelphoto4 = tkinter.Label(instructiontp, image=photo,width=wp3,height=hp3)
        labelphoto4.place(x=0, y=0,anchor='nw')
        
        
        
        frame5=tkinter.Frame(instructiontp,width=0.72*height,height=0.055*height,bg='deepskyblue')
        frame5.place(x=0,y=0.445*height,anchor='nw')
        
        im=Image.open(f'{os.getcwd()}/infor/zheng.png')
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button21=tkinter.Button(instructiontp,image=imgBtn,command=fangdaF)
        button21.place(x=0.36*height,y=0.5*height,anchor='se')
        
        im=Image.open(f'{os.getcwd()}/infor/fu.png')
        imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button22=tkinter.Button(instructiontp,image=imgBtn2,command=suoxiaoF)
        button22.place(x=0.36*height,y=0.5*height,anchor='sw')
        win.mainloop()
    
    #如上同理
    def zlt():
        if (newquestion==1 and zdyallfunction.jys==[]) and len(zdyallfunction.xys)==len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='您可在增加约束或提交比对后查看')
            return 0
        def fangdaN():
            zdyallfunction.amplifyN(2)
            zdyallfunction.drawN()
            im=Image.open(f'{os.getcwd()}/drawing/N.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp3, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
        def suoxiaoN():
            zdyallfunction.amplifyN(1/2)
            zdyallfunction.drawN()
            im=Image.open(f'{os.getcwd()}/drawing/N.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp3, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
    
        zdyallfunction.drawN()
        tp3 = tkinter.Toplevel()
        tp3.title('轴力图')
        tp3.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp3.geometry('%dx%d+%d+%d'%(0.72*height,0.5*height,dx,dy))
        tp3.resizable(0,0)
        im=Image.open(f'{os.getcwd()}/drawing/N.png')
        hp3=int(0.45*height)
        wp3=int(0.72*height)
        photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
        labelphoto4 = tkinter.Label(tp3, image=photo,width=wp3,height=hp3)
        labelphoto4.place(x=0, y=0,anchor='nw')
        
        
        
        frame5=tkinter.Frame(tp3,width=0.72*height,height=0.055*height,bg='deepskyblue')
        frame5.place(x=0,y=0.445*height,anchor='nw')
        
        im=Image.open(f'{os.getcwd()}/infor/zheng.png')
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button21=tkinter.Button(tp3,image=imgBtn,command=fangdaN)
        button21.place(x=0.36*height,y=0.5*height,anchor='se')
        
        im=Image.open(f'{os.getcwd()}/infor/fu.png')
        imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button22=tkinter.Button(tp3,image=imgBtn2,command=suoxiaoN)
        button22.place(x=0.36*height,y=0.5*height,anchor='sw')
        win.mainloop()
     
    #如上同理
    def bxt():
        def fangdaD():
            zdyallfunction.amplifydeformation(3)
            zdyallfunction.drawdeformation()
            im=Image.open(f'{os.getcwd()}/drawing/deformation.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp4, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
        def suoxiaoD():
            zdyallfunction.amplifydeformation(1/3)
            zdyallfunction.drawdeformation()
            im=Image.open(f'{os.getcwd()}/drawing/deformation.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp4, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
    
        zdyallfunction.drawdeformation()
        tp4 = tkinter.Toplevel()
        tp4.title('变形图')
        tp4.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp4.geometry('%dx%d+%d+%d'%(0.72*height,0.5*height,dx,dy))
        tp4.resizable(0,0)
        im=Image.open(f'{os.getcwd()}/drawing/deformation.png')
        hp3=int(0.45*height)
        wp3=int(0.72*height)
        photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
        labelphoto4 = tkinter.Label(tp4, image=photo,width=wp3,height=hp3)
        labelphoto4.place(x=0, y=0,anchor='nw')
        
        
        
        frame5=tkinter.Frame(tp4,width=0.72*height,height=0.055*height,bg='deepskyblue')
        frame5.place(x=0,y=0.445*height,anchor='nw')
        
        im=Image.open(f'{os.getcwd()}/infor/zheng.png')
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button21=tkinter.Button(tp4,image=imgBtn,command=fangdaD)
        button21.place(x=0.36*height,y=0.5*height,anchor='se')
        
        im=Image.open(f'{os.getcwd()}/infor/fu.png')
        imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button22=tkinter.Button(tp4,image=imgBtn2,command=suoxiaoD)
        button22.place(x=0.36*height,y=0.5*height,anchor='sw')
        win.mainloop()    
        
    def showresultframe():
        frame3.place(x=width-0.5*width,y=0.5*height,anchor='se')
    frame3=tkinter.Frame(instructiontp,height=0.5*height,width=0.2*height,)
#    frame3.place(x=width-0.5*width,y=0.5*height,anchor='se')
    
    def destroy_inshelp():
        global inshelp1,inshelp2,inshelp3,inshelp4,inshelp5
        try:
            inshelp1.destroy()
        except:
            pass
        try:
            inshelp2.destroy()
        except:
            pass     
        try:
            inshelp3.destroy()
        except:
            pass
        try:
            inshelp4.destroy()
        except:
            pass
        try:
            inshelp5.destroy()
        except:
            pass
    
    button11=tkinter.Button(frame3,text='弯矩图',font=('微软雅黑',12),width=10,height=1,bg='springgreen',command=wjt)
    button12=tkinter.Button(frame3,text='剪力图',font=('微软雅黑',12),width=10,height=1,bg='springgreen',command=jlt)
    button13=tkinter.Button(frame3,text='轴力图',font=('微软雅黑',12),width=10,height=1,bg='springgreen',command=zlt)
    button14=tkinter.Button(frame3,text='变形图',font=('微软雅黑',12),width=10,height=1,bg='springgreen',command=bxt)
    button11.grid(row=0)
    button12.grid(row=1)
    button13.grid(row=2)
    button14.grid(row=3)
    def exitinsturctiontp():
        global questionselection
        global instructionpartexist
        instructionpartexist=0
        
        try:
            questionselection.deiconify()
        except:
            pass
        global inshelp1,inshelp2,inshelp3,inshelp4,inshelp5
        try:
            inshelp1.destroy()
        except:
            pass
        try:
            inshelp2.destroy()
        except:
            pass     
        try:
            inshelp3.destroy()
        except:
            pass
        try:
            inshelp4.destroy()
        except:
            pass
        try:
            inshelp5.destroy()
        except:
            pass
        
        instructiontp.destroy()
        global achievement
        achievement=ACHIEVEMENTSFRAME(tp2,height=height,width=0.1*width,highlightbackground='black',highlightthickness=4)
        achievement.place(x=width,y=0,anchor='nw')
        achievement.bind()
    buttonmoveleft3=tkinter.Button(instructiontp,text='返回',command=exitinsturctiontp,fg='white',bg='black',font=('微软雅黑',12,'bold'))
    buttonmoveleft3.place(x=0,y=height*1.05,anchor='sw')
    instructiontp.protocol("WM_DELETE_WINDOW",exitinsturctiontp)
    chuti()












def showrecommendation():
    global tp2
    try:
        tp2.withdraw()
    except:
        pass
    global recommendation
    recommendation=RECOMMENDATION()
    tkinter.messagebox.showinfo(title='提示', message='请您耐心等待界面刷新！')
    recommendation.qualifyrecommendationquestions()
    win.mainloop()


class QUESTIONSELECTION(tkinter.Toplevel):
    def __init__(self,master=None,**kw):
        tkinter.Toplevel.__init__(self,master,**kw)
        self.geometry('%dx%d+%d+%d'%(1.1*width,height,dx,dy))
        self.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.selectiondic={}
        self.selectiondic['instruction']='0'
        self.selectiondic['rookie']=[19,16,17,18]
        self.selectiondic['primary']=[7,12,8,0]
        self.selectiondic['normal']=[1,11,13,14]
        self.selectiondic['hard']=[3,5,6,9]
        self.selectiondic['challenge']=[2,4,10,0]
        # self.selectiondic={'instruction',{'rookie':'7,12,8,0'},{'primary':'1,11,13,14'},{'normal':'3,5,6,9'},{'hard':'2,4,10,0'},'like','free'}
        self.selection='instruction'
        
        self.instructionframe=tkinter.Frame(self,height=0.8*height,width=0.6*width)
        self.multiquestionframe=tkinter.Frame(self,height=height,width=width)
        self.instructionbutton=tkinter.Button(self,text='引导题目',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.showinstructionframe)
        self.rookiebutton=tkinter.Button(self,text='入门题目',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.rookiequestions)
        self.primarybutton=tkinter.Button(self,text='初级题目',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.primaryquestions)
        self.normalbutton=tkinter.Button(self,text='中级题目',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.normalquestions)
        self.hardbutton=tkinter.Button(self,text='困难题目',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.hardquestions)
        self.challengebutton=tkinter.Button(self,text='挑战题目',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.challengequestions)
        self.likebutton=tkinter.Button(self,text='猜你喜欢',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=showrecommendation)
        self.freesearchbutton=tkinter.Button(self,text='自由搜索',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.showfreesearchframe)
        
        self.lefttopcanvas=tkinter.Canvas(self.multiquestionframe,width=0.4*width,height=0.4*height)
        self.righttopcanvas=tkinter.Canvas(self.multiquestionframe,width=0.4*width,height=0.4*height)
        self.leftbottomcanvas=tkinter.Canvas(self.multiquestionframe,width=0.4*width,height=0.4*height)
        self.rightbottomcanvas=tkinter.Canvas(self.multiquestionframe,width=0.4*width,height=0.4*height)
        
        self.instructioncanvas=tkinter.Canvas(self.instructionframe,width=0.5*width,height=0.5*height)
        
        self.lefttoplable=tkinter.Label(self.multiquestionframe,text='',font=('微软雅黑',10,'bold'))
        self.righttoplable=tkinter.Label(self.multiquestionframe,text='',font=('微软雅黑',10,'bold'))
        self.leftbottomlable=tkinter.Label(self.multiquestionframe,text='',font=('微软雅黑',10,'bold'))
        self.rightbottomlable=tkinter.Label(self.multiquestionframe,text='',font=('微软雅黑',10,'bold'))
        self.instructionlable=tkinter.Label(self.instructionframe,text='若您是首次使用本软件的作答模式可以通过这道题目快速的熟悉相关的操作与功能',font=('微软雅黑',12,'bold'))
        self.noticelable=tkinter.Label(self,text='请选择左侧的题目类型，首次使用可点击引导题目快速熟悉操作',font=('微软雅黑',15,'bold'),fg='red')
        
        
        
        def showinstructionpart():
            self.withdraw()
            instructionpart()
        
        self.lefttopbutton=tkinter.Button(self.multiquestionframe,text='去作答',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.lefttopgo)
        self.righttopbutton=tkinter.Button(self.multiquestionframe,text='去作答',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.righttopgo)
        self.leftbottombutton=tkinter.Button(self.multiquestionframe,text='去作答',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.leftbottomgo)
        self.rightbottombutton=tkinter.Button(self.multiquestionframe,text='去作答',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.rightbottomgo)
        self.instructiongobutton=tkinter.Button(self.instructionframe,text='去作答',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=showinstructionpart)
        
        
        self.questionnum=0
        
        
        self.instructionbutton.place(x=0,y=0.05*height,anchor='nw')
        self.rookiebutton.place(x=0,y=0.15*height,anchor='nw')
        self.primarybutton.place(x=0,y=0.25*height,anchor='nw')
        self.normalbutton.place(x=0,y=0.35*height,anchor='nw')
        self.hardbutton.place(x=0,y=0.45*height,anchor='nw')
        self.challengebutton.place(x=0,y=0.55*height,anchor='nw')
        self.freesearchbutton.place(x=0,y=0.65*height,anchor='nw')
        self.likebutton.place(x=0,y=0.75*height,anchor='nw')
        
        
        
        self.instructioncanvas.place(x=0*width,y=0*height,anchor='nw')
        
        self.instructionframe.place(x=0.3*width,y=0.1*height)
        
        self.noticelable.place(x=0.4*width,y=0.4*height)
        self.movebackbutton=tkinter.Button(self,text='返回',fg='white',bg='black',font=('微软雅黑',12,'bold'),command=self.moveformer)
        self.movebackbutton.place(x=0,y=height,anchor='sw')
        self.resizable(0,0)
        #        im=Image.open(f'{os.getcwd()}/questions/instructionq.png')
        #        photo = ImageTk.PhotoImage(im.resize((int(0.5*width),int(0.5*height)),Image.ANTIALIAS))
        #        self.instructioncanvas.create_image(0,0,anchor='nw',image = photo)
        #        self.instructionlable.place(x=0,y=0.52*height,anchor='nw')
        #        self.instructiongobutton.place(x=0.2*width,y=0.6*height)



    #        win.mainloop()
    def moveformer(self):
        global tp2
        try:
            tp2.destroy()
        except:
            pass
        self.destroy()
        modechoice()
    def lefttopgo(self):
        self.questionnum=self.selectiondic[self.selection][0]
        self.chuti()
    def righttopgo(self):
        self.questionnum=self.selectiondic[self.selection][1]
        self.chuti()
    def leftbottomgo(self):
        self.questionnum=self.selectiondic[self.selection][2]
        self.chuti()
    def rightbottomgo(self):
        self.questionnum=self.selectiondic[self.selection][3]
        self.chuti()
    def showmultiquestions(self):
        try:
            self.instructionframe.place_forget()
        except:
            pass
        try:
            self.freesearchframe.place_forget()
        except:
            pass
        self.lefttopcanvas.delete('all')
        self.righttopcanvas.delete('all')
        self.leftbottomcanvas.delete('all')
        self.rightbottomcanvas.delete('all')
        self.multiquestionframe.place(x=0.1*width,y=0,anchor='nw')
        self.lefttopcanvas.place(x=0,y=0,anchor='nw')
        self.righttopcanvas.place(x=0.5*width,y=0,anchor='nw')
        self.leftbottomcanvas.place(x=0,y=0.5*height,anchor='nw')
        self.rightbottomcanvas.place(x=0.5*width,y=0.5*height,anchor='nw')
        self.lefttopbutton.place(x=0.4*width,y=0.4*height,anchor='ne')
        self.righttopbutton.place(x=0.9*width,y=0.4*height,anchor='ne')
        self.leftbottombutton.place(x=0.4*width,y=0.9*height,anchor='ne')
        self.rightbottombutton.place(x=0.9*width,y=0.9*height,anchor='ne')
        if self.selectiondic[self.selection][0]==0:
            self.lefttopbutton.place_forget()
        if self.selectiondic[self.selection][1]==0:
            self.righttopbutton.place_forget()
        if self.selectiondic[self.selection][2]==0:
            self.leftbottombutton.place_forget()
        if self.selectiondic[self.selection][3]==0:
            self.rightbottombutton.place_forget()
        
        
        if self.selectiondic[self.selection][0]!=0:
            im1=Image.open(f'{os.getcwd()}/questions/q%s.png'%str(self.selectiondic[self.selection][0]))
            photo1= ImageTk.PhotoImage(im1.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
            self.lefttopcanvas.create_image(0,0,anchor='nw',image = photo1)
            
        if self.selectiondic[self.selection][1]!=0:
            im2=Image.open(f'{os.getcwd()}/questions/q%s.png'%str(self.selectiondic[self.selection][1]))
            photo2= ImageTk.PhotoImage(im2.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
            self.righttopcanvas.create_image(0,0,anchor='nw',image = photo2)
        
        if self.selectiondic[self.selection][2]!=0:
            im3=Image.open(f'{os.getcwd()}/questions/q%s.png'%str(self.selectiondic[self.selection][2]))
            photo3= ImageTk.PhotoImage(im3.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
            self.leftbottomcanvas.create_image(0,0,anchor='nw',image = photo3)
            
        if self.selectiondic[self.selection][3]!=0:
            im4=Image.open(f'{os.getcwd()}/questions/q%s.png'%str(self.selectiondic[self.selection][3]))
            photo4= ImageTk.PhotoImage(im4.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
            self.rightbottomcanvas.create_image(0,0,anchor='nw',image = photo4)
        win.mainloop()
    
    
    
    
    def rookiequestions(self):
        self.selection='rookie'
        self.noticelable.place_forget()
        self.showmultiquestions()
        
    def primaryquestions(self):
        self.selection='primary'
        self.noticelable.place_forget()
        self.showmultiquestions()
    
    def normalquestions(self):
        self.selection='normal'
        self.noticelable.place_forget()
        self.showmultiquestions()
    
    def hardquestions(self):
        self.selection='hard'
        self.noticelable.place_forget()
        self.showmultiquestions()
    
    def challengequestions(self):
        self.selection='challenge'
        self.noticelable.place_forget()
        self.showmultiquestions()
    
    def showinstructionframe(self):
        self.noticelable.place_forget()
        try:
            self.multiquestionframe.place_forget()
        except:
            pass
        try:
            self.freesearchframe.place_forget()
        except:
            pass
        self.instructionframe.place(x=0.3*width,y=0.1*height)
        self.instructionlable.place(x=0,y=0.52*height,anchor='nw')
        self.instructiongobutton.place(x=0.2*width,y=0.6*height)
        im=Image.open(f'{os.getcwd()}/questions/instructionq.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.5*width),int(0.5*height)),Image.ANTIALIAS))
        self.instructioncanvas.create_image(0,0,anchor='nw',image = photo)
        win.mainloop()
        
    def showfreesearchframe(self):
        try:
            self.instructionframe.place_forget()
        except:
            pass
        try:
            self.multiquestionframe.place_forget()
        except:
            pass
        
        self.freesearchframe=FREESEARCH(self,height=height,width=width)
        self.freesearchframe.place(x=0.2*width,y=0.05*height)
        
        global evaluation,tp2
        try:
            evaluation=EVALUATION(tp2,height=0.1*height,width=0.35*width)
            evaluation.place(x=0.62*width,y=0.5*height,anchor='nw')
            evaluation.bind()
        except:
            pass


    def chuti(self):
        
        global questionsymbol
        questionsymbol='同济官方_%s'%self.questionnum
        zdyallfunction.questionsymbol=questionsymbol
        global gangdu,newquestion,rightanswerquestion
        newquestion=1
        rightanswerquestion=0
        ts = time.time()
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        zdyallfunction.starttime=dt
        #        questionsymbol='Tongji_11'
        text2.delete('0.0','end')
        zdyallfunction.jys=[]
        zdyallfunction.xys=[]
        zdyallfunction.scxys=[]
        c1.ufocus=0
        zdyallfunction.switchbjg=0
        lb1.delete(0,'end')
        
        gangdu=[]
        zdyallfunction.daduan=0
        zdyallfunction.duandian=[]
        
        zdyallfunction.getquestion(questionsymbol)
        zdyallfunction.fileinelements()
        zdyallfunction.file()
        zdyallfunction.calculation()
        im=Image.open(f'{os.getcwd()}/questions/q%s.png'%self.questionnum)
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        c3.create_image(0,0,anchor='nw',image = photo)
        global smallest_index
        smallest_index=-1
        global gjxx
        gjxx=[]
        for i in range(len(zdyallfunction.calelements)):
            num=zdyallfunction.calelements[i]['num']
            EA=zdyallfunction.calelements[i]['EA']
            l=zdyallfunction.calelements[i]['l']
            if zdyallfunction.calelements[i]['EA']>=1e8:
                EA=-1
            else:
                EA=zdyallfunction.calelements[i]['EA']
            if zdyallfunction.calelements[i]['EI']>=1e6:
                EI=-1
            else:
               EI=zdyallfunction.calelements[i]['EI'] 
            gjxx_='  杆件（%d）L=%d  EA=%d EI=%d'%(num,l,EA,EI)
            gjxx.append(gjxx_)
        lb1.delete(0,'end')
        for information in gjxx:
            lb1.insert('end',information)
        for i in range(len(zdyallfunction.elements)):
            zdyallfunction.duandian.append([0,1])
        zdyallfunction.drawuserM(smallest_index)
        c1.relativeposition()
        zdyallfunction.createanswers()
        if zdyallfunction.timutishifangshi!="自定义提示":
            zdyallfunction.bianbiedcx()
            zdyallfunction.bianbietixing()
        self.withdraw()
        global tp2
        tp2.deiconify()
        c1.showuserM()
        win.mainloop()



class QuestionCard(tkinter.Frame):
    """
    展示单个题目与跳转做题页面按钮的卡片
    qid用1.button传递的参数2.显示在线查询数据库后的题目（为你推荐、搜索模块）
    """
    def __init__(self,master,img,qid='',description='题目描述',imagePath='',iw=420,ih=260,**kw):
        """
        :para img:使用PIL已打开的图片\n
        :para qid:对应数据库的basic_info表中的questionsymbol列\n
        :para iw:图片宽度image_width\n
        :para ih:图片高度 image_height 
        """
        tkinter.Frame.__init__(self,master,**kw)
        self.master = master
        self.grid()
        self.qid = qid
        self.img = img
        self.description = description
        self.imagePath = imagePath
        self.iw = int(iw)
        self.ih = int(ih)
        self.createImage()
        self.createWidgets()
#        self.bind('<<SelectQ>>', lambda e: print("test virtual event"))
    def createImage(self):
        cutImg = ImageTk.PhotoImage(self.img.resize((self.iw,self.ih)))
        lblImg = tkinter.Label(self,image=cutImg,pady=5)
        lblImg.image = cutImg
        lblImg.grid(row=0)
    def createWidgets(self):
        btnNavigator = tkinter.Button(self,text="去做题",command=lambda: self.navigateToSolution(self.qid),pady=5)
        lblDescription = tkinter.Label(self, text='出题年份：'+self.description)
        lblDescription.grid(row=1,stick=tkinter.W)
        btnNavigator.grid(row=1,stick=tkinter.E)
    def navigateToSolution(self,qid):
        print("要跳转到的题目，questionsymbol=", qid)
        kaoyantoplevel = self.winfo_toplevel()
        global questionsymbol, zuodamodeImagePath
        zuodamodeImagePath = self.imagePath
        questionsymbol =  qid
        kaoyantoplevel.event_generate('<<SelectQ>>')




class MultiPage(tkinter.Frame):
    """
    用于展示多个题目，带有翻页功能的Frame
    """
    def __init__(self, master=None, questionList=[], **kw):
        tkinter.Frame.__init__(self,master,**kw)
        self.master = master

        self.questionList = questionList

        # 题目信息列表，即questionList
        self.questionGroup = self.cutList(self.questionList, 4)
        # 当前页码
        self.current = 0
        # 总页数
        self.total = len(self.questionGroup)
        # 页数指示变量
        self.info = tkinter.StringVar(self,value="第 {} 页/共 {} 页".format(self.current+1, self.total))
        
        self.pack(fill=tkinter.BOTH,expand=True)
        self.createWidgets()
        self.load(self.current)
        #self.bind('<<SelectQ>>', lambda e: print("test virtual event"))

    def cutList(self, init_list, childern_list_len):
        '''
        将列表元素按若干个一组分组，若不能正好分完，则剩余的单独一组
        init_list为初始化的列表，childern_list_len初始化列表中的几个数据组成一个小列表
        :param init_list:需要切割的列表
        :param childern_list_len:子列表长度
        :return:
        '''
        list_of_group = zip(*(iter(init_list),) *childern_list_len)
        end_list = [list(i) for i in list_of_group]
        count = len(init_list) % childern_list_len
        end_list.append(init_list[-count:]) if count !=0 else end_list
        return end_list
    def createWidgets(self):
        self.frmContent = tkinter.Frame(self,pady=10)
        self.frmFooter = tkinter.Frame(self,pady=10)
        self.frmContent.pack(fill=tkinter.BOTH, expand=True)
        self.frmFooter.pack(fill=tkinter.BOTH)
        # textvariable绑定至StringVar
        lblInfo = tkinter.Label(self.frmFooter,textvariable=self.info)
        
        tkinter.Button(self.frmFooter,text='上一页',command=self.previous).pack(side=tkinter.LEFT,expand=True)
        lblInfo.pack(side=tkinter.LEFT,expand=True)
        tkinter.Button(self.frmFooter,text='下一页',command=self.next).pack(side=tkinter.RIGHT,expand=True)
    def load(self, index):
        """
        读取并加载新的题目页，包含4道题
        :param index: 当前页数，从0开始计 
        """
        # 在布局前需要清除fram所有子元素
        for child in self.frmContent.winfo_children():
            child.destroy()

        qList = self.questionGroup[index]
        # 待生成的卡片列表
        cardList = []
        for item in qList:
            print("item",item)
            # 在这里打开并读取图片文件
            img = Image.open(item['path'])
            qid = item['qid']
            card = QuestionCard(self.frmContent, img=img, qid=qid, description=item['description'],imagePath=item['path'],iw=0.4*width, ih=0.4*height)
            cardList.append(card)
        cardList[0].grid(column=0,row=0,padx=5,pady=5)
        cardList[1].grid(column=1,row=0,padx=5,pady=5)
        cardList[2].grid(column=0,row=1,padx=5,pady=5)
        cardList[3].grid(column=1,row=1,padx=5,pady=5)

    def previous(self):
        """
        向前翻页
        """
        # 异常处理
        if self.current == 0:
            tkinter.messagebox.showerror(title="错误",message="已经是第一页")
        else:
            self.current = self.current - 1
        # 更新页码指示变量
        self.info.set("第 {} 页/共 {} 页".format(self.current+1, self.total))
        self.load(self.current)
    def next(self):
        """
        向后翻页
        """
        if self.current == self.total - 1:
            tkinter.messagebox.showerror(title="错误",message="已经是最后一页")
        else:
            self.current = self.current + 1
        self.info.set("第 {} 页/共 {} 页".format(self.current+1, self.total))
        self.load(self.current)




class QuestionChoice(tkinter.Frame):
    def __init__(self,master=None,**kw):
        tkinter.Frame.__init__(self,master,**kw)
        self.master = master
        self.master.geometry('%dx%d+%d+%d'%(1.6*0.8*sh,0.8*sh,0.1*sw,0.1*sh))
        self.questionList = self.readFile()
        # 初始化组件
        self.pack(fill=tkinter.BOTH, expand=True)
        self.createWidgets()
        #self.bind('<<SelectQ>>', lambda e: print("test virtual event"))

    def createWidgets(self):
        # 字体元组，用于设置字体
        self.fontTitle = ("微软雅黑", 20,"bold")
        self.fontContent = ("宋体", 12, "normal")
        # Frame布局
        # frmContainer = tkinter.Frame(self, highlightbackground="red",highlightthickness=0)
        frmContentL = tkinter.Frame(self)
        frmContentR = tkinter.Frame(self, highlightbackground="yellow",highlightthickness=0)
        frmHeader = tkinter.Frame(frmContentL, highlightbackground="blue",highlightthickness=0)
        frmHeader.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        frmFooter = tkinter.Frame(frmContentL, highlightbackground="#46dc52",highlightthickness=0)
        frmFooter.pack(fill=tkinter.BOTH, side=tkinter.BOTTOM)
        frmChangePage = tkinter.Frame(frmContentR, highlightbackground="blue",highlightthickness=0)
        frmChangePage.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        # frmContainer.pack(fill=tkinter.BOTH, expand=True)
        frmContentL.pack(fill=tkinter.Y,side=tkinter.LEFT)
        frmContentR.pack(fill=tkinter.BOTH,side=tkinter.RIGHT,expand=True)
        
        # 标题
#        tkinter.Label(
#            frmHeader,
#            height=2,
#            text="题目选择", 
#            font=self.fontTitle
#            ).pack(
#                pady=20
#                )
#        
#        tkinter.Label(
#            frmContentL, 
#            text="右边是题目预览\n点击题目下方的‘去作答’\n即可开始作答\n点击‘上一页’、‘下一页’可以翻页", 
#            font=self.fontContent
#            ).pack(
#                pady=20
#                )
#        tkinter.Label(
#            frmFooter,
#            text="点击“返回”，回到专题选择界面",
#            font=self.fontContent
#            ).pack(
#                pady=20
#                )
        btnBack = tkinter.Button(
            frmFooter,
            text="返回",
            command=self.moveformer
            )
        btnBack.pack(
            side=tkinter.LEFT,
            padx=10,
            pady=10
            )
        
        # 布局右侧Frame，调用了MultiPage组件        
        frmQuestion = MultiPage(frmContentR, questionList=self.questionList)
        frmQuestion.pack(fill=tkinter.BOTH,side=tkinter.RIGHT,expand=True)
    
    def readFile(self):
        # 从kaoyan文件夹中读取文件生成列表
        dir = ''
        questionList = []
        for dir,dir_abs,files in os.walk(dir):
            for file in files:
                path = os.path.join(dir,file)
                filename = file.split('.')[0]
                qid = '同济考研真题_' + filename.split('-')[0][1:] #截取文件名中'q1.png'.之前的文件名并去除前缀q
                years = filename.split('-')[1]
                questionList.append({'qid':qid, 'path':path, 'description':years})
        return questionList

    def close(self):
        # 关闭当前Frame，但窗口保留
        self.destroy()
    def forward(self):
        self.close()
        # 打开做题目窗口

    def moveformer(self):
        global tp2
        try:
            tp2.destroy()
        except:
            pass
        self.master.destroy()
        modechoice()
# 两个继承类, 考研和期末的差异可以在这里实现
# 目前这里只通过重写readFIle方法实现读取不同文件夹里的图片
class KaoYanQuestionChoice(QuestionChoice):
    def __init__(self,master=None,**kw):
        QuestionChoice.__init__(self,master,**kw)
    def readFile(self):
        # 从kaoyan文件夹中读取文件生成列表
        dir = f'{os.getcwd()}\\questions\\kaoyan\\'
        questionList = []
        for dir,dir_abs,files in os.walk(dir):
            for file in files:
                path = os.path.join(dir,file)
                filename = file.split('.')[0]
#                print('filename',filename)
                qid = '同济考研真题_' + filename.split('-')[0][1:] #截取文件名中'q1.png'.之前的文件名并去除前缀q
                years = filename.split('-')[1]
                questionList.append({'qid':qid, 'path':path, 'description':years})
        return questionList
class QiMoQuestionChoice(QuestionChoice):
    def __init__(self,master=None,**kw):
        QuestionChoice.__init__(self,master,**kw)
    def readFile(self):
        # 从kaoyan文件夹中读取文件生成列表
        dir = f'{os.getcwd()}\\questions\\qimo\\'
        questionList = []
        for dir,dir_abs,files in os.walk(dir):
            for file in files:
                path = os.path.join(dir,file)
                qid = '同济期末真题_' + file.split('.')[0][1:10] #截取文件名中'q1.png'.之前的文件名并去除前缀q
                questionList.append({'qid':qid, 'path':path})
        return questionList



class KaoyanToplevel(tkinter.Toplevel):
    def __init__(self, master=None, **kw):
        tkinter.Toplevel.__init__(self, master, **kw)
        self.questionnum = 3
        kaoyan = KaoYanQuestionChoice(self)
        self.bind('<<SelectQ>>', self.chuti)

    def chuti(self, event):
        # print(event.widget.qid)
        # global questionsymbol
        # questionsymbol = '同济官方_%s' % self.questionnum
        print("questionsymbol",questionsymbol)
        self.questionnum = questionsymbol.split('_',1)[-1]
        zdyallfunction.questionsymbol = questionsymbol
        global gangdu, newquestion, rightanswerquestion
        newquestion = 1
        rightanswerquestion = 0
        ts = time.time()
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        zdyallfunction.starttime = dt
        #        questionsymbol='Tongji_11'
        text2.delete('0.0', 'end')
        zdyallfunction.jys = []
        zdyallfunction.xys = []
        zdyallfunction.scxys = []
        c1.ufocus = 0
        zdyallfunction.switchbjg = 0
        lb1.delete(0, 'end')

        gangdu = []
        zdyallfunction.daduan = 0
        zdyallfunction.duandian = []

        zdyallfunction.getquestion(questionsymbol)
        zdyallfunction.fileinelements()
        zdyallfunction.file()
        zdyallfunction.calculation()
        im = Image.open(zuodamodeImagePath)
        photo = ImageTk.PhotoImage(im.resize((wp, hp), Image.ANTIALIAS))
        c3.create_image(0, 0, anchor='nw', image=photo)
        global smallest_index
        smallest_index = -1
        global gjxx
        gjxx = []
        for i in range(len(zdyallfunction.calelements)):
            num = zdyallfunction.calelements[i]['num']
            EA = zdyallfunction.calelements[i]['EA']
            l = zdyallfunction.calelements[i]['l']
            if zdyallfunction.calelements[i]['EA'] >= 1e8:
                EA = -1
            else:
                EA = zdyallfunction.calelements[i]['EA']
            if zdyallfunction.calelements[i]['EI'] >= 1e6:
                EI = -1
            else:
               EI = zdyallfunction.calelements[i]['EI']
            gjxx_ = '  杆件（%d）L=%d  EA=%d EI=%d' % (num, l, EA, EI)
            gjxx.append(gjxx_)
        lb1.delete(0, 'end')
        for information in gjxx:
            lb1.insert('end', information)
        for i in range(len(zdyallfunction.elements)):
            zdyallfunction.duandian.append([0, 1])
        zdyallfunction.drawuserM(smallest_index)
        c1.relativeposition()
        zdyallfunction.createanswers()
        if zdyallfunction.timutishifangshi != "自定义提示":
            zdyallfunction.bianbiedcx()
            zdyallfunction.bianbietixing()
        self.withdraw()
        global tp2
        tp2.deiconify()
        c1.showuserM()
        win.mainloop()






class HELPTOPLEVEL(tkinter.Toplevel):
    def __init__(self,master=None,name=None,ratio=None,picturename=None,message=None,dx=(sw-width)/2,dy=(sh-height*1.05)/2,**kw):
        tkinter.Toplevel.__init__(self,master,**kw)
        self.name=name
        self.ratio=ratio
        self.picturename=picturename
        self.title('%s'%self.name)
        self.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.geometry('%dx%d+%d+%d'%(0.5*width,int(0.5*width/ratio),dx,dy))
        self.message=message
        self.resizable(0,0)



    def bind(self):
        self.canvas=tkinter.Canvas(self,height=int(0.5*width/self.ratio),width=0.5*width)
        im=Image.open(f'{os.getcwd()}/help/%s'%self.picturename)
        photo = ImageTk.PhotoImage(im.resize((int(0.5*width),int(0.5*width/self.ratio)),Image.ANTIALIAS))
        self.canvas.create_image(0,0,anchor='nw',image = photo)
        self.canvas.place(x=0,y=0,anchor='nw')
        if self.message!=None:
            def shownextstep():
                self.destroy()
                tkinter.messagebox.showinfo(title='下一步', message='%s'%self.message)
            self.protocol("WM_DELETE_WINDOW",shownextstep)
        
        win.mainloop()


class EVALUATION(tkinter.Frame):
    def __init__(self,master=None,**kw):
        tkinter.Frame.__init__(self,master,**kw)
        
        
    def bind(self):
        
        
        self.thumbcanvas=tkinter.Canvas(self,height=0.1*height,width=0.1*height)
        im2=Image.open(f'{os.getcwd()}/infor/nothumb1.png') 
        photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
        self.thumbcanvas.create_image(0,0,anchor='nw',image = photo2)
        self.thumbstate=0
        self.thumbcanvas.bind("<Button-1>", self.changethumb) 
        
        
        self.badpostcanvas=tkinter.Canvas(self,height=0.1*height,width=0.1*height)
        im3=Image.open(f'{os.getcwd()}/infor/nobadpost.jpg') 
        photo3 = ImageTk.PhotoImage(im3.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
        self.badpostcanvas.create_image(0,0,anchor='nw',image = photo3)
        self.badpoststate=0
        self.badpostcanvas.bind("<Button-1>", self.changebadpost) 
        
        
        self.starlable=tkinter.Label(self,text='难度评分:',font=('微软雅黑',10))
        self.canvas=tkinter.Canvas(self,height=0.1*height,width=int(2.446*0.1*height))
        im=Image.open(f'{os.getcwd()}/infor/nostar.png')
        photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
        self.canvas.create_image(0,0,anchor='nw',image = photo)
        
        
        
        self.thumbcanvas.place(x=0,y=0,anchor='nw')
        self.badpostcanvas.place(x=0.1*height,y=0,anchor='nw')
        
        self.canvas.bind("<Button-1>", self.showstar) 
        
        self.starlable.place(x=0.3*height,y=0.05*height,anchor='ne')
        self.canvas.place(x=0.3*height,y=0,anchor='nw')
        win.mainloop()
    
    
    
    
    def changebadpost(self,event):
        if self.badpoststate==0:
            self.badpoststate=1
            self.badpostcanvas.delete('all')
            im3=Image.open(f'{os.getcwd()}/infor/yesbadpost.jpg') 
            photo3 = ImageTk.PhotoImage(im3.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
            self.badpostcanvas.create_image(0,0,anchor='nw',image = photo3)
            
            if self.thumbstate==1:
                self.thumbstate=0
                self.thumbcanvas.delete('all')
                im2=Image.open(f'{os.getcwd()}/infor/nothumb1.png') 
                photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
                self.thumbcanvas.create_image(0,0,anchor='nw',image = photo2)
            
            
                        
            
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="select * from thumbs_up where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
            cursor.execute(sql)
            result=cursor.fetchone()
            if (result==None):
                sql="insert into thumbs_up values('%s','%s','-1')"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
                cursor.execute(sql)
                sql="update basic_questioninfor set badpost=badpost+1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
            else:
                if result[2]==-1:
                    conn.commit()
                    cursor.close()
                    conn.close()
                elif result[2]==0:
                    sql="update thumbs_up set thumbup=-1 where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
                    cursor.execute(sql)
                    sql="update basic_questioninfor set badpost=badpost+1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    conn.close()
                elif result[2]==1:
                    sql="update thumbs_up set thumbup=-1 where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
                    cursor.execute(sql)
                    sql="update basic_questioninfor set badpost=badpost+1,thumbs=thumbs-1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
        elif self.badpoststate==1:
            self.badpoststate=0
            self.badpostcanvas.delete('all')
            im3=Image.open(f'{os.getcwd()}/infor/nobadpost.jpg') 
            photo3 = ImageTk.PhotoImage(im3.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
            self.badpostcanvas.create_image(0,0,anchor='nw',image = photo3)
                        
            
            
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="select * from thumbs_up where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
            cursor.execute(sql)
            result=cursor.fetchone()
            sql="update thumbs_up set thumbup=0 where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
            cursor.execute(sql)
            sql="update basic_questioninfor set badpost=badpost-1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()

            
                    
            
        win.mainloop()
            
    
    def changethumb(self,event):
        if self.thumbstate==0:
            self.thumbstate=1
            self.thumbcanvas.delete('all')
            im2=Image.open(f'{os.getcwd()}/infor/yesthumb1.png') 
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
            self.thumbcanvas.create_image(0,0,anchor='nw',image = photo2)
            
            if self.badpoststate==1:
                self.badpoststate=0
                self.badpostcanvas.delete('all')
                im3=Image.open(f'{os.getcwd()}/infor/nobadpost.jpg') 
                photo3 = ImageTk.PhotoImage(im3.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
                self.badpostcanvas.create_image(0,0,anchor='nw',image = photo3)

            
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="select * from thumbs_up where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
            cursor.execute(sql)
            result=cursor.fetchone()
            if (result==None):
                sql="insert into thumbs_up values('%s','%s','1')"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
                cursor.execute(sql)
                sql="update basic_questioninfor set thumbs=thumbs+1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
            else:
                if result[2]==1:
                    conn.commit()
                    cursor.close()
                    conn.close()
                elif result[2]==0:
                    sql="update thumbs_up set thumbup=1 where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
                    cursor.execute(sql)
                    sql="update basic_questioninfor set thumbs=thumbs+1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    conn.close()
                elif result[2]==-1:
                    sql="update thumbs_up set thumbup=1 where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
                    cursor.execute(sql)
                    sql="update basic_questioninfor set thumbs=thumbs+1,badpost=badpost-1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    conn.close()
#                    

            
            
        elif self.thumbstate==1:
            self.thumbstate=0
            self.thumbcanvas.delete('all')
            im2=Image.open(f'{os.getcwd()}/infor/nothumb1.png') 
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
            self.thumbcanvas.create_image(0,0,anchor='nw',image = photo2)
            
            
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update thumbs_up set thumbup=0 where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
            cursor.execute(sql)
            sql="update basic_questioninfor set thumbs=thumbs-1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
#            
        win.mainloop()
            
            
    
    
    def showstar(self,event):
        x1=event.x
        y1=event.y
        
        def difficultyevaluation(x):
            num=int(x)
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="select * from difficulties_record where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
            cursor.execute(sql)
            result=cursor.fetchone()
            if (result==None):
                sql="select count(*) from difficulties_record where questionsymbol='%s'"%(zdyallfunction.questionsymbol)
                cursor.execute(sql)
                frequency=int(cursor.fetchone()[0])
                print(frequency)
                sql="insert into difficulties_record values('%s','%s','%d')"%(zdyallfunction.userID,zdyallfunction.questionsymbol,num)
                cursor.execute(sql)
                sql="update basic_questioninfor set difficulty=(difficulty*%d+%d)/(%d+1) where questionsymbol='%s'"%(frequency,num,frequency,zdyallfunction.questionsymbol)
                cursor.execute(sql)
                
                sql="update achievements set honorcredits=honorcredits+5 where userID='%s'"%zdyallfunction.userID
                cursor.execute(sql)
                sql="update achievements set honorcredits=honorcredits+5 where userID='%s'"%(zdyallfunction.questionsymbol.split('_')[0])
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                global achievement
                achievement.honorcreditslable['text']=int(achievement.honorcreditslable['text'])+5

            else:
                sql="select count(*) from difficulties_record where questionsymbol='%s'"%(zdyallfunction.questionsymbol)
                cursor.execute(sql)
                frequency=int(cursor.fetchone()[0])
                sql="select difficulty from difficulties_record where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
                cursor.execute(sql)
                formerdifficulty=int(cursor.fetchone()[0])
                sql="update difficulties_record set difficulty=%d where userID='%s' and questionsymbol='%s'"%(num,zdyallfunction.userID,zdyallfunction.questionsymbol)
                cursor.execute(sql)
                sql="update basic_questioninfor set difficulty=(difficulty*%d-%d+%d)/%d where questionsymbol='%s'"%(frequency,formerdifficulty,num,frequency,zdyallfunction.questionsymbol)
                print(sql)
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
        
        
        if x1/self.canvas.winfo_width()<0.2:
            self.canvas.delete('all')
            im=Image.open(f'{os.getcwd()}/infor/onestar.png')
            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
            self.canvas.create_image(0,0,anchor='nw',image = photo)
            difficultyevaluation(1)
            win.mainloop()
        elif x1/self.canvas.winfo_width()>=0.2 and x1/self.canvas.winfo_width()<0.4:
            self.canvas.delete('all')
            im=Image.open(f'{os.getcwd()}/infor/twostar.png')
            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
            self.canvas.create_image(0,0,anchor='nw',image = photo)
            difficultyevaluation(2)
            win.mainloop()
        elif x1/self.canvas.winfo_width()>=0.4 and x1/self.canvas.winfo_width()<0.6:
            self.canvas.delete('all')
            im=Image.open(f'{os.getcwd()}/infor/threestar.png')
            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
            self.canvas.create_image(0,0,anchor='nw',image = photo)
            difficultyevaluation(3)
            win.mainloop()
        elif x1/self.canvas.winfo_width()>=0.6 and x1/self.canvas.winfo_width()<0.8:
            self.canvas.delete('all')
            im=Image.open(f'{os.getcwd()}/infor/fourstar.png')
            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
            self.canvas.create_image(0,0,anchor='nw',image = photo)
            difficultyevaluation(4)
            win.mainloop()
        elif x1/self.canvas.winfo_width()>=0.8 and x1/self.canvas.winfo_width()<1:
            self.canvas.delete('all')
            im=Image.open(f'{os.getcwd()}/infor/fivestar.png')
            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
            self.canvas.create_image(0,0,anchor='nw',image = photo)
            difficultyevaluation(5)

                
            
            
            win.mainloop()







#class EVALUATION(tkinter.Frame):
#    def __init__(self,master=None,**kw):
#        tkinter.Frame.__init__(self,master,**kw)
#        
#        
#    def bind(self):
#        
#        
#        self.thumbcanvas=tkinter.Canvas(self,height=0.1*height,width=0.1*height)
#        im2=Image.open(f'{os.getcwd()}/infor/nothumb1.png') 
#        photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
#        self.thumbcanvas.create_image(0,0,anchor='nw',image = photo2)
#        self.thumbstate=0
#        self.thumbcanvas.bind("<Button-1>", self.changethumb) 
#        
#        self.starlable=tkinter.Label(self,text='难度评分:',font=('微软雅黑',10))
#        self.canvas=tkinter.Canvas(self,height=0.1*height,width=int(2.446*0.1*height))
#        im=Image.open(f'{os.getcwd()}/infor/nostar.png')
#        photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
#        self.canvas.create_image(0,0,anchor='nw',image = photo)
#        
#        
#        
#        self.thumbcanvas.place(x=0,y=0,anchor='nw')
#        self.canvas.bind("<Button-1>", self.showstar) 
#        self.starlable.place(x=0.12*width,y=0.05*height,anchor='ne')
#        self.canvas.place(x=0.12*width,y=0,anchor='nw')
#        win.mainloop()
#    
#    
#    def changethumb(self,event):
#        if self.thumbstate==0:
#            self.thumbstate=1
#            self.thumbcanvas.delete('all')
#            im2=Image.open(f'{os.getcwd()}/infor/yesthumb1.png') 
#            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
#            self.thumbcanvas.create_image(0,0,anchor='nw',image = photo2)
#            
#            
#            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
#            cursor = conn.cursor()
#            sql="select * from thumbs_up where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
#            cursor.execute(sql)
#            result=cursor.fetchone()
#            if (result==None):
#                sql="insert into thumbs_up values('%s','%s','1')"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
#                cursor.execute(sql)
#                sql="update basic_questioninfor set thumbs=thumbs+1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
#                cursor.execute(sql)
#                conn.commit()
#                cursor.close()
#                conn.close()
#            else:
#                if result[2]==1:
#                    conn.commit()
#                    cursor.close()
#                    conn.close()
#                elif result[2]==0:
#                    sql="update thumbs_up set thumbup=1 where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
#                    cursor.execute(sql)
#                    sql="update basic_questioninfor set thumbs=thumbs+1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
#                    cursor.execute(sql)
#                    conn.commit()
#                    cursor.close()
#                    conn.close()
#                    
#
#            
#            
#            win.mainloop()
#        elif self.thumbstate==1:
#            self.thumbstate=0
#            self.thumbcanvas.delete('all')
#            im2=Image.open(f'{os.getcwd()}/infor/nothumb1.png') 
#            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*height),int(0.1*height)),Image.ANTIALIAS))
#            self.thumbcanvas.create_image(0,0,anchor='nw',image = photo2)
#            
#            
#            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
#            cursor = conn.cursor()
#            sql="update thumbs_up set thumbup=0 where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
#            cursor.execute(sql)
#            sql="update basic_questioninfor set thumbs=thumbs-1 where questionsymbol='%s'"%zdyallfunction.questionsymbol
#            cursor.execute(sql)
#            conn.commit()
#            cursor.close()
#            conn.close()
#            
#            win.mainloop()
#            
#            
#    
#    
#    def showstar(self,event):
#        x1=event.x
#        y1=event.y
#        
#        def difficultyevaluation(x):
#            num=int(x)
#            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
#            cursor = conn.cursor()
#            sql="select * from difficulties_record where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
#            cursor.execute(sql)
#            result=cursor.fetchone()
#            if (result==None):
#                sql="select count(*) from difficulties_record where questionsymbol='%s'"%(zdyallfunction.questionsymbol)
#                cursor.execute(sql)
#                frequency=int(cursor.fetchone()[0])
#                print(frequency)
#                sql="insert into difficulties_record values('%s','%s','%d')"%(zdyallfunction.userID,zdyallfunction.questionsymbol,num)
#                cursor.execute(sql)
#                sql="update basic_questioninfor set difficulty=(difficulty*%d+%d)/(%d+1) where questionsymbol='%s'"%(frequency,num,frequency,zdyallfunction.questionsymbol)
#                cursor.execute(sql)
#                
#                sql="update achievements set honorcredits=honorcredits+5 where userID='%s'"%zdyallfunction.userID
#                cursor.execute(sql)
#                sql="update achievements set honorcredits=honorcredits+5 where userID='%s'"%(zdyallfunction.questionsymbol.split('_')[0])
#                cursor.execute(sql)
#                conn.commit()
#                cursor.close()
#                conn.close()
#                global achievement
#                achievement.honorcreditslable['text']=int(achievement.honorcreditslable['text'])+5
#
#            else:
#                sql="select count(*) from difficulties_record where questionsymbol='%s'"%(zdyallfunction.questionsymbol)
#                cursor.execute(sql)
#                frequency=int(cursor.fetchone()[0])
#                print(frequency)
#                sql="select difficulty from difficulties_record where userID='%s' and questionsymbol='%s'"%(zdyallfunction.userID,zdyallfunction.questionsymbol)
#                cursor.execute(sql)
#                formerdifficulty=int(cursor.fetchone()[0])
#                print(formerdifficulty)
#                sql="update difficulties_record set difficulty=%d where userID='%s' and questionsymbol='%s'"%(num,zdyallfunction.userID,zdyallfunction.questionsymbol)
#                cursor.execute(sql)
#                sql="update basic_questioninfor set difficulty=(difficulty*%d-%d+%d)/%d where questionsymbol='%s'"%(frequency,formerdifficulty,num,frequency,zdyallfunction.questionsymbol)
#                print(sql)
#                cursor.execute(sql)
#                conn.commit()
#                cursor.close()
#                conn.close()
#        
#        
#        if x1/self.canvas.winfo_width()<0.2:
#            self.canvas.delete('all')
#            im=Image.open(f'{os.getcwd()}/infor/onestar.png')
#            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
#            self.canvas.create_image(0,0,anchor='nw',image = photo)
#            difficultyevaluation(1)
#            win.mainloop()
#        elif x1/self.canvas.winfo_width()>=0.2 and x1/self.canvas.winfo_width()<0.4:
#            self.canvas.delete('all')
#            im=Image.open(f'{os.getcwd()}/infor/twostar.png')
#            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
#            self.canvas.create_image(0,0,anchor='nw',image = photo)
#            difficultyevaluation(2)
#            win.mainloop()
#        elif x1/self.canvas.winfo_width()>=0.4 and x1/self.canvas.winfo_width()<0.6:
#            self.canvas.delete('all')
#            im=Image.open(f'{os.getcwd()}/infor/threestar.png')
#            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
#            self.canvas.create_image(0,0,anchor='nw',image = photo)
#            difficultyevaluation(3)
#            win.mainloop()
#        elif x1/self.canvas.winfo_width()>=0.6 and x1/self.canvas.winfo_width()<0.8:
#            self.canvas.delete('all')
#            im=Image.open(f'{os.getcwd()}/infor/fourstar.png')
#            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
#            self.canvas.create_image(0,0,anchor='nw',image = photo)
#            difficultyevaluation(4)
#            win.mainloop()
#        elif x1/self.canvas.winfo_width()>=0.8 and x1/self.canvas.winfo_width()<1:
#            self.canvas.delete('all')
#            im=Image.open(f'{os.getcwd()}/infor/fivestar.png')
#            photo = ImageTk.PhotoImage(im.resize((int(2.446*0.1*height),int(0.1*height)),Image.ANTIALIAS))
#            self.canvas.create_image(0,0,anchor='nw',image = photo)
#            difficultyevaluation(5)
#
#                
#            
#            
#            win.mainloop()






class RANKTREE(ttk.Treeview):
        def __init__(self,master=None,**kw):
            ttk.Treeview.__init__(self,master,**kw)
            self.engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
            self.page=0
            self.geshu=10
            self.searchway=-1
            s = ttk.Style()
            s.configure('Treeview', rowheight=int(50/1800*sh),font=('微软雅黑',9))
            sql="select a.* ,@rank:=@rank + 1 AS rank_no from (select achievements.*,basic_infor.school from basic_infor, achievements where basic_infor.userID=achievements.userID and basic_infor.school='%s' ORDER BY `levelcredits` DESC ) as a,(SELECT @rank:= 0) as b limit 10"%zdyallfunction.school
            self.df=pd.read_sql_query(sql, self.engine)
            sql="select count(*) from basic_infor, achievements where basic_infor.userID=achievements.userID and basic_infor.school='%s' ORDER BY `levelcredits` DESC "%zdyallfunction.school
            temp=pd.read_sql_query(sql, self.engine)
            self.num=temp.iloc[0,0]
            print(self.df)
            for i in range(len(self.df)):
                tt=[]
                tt.append(self.df.loc[i,'userID'])
                tt.append(self.df.loc[i,'school'])
                tt.append(self.df.loc[i,'levelcredits'])
                tt.append(self.df.loc[i,'honorcredits'])
                tt.append(int(self.df.loc[i,'rank_no']))
                tt=tuple(tt)
                self.insert('',i,values=tt)
        
        def altergeshu(self,x):
            self.geshu=x
        def delself(self):
            x=self.get_children()
            for item in x:
                self.delete(item)
        def showinfor(self):
            for i in range(len(self.df)):
                tt=[]
                tt.append(self.df.loc[i,'userID'])
                tt.append(self.df.loc[i,'school'])
                tt.append(self.df.loc[i,'levelcredits'])
                tt.append(self.df.loc[i,'honorcredits'])
                tt.append(int(self.df.loc[i,'rank_no']))
                tt=tuple(tt)
                self.insert('',i,values=tt)


class RANKINGLIST(tkinter.Toplevel):
    def __init__(self,master=None,**kw):
        tkinter.Toplevel.__init__(self,master,**kw)
        self.title('排行榜')
        self.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.geometry('%dx%d+%d+%d'%(0.5*width,height,dx,dy))
        self.engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        self.choiceframe=tkinter.Frame(self,height=0.1*height,width=0.3*width)
        self.choiceframe.place(x=0,y=0.25*width,anchor='nw')
        self.regioncmb= ttk.Combobox(self.choiceframe,width=16)
        self.regioncmb['value'] = (zdyallfunction.school,'所有人')
        self.regioncmb.current(0)
        self.rankwaycmb= ttk.Combobox(self.choiceframe,width=12)
        self.rankwaycmb['value'] = ('总等级经验值','荣誉积分')
        self.rankwaycmb.current(0)
        #self.button_qualify=tkinter.Button(self.choiceframe,text='确认',fg='red',font=('微软雅黑',10),width=10,height=1)
        
        
        
        self.regioncmb.grid(row=0,column=0)
        self.rankwaycmb.grid(row=0,column=1)
        
        self.treeframe=tkinter.Frame(self,height=0.9*height-0.25*width,width=0.3*width)
        self.treeframe.place(x=0,y=0.25*width+0.1*height,anchor='nw')
        ybar=tkinter.Scrollbar(self.treeframe,orient='vertical')
        self.tree=RANKTREE(self.treeframe,height=10,columns=('col1','col2','col3','col4','col5'),show='headings',selectmode='browse',yscrollcommand=ybar.set)
        ybar['command']=self.tree.yview
        self.tree.column('#1', width=cellwidth*2, anchor='center')
        self.tree.column('#2', width=int(cellwidth*1.5), anchor='center')
        self.tree.column('#3', width=int(cellwidth*1.5), anchor='center')
        self.tree.column('#4', width=int(cellwidth*1.5), anchor='center')
        self.tree.column('#5', width=cellwidth*2, anchor='center')
        self.tree.heading('col1', text='用户')
        self.tree.heading('col2', text='学校')
        self.tree.heading('col3', text='总等级经验值')
        self.tree.heading('col4', text='荣誉积分')
        self.tree.heading('col5', text='排行')
        
        self.tree.grid(row=0)
        ybar.grid(row=0,column=1,sticky='ns')
        
        self.myframe1=tkinter.Frame(self,height=0.1*height,width=0.5*width)
        self.myframe1.place(x=0,y=0.9*height,anchor='nw')
        self.myframe2=tkinter.Frame(self,height=0.1*height,width=0.5*width)
        self.myframe2.place(x=0.35*width,y=0.9*height,anchor='ne')


        sql="select * from (select c.*,@rank:=@rank + 1 as rank_no from (select a.`levelcredits` ,a.`honorcredits` ,`basic_infor`.* from `achievements` as a, `basic_infor` where school='%s' and a.userID=`basic_infor`.userID order by `levelcredits` desc ) as c,(SELECT @rank:= 0) as b) as d where d.userID='%s'"%(zdyallfunction.school,zdyallfunction.userID)
        self.myinfor=pd.read_sql_query(sql, self.engine)
        print(self.myinfor)
        self.mylevelcreditslable1=tkinter.Label(self.myframe1,text='我的总等级经验值：',font=('微软雅黑',10,'bold'))
        self.mylevelcreditslable2=tkinter.Label(self.myframe1,text='%s'%self.myinfor.loc[0,'levelcredits'],font=('微软雅黑',15,'bold'),fg='red')
        self.myhonorcreditslable1=tkinter.Label(self.myframe1,text='我的荣誉积分：',font=('微软雅黑',10,'bold'))
        self.myhonorcreditslable2=tkinter.Label(self.myframe1,text='%s'%self.myinfor.loc[0,'honorcredits'],font=('微软雅黑',15,'bold'),fg='red')
        self.myranklable1=tkinter.Label(self.myframe2,text='我的排名：',font=('微软雅黑',10,'bold'))
        self.myranklable2=tkinter.Label(self.myframe2,text='%s'%int(self.myinfor.loc[0,'rank_no']),font=('微软雅黑',15,'bold'),fg='red')
        self.myrankpercentagelable1=tkinter.Label(self.myframe2,text='超越用户： ',font=('微软雅黑',10,'bold'))
        self.myrankpercentagelable2=tkinter.Label(self.myframe2,text='%d'%round((self.tree.num-self.myinfor.loc[0,'rank_no']+1)/(self.tree.num)*100)+'%',font=('微软雅黑',15,'bold'),fg='red')
        #self.myrankpercentagelable3=tkinter.Label(self.myframe2,text='用户',font=('微软雅黑',10,'bold'))
        self.mylevelcreditslable1.grid(row=0,column=0)
        self.mylevelcreditslable2.grid(row=0,column=1)
        self.myhonorcreditslable1.grid(row=1,column=0)
        self.myhonorcreditslable2.grid(row=1,column=1)
        self.myranklable1.grid(row=0,column=0)
        self.myranklable2.grid(row=0,column=1)
        self.myrankpercentagelable1.grid(row=1,column=0)
        self.myrankpercentagelable2.grid(row=1,column=1)
        #self.myrankpercentagelable3.grid(row=1,column=2)
        self.resizable(0,0)
        
    
    def showaddpage(self):
        self.tree.addpage()
        
    
    
    def changerank(self,event):
        
        if self.regioncmb.get()=='所有人':
            if self.rankwaycmb.get()=='总等级经验值':
                sql="select c.*,basic_infor.school from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `levelcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID and basic_infor.userID='%s' order by c.rank_no limit 10"%zdyallfunction.userID
                self.myinfor=pd.read_sql_query(sql, self.engine)
                
                sql="select c.*,basic_infor.school from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `levelcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID order by c.rank_no limit 10"
                self.tree.df=pd.read_sql_query(sql, self.tree.engine)
                self.tree.delself()
                self.tree.showinfor()
                sql="select count(*) from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `levelcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID order by c.rank_no"
                temp=pd.read_sql_query(sql, self.tree.engine)
                self.tree.num=temp.iloc[0,0]
                self.tree.page=0
            else:
                sql="select c.*,basic_infor.school from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `honorcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID and basic_infor.userID='%s' order by c.rank_no limit 10"%zdyallfunction.userID
                self.myinfor=pd.read_sql_query(sql, self.engine)
                
                sql="select c.*,basic_infor.school from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `honorcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID order by c.rank_no limit 10"
                self.tree.df=pd.read_sql_query(sql, self.tree.engine)
                self.tree.delself()
                self.tree.showinfor()
                sql="select count(*) from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `honorcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID order by c.rank_no"
                temp=pd.read_sql_query(sql, self.tree.engine)
                self.tree.num=temp.iloc[0,0]
                self.tree.page=0
        else:
            if self.rankwaycmb.get()=='总等级经验值':
                sql="select * from (select c.*,@rank:=@rank + 1 as rank_no from (select a.`levelcredits` ,a.`honorcredits` ,`basic_infor`.* from `achievements` as a, `basic_infor` where school='%s' and a.userID=`basic_infor`.userID order by `levelcredits` desc ) as c,(SELECT @rank:= 0) as b) as d where d.userID='%s'"%(zdyallfunction.school,zdyallfunction.userID)
#                sql="select c.*,basic_infor.school from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `levelcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID and basic_infor.userID='%s' and basic_infor.school='%s' order by c.rank_no limit 10"%(zdyallfunction.userID,zdyallfunction.school)
                self.myinfor=pd.read_sql_query(sql, self.engine)
                print(self.myinfor)
                
                
                sql="select c.*,@rank:=@rank + 1 as rank_no from (select a.`levelcredits` ,a.`honorcredits` ,`basic_infor`.* from `achievements` as a, `basic_infor` where school='%s' and a.userID=`basic_infor`.userID order by `levelcredits` desc ) as c,(SELECT @rank:= 0) as b limit 10 "%zdyallfunction.school
#                sql="select a.* ,@rank:=@rank + 1 AS rank_no from (select achievements.*,basic_infor.school from basic_infor, achievements where basic_infor.userID=achievements.userID and basic_infor.school='%s' ORDER BY `levelcredits` DESC ) as a,(SELECT @rank:= 0) as b limit 10"%zdyallfunction.school
                self.tree.df=pd.read_sql_query(sql, self.tree.engine)
                self.tree.delself()
                self.tree.showinfor()
                sql="select count(*) from basic_infor, achievements where basic_infor.userID=achievements.userID and basic_infor.school='%s' ORDER BY `levelcredits` DESC "%zdyallfunction.school
                temp=pd.read_sql_query(sql, self.tree.engine)
                self.tree.num=temp.iloc[0,0]
                self.tree.page=0
            else:
                sql="select * from (select c.*,@rank:=@rank + 1 as rank_no from (select a.`levelcredits` ,a.`honorcredits` ,`basic_infor`.* from `achievements` as a, `basic_infor` where school='%s' and a.userID=`basic_infor`.userID order by `honorcredits` desc ) as c,(SELECT @rank:= 0) as b) as d where d.userID='%s'"%(zdyallfunction.school,zdyallfunction.userID)
#                sql="select c.*,basic_infor.school from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `honorcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID and basic_infor.userID='%s' order by c.rank_no limit 10"%(zdyallfunction.userID,zdyallfunction.school)
#                sql="select a.* ,@rank:=@rank + 1 AS rank_no from (select achievements.*,basic_infor.school from basic_infor, achievements where basic_infor.userID=achievements.userID and basic_infor.userID='%s' and basic_infor.school='%s' ORDER BY `honorcredits` DESC ) as a,(SELECT @rank:= 0) as b limit 10"%(zdyallfunction.userID,zdyallfunction.school)
                self.myinfor=pd.read_sql_query(sql, self.engine)
                sql="select c.*,@rank:=@rank + 1 as rank_no from (select a.`levelcredits` ,a.`honorcredits` ,`basic_infor`.* from `achievements` as a, `basic_infor` where school='%s' and a.userID=`basic_infor`.userID order by `honorcredits` desc ) as c,(SELECT @rank:= 0) as b limit 10 "%zdyallfunction.school
#                sql="select a.* ,@rank:=@rank + 1 AS rank_no from (select achievements.*,basic_infor.school from basic_infor, achievements where basic_infor.userID=achievements.userID and basic_infor.school='%s' ORDER BY `honorcredits` DESC ) as a,(SELECT @rank:= 0) as b limit 10"%zdyallfunction.school
                self.tree.df=pd.read_sql_query(sql, self.tree.engine)
                self.tree.delself()
                self.tree.showinfor()
                sql="select count(*) from basic_infor, achievements where basic_infor.userID=achievements.userID and basic_infor.school='%s' ORDER BY `levelcredits` DESC "%zdyallfunction.school
                temp=pd.read_sql_query(sql, self.tree.engine)
                self.tree.num=temp.iloc[0,0]
                self.tree.page=0
        self.myranklable2['text']='%s'%int(self.myinfor.loc[0,'rank_no'])
        self.myrankpercentagelable2['text']='%d'%round((self.tree.num-self.myinfor.loc[0,'rank_no']+1)/(self.tree.num)*100)+'%'


    def bind(self):
        
        self.button_addpage=tkinter.Button(self.choiceframe,text='下一页',fg='red',font=('微软雅黑',10),width=10,height=1,command=self.addpage)
        self.button_minuspage=tkinter.Button(self.choiceframe,text='上一页',fg='red',font=('微软雅黑',10),width=10,height=1,command=self.minuspage)
        self.button_addpage.grid(row=0,column=3)
        self.button_minuspage.grid(row=0,column=2)
        self.regioncmb.bind("<<ComboboxSelected>>",self.changerank)
        self.rankwaycmb.bind("<<ComboboxSelected>>",self.changerank)
        self.canvas=tkinter.Canvas(self,height=0.25*width,width=0.5*width)
        self.canvas.place(x=0,y=0,anchor='nw')
        im=Image.open(f'{os.getcwd()}/infor/rank.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.5*width),int(0.25*width)),Image.ANTIALIAS))
        self.canvas.create_image(0,0,anchor='nw',image = photo)
        
        
        win.mainloop()
    
    def getinfor(self):
        if self.regioncmb.get()=='所有人':
            if self.rankwaycmb.get()=='总等级经验值':
                sql="select c.*,basic_infor.school from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `levelcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID order by c.rank_no limit %d,%d"%(self.tree.page*self.tree.geshu,self.tree.geshu)
                self.tree.df=pd.read_sql_query(sql, self.tree.engine)
            else:
                sql="select c.*,basic_infor.school from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `honorcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID order by c.rank_no limit %d,%d"%(self.tree.page*self.tree.geshu,self.tree.geshu)
                self.tree.df=pd.read_sql_query(sql, self.tree.engine)
        else:
            if self.rankwaycmb.get()=='总等级经验值':
                sql="select * from (select a.* ,@rank:=@rank + 1 AS rank_no from (select achievements.*,basic_infor.school from basic_infor, achievements where basic_infor.userID=achievements.userID and basic_infor.school='%s' ORDER BY `levelcredits` DESC ) as a,(SELECT @rank:= 0) as b ) as d limit %d,%d"%(zdyallfunction.school,self.tree.page*self.tree.geshu,self.tree.geshu)
                self.tree.df=pd.read_sql_query(sql, self.tree.engine)
            else:
                #sql="select c.*,basic_infor.school from basic_infor,(select a.*,@rank:=@rank + 1 AS rank_no from (select * from `achievements` ORDER BY `honorcredits` DESC ) as a ,(SELECT @rank:= 0) as b) as c where basic_infor.userID=c.userID and basic_infor.school='%s' order by c.rank_no limit %d,%d"%(zdyallfunction.school,self.tree.page*self.tree.geshu,self.tree.geshu)
                sql="select * from (select a.* ,@rank:=@rank + 1 AS rank_no from (select achievements.*,basic_infor.school from basic_infor, achievements where basic_infor.userID=achievements.userID and basic_infor.school='%s' ORDER BY `honorcredits` DESC ) as a,(SELECT @rank:= 0) as b ) as d limit %d,%d"%(zdyallfunction.school,self.tree.page*self.tree.geshu,self.tree.geshu)
                self.tree.df=pd.read_sql_query(sql, self.tree.engine)

                
                
    def addpage(self):
        self.tree.page=self.tree.page+1
        if (self.tree.page)*self.tree.geshu>=self.tree.num:
            tkinter.messagebox.showinfo(title='提示', message='已经到尾了')
            self.tree.page=self.tree.page-1
            return
        self.tree.delself()
        self.getinfor()
        print(self.tree.df)
        self.tree.showinfor()
    
    def minuspage(self):
        if self.tree.page>0:
            self.tree.page=self.tree.page-1
            self.tree.delself()
            self.getinfor()
            self.tree.showinfor()
        else:
            tkinter.messagebox.showinfo(title='提示', message='已经到头了')
        



class RANKHELP(tkinter.Toplevel):
    def __init__(self,master=None,**kw):
        tkinter.Toplevel.__init__(self,master,**kw)
        self.title('获取经验与荣誉积分')
        self.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.geometry('%dx%d+%d+%d'%(int(0.7*width),int(0.393*width),dx,dy))
        self.canvas=tkinter.Canvas(self,height=int(0.393*width),width=int(0.7*width))
        im=Image.open(f'{os.getcwd()}/infor/rankhelp.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.7*width),int(0.393*width)),Image.ANTIALIAS))
        self.canvas.create_image(0,0,anchor='nw',image = photo)
        self.canvas.place(x=0,y=0,anchor='nw')
        self.resizable(0,0)
        win.mainloop()

class ACHIEVEMENTSFRAME(tkinter.Frame):
    def __init__(self,master=None,**kw):
        tkinter.Frame.__init__(self,master,**kw)
        self.engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        sql = "select * from achievements where userID='%s'"%zdyallfunction.userID
        self.detailachievements = pd.read_sql_query(sql, self.engine)
        self.levelstandard=[]
        levelsum=0
        for i in range(99):
            levelsum=levelsum+10*i
            self.levelstandard.append(levelsum)
        for i in range(len(self.levelstandard)-1):
            if self.detailachievements.iloc[0,1]>=self.levelstandard[i] and self.detailachievements.iloc[0,1]<self.levelstandard[i+1]:
                self.showlevel=i+1
                self.levellinspace=self.levelstandard[i+1]-self.detailachievements.iloc[0,1]
                break

    def showzuodahelp(self):
        zuodahelp=HELPTOPLEVEL(name='作答功能简介',ratio=2.165,picturename='zuodahelp.jpg')
        zuodahelp.bind()
        
    def showcontacthelp(self):
        contacthelp=HELPTOPLEVEL(name='联系我们',ratio=1.16,picturename='contact.png')
        contacthelp.bind()
        
    def bind(self):
        
        self.nameframe=tkinter.Frame(self,height=0.14*height,width=0.09*width)
        self.nicknamelable=tkinter.Label(self.nameframe,text='%s'%zdyallfunction.nickname,font=('微软雅黑',10,'bold'))

        self.LVframe=tkinter.Frame(self,height=0.14*height,width=0.09*width)
        self.levellable=tkinter.Label(self.LVframe,text='LV=%s'%self.showlevel,font=('times',15,'bold'))

        self.honorcreditslable=tkinter.Label(self,text='%d'%self.detailachievements.iloc[0,2],font=('times',15,'bold'))
        self.namecanvas=tkinter.Canvas(self.nameframe,height=0.1*height,width=0.09*width)
        self.LVcanvas=tkinter.Canvas(self.LVframe,height=0.1*height,width=0.09*width)
        im=Image.open(f'{os.getcwd()}/infor/person.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        self.namecanvas.create_image(0,0,anchor='nw',image = photo)
        if self.showlevel<=10:
            im2=Image.open(f'{os.getcwd()}/infor/LV1.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        elif self.showlevel>10 and self.showlevel<=20:
            im2=Image.open(f'{os.getcwd()}/infor/LV2.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        elif self.showlevel>20 and self.showlevel<=30:
            im2=Image.open(f'{os.getcwd()}/infor/LV3.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        elif self.showlevel>30 and self.showlevel<=40:
            im2=Image.open(f'{os.getcwd()}/infor/LV4.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        elif self.showlevel>40 and self.showlevel<=50:
            im2=Image.open(f'{os.getcwd()}/infor/LV5.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        elif self.showlevel>50 and self.showlevel<=60:
            im2=Image.open(f'{os.getcwd()}/infor/LV6.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        elif self.showlevel>60 and self.showlevel<=70:
            im2=Image.open(f'{os.getcwd()}/infor/LV7.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        elif self.showlevel>70 and self.showlevel<=80:
            im2=Image.open(f'{os.getcwd()}/infor/LV8.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        elif self.showlevel>80 and self.showlevel<=90:
            im2=Image.open(f'{os.getcwd()}/infor/LV9.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        elif self.showlevel>90 and self.showlevel<=99:
            im2=Image.open(f'{os.getcwd()}/infor/LV10.png')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))   
        self.LVcanvas.create_image(0,0,anchor='nw',image = photo2)
        
        self.LVdetailcanvas=tkinter.Canvas(self.LVframe,height=0.1*height,width=0.09*width)
        self.LVdetailcanvas.create_rectangle(
                        0, 0.045*height,
                        0.09*width, 0.055*height,
                        fill='white')
        self.LVdetailcanvas.create_rectangle(
                0, 0.045*height,
                (int(self.detailachievements.iloc[0,1])-self.levelstandard[self.showlevel-1])/(int(self.levelstandard[self.showlevel]-self.levelstandard[self.showlevel-1]))*0.09*width, 0.055*height,
                fill='green')
        
        self.LVdetailcanvas.create_text(0.04*width, 0.03*height, text='%s/%s'%(int(self.detailachievements.iloc[0,1])-self.levelstandard[self.showlevel-1],int(self.levelstandard[self.showlevel])-self.levelstandard[self.showlevel-1]),font=('times',12,'bold'))
        self.honorcanvas=tkinter.Canvas(self,height=0.1*height,width=0.09*width)
        im3=Image.open(f'{os.getcwd()}/infor/honorcredits.png')
        photo3 = ImageTk.PhotoImage(im3.resize((int(0.1*width),int(0.1*height)),Image.ANTIALIAS))
        self.honorcanvas.create_image(0,0,anchor='nw',image = photo3)
        self.rankbutton=tkinter.Button(self,text='查看排行榜',font=('微软雅黑',10,'bold'),fg='white',bg='black',command=self.showranklist)
        self.helpbutton=tkinter.Button(self,text='升级与获取积分',font=('微软雅黑',10,'bold'),fg='white',bg='black',command=self.showrankhelp)
        
        self.nameframe.place(x=0,y=0,anchor='nw')
        self.namecanvas.pack()
        self.nicknamelable.pack()
        spaceframe1=tkinter.Frame(self,bg='black',height=0.005*height,width=0.15*width)
        spaceframe1.place(x=-0.01*width,y=0.14*height,anchor='nw')
        self.LVframe.place(x=0,y=0.16*height,anchor='nw')
        self.LVcanvas.pack()
        self.levellable.pack()
        self.LVdetailcanvas.pack()

    
        spaceframe2=tkinter.Frame(self,bg='black',height=0.005*height,width=0.15*width)
        spaceframe2.place(x=-0.01*width,y=0.39*height,anchor='nw')
        self.zuodahelpbutton=tkinter.Button(self,text='作答功能简介',font=('微软雅黑',10,'bold'),fg='white',bg='black',command=self.showzuodahelp)
        self.contacthelpbutton=tkinter.Button(self,text='联系我们',font=('微软雅黑',10,'bold'),fg='white',bg='black',command=self.showcontacthelp)
        self.contactrightnowbutton=tkinter.Button(self,text='留言信箱',font=('微软雅黑',10,'bold'),fg='white',bg='black',command=self.showmessagebox)
        
        self.honorcanvas.place(x=0,y=0.42*height,anchor='nw')
        self.honorcreditslable.place(x=0.03*width,y=0.54*height,anchor='nw')
        self.rankbutton.place(x=0.005*width,y=0.6*height)
        self.helpbutton.place(x=0.0*width,y=0.68*height)
        self.zuodahelpbutton.place(x=0,y=0.76*height)
        self.contacthelpbutton.place(x=0,y=0.84*height)
        self.contactrightnowbutton.place(x=0,y=0.92*height)
        
        win.mainloop()

    def showranklist(self):
        ranklist=RANKINGLIST()
        ranklist.bind()
    
    def showrankhelp(self):
        rankhelp=RANKHELP()

    def showmessagebox(self):
        MESSAGEBOARD()



















class Rope(tkinter.Toplevel):
    def __init__(self,master=None,**kw):
        tkinter.Toplevel.__init__(self,master,**kw)
        self.title('rope method')
        self.iconbitmap('infor/tubiao.ico')
        self.geometry('%dx%d+%d+%d'%(0.5*width,0.4*height,dx,dy))
        self.canvas=tkinter.Canvas(self,height=0.4*height,width=0.4*width,bg='white')
        self.canvas.place(x=0,y=0,anchor='nw')
        self.r=8*sh/1920
        #        self.line1 = self.canvas.create_line(0.05*width, 0.2*height, 0.35*width, 0.2*height, fill = "#DAA520",width=10)
        self.line1 = self.canvas.create_line(0.05*width, 0.2*height, 0.35*width, 0.2*height, fill = "#CD853F",width=10)
        self.line2=self.canvas.create_line(0.05*width,0.2*height,0.04*width,0.19*height,fill='black',width=int(5*sh/1920))
        self.line3=self.canvas.create_line(0.05*width,0.2*height,0.04*width,0.2*height,fill='black',width=int(5*sh/1920))
        self.line4=self.canvas.create_line(0.05*width,0.2*height,0.04*width,0.21*height,fill='black',width=int(5*sh/1920))
        self.line5=self.canvas.create_line(0.35*width,0.2*height,0.36*width,0.19*height,fill='black',width=int(5*sh/1920))
        self.line6=self.canvas.create_line(0.35*width,0.2*height,0.36*width,0.2*height,fill='black',width=int(5*sh/1920))
        self.line7=self.canvas.create_line(0.35*width,0.2*height,0.36*width,0.21*height,fill='black',width=int(5*sh/1920))
        self.button1=tkinter.Button(self,width=15,text='功能说明',fg='white',bg='black',command=self.instruction)
        self.button1.place(x=0.4*width,y=0.25*height,anchor='nw')
        self.button2=tkinter.Button(self,width=15,text='初始化',fg='white',bg='black',command=self.clearrope)
        self.button2.place(x=0.4*width,y=0.15*height,anchor='nw')
        self.pointpositions=[]
        class Point():
            def __init__(self,x,y):
                self.x=x
                self.y=y
        self.p1=Point(0.08*width,0.2*height)
        self.p2=Point(0.11*width,0.2*height)
        self.p3=Point(0.14*width,0.2*height)
        self.p4=Point(0.17*width,0.2*height)
        self.p5=Point(0.2*width,0.2*height)
        self.p6=Point(0.23*width,0.2*height)
        self.p7=Point(0.26*width,0.2*height)
        self.p8=Point(0.29*width,0.2*height)
        self.p9=Point(0.32*width,0.2*height)
        self.pointpositions.append(self.p1)
        self.pointpositions.append(self.p2)
        self.pointpositions.append(self.p3)
        self.pointpositions.append(self.p4)
        self.pointpositions.append(self.p5)
        self.pointpositions.append(self.p6)
        self.pointpositions.append(self.p7)
        self.pointpositions.append(self.p8)
        self.pointpositions.append(self.p9)
        self.unit=0.02*height
        for point in self.pointpositions:
            self.canvas.create_oval(point.x-10*sh/1800,point.y-10*sh/1800,point.x+10*sh/1800,point.y+10*sh/1800,fill='black')
        self.deltamatrixs=pd.DataFrame(np.zeros((9,9)))
        self.deltamatrixs.iloc[0]=[0.36,0.32,0.28,0.24,0.2,0.16,0.12,0.08,0.04]
        self.deltamatrixs.iloc[1]=[0.32,0.64,0.56,0.48,0.4,0.32,0.24,0.16,0.08]
        self.deltamatrixs.iloc[2]=[0.28,0.56,0.84,0.72,0.6,0.48,0.36,0.24,0.12]
        self.deltamatrixs.iloc[3]=[0.24,0.48,0.72,0.96,0.8,0.64,0.48,0.32,0.16]
        self.deltamatrixs.iloc[4]=[0.2,0.4,0.6,0.8,1,0.8,0.6,0.4,0.2]
        self.deltamatrixs.iloc[5]=[0.16,0.32,0.48,0.64,0.8,0.96,0.72,0.48,0.24]
        self.deltamatrixs.iloc[6]=[0.12,0.24,0.36,0.48,0.6,0.72,0.84,0.56,0.28]
        self.deltamatrixs.iloc[7]=[0.08,0.16,0.24,0.32,0.4,0.48,0.56,0.64,0.32]
        self.deltamatrixs.iloc[8]=[0.04,0.08,0.12,0.16,0.2,0.24,0.28,0.32,0.36]
        #        self.deltamatrixs=pd.DataFrame([0.36,0.32,0.28,0.24,0.2,0.16,0.12,0.08,0.04],
        #                       [0.32,0.64,0.56,0.48,0.4,0.32,0.24,0.16,0.08],
        #                       [0.28,0.56,0.84,0.72,0.6,0.48,0.36,0.24,0.12],
        #                       [0.24,0.48,0.72,0.96,0.8,0.64,0.48,0.32,0.16],
        #                       [0.2,0.4,0.6,0.8,1,0.8,0.6,0.4,0.2],
        #                       [0.16,0.32,0.48,0.64,0.8,0.96,0.72,0.48,0.24],
        #                       [0.12,0.24,0.36,0.48,0.6,0.72,0.84,0.56,0.28]
        #                       [0.08,0.16,0.24,0.32,0.4,0.48,0.56,0.64,0.32],
        #                       [0.04,0.08,0.12,0.16,0.2,0.24,0.28,0.32,0.36])

        self.diagramdelta=[0.36,0.64,0.84,0.96,1,0.96,0.84,0.64,0.36]
        self.F=np.zeros((9,1))
        self.delta=[0,0,0,0,0,0,0,0,0]
        self.resizable(0,0)
        
    def instruction(self):
        tkinter.messagebox.showinfo(title='使用说明', message='rope method通过绳子的变形,模拟简支梁在一个或多个集中力下的弯矩图\n您可以点击并拖动绳子内部的节点，模拟简支梁受力下的弯矩图')
    def bind(self):
        self.canvas.bind('<Button-1>',self.move)

    def delcanvasitems(self):
        self.canvas.delete(tkinter.ALL)
    def drawrope(self):
        self.canvas.create_line(0.05*width,0.2*height,0.08*width,int(self.pointpositions[0].y+self.delta[0]), fill = "#CD853F",width=10)
        self.canvas.create_line(0.08*width,int(self.pointpositions[0].y+self.delta[0]),0.11*width,int(self.pointpositions[1].y+self.delta[1]), fill = "#CD853F",width=10)
        self.canvas.create_line(0.11*width,int(self.pointpositions[1].y+self.delta[1]),0.14*width,int(self.pointpositions[2].y+self.delta[2]), fill = "#CD853F",width=10)
        self.canvas.create_line(0.14*width,int(self.pointpositions[2].y+self.delta[2]),0.17*width,int(self.pointpositions[3].y+self.delta[3]), fill = "#CD853F",width=10)
        self.canvas.create_line(0.17*width,int(self.pointpositions[3].y+self.delta[3]),0.2*width,int(self.pointpositions[4].y+self.delta[4]), fill = "#CD853F",width=10)
        self.canvas.create_line(0.2*width,int(self.pointpositions[4].y+self.delta[4]),0.23*width,int(self.pointpositions[5].y+self.delta[5]), fill = "#CD853F",width=10)
        self.canvas.create_line(0.23*width,int(self.pointpositions[5].y+self.delta[5]),0.26*width,int(self.pointpositions[6].y+self.delta[6]), fill = "#CD853F",width=10)
        self.canvas.create_line(0.26*width,int(self.pointpositions[6].y+self.delta[6]),0.29*width,int(self.pointpositions[7].y+self.delta[7]), fill = "#CD853F",width=10)
        self.canvas.create_line(0.29*width,int(self.pointpositions[7].y+self.delta[7]),0.32*width,int(self.pointpositions[8].y+self.delta[8]), fill = "#CD853F",width=10)
        self.canvas.create_line(0.32*width,int(self.pointpositions[8].y+self.delta[8]),0.35*width,0.2*height, fill = "#CD853F",width=10)
        for i in range(9):
            x=int(self.pointpositions[i].x)
            y=int(self.pointpositions[i].y+self.delta[i])
            self.canvas.create_oval(x-10*sh/1800,y-10*sh/1800,x+10*sh/1800,y+10*sh/1800,fill='black')
        self.line2=self.canvas.create_line(0.05*width,0.2*height,0.04*width,0.19*height,fill='black',width=int(5*sh/1920))
        self.line3=self.canvas.create_line(0.05*width,0.2*height,0.04*width,0.2*height,fill='black',width=int(5*sh/1920))
        self.line4=self.canvas.create_line(0.05*width,0.2*height,0.04*width,0.21*height,fill='black',width=int(5*sh/1920))
        self.line5=self.canvas.create_line(0.35*width,0.2*height,0.36*width,0.19*height,fill='black',width=int(5*sh/1920))
        self.line6=self.canvas.create_line(0.35*width,0.2*height,0.36*width,0.2*height,fill='black',width=int(5*sh/1920))
        self.line7=self.canvas.create_line(0.35*width,0.2*height,0.36*width,0.21*height,fill='black',width=int(5*sh/1920))
        for i in range(9):
            if int(self.F[i])>0:
                x=int(self.pointpositions[i].x)
                y=int(self.pointpositions[i].y+self.delta[i])+0.02*height
                self.canvas.create_text(x,y,text='↓F='+str(int(self.F[i])))
            if int(self.F[i])<0:
                x=int(self.pointpositions[i].x)
                y=int(self.pointpositions[i].y+self.delta[i])-0.02*height
                self.canvas.create_text(x,y,text='↑F='+str(int(abs(self.F[i]))))
        self.canvas.create_line(0.05*width, 0.2*height, 0.35*width, 0.2*height,fill='red',  
                               dash=(4, 4),width=2)
    def move(self,event):
        self.choicepoint=-1
        x=event.x
        y=event.y
        print(event.x)
        print(event.y)
        for i in range(len(self.pointpositions)):
            if abs(self.pointpositions[i].x-x)<10 and abs(y-self.pointpositions[i].y-self.delta[i])<10:
                self.choicepoint=i
                self.canvas.create_oval(self.pointpositions[i].x-10*sh/1800,self.pointpositions[i].y-10*sh/1800+int(self.delta[i]),
                                        self.pointpositions[i].x+10*sh/1800,self.pointpositions[i].y+10*sh/1800+int(self.delta[i]),fill='red')
        if self.choicepoint>=0:
            self.canvas.bind('<ButtonRelease-1>',self.redraw)
    def redraw(self,event):
        if self.choicepoint>=0:
            num=self.choicepoint
            tempF=0
            tempF=round((event.y-self.pointpositions[num].y-int(self.delta[num]))/self.unit/self.diagramdelta[num])
            print(tempF)
            self.F[num]=self.F[num]+tempF
            #            deltay=tempF*self.unit
            #            self.pointpositions[num].y=deltay+self.pointpositions[num].y
            self.delta=np.dot(self.deltamatrixs,self.F)
            self.delta=self.delta*self.unit
            self.delcanvasitems()
            self.drawrope()
    def clearrope(self):
        self.canvas.delete('all')
        self.line1 = self.canvas.create_line(0.05*width, 0.2*height, 0.35*width, 0.2*height, fill = "#CD853F",width=10)
        self.line2=self.canvas.create_line(0.05*width,0.2*height,0.04*width,0.19*height,fill='black',width=int(5*sh/1920))
        self.line3=self.canvas.create_line(0.05*width,0.2*height,0.04*width,0.2*height,fill='black',width=int(5*sh/1920))
        self.line4=self.canvas.create_line(0.05*width,0.2*height,0.04*width,0.21*height,fill='black',width=int(5*sh/1920))
        self.line5=self.canvas.create_line(0.35*width,0.2*height,0.36*width,0.19*height,fill='black',width=int(5*sh/1920))
        self.line6=self.canvas.create_line(0.35*width,0.2*height,0.36*width,0.2*height,fill='black',width=int(5*sh/1920))
        self.line7=self.canvas.create_line(0.35*width,0.2*height,0.36*width,0.21*height,fill='black',width=int(5*sh/1920))
        self.pointpositions=[]
        class Point():
            def __init__(self,x,y):
                self.x=x
                self.y=y
        self.p1=Point(0.08*width,0.2*height)
        self.p2=Point(0.11*width,0.2*height)
        self.p3=Point(0.14*width,0.2*height)
        self.p4=Point(0.17*width,0.2*height)
        self.p5=Point(0.2*width,0.2*height)
        self.p6=Point(0.23*width,0.2*height)
        self.p7=Point(0.26*width,0.2*height)
        self.p8=Point(0.29*width,0.2*height)
        self.p9=Point(0.32*width,0.2*height)
        self.pointpositions.append(self.p1)
        self.pointpositions.append(self.p2)
        self.pointpositions.append(self.p3)
        self.pointpositions.append(self.p4)
        self.pointpositions.append(self.p5)
        self.pointpositions.append(self.p6)
        self.pointpositions.append(self.p7)
        self.pointpositions.append(self.p8)
        self.pointpositions.append(self.p9)
        self.unit=0.02*height
        for point in self.pointpositions:
            self.canvas.create_oval(point.x-10*sh/1800,point.y-10*sh/1800,point.x+10*sh/1800,point.y+10*sh/1800,fill='black')
        self.F=np.zeros((9,1))
        self.delta=[0,0,0,0,0,0,0,0,0]


















class Tabletree(ttk.Treeview):
    def qualifyframeparent(self,frameparent):
        self.frameparent=frameparent
    def total(self,totalcolumn,totalrow):
        self.totalcolumn=totalcolumn
        self.totalrow=totalrow
    def qualifynum(self,num):
        self.num=num
    def updatenum(self):
        zdyallfunction.updatenum(self.num)
    def textstate(self):
        self.textexist=0
    def createinformatrix(self):
        self.informatrix=pd.DataFrame((np.full((self.totalrow,self.totalcolumn),np.nan)))
    def updateinformatrix(self):
        if len(self.text.get(0.0,'end'))!=1 and self.text.get('end')=="":
            self.informatrix[self.columnnow][self.rownow]=float(self.text.get(0.0,'end'))
            zdyallfunction.updateinformatrixs(self.num,self.informatrix)
        else:
            self.informatrix[self.columnnow][self.rownow]=np.nan
            zdyallfunction.updateinformatrixs(self.num,self.informatrix)
    
    def selectItem(self,event):
        if self.textexist==1:
            self.updatedata(event)
            self.destroyframe(event)
        self.updatenum()
        x=event.x
        y=event.y
        self.tk_focusNext()
        widget=event.widget
        standardbbox=widget.bbox("I001","#1")
        self.standardx=standardbbox[0]
        self.standardy=standardbbox[1]
        self.w=standardbbox[2]
        self.h=standardbbox[3]
        iid = widget.identify_row(y)
        column = event.widget.identify_column(x)
        if iid=='':
            return
        bbox=widget.bbox(iid,column)
        self.columnnow=int((bbox[0]-standardbbox[0])/self.w)
        self.rownow=int((bbox[1]-standardbbox[1])/self.h)
        self.frame=tkinter.Frame(self.frameparent,width=int(self.w),height=int(self.h))
        self.frame.place(x=bbox[0],y=bbox[1],anchor='nw')
        self.text=tkinter.Text(self.frame,fg='red')
        self.text.place(x=0,y=0,anchor='nw')
        
        self.text.focus()
        self.text.bind('<Left>',self.leftmove)
        self.text.bind('<Right>',self.rightmove)
        self.text.bind('<Up>',self.upmove)
        self.text.bind('<Down>',self.downmove)
        self.text.bind('<Return>',self.endupdata)
        self.text.bind('<Escape>',self.destroyframe)
        #        self.text.bind('<Tab>',self.rightmove)
        self.textexist=1
        
    def binding(self):
        self.bind('<ButtonRelease-1>', self.selectItem)
        self.bind('Leave',self.endupdata)
    def leftmove(self,event):
        if self.textexist==0:
            return
        if self.columnnow>0:
            state=self.updatedata(event)
            if state==1:
                self.frame.place(x=self.standardx+(self.columnnow-1)*self.w,y=self.standardy+self.rownow*self.h,anchor='nw')
                self.columnnow=self.columnnow-1
                self.text.delete(0.0,'end')
                if(pd.isnull(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])==False):
                    if math.modf(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]==0):
                        self.text.insert('end',int(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]))
                    else:
                        self.text.insert('end',zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])

            
    def rightmove(self,event):
        if self.textexist==0:
            return
        if self.columnnow<(self.totalcolumn-1):
            state=self.updatedata(event)
            if state==1:
                self.frame.place(x=self.standardx+(self.columnnow+1)*self.w,y=self.standardy+self.rownow*self.h,anchor='nw')
                self.columnnow=self.columnnow+1
                self.text.delete(0.0,'end')
                if(pd.isnull(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])==False):
                    if math.modf(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]==0):
                        self.text.insert('end',int(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]))
                    else:
                        self.text.insert('end',zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])
        elif self.columnnow==(self.totalcolumn-1):
            state=self.updatedata(event)
            if state==1:
                self.frame.place(x=self.standardx,y=self.standardy+(self.rownow+1)*self.h,anchor='nw')
                self.columnnow=0
                self.rownow=self.rownow+1
                self.text.delete(0.0,'end')
                if(pd.isnull(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])==False):
                    if math.modf(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]==0):
                        self.text.insert('end',int(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]))
                    else:
                        self.text.insert('end',zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])
    def upmove(self,event):
        if self.textexist==0:
            return
        if self.rownow>0:
            state=self.updatedata(event)
            if state==1:
                self.frame.place(x=self.standardx+(self.columnnow)*self.w,y=self.standardy+(self.rownow-1)*self.h,anchor='nw')
                self.rownow=self.rownow-1
                self.text.delete(0.0,'end')
                if(pd.isnull(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])==False):
                    if math.modf(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]==0):
                        self.text.insert('end',int(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]))
                    else:
                        self.text.insert('end',zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])
            
    def downmove(self,event):
        if self.textexist==0:
            return
        if self.rownow<14:
            state=self.updatedata(event)
            if state==1:
                self.frame.place(x=self.standardx+(self.columnnow)*self.w,y=self.standardy+(self.rownow+1)*self.h,anchor='nw')
                self.rownow=self.rownow+1
                self.text.delete(0.0,'end')
                if(pd.isnull(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])==False):
                    if math.modf(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]==0):
                        self.text.insert('end',int(zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow]))
                    else:
                        self.text.insert('end',zdyallfunction.informatrixs[self.num][self.columnnow][self.rownow])
           
    def updatedata(self,event):
        if self.textexist==0:
            return
        state=self.catcherr()
        if state==0:
            return state
        if len(self.text.get(0.0,'end'))!=1 and self.text.get('end')=="":
            x=self.standardx+(self.columnnow+1)*self.w
            y=self.standardy+(self.rownow+1)*self.h
            iid = self.identify_row(y)
            column = self.identify_column(x)
            self.set(item=iid,column=column,value=self.text.get(0.0,'end'))
            self.updateinformatrix()
            self.updatenum()
            return 1
        else:
            x=self.standardx+(self.columnnow+1)*self.w
            y=self.standardy+(self.rownow+1)*self.h
            iid = self.identify_row(y)
            column = self.identify_column(x)
            self.set(item=iid,column=column,value='')
            self.updateinformatrix()
            self.updatenum()
            return 1
         
    def destroyframe(self,event):
        self.frame.destroy()
        self.textexist=0
        
    def endupdata(self,event):
        if self.textexist==0:
            return
        state=self.updatedata(event)
        if state==0:
            return
        self.destroyframe(event)
    
    def finalendup(self):
        if self.textexist==0:
            return
        state=self.catcherr()
        if state==0:
            return
        if len(self.text.get(0.0,'end'))!=1 and self.text.get('end')=="":
            x=self.standardx+(self.columnnow+1)*self.w
            y=self.standardy+(self.rownow+1)*self.h
            iid = self.identify_row(y)
            column = self.identify_column(x)
            self.set(item=iid,column=column,value=self.text.get(0.0,'end'))
            self.updateinformatrix()
        else:
            x=self.standardx+(self.columnnow+1)*self.w
            y=self.standardy+(self.rownow+1)*self.h
            iid = self.identify_row(y)
            column = self.identify_column(x)
            self.set(item=iid,column=column,value='')
            self.updateinformatrix()
        self.frame.destroy()
        self.textexist=0
    def now(self,event):
       return(self.bbox("I001","#1"))
    def catcherr(self):
        if len((self.text.get(0.0,'end')))>1:
            try:
                float(self.text.get(0.0,'end'))
            except ValueError:
                tkinter.messagebox.showinfo(title='提示', message='输入的内容只能为数字')
                self.frame.destroy()
                self.textexist=0
                return 0
            else:
                return 1
        return 1









class Xuanzecanvas(tkinter.Canvas):
    def __init__(self,master=None,**kw):
        tkinter.Canvas.__init__(self,master,**kw)
        self.smallest_index=-1
        self.ufocus=0
        
    def qualifypartner(self,x):
        self.partner=x
    def createduandian(self):
        zdyallfunction.daduan=0
        zdyallfunction.duandian=[]
        for i in range(len(zdyallfunction.elements)):
            zdyallfunction.duandian.append([0,1])

    def drawuserM(self):
        zdyallfunction.drawuserM(self.smallest_index)
        
        
    def showuserM(self):
        im=Image.open(f'{os.getcwd()}/drawing/userM.png')
        photo = ImageTk.PhotoImage(im.resize((self.winfo_width(),self.winfo_height()),Image.ANTIALIAS))
        self.create_image(0,0,anchor='nw',image = photo)  
        self.mainloop()
        
        
    def showusermenu(self,event):
    #        if self.ufocus==1:
    #            self.menu2.post(event.x_root, event.y_root)
        if self.smallest_index!=-1:
            self.menu2.post(event.x_root, event.y_root)
           
            
    def sc(self):
        zdyallfunction.shanchuuserM(self.smallest_index)
        self.paintline(zdyallfunction.c,c1.relposition)
        self.ufocus=0
        self.smallest_index=-1
        self.delete('choice')
    #        zdyallfunction.drawuserM(self.smallest_index)
    #        self.showuserM()
        
    def dd(self):
        zdyallfunction.ddzt()
        zdyallfunction.drawuserM(self.smallest_index)
        im=Image.open(f'{os.getcwd()}/drawing/userM.png')
        photo = ImageTk.PhotoImage(im.resize((self.winfo_width(),self.winfo_height()),Image.ANTIALIAS))
        self.create_image(0,0,anchor='nw',image = photo)
        global instructionpartexist
        if instructionpartexist==1:
            global inshelp3
            try:
                inshelp3.destroy()
            except:
                pass
            inshelp3=HELPTOPLEVEL(name='操作简介',ratio=1.6,picturename='instructionhelp3.jpg',dx=(sw-width)/2+0.5*width,dy=(sh-height*1.05)/2+0.5*height)
            inshelp3.bind()
            destroy_inshelp()
        win.mainloop()
    
    def scdd(self):
        zdyallfunction.duandian[self.smallest_index]=[0,1]
        self.ufocus=0
        self.smallest_index=-1
        self.delete('seperate_point')
        self.delete('choice')
        for i in range(len(zdyallfunction.duandian)):
            for j in zdyallfunction.duandian[i]:
                if j!=0 and j!=1:
                    xc=self.relposition[i]['pix']+j*(self.relposition[i]['pjx']-self.relposition[i]['pix'])
                    yc=self.relposition[i]['piy']+j*(self.relposition[i]['pjy']-self.relposition[i]['piy'])
                    circle_dimension=int(10/1800*height)
                    self.create_oval(xc-circle_dimension,yc-circle_dimension,
                                     xc+circle_dimension,yc+circle_dimension,tag='seperate_point',fill='red')
        
    #        zdyallfunction.drawuserM(-1)
    #        im2=Image.open(f'{os.getcwd()}/drawing/userM.png')
    #        photo2 = ImageTk.PhotoImage(im2.resize((self.winfo_width(),self.winfo_height()),Image.ANTIALIAS))
    #        self.create_image(0,0,anchor='nw',image = photo2)
    #        win.mainloop()

        
    def relativeposition(self):
        self.bind("<Button-1>", self.userMfocuson)
        self.bind("<Button-3>", self.showusermenu)
        self.menu2=tkinter.Menu(tearoff=False)
        submenu21=tkinter.Menu(self.menu2,tearoff=False)
        self.menu2.add_cascade(label="作答",menu=submenu21)
        submenu21.add_command(label="直线",command=self.partner.zhixian)
        #,command=zhixian
        submenu21.add_command(label="曲线",command=self.partner.quxian)
        #,command=quxian
        self.menu2.add_command(label="删除",command=self.sc)
        #,command=sc
        self.menu2.add_command(label="断点",command=self.dd)
        #,command=dd
        self.menu2.add_command(label="删除断点",command=self.scdd)
        #,command=dd
        hp2=self.winfo_height()
        wp2=self.winfo_width()
        hp2=0.5*height
        wp2=0.5*width
        self.relposition=[]
        res=zdyallfunction.res
        #确定x的坐标范围xrange，y的坐标范围yrange，还有最大最小的x，y坐标
        xrange=zdyallfunction.xrange
        yrange=zdyallfunction.yrange
        xflim=zdyallfunction.xflim
        yflim=zdyallfunction.yflim
        xzlim=zdyallfunction.xzlim
        yzlim=zdyallfunction.yzlim
        dx=xrange[1]-xrange[0]
        dy=yrange[1]-yrange[0]
        #xlong，x方向范围比y方向范围大，figsize都是1：1.6，
        #无非就是以x长度为标准，或以y长度为标准x/1.6或y/1.6
        xlong=zdyallfunction.xlong
        if xlong:
            for i in range(len(zdyallfunction.elements)):
                relposition_={}
                relposition_['num']=i+1
                relposition_['pix']=(zdyallfunction.elements[i]['pi']['x']-xflim+res)/dx*wp2
                relposition_['piy']=(dy-zdyallfunction.elements[i]['pi']['y']-(xzlim-xflim+2*res)/3.2+(yzlim-yflim)/2+yflim)/dy*hp2
                relposition_['pjx']=(zdyallfunction.elements[i]['pj']['x']-xflim+res)/dx*wp2
                relposition_['pjy']=(dy-zdyallfunction.elements[i]['pj']['y']-(xzlim-xflim+2*res)/3.2+(yzlim-yflim)/2+yflim)/dy*hp2
                relposition_['alp']=zdyallfunction.elements[i]['alp']
                self.relposition.append(relposition_.copy())
        else:
            for i in range(len(zdyallfunction.elements)):
                relposition_={}
                relposition_['num']=i+1
                relposition_['pix']=(zdyallfunction.elements[i]['pi']['x']-xflim+0.5*dx-0.5*(xzlim-xflim))/dx*wp2
                relposition_['piy']=(dy-zdyallfunction.elements[i]['pi']['y']-res+yflim)/dy*hp2
                relposition_['pjx']=(zdyallfunction.elements[i]['pj']['x']-xflim+0.5*dx-0.5*(xzlim-xflim))/dx*wp2
                relposition_['pjy']=(dy-zdyallfunction.elements[i]['pj']['y']-res+yflim)/dy*hp2
                relposition_['alp']=zdyallfunction.elements[i]['alp']
                self.relposition.append(relposition_.copy())
                
                
    def relativeposition_for_manage(self):
        hp2=self.winfo_height()
        wp2=self.winfo_width()
#        hp2=0.5*height
#        wp2=0.5*width
        self.relposition=[]
        res=zdyallfunction.res
        #确定x的坐标范围xrange，y的坐标范围yrange，还有最大最小的x，y坐标
        xrange=zdyallfunction.xrange
        yrange=zdyallfunction.yrange
        xflim=zdyallfunction.xflim
        yflim=zdyallfunction.yflim
        xzlim=zdyallfunction.xzlim
        yzlim=zdyallfunction.yzlim
        dx=xrange[1]-xrange[0]
        dy=yrange[1]-yrange[0]
        #xlong，x方向范围比y方向范围大，figsize都是1：1.6，
        #无非就是以x长度为标准，或以y长度为标准x/1.6或y/1.6
        xlong=zdyallfunction.xlong
        if xlong:
            for i in range(len(zdyallfunction.elements)):
                relposition_={}
                relposition_['num']=i+1
                relposition_['pix']=(zdyallfunction.elements[i]['pi']['x']-xflim+res)/dx*wp2
                relposition_['piy']=(dy-zdyallfunction.elements[i]['pi']['y']-(xzlim-xflim+2*res)/3.2+(yzlim-yflim)/2+yflim)/dy*hp2
                relposition_['pjx']=(zdyallfunction.elements[i]['pj']['x']-xflim+res)/dx*wp2
                relposition_['pjy']=(dy-zdyallfunction.elements[i]['pj']['y']-(xzlim-xflim+2*res)/3.2+(yzlim-yflim)/2+yflim)/dy*hp2
                relposition_['alp']=zdyallfunction.elements[i]['alp']
                self.relposition.append(relposition_.copy())
        else:
            for i in range(len(zdyallfunction.elements)):
                relposition_={}
                relposition_['num']=i+1
                relposition_['pix']=(zdyallfunction.elements[i]['pi']['x']-xflim+0.5*dx-0.5*(xzlim-xflim))/dx*wp2
                relposition_['piy']=(dy-zdyallfunction.elements[i]['pi']['y']-res+yflim)/dy*hp2
                relposition_['pjx']=(zdyallfunction.elements[i]['pj']['x']-xflim+0.5*dx-0.5*(xzlim-xflim))/dx*wp2
                relposition_['pjy']=(dy-zdyallfunction.elements[i]['pj']['y']-res+yflim)/dy*hp2
                relposition_['alp']=zdyallfunction.elements[i]['alp']
                self.relposition.append(relposition_.copy())
                
    def userMfocuson(self,event):
        #if zdyallfunction.daduan==0用户在选择杆件，而不是断点
        self.delete('choice')
        if zdyallfunction.daduan==0:
            print(f"鼠标左键点击了一次坐标是:x={event.x}y={event.y}")
            self.smallest_index=-1
            distance=[]
            #记录每根杆件与点击点之间的距离
            for i in range(len(self.relposition)):
                print(self.winfo_height())
                print(self.winfo_width())
                pix=self.relposition[i]['pix']
                piy=self.relposition[i]['piy']
                pjx=self.relposition[i]['pjx']
                pjy=self.relposition[i]['pjy']
                if self.relposition[i]['alp']==90 or self.relposition[i]['alp']==-90:
                    distance_=abs(event.x-pix)
                    distance.append(distance_)
                    
                else:
                    k=(piy-pjy)/(pix-pjx)
                    b=piy-k*pix
                    distance_=abs(event.y-k*event.x-b)/np.sqrt(1+k*k)
                    distance.append(distance_)
            for i in range(len(distance)):
                pix=self.relposition[i]['pix']
                piy=self.relposition[i]['piy']
                pjx=self.relposition[i]['pjx']
                pjy=self.relposition[i]['pjy']
                #距离小于0.02*height即认为是用户选择的杆件
                if distance[i]<0.02*self.winfo_height():
                    if (event.x>=min(pix,pjx) and event.x<=max(pix,pjx)) or (event.y>=min(piy,pjy) and event.y<=max(piy,pjy)):
                        self.smallest_index=i
            #存在这种杆件smallest_index!=-1
            if self.smallest_index!=-1:
                pix=self.relposition[self.smallest_index]['pix']
                piy=self.relposition[self.smallest_index]['piy']
                pjx=self.relposition[self.smallest_index]['pjx']
                pjy=self.relposition[self.smallest_index]['pjy']
                #ufocus需要高亮表示某根杆件
                self.ufocus=1
                #duandian长度大于2确定杆件存在断点，ps和pe不一定为0和1，以下代码确定用户要选择哪一段
                if len(zdyallfunction.duandian[self.smallest_index])>2:
                    #90度-90度特殊情况
                   if self.relposition[self.smallest_index]['alp']==90 or self.relposition[self.smallest_index]['alp']==-90:
                       pp=(event.y-piy)/(pjy-piy)
                       for j in range(len(zdyallfunction.duandian[self.smallest_index])-1):
                           if (zdyallfunction.duandian[self.smallest_index][j]-pp)*(zdyallfunction.duandian[self.smallest_index][j+1]-pp)<0:
                               zdyallfunction.ps=zdyallfunction.duandian[self.smallest_index][j]
                               zdyallfunction.pe=zdyallfunction.duandian[self.smallest_index][j+1]
                   else:
                       pp=(event.x-pix)/(pjx-pix)
                       for j in range(len(zdyallfunction.duandian[self.smallest_index])-1):
                           if (zdyallfunction.duandian[self.smallest_index][j]-pp)*(zdyallfunction.duandian[self.smallest_index][j+1]-pp)<0:
                               zdyallfunction.ps=zdyallfunction.duandian[self.smallest_index][j]
                               zdyallfunction.pe=zdyallfunction.duandian[self.smallest_index][j+1]
                else:
                    zdyallfunction.ps=0
                    zdyallfunction.pe=1
            else:
                self.ufocus=0
                self.smallest_index=-1
            if self.smallest_index!=-1:
                self.create_line(pix+zdyallfunction.ps*(pjx-pix), piy+zdyallfunction.ps*(pjy-piy),
                  pix+zdyallfunction.pe*(pjx-pix), pjy+zdyallfunction.ps*(pjy-piy),
                  fill='orange',  # 红色
                  width=10,
                  dash=(2,2),tag=('choice')# 虚线
                  )

    #            zdyallfunction.drawuserM(self.smallest_index)
    #            self.showuserM()
            #用户已经选择好杆件，决定要对这个杆件断点
        else:
            i=self.smallest_index
            x=event.x
            y=event.y
            pix=self.relposition[i]['pix']
            piy=self.relposition[i]['piy']
            pjx=self.relposition[i]['pjx']
            pjy=self.relposition[i]['pjy']
            l=np.sqrt((pix-pjx)**2+(piy-pjy)**2)
            if self.relposition[i]['alp']==90 or self.relposition[i]['alp']==-90:
                    #point确定断点相对位置
                    point=np.round(abs((event.y-piy)/(pjy-piy)),1)
                    #如果断点不存在意味着增加，断点存在意味着删去
                    if point not in zdyallfunction.duandian[self.smallest_index]:
                        zdyallfunction.duandian[self.smallest_index].append(point)
                        zdyallfunction.duandian[self.smallest_index].sort()
                    else:
                        zdyallfunction.duandian[self.smallest_index].remove(point)
                        zdyallfunction.duandian[self.smallest_index].sort()
            else:
                point=abs(np.sqrt(((event.x-pix)**2+(event.y-piy)**2))/l)
                point=np.round(point,1)
                if point not in zdyallfunction.duandian[self.smallest_index]:
                    zdyallfunction.duandian[self.smallest_index].append(point)
                    zdyallfunction.duandian[self.smallest_index].sort()
                else:
                    zdyallfunction.duandian[self.smallest_index].remove(point)
                    zdyallfunction.duandian[self.smallest_index].sort()
            zdyallfunction.daduan=0
            self.smallest_index=-1
            self.ufocus=0
    #            zdyallfunction.drawuserM(self.smallest_index)
            for i in range(len(zdyallfunction.duandian)):
                for j in zdyallfunction.duandian[i]:
                    if j!=0 and j!=1:
                        xc=self.relposition[i]['pix']+j*(self.relposition[i]['pjx']-self.relposition[i]['pix'])
                        yc=self.relposition[i]['piy']+j*(self.relposition[i]['pjy']-self.relposition[i]['piy'])
                        circle_dimension=int(10/1800*height)
                        self.create_oval(xc-circle_dimension,yc-circle_dimension,
                                         xc+circle_dimension,yc+circle_dimension,tag='seperate_point',fill='red')
            self.paintline(zdyallfunction.c,c1.relposition)
    #            self.showuserM()
    
    
    
    def deletepaintline(self,tagname):
        self.delete(tagname)
    
    
    def paintline(self,user_moment_answer,relposition):
        self.delete('drawn_line')
        amplification_factor=30/1800*height
        for i in range(len(user_moment_answer)):
            cos=math.cos(math.pi*relposition[i]['alp']/180)
            sin=math.sin(math.pi*relposition[i]['alp']/180)
            for j in range(len(user_moment_answer[i])):
                a=(relposition[i]['pix']+user_moment_answer[i][j].ns*(relposition[i]['pjx']-relposition[i]['pix']))
                b=(relposition[i]['piy']+user_moment_answer[i][j].ns*(relposition[i]['pjy']-relposition[i]['piy']))
                c=(relposition[i]['pix']+user_moment_answer[i][j].ne*(relposition[i]['pjx']-relposition[i]['pix']))
                d=(relposition[i]['piy']+user_moment_answer[i][j].ne*(relposition[i]['pjy']-relposition[i]['piy']))
                
                
                length=pow((a-c)**2+(b-d)**2,0.5)

                #二维坐标变换函数(局部坐标系———>世界坐标系)
                def change_x(a,b,sin,cos,x,y):
                    return (x*cos+y*sin+a)
                def change_y(a,b,sin,cos,x,y):
                    return (y*cos-x*sin+b)   
                #判断弯矩图类型并绘制弯矩图
                #直线类型
                if (user_moment_answer[i][j].type=='l'):
                    x1=change_x(a,b,sin,cos,0,amplification_factor*user_moment_answer[i][j].Mi)
                    x3=change_x(a,b,sin,cos,length,amplification_factor*user_moment_answer[i][j].Mj)
                    y1=change_y(a,b,sin,cos,0,amplification_factor*user_moment_answer[i][j].Mi)
                    y3=change_y(a,b,sin,cos,length,amplification_factor*user_moment_answer[i][j].Mj)
                    self.create_line(x1,y1,x3,y3,fill='Green',tag='drawn_line',width=2)
                    
                    m1=0
                    
                    for x in range(0,int(length),8):
                        y2=(amplification_factor*(user_moment_answer[i][j].Mj-user_moment_answer[i][j].Mi)*x/length)+amplification_factor*user_moment_answer[i][j].Mi
                        self.create_line(change_x(a,b,sin,cos,m1,0),change_y(a,b,sin,cos,m1,0),change_x(a,b,sin,cos,m1,y2),change_y(a,b,sin,cos,m1,y2),fill='Green',tag='drawn_line',width=2)
                        m1=x
                    m1=int(length)
                    y2=(amplification_factor*(user_moment_answer[i][j].Mj-user_moment_answer[i][j].Mi)*x/length)+amplification_factor*user_moment_answer[i][j].Mi
                    self.create_line(change_x(a,b,sin,cos,m1,0),change_y(a,b,sin,cos,m1,0),change_x(a,b,sin,cos,m1,y2),change_y(a,b,sin,cos,m1,y2),fill='Green',tag='drawn_line',width=2)
                        
                #抛物线类型
                if (user_moment_answer[i][j].type=='p'):
                    x1=0
                    y1=user_moment_answer[i][j].Mi*amplification_factor
                    x2=0.5*length
                    y2=user_moment_answer[i][j].Mmid*amplification_factor
                    x3=length
                    y3=user_moment_answer[i][j].Mj*amplification_factor
                    m=x1
                    n=y1
                    a1=-(((y2-y3)*x1-(x2-x3)*y1+x2*y3-x3*y2)/((x2-x3)*(x1-x2)*(x1-x3)))
                    b1=((y2-y3)*(x1**2)+(x2**2)*y3-(x3**2)*y2-((x2**2)-(x3**2))*y1)/((x2-x3)*(x1-x2)*(x1-x3))
                    c1=((x2*y3-x3*y2)*(x1**2)-((x2**2)*y3-(x3**2)*y2)*x1+((x2**2)*x3-x2*(x3**2))*y1)/((x2-x3)*(x1-x2)*(x1-x3))
                    
                    for x in range(int(x1*100),int(x3*100),15):
                        x=0.01*x
                        y=a1*(x**2)+b1*x+c1
                        self.create_line(change_x(a,b,sin,cos,m,n),change_y(a,b,sin,cos,m,n),change_x(a,b,sin,cos,x,y),change_y(a,b,sin,cos,x,y),fill='Green',tag='drawn_line',width=2)
                        m=x
                        n=y
                        
                    m1=0
                    
                    for x in range(0,int(length),8):
                        y2=a1*(x**2)+b1*x+c1
                        self.create_line(change_x(a,b,sin,cos,m1,0),change_y(a,b,sin,cos,m1,0),change_x(a,b,sin,cos,m1,y2),change_y(a,b,sin,cos,m1,y2),fill='Green',tag='drawn_line',width=2)
                        m1=x
                    m1=int(length)
                    self.create_line(change_x(a,b,sin,cos,m1,0),change_y(a,b,sin,cos,m1,0),change_x(a,b,sin,cos,m1,y2),change_y(a,b,sin,cos,m1,y2),fill='Green',tag='drawn_line',width=2)


        




class Zuodacanvas(tkinter.Canvas):
    def __init__(self,master=None,**kw):
        tkinter.Canvas.__init__(self,master,**kw)
        self.b1=tkinter.Button(self,font=('Arial',3),width=1,height=1,bg='green')
        self.b2=tkinter.Button(self,font=('Arial',3),width=1,height=1,bg='green')
        self.b3=tkinter.Button(self,font=('Arial',3),width=1,height=1,bg='green')
        self.switchjiami=0
        self.dangwei=1
        self.positions=[]
        self.positions.append([0,0])
        self.positions.append([0,0])
        self.positions.append([0,0])
        self.b1.bind("<Button-1>", self.xFunc1)
        self.b2.bind("<Button-1>", self.xFunc2)
        self.b3.bind("<Button-1>", self.xFunc3) 
        self.magexist=0
       #f1，确定拖动点
    def f1(self,event):
    #        global x0,y0,dangwei,d
        x1=event.x_root
        y1=event.y_root
        print(x1,y1)
        #xw，yw界面的左上角在全屏的位置
        xw=self.winfo_rootx()
        yw=self.winfo_rooty()
        x=x1-xw-self.xli
        y=y1-yw-self.yli
    #    x=x1-xw-10-xli
    #    y=y1-46*sh/1800-yw-10-yli-34*sh/1800
        print('x1=%d,y1=%d'%(x1,y1))
        cos=np.cos(self.alp/180*3.14159)
        sin=np.sin(self.alp/180*3.14159)
        y_=x*sin+y*cos
        #不同档位，不同的捕捉方式
        if self.dangwei==1:
            y_=round(y_/self.d)*self.d
        if self.dangwei==0.5:
            y_=round(2*y_/self.d)/2*self.d
        if self.dangwei==0.25:
            y_=round(4*y_/self.d)/4*self.d
        x=y_*sin+self.xli
        y=y_*cos+self.yli
        event.widget.place(x=x,y=y,anchor='center')
        #显示弯矩控制点的相对大小（距离杆件的距离）
    #        global varnum
    #        varnum.set('%s'%(abs(y_/self.d)))
            #positions记录位置
        self.positions[0][0]=x
        self.positions[0][1]=y
        self.drawlines()
    #        if self.magexist==1:
        self.delete('mag')
        self.create_text(int(0.1*self.winfo_height()),int(0.1*self.winfo_height()),text=np.round(abs(y_/self.d)*4)/4,font=('Arial',15,'bold'),tag='mag')
    #        self.magexist=1
        
    #同理如上
    def f2(self,event):
        x1=event.x_root
        y1=event.y_root
        xw=self.winfo_rootx()
        yw=self.winfo_rooty()
        x=x1-xw-self.xli
        y=y1-yw-self.yli
    #    x=x1-xw-10-(xlj+xli)/2
    #    y=y1-46*sh/1800-yw-10-(ylj+yli)/2-34*sh/1800
        cos=np.cos(self.alp/180*3.14159)
        sin=np.sin(self.alp/180*3.14159)
        y_=x*sin+y*cos
        if self.dangwei==1:
            y_=round(y_/self.d)*self.d
        if self.dangwei==0.5:
            y_=round(2*y_/self.d)/2*self.d
        if self.dangwei==0.25:
            y_=round(4*y_/self.d)/4*self.d
        x=y_*sin+(self.xlj+self.xli)/2
        y=y_*cos+(self.ylj+self.yli)/2
        event.widget.place(x=x,y=y,anchor='center')
    #        global varnum
    #        varnum.set('%s'%(abs(y_/self.d)))
        self.positions[1][0]=x
        self.positions[1][1]=y  
        self.drawlines()
        self.delete('mag')
        self.num=abs(y_/self.d)
    #        if(abs(y_/self.d)==2.75):
    #            self.create_text(int(0.1*self.winfo_height()),int(0.1*self.winfo_height()),text='2.75',font=('Arial',15,'bold'),tag='mag')
        self.create_text(int(0.1*self.winfo_height()),int(0.1*self.winfo_height()),text=np.round(abs(y_/self.d)*4)/4,font=('Arial',15,'bold'),tag='mag')

    
    #同理如上    
    def f3(self,event):
        x1=event.x_root
        y1=event.y_root
        xw=self.winfo_rootx()
        yw=self.winfo_rooty()
        x=x1-xw-self.xli
        y=y1-yw-self.yli
    #    xw=win.winfo_x()
    #    yw=win.winfo_y()
    #    x=x1-xw-10-xlj
    #    y=y1-46*sh/1800-yw-10-ylj-34*sh/1800
        cos=np.cos(self.alp/180*3.14159)
        sin=np.sin(self.alp/180*3.14159)
        y_=x*sin+y*cos
        if self.dangwei==1:
            y_=round(y_/self.d)*self.d
        if self.dangwei==0.5:
            y_=round(2*y_/self.d)/2*self.d
        if self.dangwei==0.25:
            y_=round(4*y_/self.d)/4*self.d
        x=y_*sin+self.xlj
        y=y_*cos+self.ylj
        event.widget.place(x=x,y=y,anchor='center')
    #        global varnum
    #        varnum.set('%s'%(abs(y_/selfd)))
        self.positions[2][0]=x
        self.positions[2][1]=y  
        self.drawlines()
        self.delete('mag')
        self.num=abs(y_/self.d)
        self.create_text(int(0.1*self.winfo_height()),int(0.1*self.winfo_height()),text=np.round(abs(y_/self.d)*4)/4,font=('Arial',15,'bold'),tag='mag')
    
    
    
    
    
    #xFunc1第一个控制点的拖动
    def xFunc1(self,event):
        global x0,y0
        x0=event.x_root
        y0=event.y_root
        print(f"鼠标左键点击了一次坐标是:x={event.x_root}y={event.y_root}")
        #释放后，绑定另一个鼠标事件
        self.b1.bind("<ButtonRelease-1>", self.f1)
        #删去原来的图形
        for i in self.h:
            self.delete(i)
        
    #同理如上
    def xFunc2(self,event):
        global x0,y0
        x0=event.x_root
        y0=event.y_root
        print(f"鼠标左键点击了一次坐标是:x={event.x_root}y={event.y_root}")
        self.b2.bind("<ButtonRelease-1>", self.f2)    
        for i in self.h:
            self.delete(i)
        
    #同理如上  
    def xFunc3(self,event):
        global x0,y0
        x0=event.x_root
        y0=event.y_root
        print(f"鼠标左键点击了一次坐标是:x={event.x_root}y={event.y_root}")
        self.b3.bind("<ButtonRelease-1>", self.f3)
        for i in self.h:
            self.delete(i)
    
    
    
        
    
 
    def qualifypartner(self,x):
        self.partner=x
    def createbutton(self):
        self.b1=tkinter.Button(text='取半结构',font=('微软雅黑',1),bg='green')
        self.b1.pack()
    def zhixian(self):
#        print("smallest_index=")
#        print(smallest_index)
        temp=[]
        #标准答案的断点
        for a_ in zdyallfunction.a[self.partner.smallest_index]:
            if a_.ns not in temp:
                temp.append(a_.ns)
            if a_.ne not in temp:
                temp.append(a_.ne)
            temp.sort()
        #断点正确进行下一步
        if temp==zdyallfunction.duandian[self.partner.smallest_index]:
            self.delete(tkinter.ALL)
            self.choice='l'
            self.choiceelement=self.partner.smallest_index+1
    #            print(choice,choiceelement)
            self.cline()
            self.buttonposition()
            self.drawlines()
            global instructionpartexist
            if instructionpartexist==1:
                global inshelp4
                inshelp4=HELPTOPLEVEL(name='操作简介',ratio=1.6,picturename='instructionhelp4.jpg',dx=(sw-width)/2+0.5*width,dy=(sh-height*1.05)/2+0.5*height)
                inshelp4.bind()
        else:
            tkinter.messagebox.showinfo(title='提示', message='断点有误，请改正,请先在集中力处打断杆件，再作答')
            if instructionpartexist==1:
                global inshelp3
                inshelp3=HELPTOPLEVEL(name='操作简介',ratio=1.6,picturename='instructionhelp3.jpg',dx=(sw-width)/2,dy=(sh-height*1.05)/2)
                inshelp3.bind()
    def quxian(self):
        temp=[]
        #标准答案的断点
        for a_ in zdyallfunction.a[self.partner.smallest_index]:
            if a_.ns not in temp:
                temp.append(a_.ns)
            if a_.ne not in temp:
                temp.append(a_.ne)
            temp.sort()
        #断点正确进行下一步
        if temp==zdyallfunction.duandian[self.partner.smallest_index]:
            self.delete(tkinter.ALL)
            self.choice='p'
            self.choiceelement=self.partner.smallest_index+1
    #            print(choice,choiceelement)
            self.cline()
            self.buttonposition()
            self.drawlines()
#            global instructionpartexist
            if instructionpartexist==1:
                global inshelp5
                inshelp5=HELPTOPLEVEL(name='操作简介',ratio=1.6,picturename='instructionhelp5.jpg',dx=(sw-width)/2,dy=(sh-height*1.05)/2)
                inshelp5.bind()
        else:
            tkinter.messagebox.showinfo(title='提示', message='断点有误，请改正,请先在集中力处打断杆件，再作答')
#            global instructionpartexist
            if instructionpartexist==1:
                global inshelp3
                inshelp3=HELPTOPLEVEL(name='操作简介',ratio=1.6,picturename='instructionhelp3.jpg',dx=(sw-width)/2,dy=(sh-height*1.05)/2)
                inshelp3.bind()
                destroy_inshelp()
    def buttonposition(self):
        if self.choice=='l':
            self.b1.place(x=self.xi,y=self.yi,anchor='nw')
            self.b2.place(x=1000,y=1000,anchor='nw')
            self.b3.place(x=self.xj,y=self.yj,anchor='nw') 
        else:
            self.b1.place(x=self.xi,y=self.yi,anchor='nw')
            self.b2.place(x=self.xmid,y=self.ymid,anchor='nw')
            self.b3.place(x=self.xj,y=self.yj,anchor='nw') 
        
        self.positions[0][0]=int(self.b1.place_info()['x'])
        self.positions[0][1]=int(self.b1.place_info()['y'])
        self.positions[1][0]=int(self.b2.place_info()['x'])
        self.positions[1][1]=int(self.b2.place_info()['y'])
        self.positions[2][0]=int(self.b3.place_info()['x'])
        self.positions[2][1]=int(self.b3.place_info()['y'])
    
    def drawlines(self):
        self.h=[]
        h_=self.create_line(self.xli,self.yli,
                           self.positions[0][0],self.positions[0][1],
                           fill='blue',
                           width=2)
        self.h.append(h_)
        #曲线拟合
        if self.choice=='p': 
            x=[self.positions[0][0],self.positions[1][0],self.positions[2][0]]
            x=np.array(x)
            y=[self.positions[0][1],self.positions[1][1],self.positions[2][1]]
            y=np.array(y)
            cos=np.cos(self.alp/180*3.14159)
            sin=np.sin(self.alp/180*3.14159) 
            x_=x*cos-y*sin
            y_=x*sin+y*cos
            maxx=max(x_)
            minx=min(x_)
            maxy=max(y_)
            miny=min(y_)
            def nihe():
                x=[self.positions[0][0],self.positions[1][0],self.positions[2][0]]
                x=np.array(x)
                y=[self.positions[0][1],self.positions[1][1],self.positions[2][1]]
                y=np.array(y)
                x_=x*cos-y*sin
                y_=x*sin+y*cos
                f1 = np.polyfit(x_, y_,2)
                return(f1)
            ff=nihe()
            x_=np.arange(minx, maxx, 1)
            y_=ff[0]*x_**2+ff[1]*x_+ff[2]
            x=x_*cos+y_*sin
            y=y_*cos-x_*sin
            for i in range(len(x)-1):
                h_=self.create_line(x[i],y[i],
                           x[i+1],y[i+1],
                           fill='blue',
                           width=2)
                self.h.append(h_)
                
        if self.choice=='l':
            h_=self.create_line(self.positions[0][0],self.positions[0][1],
                           self.positions[2][0],self.positions[2][1],
                           fill='blue',
                           width=2)
            self.h.append(h_) 
        
    #    
        h_=self.create_line(self.xlj,self.ylj,
                           self.positions[2][0],self.positions[2][1],
                           fill='blue',
                           width=2)
        self.h.append(h_)

    def cline(self):
        #st记录线的编号
        st=[]
        #    global xi,yi,xj,yj,xmid,ymid,d,choiceelement
        self.alp=zdyallfunction.elements[self.choiceelement-1]['alp']
        print(self.choiceelement)
        print(self.alp)
    #        global switchjiami
        #sl轴线的长度，比对角线长
        sl=1500
        #d控制轴线之间的距离
        self.d=self.winfo_height()/12
        d=self.d
        bc=self.winfo_height()
        while(self.alp>90 ):
            self.alp=self.alp-180
        while(self.alp<-90):
            self.alp=self.alp+180
        cos=np.cos(self.alp/180*3.14159)
        sin=np.sin(self.alp/180*3.14159)  
        if 0<=self.alp<=45:
            #在选取原点之上的轴线个数为ns，在选取原点之下的轴线个数为ne
            #不同角度，原点不同，可能为左下，可能为右上，可能为左上
            ns=bc/d*cos
            nx=bc/d*sin 
            #n取个比较中心的轴线，在上面画杆件
            n=np.round((ns-nx)/2)          
            if self.alp<30:
                #画杆件
                st_=self.create_line(d*cos,bc-n*d/cos-d*sin,
                               (d+bc/1.5)*cos,bc-n*d/cos-((d+bc/1.5)*sin),
                              fill='black',
                               width=4)
                st.append(st_)
                #确定3个控制点的坐标，在self里的坐标
                self.xi=d*cos-d*sin
                self.yi=bc-n*d/cos-d*sin-d*cos
                self.xj=(d+bc/1.5)*cos-d*sin
                self.yj=bc-n*d/cos-(d+bc/1.5)*sin-d*cos
                self.xmid=(d+bc/3)*cos+d*sin
                self.ymid=(bc-n*d/cos-(d+bc/3)*sin)+d*cos
            elif 30<=self.alp<40:
                st_=self.create_line(3*d*cos,bc-n*d/cos-3*d*sin,
                               (3*d+bc/1.5)*cos,bc-n*d/cos-((3*d+bc/1.5)*sin),
                              fill='black',
                               width=4)
                st.append(st_)
                self.xi=3*d*cos-d*sin
                self.yi=bc-n*d/cos-3*d*sin-d*cos
                self.xj=(3*d+bc/1.5)*cos-d*sin
                self.yj=bc-n*d/cos-(3*d+bc/1.5)*sin-d*cos
                self.xmid=(d+bc/3)*cos+3*d*sin
                self.ymid=(bc-n*d/cos-(3*d+bc/3)*sin)+d*cos
            else:
                st_=self.create_line(4*d*cos,bc-n*d/cos-4*d*sin,
                               (4*d+bc/1.5)*cos,bc-n*d/cos-((4*d+bc/1.5)*sin),
                              fill='black',
                               width=4)
                st.append(st_)
                self.xi=4*d*cos-d*sin
                self.yi=bc-n*d/cos-4*d*sin-d*cos
                self.xj=(4*d+bc/1.5)*cos-d*sin
                self.yj=bc-n*d/cos-(4*d+bc/1.5)*sin-d*cos
                self.xmid=(d+bc/3)*cos+4*d*sin
                self.ymid=(bc-n*d/cos-(4*d+bc/3)*sin)+d*cos
            st_=self.create_line(0, bc,
                                   sl*cos, bc-sl*sin,
                                   fill='red',  
                                   dash=(4, 4)  
                                   )
            st.append(st_)
            #画轴线
            for i in range(1,15):
                st_=self.create_line(0, bc-d*i/cos,
                                   sl*cos, bc-d*i/cos-sl*sin,
                                   fill='red',  
                                   dash=(4, 4)  
                                   )
                st.append(st_)
                st_=self.create_line(0, bc+d*i/cos,
                                   sl*cos, bc+d*i/cos-sl*sin,
                                   fill='red',  
                                   dash=(4, 4)  
                                   )
                st.append(st_)
                #加密轴线
                if self.switchjiami:
                    st_=self.create_line(0, bc-d*(i-0.5)/cos,
                                       sl*cos, bc-d*(i-0.5)/cos-sl*sin,
                                       fill='blue',  
                                       dash=(4, 4)  
                                       )
                    st.append(st_)
                    st_=self.create_line(0, bc+d*(i-0.5)/cos,
                                       sl*cos, bc+d*(i-0.5)/cos-sl*sin,
                                       fill='blue',  
                                       dash=(4, 4)  
                                       )
                    st.append(st_)
    
        if 45<self.alp<=90:
            ns=bc/d*sin
            nx=bc/d*cos
            n=np.round((ns-nx)/2)   
            if self.alp>60:
                st_=self.create_line(bc-d/sin*n-d*cos,d*sin,
                               bc-d/sin*n-(d+bc/1.5)*cos,(d+bc/1.5)*sin,
                                fill='black',
                                width=4)
                st.append(st_)
                self.xj=bc-d/sin*n-d*cos-d*sin
                self.yj=d*sin-d*cos
                self.xi=bc-d/sin*n-(d+bc/1.5)*cos-d*sin
                self.yi=(d+bc/1.5)*sin-d*cos
                self.xmid=bc-d/sin*n-(d+bc/3)*cos+d*sin
                self.ymid=(d+bc/3)*sin+d*cos
            elif 50<self.alp<60:
                st_=self.create_line(bc-d/sin*n-3*d*cos,3*d*sin,
                               bc-d/sin*n-(3*d+bc/1.5)*cos,(3*d+bc/1.5)*sin,
                                fill='black',
                                width=4)
                st.append(st_)
                self.xj=bc-d/sin*n-3*d*cos-d*sin
                self.yj=3*d*sin-d*cos
                self.xi=bc-d/sin*n-(3*d+bc/1.5)*cos-d*sin
                self.yi=(3*d+bc/1.5)*sin-d*cos
                self.xmid=bc-d/sin*n-(3*d+bc/3)*cos+d*sin
                self.ymid=(3*d+bc/3)*sin+d*cos
            else:
                st_=self.create_line(bc-d/sin*n-4*d*cos,4*d*sin,
                               bc-d/sin*n-(4*d+bc/1.5)*cos,(4*d+bc/1.5)*sin,
                                fill='black',
                                width=4)
                st.append(st_)
                self.xj=bc-d/sin*n-4*d*cos-d*sin
                self.yj=4*d*sin-d*cos
                self.xi=bc-d/sin*n-(4*d+bc/1.5)*cos-d*sin
                self.yi=(4*d+bc/1.5)*sin-d*cos
                self.xmid=bc-d/sin*n-(4*d+bc/3)*cos+d*sin
                self.ymid=(4*d+bc/3)*sin+d*cos
            st_=self.create_line(bc, 0,
                                   bc-sl*cos, sl*sin,
                                   fill='red',  
                                   dash=(4, 4)  
                                   )
            st.append(st_)  
            for i in range(1,15):
                st_=self.create_line(bc-d*i/sin, 0,
                                   bc-d*i/sin-sl*cos, sl*sin,
                                   fill='red',  
                                   dash=(4, 4)  
                                   )
                st.append(st_)
                st_=self.create_line(bc+d*i/sin, 0,
                                   bc+d*i/sin-sl*cos, sl*sin,
                                   fill='red',  
                                   dash=(4, 4)  
                                   )
                st.append(st_)
                if self.switchjiami:
                    st_=self.create_line(bc-d*(i-0.5)/sin, 0,
                                   bc-d*(i-0.5)/sin-sl*cos, sl*sin,
                                   fill='blue',  
                                   dash=(4, 4)  
                                   )
                    st.append(st_)
                    st_=self.create_line(bc+d*(i-0.5)/sin, 0,
                                   bc+d*(i-0.5)/sin-sl*cos, sl*sin,
                                   fill='blue',  
                                   dash=(4, 4)  
                                   )
                    st.append(st_)
                
                
                
        if -45<=self.alp<0:
            ns=bc/d*sin*-1
            nx=bc/d*cos
            n=np.round((ns-nx)/2)
            if self.alp>-20:
                st_=self.create_line(d*cos,d*-1*sin-n*d/cos,
                                       (d+bc/1.5)*cos,(d+bc/1.5)*-1*sin-n*d/cos,
                                       fill='black',
                                       width=4)
                st.append(st_)
                self.xi=d*cos-d*sin
                self.yi=d*-1*sin-n*d/cos-d*cos
                self.xj=(d+bc/1.5)*cos-d*sin
                self.yj=(d+bc/1.5)*-1*sin-n*d/cos-d*cos
                self.xmid=(d+bc/3)*cos+d*sin
                self.ymid=(d+bc/3)*-1*sin-n*d/cos+d*cos
            elif -40<self.alp<=-20:
                st_=self.create_line(3*d*cos,3*d*-1*sin-n*d/cos,
                                       (3*d+bc/1.5)*cos,(3*d+bc/1.5)*-1*sin-n*d/cos,
                                       fill='black',
                                       width=4)
                st.append(st_)
                self.xi=3*d*cos-d*sin
                self.yi=3*d*-1*sin-n*d/cos-d*cos
                self.xj=(3*d+bc/1.5)*cos-d*sin
                self.yj=(3*d+bc/1.5)*-1*sin-n*d/cos-d*cos
                self.xmid=(3*d+bc/3)*cos+d*sin
                self.ymid=(3*d+bc/3)*-1*sin-n*d/cos+d*cos
            else:
                st_=self.create_line(4*d*cos,4*d*-1*sin-n*d/cos,
                                       (4*d+bc/1.5)*cos,(4*d+bc/1.5)*-1*sin-n*d/cos,
                                       fill='black',
                                       width=4)
                st.append(st_)
                self.xi=4*d*cos-d*sin
                self.yi=4*d*-1*sin-n*d/cos-d*cos
                self.xj=(4*d+bc/1.5)*cos-d*sin
                self.yj=(4*d+bc/1.5)*-1*sin-n*d/cos-d*cos
                self.xmid=(4*d+bc/3)*cos+d*sin
                self.ymid=(4*d+bc/3)*-1*sin-n*d/cos+d*cos
            st_=self.create_line(0,0,
                                   sl*cos,-sl*sin,
                                   fill='red',  
                                   dash=(4, 4))
            st.append(st_)
            for i in range(1,15):
                st_=self.create_line(0,d/cos*i,
                                   sl*cos,d/cos*i-sl*sin,
                                   fill='red',  
                                   dash=(4, 4))
                st.append(st_)
                st_=self.create_line(0,-d/cos*i,
                                   sl*cos,-d/cos*i-sl*sin,
                                   fill='red',  
                                   dash=(4, 4))
                st.append(st_)
                if self.switchjiami:
                    st_=self.create_line(0,d/cos*(i-0.5),
                                       sl*cos,d/cos*(i-0.5)-sl*sin,
                                       fill='blue',  
                                       dash=(4, 4))
                    st.append(st_)
                    st_=self.create_line(0,-d/cos*(i-0.5),
                                       sl*cos,-d/cos*(i-0.5)-sl*sin,
                                       fill='blue',  
                                       dash=(4, 4))
                    st.append(st_)
                
        if -90<=self.alp<-45:
            ns=bc/d*sin*-1
            nx=bc/d*cos
            n=np.round((ns-nx)/2)
            if self.alp<-60:
                st_=self.create_line(d*n/sin*-1+d*cos,d*sin*-1,
                                       d*n/sin*-1+(d+bc/1.5)*cos,(d+bc/1.5)*sin*-1,
                                       fill='black',
                                       width=4)
                st.append(st_)
                self.xi=d*n/sin*-1+d*cos-d*sin
                self.yi=d*sin*-1-d*cos
                self.xj=d*n/sin*-1+(d+bc/1.5)*cos-d*sin
                self.yj=(d+bc/1.5)*sin*-1-d*cos
                self.xmid=d*n/sin*-1+(d+bc/3)*cos+d*sin
                self.ymid=(d+bc/3)*sin*-1+d*cos
            elif -60<=self.alp<-50:
                st_=self.create_line(d*n/sin*-1+3*d*cos,3*d*sin*-1,
                                       d*n/sin*-1+(3*d+bc/1.5)*cos,(3*d+bc/1.5)*sin*-1,
                                       fill='black',
                                       width=4)
                st.append(st_)
                self.xi=d*n/sin*-1+3*d*cos-d*sin
                self.yi=3*d*sin*-1-d*cos
                self.xj=d*n/sin*-1+(3*d+bc/1.5)*cos-d*sin
                self.yj=(3*d+bc/1.5)*sin*-1-d*cos
                self.xmid=d*n/sin*-1+(3*d+bc/3)*cos+d*sin
                self.ymid=(3*d+bc/3)*sin*-1+d*cos
            else:
                st_=self.create_line(d*n/sin*-1+4*d*cos,4*d*sin*-1,
                                       d*n/sin*-1+(4*d+bc/1.5)*cos,(4*d+bc/1.5)*sin*-1,
                                       fill='black',
                                       width=4)
                st.append(st_)
                self.xi=d*n/sin*-1+4*d*cos-d*sin
                self.yi=4*d*sin*-1-d*cos
                self.xj=d*n/sin*-1+(4*d+bc/1.5)*cos-d*sin
                self.yj=(4*d+bc/1.5)*sin*-1-d*cos
                self.xmid=d*n/sin*-1+(4*d+bc/3)*cos+d*sin
                self.ymid=(4*d+bc/3)*sin*-1+d*cos
            st_=self.create_line(0,0,
                                   sl*cos,-sl*sin,
                                   fill='red',  
                                   dash=(4, 4),
                                   )
            st.append(st_)
            for i in range(1,15):
                st_=self.create_line(d/sin*-1*i,0,
                                   d/sin*-1*i+sl*cos,sl*sin*-1,
                                   fill='red',  
                                   dash=(4, 4))
                st.append(st_)
                st_=self.create_line(d/sin*i,0,
                                   d/sin*i+sl*cos,sl*sin*-1,
                                   fill='red',  
                                   dash=(4, 4))
                st.append(st_)
                if self.switchjiami:
                    st_=self.create_line(d/sin*-1*(i-0.5),0,
                                       d/sin*-1*(i-0.5)+sl*cos,sl*sin*-1,
                                       fill='blue',  
                                       dash=(4, 4))
                    st.append(st_)
                    st_=self.create_line(d/sin*(i-0.5),0,
                                       d/sin*(i-0.5)+sl*cos,sl*sin*-1,
                                       fill='blue',  
                                       dash=(4, 4))
                    st.append(st_)
        #i端和j端在杆线上的投影位置
        self.xli=self.xi+d*sin
        self.yli=self.yi+d*cos
        self.xlj=self.xj+d*sin
        self.ylj=self.yj+d*cos





















global cellwidth
cellwidth=int(120/1800*sh)
global cellheight
cellheight=int(50/1800*sh)



global managemode,zdymode
managemode=0
zdymode=0

global zdytimumodeexist,zdytishimodeexist,zdyceshimodeexist
zdytimumodeexist=0
zdytishimodeexist=0
zdyceshimodeexist=0
global hostname,softwareversion
hostname=socket.gethostname()
softwareversion=2

global newofferquestion
newofferquestion=1

def register():
    tp = tkinter.Toplevel()
    tp.title('注册界面')
    tp.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
    tp.geometry('%dx%d+%d+%d'%(0.4*width,0.7*height,dx,dy))
    frame=tkinter.Frame(tp,width=0.2*width,height=0.5*height)
    frame.place(x=0.02*width,y=0.05*height)
    
    register_userID_lable=tkinter.Label(frame,text='账户名: ',font=('微软雅黑',12))
    
    register_userID_entry=tkinter.Entry(frame,width=20)
    def checkuserID(event):
        #        engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        #        sql = "select * from basic_infor where userID='%s'"%(register_userID_entry.get())
        #        df = pd.read_sql_query(sql, engine)
        #        if len(df)>0:
        #            tkinter.messagebox.showinfo(title='提示', message='此账户已存在！')
        #            return

        for ch in register_userID_entry.get():
            if u'\u4e00' <= ch <= u'\u9fff':
                register_userID_entry.config(fg='red')
                tkinter.messagebox.showinfo(title='提示', message='账户名必须是数字与字母组合！')
                return 
        if register_userID_entry.get().isalnum()==False or register_userID_entry.get().isdigit()==True or register_userID_entry.get().isalpha():

            register_userID_entry.config(fg='red')
            tkinter.messagebox.showinfo(title='提示', message='账户名必须是数字与字母组合！')
        else:
            register_userID_entry.config(fg='black')
    def inituserID(event):
        register_userID_entry.config(fg='black')
    register_userID_entry.bind('<FocusOut>',checkuserID)
    register_userID_entry.bind('<FocusIn>',inituserID)
    register_userID_notice=tkinter.Label(frame,text='账户名为字母与数字组合',font=('微软雅黑',8),fg='red')
    lspace1=tkinter.Label(frame,text='    ')
    lspace2=tkinter.Label(frame,text='    ')
    lspace3=tkinter.Label(frame,text='    ')
    lspace4=tkinter.Label(frame,text='    ')
    lspace5=tkinter.Label(frame,text='    ')
    lspace6=tkinter.Label(frame,text='    ')
    lspace7=tkinter.Label(frame,text='    ')
    
    def checkpassward(event):
        print(register_passwardcomfirm_entry.get())
        print(register_passward_entry.get())
        if register_passwardcomfirm_entry.get()!=register_passward_entry.get():
            tkinter.messagebox.showinfo(title='提示', message='两次密码输入不一致！')
    register_passward_lable=tkinter.Label(frame,text='密码: ',font=('微软雅黑',12))
    register_passward_entry=tkinter.Entry(frame,width=20)
    register_passwardconfirm_lable=tkinter.Label(frame,text='确认密码: ',font=('微软雅黑',12))
    register_passwardcomfirm_entry=tkinter.Entry(frame,width=20)

    register_passwardcomfirm_entry.bind('<FocusOut>',checkpassward)
    
    register_nickname_lable=tkinter.Label(frame,text='昵称: ',font=('微软雅黑',12))
    register_nickname_entry=tkinter.Entry(frame,width=20)
    register_identity_lable=tkinter.Label(frame,text='身份: ',font=('微软雅黑',12))
    register_identity_cmb= ttk.Combobox(frame)
    register_identity_cmb['value'] = ('学生','老师','其他')
    register_identity_cmb.current(0)
    register_school_lable=tkinter.Label(frame,text='学校: ',font=('微软雅黑',12))
    register_school_entry=tkinter.Entry(frame,width=20)
    register_school_notice=tkinter.Label(frame,text='请将学校名称填写完整以便您参加排行榜',font=('微软雅黑',8),fg='red')
    register_grade_lable=tkinter.Label(frame,text='年级: ',font=('微软雅黑',12))
    register_grade_cmb= ttk.Combobox(frame)
    register_grade_cmb['value'] = ('其他','大一','大二','大三','大四','研究生')
    register_grade_cmb.current(0)
    register_mail_lable=tkinter.Label(frame,text='邮箱: ',font=('微软雅黑',12))
    register_mail_entry=tkinter.Entry(frame,width=20)
    def qualifyregister():
        
        for ch in register_userID_entry.get():
            if u'\u4e00' <= ch <= u'\u9fff':
                register_userID_entry.config(fg='red')
                tkinter.messagebox.showinfo(title='提示', message='账户名必须是数字与字母组合！')
                return 
        if register_userID_entry.get().isalnum()==False or register_userID_entry.get().isdigit()==True or register_userID_entry.get().isalpha()==True:
            register_userID_entry.config(fg='red')
            tkinter.messagebox.showinfo(title='提示', message='账户名必须是数字与字母组合！')
            return
        if register_passwardcomfirm_entry.get()!=register_passward_entry.get():
            tkinter.messagebox.showinfo(title='提示', message='两次密码输入不一致！')
            return
        if len(register_nickname_entry.get())==0 or len(register_school_entry.get())==0 or len(register_mail_entry.get())==0:
            tkinter.messagebox.showinfo(title='提示', message='基本信息不可为空！')
            return

        engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        sql = "select * from basic_infor where userID='%s'"%(register_userID_entry.get())
        df = pd.read_sql_query(sql, engine)
        if len(df)>0:
            tkinter.tkinter.messagebox.showinfo(title='提示', message='此账户已存在！')
            return
        df=pd.DataFrame(np.zeros((1,9)))
        df.iloc[0,0]=register_userID_entry.get()
        df.iloc[0,1]=register_passward_entry.get()
        df.iloc[0,2]=register_nickname_entry.get()
        df.iloc[0,3]=register_identity_cmb.get()
        df.iloc[0,4]=register_school_entry.get()
        df.iloc[0,5]=register_grade_cmb.get()
        df.iloc[0,6]=register_mail_entry.get()
        df.iloc[0,7]=softwareversion
        df.iloc[0,8]=hostname
        df.columns=['userID','passward','nickname','identity','school','grade','mail','softwareversion','equipment']
        df.to_sql('basic_infor', engine, index= False,if_exists='append')
        df=pd.DataFrame(np.zeros((1,4)))
        df.iloc[0,0]=register_userID_entry.get()
        df.iloc[0,1]=0
        df.iloc[0,2]=0
        df.iloc[0,3]=0
        df.columns=['userID','levelcredits','honorcredits','totaltime']
        df.to_sql('achievements', engine, index= False,if_exists='append')
        tkinter.messagebox.showinfo(title='提示', message='注册成功！')
        tp.destroy()
        
    register_qualify_button=tkinter.Button(frame,text='确认注册',font=('微软雅黑',12),command=qualifyregister)
    
    register_userID_lable.grid(row=0,column=0)
    register_userID_entry.grid(row=0,column=1)
    register_userID_notice.grid(row=0,column=2)
    lspace1.grid(row=1,column=0)
    register_passwardconfirm_lable.grid(row=4,column=0)
    register_passwardcomfirm_entry.grid(row=4,column=1)
    
    register_passward_lable.grid(row=2,column=0)
    register_passward_entry.grid(row=2,column=1)
    lspace2.grid(row=3,column=0)
    register_nickname_lable.grid(row=6,column=0)
    register_nickname_entry.grid(row=6,column=1)
    lspace3.grid(row=5,column=0)
    register_identity_lable.grid(row=8,column=0)
    register_identity_cmb.grid(row=8,column=1)
    lspace4.grid(row=7,column=0)
    register_school_lable.grid(row=10,column=0)
    register_school_entry.grid(row=10,column=1)
    register_school_notice.grid(row=10,column=2)
    lspace5.grid(row=9,column=0)
    register_grade_lable.grid(row=12,column=0)
    register_grade_cmb.grid(row=12,column=1)
    lspace6.grid(row=11,column=0)
    register_mail_lable.grid(row=14,column=0)
    register_mail_entry.grid(row=14,column=1)
    lspace7.grid(row=13,column=0)
    register_qualify_button.grid(row=15,column=1)
    

login_frame=tkinter.Frame(win,width=0.2*width,height=0.3*height)
login_frame.place(x=0.1*width,y=0.5*height)
login_userID_lable=tkinter.Label(login_frame,text='账户名: ',font=('微软雅黑',12))
login_userID_entry=tkinter.Entry(login_frame,width=20)
login_passward_lable=tkinter.Label(login_frame,text='密码: ',font=('微软雅黑',12))
login_passward_entry=tkinter.Entry(login_frame,width=20,show='*')

lspace1=tkinter.Label(login_frame,text='  ')
lspace2=tkinter.Label(login_frame,text='  ')
def qualifylogin():
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    sql = "select * from basic_infor where userID='%s'"%(login_userID_entry.get())
    df2 = pd.read_sql_query(sql, engine)
    if len(df2)==0:
        tkinter.messagebox.showinfo(title='提示', message='不存在此账户')
        return 
    else:
        engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        sql = "select * from word "
        df = pd.read_sql_query(sql, engine)
        version=df.loc[0,'version']
        if float(version)!=softwareversion:
            tkinter.messagebox.showinfo(title='提示', message='请先下载最新版再登录')
            return
        
    #    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    #    sql = "select * from word "
    #    df = pd.read_sql_query(sql, engine)
    #    if len(df)!=0:
    #        tkinter.messagebox.showinfo(title='提示', message=df.iloc[0,0])
    #        return
    
    global logintime
    logintime=time.time()
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(logintime))
    if df2.loc[0,'passward']!=login_passward_entry.get():
        tkinter.messagebox.showinfo(title='提示', message='密码有误，请重新输入！')
        return
    if df2.loc[0,'passward']==login_passward_entry.get():
        print('1234566')
        tkinter.messagebox.showinfo(title='提示', message='登录成功')
        
        global userID,nickname
        userID=df2.loc[0,'userID']
        nickname=df2.loc[0,'nickname']
        zdyallfunction.userID=userID
        zdyallfunction.nickname=nickname
        zdyallfunction.school=df2.loc[0,'school']
        zdyallfunction.setbasicinfor(nickname,userID)

        if df2.loc[0,'equipment']!=hostname:
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update basic_infor set equipment='%s' where userID='%s'"%(hostname,login_userID_entry.get())
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
        df=pd.DataFrame(np.zeros((1,3)))
        df.iloc[0,0]=userID
        df.iloc[0,1]=dt
        df.columns=['userID','logintime','duration']
        engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        df.to_sql('enter_record', engine, index= False,if_exists='append')
        win.withdraw()

        modechoice()
        
def qualifylogin2(event):
    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    sql = "select * from basic_infor where userID='%s'"%(login_userID_entry.get())
    df2 = pd.read_sql_query(sql, engine)
    if len(df2)==0:
        tkinter.messagebox.showinfo(title='提示', message='不存在此账户')
        return 
    else:
        engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        sql = "select * from word "
        df = pd.read_sql_query(sql, engine)
        version=df.loc[0,'version']
        if float(version)!=softwareversion:
            tkinter.messagebox.showinfo(title='提示', message='请先下载最新版再登录')
            return
        
    #    engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
    #    sql = "select * from word "
    #    df = pd.read_sql_query(sql, engine)
    #    if len(df)!=0:
    #        tkinter.messagebox.showinfo(title='提示', message=df.iloc[0,0])
    #        return
    
    global logintime
    logintime=time.time()
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(logintime))
    if df2.loc[0,'passward']!=login_passward_entry.get():
        tkinter.messagebox.showinfo(title='提示', message='密码有误，请重新输入！')
        return
    if df2.loc[0,'passward']==login_passward_entry.get():
        tkinter.messagebox.showinfo(title='提示', message='登录成功')
        
        global userID,nickname
        userID=df2.loc[0,'userID']
        nickname=df2.loc[0,'nickname']
        zdyallfunction.userID=userID
        zdyallfunction.nickname=nickname
        zdyallfunction.school=df2.loc[0,'school']
        zdyallfunction.setbasicinfor(nickname,userID)

        if df2.loc[0,'equipment']!=hostname:
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update basic_infor set equipment='%s' where userID='%s'"%(hostname,login_userID_entry.get())
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
        df=pd.DataFrame(np.zeros((1,3)))
        df.iloc[0,0]=userID
        df.iloc[0,1]=dt
        df.columns=['userID','logintime','duration']
        engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        df.to_sql('enter_record', engine, index= False,if_exists='append')
        win.withdraw()
        modechoice()


def findpassward():
    global hostname
    
    
    def resetpassward():
        
        def updatepassward():
            if find_passward_entry.get()!=find_passwardcomfirm_entry.get():
                tkinter.messagebox.showinfo(title='提示', message='两次密码输入不一致请重新输入！')
                return 0
            try:
                conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
                cursor = conn.cursor()
                sql="update basic_infor set passward='%s' where userID='%s'"%(find_passward_entry.get(),tempuserID)
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                tp.destroy()
                tkinter.messagebox.showinfo(title='提示', message='修改密码成功!')
            except:
                tkinter.messagebox.showinfo(title='提示', message='修改密码失败!')
                
            
    
        tp = tkinter.Toplevel()
        tp.title('找回密码')
        tp.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp.geometry('%dx%d+%d+%d'%(0.25*width,0.4*height,dx,dy))
        frame=tkinter.Frame(tp,width=0.2*width,height=0.4*height)
        frame.place(x=0.05*width,y=0.05*height)
        find_passward_lable=tkinter.Label(frame,text='密码: ',font=('微软雅黑',12))
        l1=tkinter.Label(frame,text='   ')
        find_passward_entry=tkinter.Entry(frame,width=20)
        l2=tkinter.Label(frame,text='   ')
        find_passwardconfirm_lable=tkinter.Label(frame,text='确认密码: ',font=('微软雅黑',12))
        l3=tkinter.Label(frame,text='   ')
        find_passwardcomfirm_entry=tkinter.Entry(frame,width=20)
        l4=tkinter.Label(frame,text='   ')
        find_passward_Button=tkinter.Button(frame,text="确认修改",font=('微软雅黑',12),command=updatepassward)
        find_passward_lable.grid(row=0,column=0)
        l1.grid(row=1,column=0)
        find_passward_entry.grid(row=2,column=0)
        l2.grid(row=3,column=0)
        find_passwardconfirm_lable.grid(row=4,column=0)
        l3.grid(row=5,column=0)
        find_passwardcomfirm_entry.grid(row=6,column=0)
        l4.grid(row=7,column=0)
        find_passward_Button.grid(row=8,column=0)
        
        
    def verificationequipment():
        engine=create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        sql="select * from basic_infor where userID='%s'"%findpassward_userID_entry.get()
        df=pd.read_sql_query(sql, engine)
        if len(df)==0:
            tkinter.messagebox.showinfo(title='提示', message='账户不存在！')
            return 0
        if df.loc[0,'equipment']==hostname:
            global tempuserID
            tempuserID=df.loc[0,'userID']
            tp.destroy()
            resetpassward()
            tkinter.messagebox.showinfo(title='提示', message='设备验证成功!')
        else:
            tkinter.messagebox.showinfo(title='提示', message='设备验证失败!')
    tp = tkinter.Toplevel()
    tp.title('找回密码')
    tp.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
    tp.geometry('%dx%d+%d+%d'%(0.25*width,0.25*height,dx,dy))
    frame=tkinter.Frame(tp,width=0.2*width,height=0.5*height)
    frame.place(x=0.05*width,y=0.05*height)
    l1=tkinter.Label(frame,text='   ')
    findpassawrd_userID_lable=tkinter.Label(frame,text='账户名: ',font=('微软雅黑',12))
    findpassward_userID_entry=tkinter.Entry(frame,width=20)
    l2=tkinter.Label(frame,text='   ')
    findpassward_verification_Button=tkinter.Button(frame,text="进行设备验证",font=('微软雅黑',12),command=verificationequipment)
    findpassawrd_userID_lable.grid(row=0,column=0)
    l1.grid(row=1,column=0)
    findpassward_userID_entry.grid(row=2,column=0)
    l2.grid(row=3,column=0)
    findpassward_verification_Button.grid(row=4,column=0)







login_passward_entry.bind('<Return>',qualifylogin2)
        
    
login_qualify_button=tkinter.Button(login_frame,text='确认登录',command=qualifylogin)
login_userID_lable.grid(row=0,column=0)
login_userID_entry.grid(row=0,column=1)
lspace1.grid(row=1,column=0)
login_passward_lable.grid(row=2,column=0)
login_passward_entry.grid(row=2,column=1)
lspace2.grid(row=3,column=0)
login_qualify_button.grid(row=2,column=2)

login_canvas=tkinter.Canvas(win,width=0.4*width,height=0.4*height)
login_canvas.place(x=0,y=0,anchor='nw')
im=Image.open(f'{os.getcwd()}/infor/welcome.png')
photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
login_canvas.create_image(0,0,anchor='nw',image = photo)

im=Image.open(f'{os.getcwd()}/infor/zhuce.png') 
imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*width),int(0.05*height)))) 
register_button=tkinter.Button(win,image=imgBtn,command=register)
register_button.place(x=0.1*width,y=0.65*height)

im2=Image.open(f'{os.getcwd()}/infor/zhaohuimima.png') 
imgBtn2 =ImageTk.PhotoImage(im2.resize((int(0.05*width),int(0.05*height)))) 
find_button=tkinter.Button(win,image=imgBtn2,command=findpassward)
find_button.place(x=0.2*width,y=0.65*height)


def exittp():
    global logintime
    logouttime=time.time()
    print(logouttime-logintime)
    duration=int(round(logouttime-logintime)/60)
    print(str(int(round(logouttime-logintime)/60))+'分')
    q=tkinter.messagebox.askokcancel(title='提示', message='本次专注时长:%d分钟\n确认要退出程序吗？'%duration)
    if q==True:
        
        conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
        cursor = conn.cursor()
        sql="select totaltime from achievements where userID='%s'"%(zdyallfunction.userID)
        cursor.execute(sql)
        result=cursor.fetchone()
        conn.commit()
        cursor.close()
        print(result[0])
        
        conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
        cursor = conn.cursor()
        sql="update achievements set totaltime='%d' where userID='%s'"%(int(result[0])+duration,zdyallfunction.userID)
        cursor.execute(sql)
        sql="update enter_record set duration='%d' where userID='%s' and logintime='%s'"%(duration,zdyallfunction.userID,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(logintime)))
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        win.destroy()

    
    
def modechoice():
    global modetp
    modetp = tkinter.Toplevel()
    modetp.title('自定义题目')
    modetp.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
    dx=(sw-0.6*width)/2
    dy=(sh-0.6*height)/2
    modetp.geometry('%dx%d+%d+%d'%(0.6*width,0.6*height,dx,dy))
    modetp.overrideredirect(1)
    frame1=tkinter.Frame(modetp,width=0.3*width,height=0.3*height,bg='white')
    frame1.place(x=0,y=0,anchor='nw')
    def showzuodamode():
        
        try:
            modetp.destroy()
        except:
            pass
        showquestionselection()


    im=Image.open(f'{os.getcwd()}/infor/zuodamode.png') 
    imgBtn =ImageTk.PhotoImage(im.resize((int(0.3*width),int(0.3*height)))) 
    buttonmode1=tkinter.Button(frame1,image=imgBtn,command=showzuodamode)
    buttonmode1.place(x=0,y=0,anchor='nw')
    def showzdytimumode():
        
        try:
            modetp.destroy()
        except:
            pass
        zdyallfunction.calelements=[]
        zdytimumode()
    frame2=tkinter.Frame(modetp,width=0.3*width,height=0.3*height,bg='white')
    frame2.place(x=0.3*width,y=0,anchor='nw')
    im2=Image.open(f'{os.getcwd()}/infor/zdymode.png')
    imgBtn2 =ImageTk.PhotoImage(im2.resize((int(0.3*width),int(0.3*height)))) 
    buttonmode2=tkinter.Button(frame2,image=imgBtn2,command=showzdytimumode)
    buttonmode2.place(x=0,y=0,anchor='nw')
    
    def showmanagemode():
        try: 
            modetp.destroy()
        except:
            pass
        global manageboject,managemode
        managemode=1
        manageobject=MYQUESTIONBANK(win)

        def moveformer():
            q=tkinter.messagebox.askokcancel(title='提示', message='确认要返回模式选择吗？')
            if q==True:
                global managemode
                managemode=0
                manageobject.destroy()
                modechoice()
        #        im3=Image.open(f'{os.getcwd()}/infor/modeselectmoveleft.png') 
        #        imgBtn3 =ImageTk.PhotoImage(im3.resize((int(0.06*width),int(0.06*height)))) 
        manageobject.buttonmoveleft3=tkinter.Button(manageobject,text='返回',command=moveformer,bg='black',fg='white',font=('微软雅黑',12,'bold'))
        manageobject.buttonmoveleft3.place(x=0,y=height,anchor='sw')

        manageobject.protocol("WM_DELETE_WINDOW",exittp)
        manageobject.bind()
        win.mainloop()
    frame3=tkinter.Frame(modetp,width=0.3*width,height=0.3*height,bg='white')
    frame3.place(x=0,y=0.3*height,anchor='nw')
    im3=Image.open(f'{os.getcwd()}/infor/managemode.png')
    imgBtn3 =ImageTk.PhotoImage(im3.resize((int(0.3*width),int(0.3*height)))) 
    buttonmode3=tkinter.Button(frame3,image=imgBtn3,command=showmanagemode)
    buttonmode3.place(x=0,y=0,anchor='nw')
    
    def showchallengemode():
        """挑战模式，此功能正在开发中"""
        try: 
            modetp.destroy()
        except:
            pass
        global questionselection
        questionselection=KaoyanToplevel()
        questionselection.protocol("WM_DELETE_WINDOW",exittp)
        zuodamode()
        print("Goto Challenge Success")
    frame4=tkinter.Frame(modetp,width=0.3*width,height=0.3*height,bg='white')
    frame4.place(x=0.3*width,y=0.3*height,anchor='nw')
    im4=Image.open(f'{os.getcwd()}/infor/challengemode.png')
    imgBtn4 =ImageTk.PhotoImage(im4.resize((int(0.3*width),int(0.3*height)))) 
    buttonmode4=tkinter.Button(frame4,image=imgBtn4,command=showchallengemode)
    buttonmode4.place(x=0,y=0,anchor='nw')
    
    


    win.mainloop()
    
    
def zdytimumode():
    global zdytimumodeexist,zdytishimodeexist,zdymode,newofferquestion
    zdytimumodeexist=1
    zdymode=1
    newofferquestion=1
    global tp,gangdu,switchEAI
    zdyallfunction.switchEAI=0
    zdyallfunction.initinformatrixs()
    zdyallfunction.jys=[]
    zdyallfunction.xys=[]
    zdyallfunction.scxys=[]
    zdyallfunction.switchbjg=0
    gangdu=[]
    tp = tkinter.Toplevel()
    def fresh(event):
        if zdyallfunction.choosetab>=0:
            if zdyallfunction.choosetab==0:
                if tree1.columnnow==0:
                    try:
                        realtimedrawquestion()
                    except:
                        pass
            elif zdyallfunction.choosetab==1:
                if tree2.columnnow==0:
                    try:
                        realtimedrawquestion()
                    except:
                        pass
            elif zdyallfunction.choosetab==2:
                if tree3.columnnow==0:
                    try:
                        realtimedrawquestion()
                    except:
                        pass
            elif zdyallfunction.choosetab==3:
                if tree4.columnnow==0:
                    try:
                        realtimedrawquestion()
                    except:
                        pass
            elif zdyallfunction.choosetab==4:
                if tree5.columnnow==0:
                    try:
                        realtimedrawquestion()
                    except:
                        pass
            elif zdyallfunction.choosetab==5:
                if tree6.columnnow==0:
                    try:
                        realtimedrawquestion()
                    except:
                        pass
            elif zdyallfunction.choosetab==6:
                if tree7.columnnow==0:
                    try:
                        realtimedrawquestion()
                    except:
                        pass
            elif zdyallfunction.choosetab==7:
                if tree8.columnnow==0:
                    try:
                        realtimedrawquestion()
                    except:
                        pass
            elif zdyallfunction.choosetab==8:
                if tree9.columnnow==0:
                    try:
                        realtimedrawquestion()
                    except:
                        pass
                    
            
    tp.bind("<Right>",fresh)
    tp.title('自定义题目')
    tp.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
    tp.geometry('%dx%d+%d+%d'%(width,height,dx,dy))
    frame1=tkinter.Frame(tp,width=0.5*width,height=0.3*height)
    frame1.place(x=0.52*width,y=0.2*height,anchor='nw')
    s = ttk.Style()
    s.configure('Treeview', rowheight=int(50/1800*sh),font=('微软雅黑',9))
    hp=int(0.5*height)
    wp=int(0.8*height)
    global canvastimu
    canvastimu=tkinter.Canvas(tp,height=hp,width=wp,bg='white')
    canvastimu.place(x=0,y=0.3*height,anchor='nw')
    lshowquestion=tkinter.Label(tp,text='请先点击新建自定义,每行输入完按键盘右键→,程序自动录入整行并预览显示',fg='red',font=('微软雅黑',9))
    lshowquestion.place(x=0.5*width,y=0.15*height,anchor='nw')
    cellwidth=int(120/1800*sh)
    cellheight=int(50/1800*sh)
    nb1=ttk.Notebook(frame1)
    def jiediantable():
        global tree1,tabjiedian
        tabjiedian=tkinter.Frame(nb1,width=0.5*width,height=0.3*height)
        nb1.add(tabjiedian,text='节点')
        tree1 = Tabletree(tabjiedian, height=15,columns=('col1','col2','col3','col4'),show='headings',selectmode='none')
        tree1.qualifyframeparent(tabjiedian)
        tree1.total(4,15)
        tree1.binding()
        tree1.textstate()
        tree1.createinformatrix()
        tree1.qualifynum(0)
        tree1.column('#1', width=cellwidth, anchor='center')
        tree1.column('#2', width=cellwidth, anchor='center')
        tree1.column('#3', width=cellwidth, anchor='center')
        tree1.column('#4', width=cellwidth, anchor='center')        
        tree1.heading('col1', text='节点号')
        tree1.heading('col2', text='x坐标')
        tree1.heading('col3', text='y坐标')
        tree1.heading('col4', text='连接方式')
        for i in range(1,20):
            tree1.insert('',i,values=('','','',''))
        tree1.grid()
        lt=tkinter.Label(tabjiedian,text="       ",height=1)
        lt.grid()



            
    def ganjiantable():
        global tree2,tabganjian
        tabganjian=tkinter.Frame(nb1,width=0.5*width,height=0.3*height)
        nb1.add(tabganjian,text='杆件')
        tree2 =Tabletree(tabganjian, height=15,columns=('col1','col2','col3','col4','col5'),show='headings',selectmode='none')
        tree2.qualifyframeparent(tabganjian)
        tree2.total(5,15)
        tree2.binding()
        tree2.textstate()
        tree2.createinformatrix()
        tree2.qualifynum(1)
        tree2.column('#1', width=cellwidth, anchor='center')
        tree2.column('#2', width=cellwidth, anchor='center')
        tree2.column('#3', width=cellwidth, anchor='center')
        tree2.column('#4', width=cellwidth, anchor='center')
        tree2.column('#5', width=cellwidth, anchor='center')
        tree2.heading('col1', text='杆件号')
        tree2.heading('col2', text='节点i')
        tree2.heading('col3', text='节点j')
        tree2.heading('col4', text='EA')
        tree2.heading('col5', text='EI')
        for i in range(1,20):
            tree2.insert('',i,values=('','','',''))
        tree2.grid()
        lt=tkinter.Label(tabganjian,text="       ",height=1)
        lt.grid()

        
			
    
    def zhizuotable():
        global tree3,tabzhizuo
        tabzhizuo=tkinter.Frame(nb1)
        nb1.add(tabzhizuo,text='刚性支座')
        tree3 =Tabletree(tabzhizuo, height=15,columns=('col1','col2','col3'),show='headings',selectmode='none')
        tree3.qualifyframeparent(tabzhizuo)
        tree3.total(3,15)
        tree3.binding()
        tree3.textstate()
        tree3.createinformatrix()
        tree3.qualifynum(2)
        tree3.column('#1', width=cellwidth, anchor='center')
        tree3.column('#2', width=cellwidth, anchor='center')
        tree3.column('#3', width=cellwidth, anchor='center')
        tree3.heading('col1', text='节点号')
        tree3.heading('col2', text='支座类型')
        tree3.heading('col3', text='角度')
        for i in range(1,20):
            tree3.insert('',i,values=('','','',''))
        #        tree3.grid(row=0,column=0)
        tree3.grid()
        lt=tkinter.Label(tabzhizuo,text="       ",height=1)
        lt.grid()

        #        l2=tkinter.Label(tabzhizuo,text="3为滑动铰支座，4为固定支座",fg='red')
        #        l2.grid()

    
    def jiedianhezaitable(): 
        global tree4,tabjiedianhezai
        tabjiedianhezai=tkinter.Frame(nb1)
        nb1.add(tabjiedianhezai,text='节点荷载')
        tree4 =Tabletree(tabjiedianhezai, height=15,columns=('col1','col2','col3','col4'),show='headings',selectmode='none')
        tree4.qualifyframeparent(tabjiedianhezai)
        tree4.total(4,15)
        tree4.binding()
        tree4.textstate()
        tree4.createinformatrix()
        tree4.qualifynum(3)
        tree4.column('#1', width=cellwidth, anchor='center')
        tree4.column('#2', width=cellwidth, anchor='center')
        tree4.column('#3', width=cellwidth, anchor='center')
        tree4.column('#4', width=cellwidth, anchor='center')
        tree4.heading('col1', text='节点号')
        tree4.heading('col2', text='Fx')
        tree4.heading('col3', text='Fy')
        tree4.heading('col4', text='M')
        for i in range(1,20):
            tree4.insert('',i,values=('','','',''))
        tree4.grid()
        lt=tkinter.Label(tabjiedianhezai,text="       ",height=1)
        lt.grid()

   
    def ganjianjizhonghezaitable():
        global tree5,tabganjianjizhonghezai
        tabganjianjizhonghezai=tkinter.Frame(nb1)
        nb1.add(tabganjianjizhonghezai,text='杆件集中荷载')
        tree5 =Tabletree(tabganjianjizhonghezai, height=15,columns=('col1','col2','col3','col4'),show='headings',selectmode='none')
        tree5.qualifyframeparent(tabganjianjizhonghezai)
        tree5.total(4,15)
        tree5.binding()
        tree5.textstate()
        tree5.createinformatrix()
        tree5.qualifynum(4)
        tree5.column('#1', width=cellwidth, anchor='center')
        tree5.column('#2', width=cellwidth, anchor='center')
        tree5.column('#3', width=cellwidth, anchor='center')
        tree5.column('#4', width=cellwidth, anchor='center')
        tree5.heading('col1', text='杆件号')
        tree5.heading('col2', text='荷载大小')
        tree5.heading('col3', text='方向')
        tree5.heading('col4', text='作用位置')
        for i in range(1,20):
            tree5.insert('',i,values=('','','',''))
        tree5.grid()
        lt=tkinter.Label(tabganjianjizhonghezai,text="       ",height=1)
        lt.grid()

    
    def ganjianfenbuhezaitable():
        global tree6,tabganjianfenbuhezai
        tabganjianfenbuhezai=tkinter.Frame(nb1)
        nb1.add(tabganjianfenbuhezai,text='分布荷载')
        tree6 =Tabletree(tabganjianfenbuhezai, height=15,columns=('col1','col2','col3','col4','col5'),show='headings',selectmode='none')
        tree6.qualifyframeparent(tabganjianfenbuhezai)
        tree6.total(5,15)
        tree6.binding()
        tree6.textstate()
        tree6.createinformatrix()
        tree6.qualifynum(5)
        tree6.column('#1', width=cellwidth, anchor='center')
        tree6.column('#2', width=cellwidth, anchor='center')
        tree6.column('#3', width=cellwidth, anchor='center')
        tree6.column('#4', width=cellwidth, anchor='center')
        tree6.column('#5', width=cellwidth, anchor='center')
        tree6.heading('col1', text='杆件号')
        tree6.heading('col2', text='荷载大小')
        tree6.heading('col3', text='方向')
        tree6.heading('col4', text='起始点')
        tree6.heading('col5', text='终点')
        for i in range(1,20):
            tree6.insert('',i,values=('','','',''))
        tree6.grid()
        lt=tkinter.Label(tabganjianfenbuhezai,text="       ",height=1)
        lt.grid()

    
    def wenduhezaitable():
        global tree7,tabwenduhezai
        tabwenduhezai=tkinter.Frame(nb1)
        nb1.add(tabwenduhezai,text='温度荷载')
        tree7 =Tabletree(tabwenduhezai, height=15,columns=('col1','col2','col3','col4','col5'),show='headings',selectmode='none')
        tree7.qualifyframeparent(tabwenduhezai)
        tree7.total(5,15)
        tree7.binding()
        tree7.textstate()
        tree7.createinformatrix()
        tree7.qualifynum(6)
        tree7.column('#1', width=cellwidth, anchor='center')
        tree7.column('#2', width=cellwidth, anchor='center')
        tree7.column('#3', width=cellwidth, anchor='center')
        tree7.column('#4', width=cellwidth, anchor='center')
        tree7.column('#5', width=cellwidth, anchor='center')
        tree7.heading('col1', text='杆件号')
        tree7.heading('col2', text='线膨胀系数')
        tree7.heading('col3', text='上端温度')
        tree7.heading('col4', text='下端温度')
        tree7.heading('col5', text='截面高度')
        for i in range(1,20):
            tree7.insert('',i,values=('','','',''))
        tree7.grid()
        lt=tkinter.Label(tabwenduhezai,text="       ",height=1)
        lt.grid()

   
    def zhizuochenjiangtable():
        global tree8,tabzhizuochenjiang
        tabzhizuochenjiang=tkinter.Frame(nb1)
        nb1.add(tabzhizuochenjiang,text='支座沉降')
        tree8 =Tabletree(tabzhizuochenjiang, height=15,columns=('col1','col2','col3','col4','col5','col6','col7'),show='headings',selectmode='none')
        tree8.qualifyframeparent(tabzhizuochenjiang)
        tree8.total(7,15)
        tree8.binding()
        tree8.textstate()
        tree8.createinformatrix()
        tree8.qualifynum(7)
        tree8.column('#1', width=cellwidth, anchor='center')
        tree8.column('#2', width=cellwidth, anchor='center')
        tree8.column('#3', width=cellwidth, anchor='center')
        tree8.column('#4', width=cellwidth, anchor='center')
        tree8.column('#5', width=cellwidth, anchor='center')
        tree8.column('#6', width=cellwidth, anchor='center')
        tree8.column('#7', width=cellwidth, anchor='center')
        tree8.heading('col1', text='杆件号')
        tree8.heading('col2', text='dx i端')
        tree8.heading('col3', text='dy i端')
        tree8.heading('col4', text='theta i端')
        tree8.heading('col5', text='dx j端')
        tree8.heading('col6', text='dy j端')
        tree8.heading('col7', text='theta j端')
        for i in range(1,20):
            tree8.insert('',i,values=('','','',''))
        tree8.grid()
        lt=tkinter.Label(tabzhizuochenjiang,text="       ",height=1)
        lt.grid()

    
    def tanhuangtable():
        global tree9,tabtanhuang
        tabtanhuang=tkinter.Frame(nb1)
        nb1.add(tabtanhuang,text='弹簧')
        tree9 = Tabletree(tabtanhuang, height=15,columns=('col1','col2','col3','col4'),show='headings',selectmode='none')
        tree9.qualifyframeparent(tabtanhuang)
        tree9.total(4,15)
        tree9.binding()
        tree9.textstate()
        tree9.createinformatrix()
        tree9.qualifynum(8)
        tree9.column('#1', width=cellwidth, anchor='center')
        tree9.column('#2', width=cellwidth, anchor='center')
        tree9.column('#3', width=cellwidth, anchor='center')
        tree9.column('#4', width=cellwidth, anchor='center')
        tree9.heading('col1', text='节点号')
        tree9.heading('col2', text='支座类型')
        tree9.heading('col3', text='角度')
        tree9.heading('col4', text='弹簧刚度')
        for i in range(1,20):
            tree9.insert('',i,values=('','','',''))
        tree9.grid()
        #        lt=tkinter.Label(tanhuangtable,text="       ",height=1)
        #        lt.grid()
    
    jiediantable()
    ganjiantable()
    zhizuotable()
    jiedianhezaitable()
    ganjianjizhonghezaitable()
    ganjianfenbuhezaitable()
    wenduhezaitable()
    zhizuochenjiangtable()
    tanhuangtable()
    nb1.pack()
    def drawquestion():
        buttonendup()
        zdyallfunction.drawquestion()
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        hp1=int(0.5*height)
        wp1=int(0.8*height)
        photo = ImageTk.PhotoImage(im.resize((wp1,hp1),Image.ANTIALIAS))
        canvastimu.create_image(0,0,anchor='nw',image = photo)
        win.mainloop()
    def realtimedrawquestion():
        zdyallfunction.drawquestion()
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        hp1=int(0.5*height)
        wp1=int(0.8*height)
        photo = ImageTk.PhotoImage(im.resize((wp1,hp1),Image.ANTIALIAS))
        canvastimu.create_image(0,0,anchor='nw',image = photo)
        win.mainloop()
    def buttonendup():
        print(zdyallfunction.choosetab)
        print("<<<<<<<>>>>>>>>")
        if (zdyallfunction.choosetab==0):
            tree1.finalendup()
        if (zdyallfunction.choosetab==1):
            tree2.finalendup()
        if (zdyallfunction.choosetab==2):
            tree3.finalendup()
        if (zdyallfunction.choosetab==3):
            tree4.finalendup()
        if (zdyallfunction.choosetab==4):
            tree5.finalendup()
        if (zdyallfunction.choosetab==5):
            tree6.finalendup()
        if (zdyallfunction.choosetab==6):
            tree7.finalendup()
        if (zdyallfunction.choosetab==7):
            tree8.finalendup()
        if (zdyallfunction.choosetab==8):
            tree9.finalendup()
    def createtablelines(event):
        global standardx,standardy
        standardbbox=tree1.now(event)
        standardy=standardbbox[1]
        standardx=standardbbox[0]
        cellwidth=standardbbox[2]
        cellheight=standardbbox[3]
        def drawtablelines(name,columns):
            for i in range(0,20):
                f=tkinter.Frame(name,bg='black',width=cellwidth*columns,height=1)
                f.place(x=0,y=standardy+i*cellheight,anchor='nw')
            for i in range(1,columns):
                f=tkinter.Frame(name,bg='black',width=1,height=15*cellheight+standardy)
                f.place(x=standardx+i*cellwidth,y=0,anchor='nw')    
        drawtablelines(tabjiedian,4)
        drawtablelines(tabganjian,5)
        drawtablelines(tabzhizuo,3) 
        drawtablelines(tabjiedianhezai,4)
        drawtablelines(tabganjianjizhonghezai,4)
        drawtablelines(tabganjianfenbuhezai,5)
        drawtablelines(tabwenduhezai,5)
        drawtablelines(tabzhizuochenjiang,7)
        drawtablelines(tabtanhuang,4)
        tree1.l=tkinter.Label(tabjiedian,text="连接方式:0代表铰接,1刚接,铰节点请按连接的杆件个数定义多个节点",fg='white',bg='black')
        tree1.l.place(x=0,y=15*cellheight+standardy,anchor='nw')
        tree2.l=tkinter.Label(tabganjian,text="节点i为初始端,节点j为终止端,抗拉或抗弯刚度输入-1代表无穷大",fg='white',bg='black')
        tree2.l.place(x=0,y=15*cellheight+standardy,anchor='nw')
        tree3.l1=tkinter.Label(tabzhizuo,text="支座类型:1杆支座，2铰支座,3滑动铰支座，4固定端",fg='white',bg='black')
        tree3.l1.place(x=0,y=15*cellheight+standardy,anchor='nw')
        tree4.l=tkinter.Label(tabjiedianhezai,text="Fx向右为正,Fy向上为正,M逆时针为正",fg='white',bg='black')
        tree4.l.place(x=0,y=15*cellheight+standardy,anchor='nw')
        tree5.l=tkinter.Label(tabganjianjizhonghezai,text="逆时针为正方向,杆件起始端指向终止端为0度,作用位置取相对距离,取值0-1",fg='white',bg='black')
        tree5.l.place(x=0,y=15*cellheight+standardy,anchor='nw')
        tree6.l=tkinter.Label(tabganjianfenbuhezai,text="逆时针为正方向,杆件起始端指向终止端为0度,起始点终点取相对距离,取值0-1",fg='white',bg='black')
        tree6.l.place(x=0,y=15*cellheight+standardy,anchor='nw')
        tree7.l=tkinter.Label(tabwenduhezai,text="取i端指向j端方向为x轴，y轴正方向为上端",fg='white',bg='black')
        tree7.l.place(x=0,y=15*cellheight+standardy,anchor='nw')
        tree8.l=tkinter.Label(tabzhizuochenjiang,text="向右为dx正方向,向上为dy正方向,逆时针为转角theta正方向",fg='white',bg='black')
        tree8.l.place(x=0,y=15*cellheight+standardy,anchor='nw')
        tree9.l=tkinter.Label(tabtanhuang,text="支座类型:1为弹性连杆,2为角弹簧",fg='white',bg='black')
        tree9.l.place(x=0,y=15*cellheight+standardy,anchor='nw')
    
    def calculateresult():
        zdyallfunction.file()
        zdyallfunction.calculation()
        zdyallfunction.drawM()
        zdyallfunction.drawN()
        zdyallfunction.drawshearforce()
        zdyallfunction.drawdeformation()

        
    #        for i in range(0,20):
    #            f=tkinter.Frame(tabjiedian,bg='black',width=cellwidth*4,height=1)
    #            f.place(x=0,y=standardy+i*cellheight,anchor='nw')
    #        for i in range(1,4):
    #            f=tkinter.Frame(tabjiedian,bg='black',width=1,height=1000)
    #            f.place(x=standardx+i*cellwidth,y=0,anchor='nw')

    def nextstep():
        zdyallfunction.sortinformatrixs()
#        for i in range(len(zdyallfunction.informatrixs)):
#            print(zdyallfunction.informatrixs[i])
        try:
            zdyallfunction.fileinelements()
        except:
            tkinter.messagebox.showinfo(title='提示', message='结构信息不完整，无法计算')
            return
        zdyallfunction.file()
        try:
            jhstate=zdyallfunction.calculation()
            if jhstate==0:
                tkinter.messagebox.showinfo(title='提示', message='是几何不定结构，无法计算')
                return
        except:
            tkinter.messagebox.showinfo(title='提示', message='结构信息不完整，无法计算')
            return
        zdyallfunction.drawquestion()
#        zdyallfunction.drawM()
#        zdyallfunction.drawN()
#        zdyallfunction.drawshearforce()
#        zdyallfunction.drawdeformation()
        tp.withdraw()
        if zdytishimodeexist==0:
            zdytishimode()
        else:
            tp1.deiconify()
        
    def formerstep():
        global zdytimumodeexist,zdytishimodeexist,zdyceshimodeexist
        zdytimumodeexist=0
        zdytishimodeexist=0
        zdyceshimodeexist=0
        tp.destroy()
        try:
            tp1.destroy
        except:
            pass
        try:
            tp2.destroy
        except:
            pass
        modechoice()
        
    def showzdytimuhelp():
        zdytimuhelp=HELPTOPLEVEL(name='自定义题目介绍',ratio=1.78,picturename='zdyhelp1.jpg')
        zdytimuhelp.bind()
        
    def showzdyintroduction():
        zdyintroductiontp = tkinter.Toplevel()
        zdyintroductiontp.title('自定义帮助')
        
    #    zdyintroductiontp.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        dx=(sw-0.8*width)/2
        dy=(sh-0.8*height)/2
        zdyintroductiontp.geometry('%dx%d+%d+%d'%(0.8*width,0.9*height,dx,dy))
        zdyintroductiontp.resizable(0,0)
    #    zdyintroductiontp_canvas = tkinter.Canvas(zdyintroductiontp,height=0.5*sh,width=0.5*sw)
    #    zdyintroductiontp_image_file = tkinter.PhotoImage(file=f'{os.getcwd()}/guides/1.gif')
    #    zdyintroductiontp_image = zdyintroductiontp_canvas.create_image(0,0,anchor='nw',image=custom_guide_window_image_file)
    #    zdyintroductiontp_canvas.pack(side='top')
    
        global page_num
        page_num=1
        
        def page_up():
            global page_num
            if page_num < 19:
               page_num = page_num + 1
               page()
            else:
                tkinter.messagebox.showinfo(title='', message='已经到尾了')
    
        def page_down():
            global page_num
            if page_num > 1:
               page_num = page_num - 1
               page()
            if page_num==1:
                tkinter.messagebox.showinfo(title='', message='已经到头了')
    
        
        
        
        
        
        '''调用图片分两步走，第一步打开，第二步重新定义尺寸，最后再使用'''
        #步骤1：
        imL=Image.open(f'{os.getcwd()}/infor/leftan.png') 
        #步骤2:这些名称都别重复 int(0.05*width),int(0.05*height)是长宽大小
        imgBtn_left =ImageTk.PhotoImage(imL.resize((int(0.05*width),int(0.05*height))))
        #最后调用:
        imR=Image.open(f'{os.getcwd()}/infor/rightan.png') 
        
        imgBtn_right =ImageTk.PhotoImage(imR.resize((int(0.05*width),int(0.05*height)))) 
        button_left = tkinter.Button(zdyintroductiontp,image=imgBtn_left,command=page_down)
        button_left.place(x=0,y=0.9*height,anchor='sw' )
    
        button_right = tkinter.Button(zdyintroductiontp,image=imgBtn_right,command=page_up)
        button_right.place(x=0.8*width,y=0.9*height,anchor='se')
    
        def page():
            global page_num
            canvas=tkinter.Canvas(zdyintroductiontp,height=0.8*height,width=0.8*width,bg='white')
            canvas.place(x=0,y=0,anchor='nw')
        
            im1=Image.open(f'{os.getcwd()}/guides/1.gif')
            photo1 = ImageTk.PhotoImage(im1.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im2=Image.open(f'{os.getcwd()}/guides/2.gif')
            photo2 = ImageTk.PhotoImage(im2.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im3=Image.open(f'{os.getcwd()}/guides/3.gif')
            photo3 = ImageTk.PhotoImage(im3.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im4=Image.open(f'{os.getcwd()}/guides/4.gif')
            photo4 = ImageTk.PhotoImage(im4.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im5=Image.open(f'{os.getcwd()}/guides/5.gif')
            photo5 = ImageTk.PhotoImage(im5.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im6=Image.open(f'{os.getcwd()}/guides/6.gif')
            photo6 = ImageTk.PhotoImage(im6.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im7=Image.open(f'{os.getcwd()}/guides/7.gif')
            photo7 = ImageTk.PhotoImage(im7.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im8=Image.open(f'{os.getcwd()}/guides/8.gif')
            photo8 = ImageTk.PhotoImage(im8.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im9=Image.open(f'{os.getcwd()}/guides/9.gif')
            photo9 = ImageTk.PhotoImage(im9.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im10=Image.open(f'{os.getcwd()}/guides/10.gif')
            photo10 = ImageTk.PhotoImage(im10.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im11=Image.open(f'{os.getcwd()}/guides/11.gif')
            photo11 = ImageTk.PhotoImage(im11.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im12=Image.open(f'{os.getcwd()}/guides/12.gif')
            photo12 = ImageTk.PhotoImage(im12.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im13=Image.open(f'{os.getcwd()}/guides/13.gif')
            photo13 = ImageTk.PhotoImage(im13.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im14=Image.open(f'{os.getcwd()}/guides/14.gif')
            photo14 = ImageTk.PhotoImage(im14.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im15=Image.open(f'{os.getcwd()}/guides/15.gif')
            photo15 = ImageTk.PhotoImage(im15.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im16=Image.open(f'{os.getcwd()}/guides/16.gif')
            photo16 = ImageTk.PhotoImage(im16.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im17=Image.open(f'{os.getcwd()}/guides/17.gif')
            photo17 = ImageTk.PhotoImage(im17.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im18=Image.open(f'{os.getcwd()}/guides/18.gif')
            photo18 = ImageTk.PhotoImage(im18.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
            im19=Image.open(f'{os.getcwd()}/guides/19.gif')
            photo19 = ImageTk.PhotoImage(im19.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
        
            if page_num == 1:
                canvas.create_image(0,0,anchor='nw',image = photo1)
            elif page_num ==2:
                canvas.create_image(0,0,anchor='nw',image = photo2)
            elif page_num ==3:
                canvas.create_image(0,0,anchor='nw',image = photo3)
            elif page_num ==4:
                canvas.create_image(0,0,anchor='nw',image = photo4)
            elif page_num ==5:
                canvas.create_image(0,0,anchor='nw',image = photo5)
            elif page_num ==6:
                canvas.create_image(0,0,anchor='nw',image = photo6)
            elif page_num ==7:
                canvas.create_image(0,0,anchor='nw',image = photo7)
            elif page_num ==8:
                canvas.create_image(0,0,anchor='nw',image = photo8)
            elif page_num ==9:
                canvas.create_image(0,0,anchor='nw',image = photo9)
            elif page_num ==10:
                canvas.create_image(0,0,anchor='nw',image = photo10)
            elif page_num ==11:
                canvas.create_image(0,0,anchor='nw',image = photo11)
            elif page_num ==12:
                canvas.create_image(0,0,anchor='nw',image = photo12)
            elif page_num ==13:
                canvas.create_image(0,0,anchor='nw',image = photo13)
            elif page_num ==14:
                canvas.create_image(0,0,anchor='nw',image = photo14)
            elif page_num ==15:
                canvas.create_image(0,0,anchor='nw',image = photo15)
            elif page_num ==16:
                canvas.create_image(0,0,anchor='nw',image = photo16)
            elif page_num ==17:
                canvas.create_image(0,0,anchor='nw',image = photo17)
            elif page_num ==18:
                canvas.create_image(0,0,anchor='nw',image = photo18)
            elif page_num ==19:
                canvas.create_image(0,0,anchor='nw',image = photo19)
            win.mainloop()
        page()
        win.mainloop()

    buttonzdy11=tkinter.Button(tp,text='预览',font=('微软雅黑',12),height=1,fg='white',bg='black',command=drawquestion)
    buttonzdy11.place(x=0.5*width,y=0.2*height,anchor='ne')
    buttonzyd12=tkinter.Button(tp,text='新建自定义',font=('微软雅黑',12),height=1,fg='white',bg='black')
    buttonzyd12.place(x=0,y=0.2*height,anchor='nw')
    buttonzyd12.bind('<ButtonRelease-1>',createtablelines)
    buttonzyd13=tkinter.Button(tp,text='简要帮助',font=('微软雅黑',12),height=1,fg='white',bg='black',command=showzdytimuhelp)
    buttonzyd13.place(x=0.15*width,y=0.2*height,anchor='nw')
    buttonzyd14=tkinter.Button(tp,text='详细帮助',font=('微软雅黑',12),height=1,fg='white',bg='black',command=showzdyintroduction)
    buttonzyd14.place(x=0.35*width,y=0.2*height,anchor='ne')
#    buttonzdy13=tkinter.Button(tp,text='计算',font=('微软雅黑',15),width=10,height=1,fg='red',command=calculateresult)
#    buttonzdy13.pack()
#    buttonzdy14=tkinter.Button(tp,text='自定义提示',font=('微软雅黑',15),width=10,height=1,fg='red',command=nextstep)
#    buttonzdy14.pack()
#    def movenext():
#        if zdytishimodeexist==0:
#            zdytishimode()
#            tp.withdraw()
#        else:
#            tp.withdraw()
#            tp2.deiconify()
#    movenextwaitlable=tkinter.Label(tp,text='')
    tp.protocol("WM_DELETE_WINDOW",exittp)
    im=Image.open(f'{os.getcwd()}/infor/zdytishimoveright.png') 
    imgBtn =ImageTk.PhotoImage(im.resize((int(0.07*width),int(0.07*height)))) 
    buttonmoveright1=tkinter.Button(tp,image=imgBtn,command=nextstep)
    buttonmoveright1.place(x=width,y=height,anchor='se')
    im2=Image.open(f'{os.getcwd()}/infor/modeselectmoveleft.png') 
    imgBtn2 =ImageTk.PhotoImage(im2.resize((int(0.07*width),int(0.07*height)))) 
    buttonmoveleft2=tkinter.Button(tp,image=imgBtn2,command=formerstep)
    buttonmoveleft2.place(x=0,y=height,anchor='sw')
    tp.resizable(0,0)

    win.mainloop()


def zdytishimode():
    zdyallfunction.ZDYTISHI.initzdytishinum()
    if managemode==1:
        try:
            if zdyallfunction.questionsymbol.split('_')[0]!=zdyallfunction.userID:
                tkinter.messagebox.showinfo(title='提示', message='请先双击选择题目！')
                return 0
        except:
            pass
        zdyallfunction.getmanagequestion(zdyallfunction.questionsymbol)
        zdyallfunction.fileinelements()
        zdyallfunction.file()
        zdyallfunction.drawquestion()
        zdyallfunction.calculation()
    
    global tp1
    global zdytimumodeexist,zdytishimodeexist,zdyceshimodeexist
    zdytishimodeexist=1
    if managemode==1:
        zdytishimodeexist=0
    tp1 = tkinter.Toplevel()
    tp1.title('自定义提示')
    tp1.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
    tp1.geometry('%dx%d+%d+%d'%(width,height,dx,dy))
    frame1=tkinter.Frame(tp1,width=0.5*width,height=0.5*height)
    frame1.place(x=0,y=0.2*height,anchor='nw')
    s = ttk.Style()
    s.configure('Treeview', rowheight=int(50/1800*sh),font=('微软雅黑',9))
    hp=int(0.5*height)
    wp=int(0.8*height)
    canvas=tkinter.Canvas(frame1,height=hp,width=wp,bg='white')
    canvas.place(x=0,y=0,anchor='nw')
    im=Image.open(f'{os.getcwd()}/drawing/question.png')
    photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
    canvas.create_image(0,0,anchor='nw',image = photo)
    choosepic=0
    
    def showzdytishihelp():
        zdytishihelp=HELPTOPLEVEL(name='自定义提示介绍',ratio=1.7,picturename='zdyhelp2.jpg')
        zdytishihelp.bind()
    zdytishihelpbutton=tkinter.Button(tp1,text='自定义提示帮助',font=('微软雅黑',12),width=14,height=1,fg='white',bg='black',command=showzdytishihelp)
    zdytishihelpbutton.place(x=0.1*width,y=0.2*height,anchor='sw')
    
    def showzdyquestion():
        global choosepic
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        canvas.create_image(0,0,anchor='nw',image = photo)
        choosepic=0
        win.mainloop()
    def showzdyM():
        zdyallfunction.drawM()
        global choosepic
        im=Image.open(f'{os.getcwd()}/drawing/M.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        canvas.create_image(0,0,anchor='nw',image = photo)
        choosepic=1
        win.mainloop()
    def showzdyshearforce():
        zdyallfunction.drawshearforce()
        global choosepic
        im=Image.open(f'{os.getcwd()}/drawing/shearforce.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        canvas.create_image(0,0,anchor='nw',image = photo)
        choosepic=2
        win.mainloop()
    def showzdyN():
        zdyallfunction.drawN()
        global choosepic
        im=Image.open(f'{os.getcwd()}/drawing/N.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        canvas.create_image(0,0,anchor='nw',image = photo)
        choosepic=3
        win.mainloop()
    def showzdydeformation():
        zdyallfunction.drawdeformation()
        global choosepic
        im=Image.open(f'{os.getcwd()}/drawing/deformation.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        canvas.create_image(0,0,anchor='nw',image = photo)
        choosepic=4
        win.mainloop()
    def zdyfangda():
        global choosepic
        if choosepic==1:
            zdyallfunction.amplifyM(2)
            zdyallfunction.drawM()
            showzdyM()
        if choosepic==2:
            zdyallfunction.amplifyF(2)
            zdyallfunction.drawshearforce()
            showzdyshearforce()
        if choosepic==3:
            zdyallfunction.amplifyN(2)
            zdyallfunction.drawN()
            showzdyN()
        if choosepic==4:
            zdyallfunction.amplifydeformation(3)
            zdyallfunction.drawdeformation()
            showzdydeformation()
    def zdysuoxiao():
        global choosepic
        if choosepic==1:
            zdyallfunction.amplifyM(1/2)
            zdyallfunction.drawM()
            showzdyM()
        if choosepic==2:
            zdyallfunction.amplifyF(1/2)
            zdyallfunction.drawshearforce()
            showzdyshearforce()
        if choosepic==3:
            zdyallfunction.amplifyN(1/2)
            zdyallfunction.drawN()
            showzdyN()
        if choosepic==4:
            zdyallfunction.amplifydeformation(1/3)
            zdyallfunction.drawdeformation()
            showzdydeformation()
            
    
    frame2=tkinter.Frame(tp1,width=0.5*width,height=0.2*height)
    frame2.place(x=0,y=0.7*height,anchor='nw')
    buttonzdy21=tkinter.Button(frame2,text='题目',font=('微软雅黑',12,'bold'),width=6,height=1,bg='deepskyblue',command=showzdyquestion)
    buttonzdy22=tkinter.Button(frame2,text='弯矩图',font=('微软雅黑',12,'bold'),width=8,height=1,bg='deepskyblue',command=showzdyM)
    buttonzdy23=tkinter.Button(frame2,text='剪力图',font=('微软雅黑',12,'bold'),width=8,height=1,bg='deepskyblue',command=showzdyshearforce)
    buttonzdy24=tkinter.Button(frame2,text='轴力图',font=('微软雅黑',12,'bold'),width=8,height=1,bg='deepskyblue',command=showzdyN)
    buttonzdy25=tkinter.Button(frame2,text='变形图',font=('微软雅黑',12,'bold'),width=8,height=1,bg='deepskyblue',command=showzdydeformation)
#    im=Image.open('infor/zheng.png')
#    imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
#    buttonzdy26=tkinter.Button(frame2,image=imgBtn,command=zdyfangda) 
#    im=Image.open('infor/fu.png')
#    imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
#    buttonzdy27=tkinter.Button(frame2,image=imgBtn2,command=zdysuoxiao)
    buttonzdy21.grid(row=1,column=0)
    buttonzdy22.grid(row=1,column=1)
    buttonzdy23.grid(row=1,column=2)
    buttonzdy24.grid(row=1,column=3)
    buttonzdy25.grid(row=1,column=4)
#    buttonzdy26.grid(row=1,column=5)
#    buttonzdy27.grid(row=1,column=6)
    nb2=ttk.Notebook(tp1)
    
    
    def qualifytishi():
        print(len(text22.get(0.0,'end')))
        if len(text22.get(0.0,'end'))<=1 and text22.get('end')=="":
            tkinter.messagebox.showinfo(title='提示', message='提示内容不能为空')
            return
        elif e21.get()=='':
            tkinter.messagebox.showinfo(title='提示', message='提示对象不能为空')
            return
        else:
            tree.insert('',zdyallfunction.zdytishinum,values=(zdyallfunction.zdytishinum+1,cmb1.get(),e21.get(),'自动判定',text22.get('0.0','end')))
            zdyallfunction.ZDYTISHI.updatezdytishi(cmb1.get(),e21.get(),0,text22.get('0.0','end'))
            e21.delete(0,'end')
            text22.delete(0.0,'end')
            text22.insert("end","")
                      
    frame3=tkinter.Frame(tp1,width=0.3*width,height=0.3*height)
    lable21=tkinter.Label(frame3,text="整体提示是为用户作答前给予的整体性特征的提示",fg='red')
    lable22=tkinter.Label(frame3,text="请在下方文本框输入，软件自动录入",fg='red')
    text21=tkinter.Text(frame3,width=40,height=10,highlightthickness=2,highlightcolor='red',
           highlightbackground='red')
    text21.insert("end","")
    lable21.pack()
    lable22.pack()
    text21.pack()
    nb2.add(frame3,text='整体提示')
    frame4=tkinter.Frame(tp1,width=0.3*width,height=0.3*height)
    nb2.add(frame4,text="细节提示")
    nb2.place(x=0.55*width,y=0.1*height)
    lable23=tkinter.Label(frame4,text="提示对象",fg='red')
    lable23.grid(row=0,column=0)
    cmb1 = ttk.Combobox(frame4)
    cmb1['value'] = ('单个节点','单个杆件','多个杆件')
    cmb1.current(0)
    cmb1.grid(row=1,column=0)
    lable24=tkinter.Label(frame4,text="对象编号（节点/杆件编号）",fg='red')
    lable25=tkinter.Label(frame4,text="多根杆件编号之间请以,分割(例如1,2,3)",fg='red')
    lable24.grid(row=2,column=0)
    lable25.grid(row=3,column=0)
    e21=tkinter.Entry(frame4,width=20)
    e21.grid(row=4,column=0)
    lable26=tkinter.Label(frame4,text="出现条件",fg='red')
    lable26.grid(row=5,column=0)
    cmb2 = ttk.Combobox(frame4)
    cmb2['value'] = ('自动判定')
    cmb2.current(0)
    cmb2.grid(row=6,column=0)
    lable27=tkinter.Label(frame4,text="提示内容",fg='red')
    lable27.grid(row=7,column=0)
    text22=tkinter.Text(frame4,width=30,height=6,highlightthickness=2,highlightcolor='red',
           highlightbackground='red')
    text22.insert("end","")
    text22.grid(row=8,column=0)
    buttonzdy28=tkinter.Button(frame4,text='确认输入',fg='red',command=qualifytishi)
    buttonzdy28.grid(row=7,column=1)
    global choosetime
    choosetime=0
    def showmenu(event):
        print('1233')
        menu.post(event.x_root, event.y_root)
    def shanchutishi():
        global oldtishirow
        zdyallfunction.ZDYTISHI.shanchutishi(oldtishirow)
        showtishi()
        
    menu=tkinter.Menu(win,tearoff=False)
    menu.add_command(label="删除",command=shanchutishi)
    def choose(event):
        global tishicellheight,tishistandardx,tishistandardy,oldtishirow
        global choosetime
        if choosetime==0:
            widget=event.widget
            standardbbox=widget.bbox("I001","#1")
            tishistandardx=standardbbox[0]
            tishistandardy=standardbbox[1]
            tishicellheight=standardbbox[3]
        x=event.x
        y=event.y
        oldtishirow=int((y-tishistandardy)/tishicellheight)
        print('oldtishirow='+str(oldtishirow))
        tree.bind('<ButtonRelease-1>',sorttishi)
        tree.bind('<Button-3>',showmenu)
        choosetime=choosetime+1

        
    def sorttishi(event):
        global tishicellheight,tishistandardx,tishistandardy,oldtishirow
        x=event.x
        y=event.y
        widget=event.widget
        newtishirow=int((y-tishistandardy)/tishicellheight)
        print('newtishirow='+str(newtishirow))
        if newtishirow!=oldtishirow:
            if newtishirow>=0 and oldtishirow>=0:
                zdyallfunction.ZDYTISHI.exchangezdytishi(oldtishirow,newtishirow)
                showtishi()
        
    def showtishi():
        deltree()
        for i in range(len(zdyallfunction.zdytishi)):
            if pd.isnull(zdyallfunction.zdytishi.iloc[i,0])==False:
                tt=[]
                tt.append(int(zdyallfunction.zdytishi.iloc[i,0]))
                tt.append(zdyallfunction.zdytishi.iloc[i,1])
                tt.append(int(zdyallfunction.zdytishi.iloc[i,2]))
                tt.append('自动判定')
                tt.append(str(zdyallfunction.zdytishi.iloc[i,4]))
                tt=tuple(tt)
                tree.insert('',i,values=tt)
        text21.delete('1.0','end')
        text21.insert('end',zdyallfunction.zhengtitishi)

        
    
    def deltree():
        x=tree.get_children()
        for item in x:
            tree.delete(item)

    tree=ttk.Treeview(tp1,height=10,columns=('col1','col2','col3','col4','col5'),show='headings',selectmode='browse')
    tree.bind('<Button-1>',choose)

    tree.column('#1', width=int(120/1800*sh), anchor='center')
    tree.column('#2', width=int(120/1800*sh), anchor='center')
    tree.column('#3', width=int(120/1800*sh), anchor='center')
    tree.column('#4', width=int(120/1800*sh), anchor='center')
    tree.column('#5', width=int(120/1800*sh)*4, anchor='center')
    tree.heading('col2', text='提示对象')
    tree.heading('col3', text='对象编号')
    tree.heading('col4', text='出现条件')
    tree.heading('col5', text='提示内容')
    tree.heading('col1', text='提示顺序')
    if managemode==1:
        showtishi()
    def zdymovenext():
        if len(text21.get(0.0,'end'))>1:
            zdyallfunction.updatezhengtitishi(text21.get(0.0,'end'))
        if zdyceshimodeexist==0:
            tp1.withdraw()
            zdyceshimode()
            print('show')
        elif zdyceshimodeexist==1:
            print('show2')
            try:
                tp1.withdraw()
                tp2.deiconify()
            except:
                pass
            
    def zdymoveformer():
        if len(text21.get(0.0,'end'))>1:
            zdyallfunction.updatezhengtitishi(text21.get(0.0,'end'))
#        im=Image.open(f'{os.getcwd()}/infor/white.png')
#        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
#        canvas.create_image(0,0,anchor='nw',image = photo)
        canvas.delete("all")
        tp1.withdraw()
        tp.deiconify()
    def managemoveformer():
        try:
            tp1.destroy()
        except:
            pass
        try:
            tp2.destroy()
        except:
            pass
    
    def managemovenext():
        if len(text21.get(0.0,'end'))>1:
            zdyallfunction.updatezhengtitishi(text21.get(0.0,'end'))
        if zdyceshimodeexist==0:
            tp1.withdraw()
            try:
                zdyceshimode()
            except:
                pass
        elif zdyceshimodeexist==1:
            tp1.withdraw()
            tp2.deiconify()
    
    ltishi=tkinter.Label(tp1,text='选中提示行后,您可右击删除或鼠标拖动修改提示顺序',fg='red')
    ltishi.place(x=0.55*width,y=0.5*height,anchor='sw')
    tree.place(x=0.55*width,y=0.5*height,anchor='nw')
    
    tp1.resizable(0,0)
    tp1.protocol("WM_DELETE_WINDOW",exittp)
    def showzhengfu():
        im=Image.open(f'{os.getcwd()}/infor/zheng.png')
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        buttonzdy26=tkinter.Button(frame2,image=imgBtn,command=zdyfangda) 
        im=Image.open(f'{os.getcwd()}/infor/fu.png')
        imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        buttonzdy27=tkinter.Button(frame2,image=imgBtn2,command=zdysuoxiao)
        buttonzdy26.grid(row=1,column=5)
        buttonzdy27.grid(row=1,column=6)
        def showmovebutton():
            if zdymode==1:
                im=Image.open(f'{os.getcwd()}/infor/ceshimoveright.png') 
                imgBtn =ImageTk.PhotoImage(im.resize((int(0.07*width),int(0.07*height)))) 
                buttonmoveright1=tkinter.Button(tp1,image=imgBtn,command=zdymovenext)
                buttonmoveright1.place(x=width,y=height,anchor='se')
                im2=Image.open(f'{os.getcwd()}/infor/zdytimumoveleft.png') 
                imgBtn2 =ImageTk.PhotoImage(im2.resize((int(0.07*width),int(0.07*height)))) 
                buttonmoveright2=tkinter.Button(tp1,image=imgBtn2,command=zdymoveformer)
                buttonmoveright2.place(x=0,y=height,anchor='sw')
                win.mainloop()
                
#                buttonmoveright1=tkinter.Button(tp1,text='向前',command=zdymovenext,fg='white',bg='black',font=('微软雅黑',10,'bold'))
#                
#                buttonmoveright1.place(x=width,y=height,anchor='se')
#                
#                buttonmoveright2=tkinter.Button(tp1,text='向后',command=zdymoveformer,fg='white',bg='black',font=('微软雅黑',10,'bold'))
#                buttonmoveright2.place(x=0,y=height,anchor='sw')
                
            if managemode==1:
#                zdyallfunction.zdytishinum=len(zdyallfunction.zdytishi)
#                print('zdyallfunction.zdytishinum='+str(zdyallfunction.zdytishinum))
                
                im=Image.open(f'{os.getcwd()}/infor/rightan.png') 
                imgBtn =ImageTk.PhotoImage(im.resize((int(0.07*width),int(0.07*height)))) 
                buttonmoveright1=tkinter.Button(tp1,image=imgBtn,command=managemovenext)
                buttonmoveright1.place(x=width,y=height,anchor='se')
                im2=Image.open(f'{os.getcwd()}/infor/leftan.png') 
                imgBtn2 =ImageTk.PhotoImage(im2.resize((int(0.07*width),int(0.07*height)))) 
                buttonmoveright2=tkinter.Button(tp1,image=imgBtn2,command=managemoveformer)
                buttonmoveright2.place(x=0,y=height,anchor='sw')
                
#                buttonmoveright1=tkinter.Button(tp1,text='向前',command=managemovenext,fg='white',bg='black',font=('微软雅黑',10,'bold'))
#                
#                buttonmoveright1.place(x=width,y=height,anchor='se')
#                
#                buttonmoveright2=tkinter.Button(tp1,text='向后',command=managemoveformer,fg='white',bg='black',font=('微软雅黑',10,'bold'))
#                buttonmoveright2.place(x=0,y=height,anchor='sw')
                win.mainloop()
                

        showmovebutton()
        win.mainloop()
    
    showzhengfu()
    
    
    win.mainloop()

def zdyceshimode():
    global tp2
    global zdyceshimodeexist,newofferquestion
    zdyceshimodeexist=1
    tp2 = tkinter.Toplevel()
    tp2.title('自定义题目测试')
    tp2.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
    tp2.geometry('%dx%d+%d+%d'%(1.1*width,height*1.05,dx,dy))
    tp2.resizable(0,0)
#    canvasbackground=tkinter.Canvas(tp2,height=height,width=width,bg='black')
#    canvasbackground.place(x=0,y=0,anchor='nw')
    
    def shangchuan():
        tp=tkinter.Toplevel()
        tp.title('保存上传')
        tp.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp.geometry('%dx%d+%d+%d'%(0.4*width,0.4*height,dx,dy))
#        lable1=tkinter.Label(tp,text="数字编号",fg='red')
#        e1=tkinter.Entry(tp,width=10)
        lable2=tkinter.Label(tp,text="公开状态",fg='red')
        cmb2 = ttk.Combobox(tp,width=10)
        cmb2['value'] = ('公开','私密')
        cmb2.current(0)
        lable3=tkinter.Label(tp,text="绘制内容",fg='red')
        cmb3 = ttk.Combobox(tp,width=10)
        cmb3['value'] = ('弯矩图')
        cmb3.current(0)
        lable4=tkinter.Label(tp,text="应用模式",fg='red')
        cmb4 = ttk.Combobox(tp,width=10)
        cmb4['value'] = ('作答模式')
        cmb4.current(0)
        lable5=tkinter.Label(tp,text="题型描述",fg='red')
        t1=tkinter.Text(tp,width=20,height=10)
        lable6=tkinter.Label(tp,text="提示方式",fg='red')
        cmb6 = ttk.Combobox(tp,width=15)
        cmb6['value'] = ('自定义提示')
        cmb6.current(0)
        lable7=tkinter.Label(tp,text="难度自评",fg='red')
        cmb7 = ttk.Combobox(tp,width=15)
        cmb7['value'] = (chr(0x2605),chr(0x2605)*2,chr(0x2605)*3,chr(0x2605)*4,chr(0x2605)*5)
        cmb7.current(0)
        def qualifyshangchuan():
            global newofferquestion
#            zdyallfunction.timunum=e1.get()
            zdyallfunction.timustate=cmb2.get()
            zdyallfunction.timuhuizhi=cmb3.get()
            zdyallfunction.timuyingyong=cmb4.get()
            zdyallfunction.timumiaoshu=t1.get('0.0','end')
            zdyallfunction.timutishifangshi=cmb6.get()
            zdyallfunction.timunandu=len(cmb7.get())
            zdyallfunction.createanswers()
            state=zdyallfunction.qualifyshangchuan()
            if state==1:
                tp.destroy()
                tkinter.messagebox.showinfo(title='提示', message='上传成功！')
                if newofferquestion==1 and zdyallfunction.timustate=='公开':
                    conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
                    cursor = conn.cursor()
                    sql="update achievements set levelcredits=levelcredits+100 where userID='%s'"%(zdyallfunction.userID)
                    cursor.execute(sql)
                    sql="update achievements set honorcredits=honorcredits+100 where userID='%s'"%(zdyallfunction.userID)
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    tkinter.messagebox.showinfo(title='提示', message='获得100经验与100荣誉积分，题目被点赞可获得额外的荣誉积分！')
                newofferquestion=0
                global achievement1
                achievement1.destroy()
                achievement1=ACHIEVEMENTSFRAME(tp2,height=height,width=0.1*width,highlightbackground='black',highlightthickness=4)
                achievement1.place(x=width,y=0,anchor='nw')
                achievement1.bind()

            else:
                tkinter.messagebox.showinfo(title='提示', message='上传失败,数字编号重复,请修改数字编号！')
        b1=tkinter.Button(tp,text='确认上传',fg='red',font=('微软雅黑',13),width=10,height=1,command=qualifyshangchuan)
        helplable=tkinter.Label(tp,text="点击确认上传后请耐心等待上传完成",fg='red')
        l=tkinter.Label(tp,width=10)
#        lable1.grid(row=0,column=0)
#        e1.grid(row=1,column=0)
        lable3.grid(row=0,column=2)
        cmb3.grid(row=1,column=2)
        lable2.grid(row=0,column=0)
        cmb2.grid(row=1,column=0)
        lable4.grid(row=2,column=2)
        cmb4.grid(row=3,column=2)
        lable5.grid(row=5,column=0)
        t1.grid(row=6,column=0)
        lable6.grid(row=2,column=0)
        cmb6.grid(row=3,column=0)
        lable7.grid(row=4,column=2)
        cmb7.grid(row=5,column=2)
        l.grid(row=8,column=1)
        b1.grid(row=6,column=2)
        helplable.grid(row=7,column=2)
        
        
        
        
    def startceshi():
        c1.smallest_index=-1
        #初始化，角约束jys，线约束xys，删除线约束scxys，半结构switchbjg
        #改变刚度的列表gangdu，断点列表duandian
        zdyallfunction.jys=[]
        zdyallfunction.xys=[]
        zdyallfunction.scxys=[]
        c1.ufocus=0
        global gangdu
        gangdu=[]
        c1.createduandian()
        c1.drawuserM()
        c1.relativeposition()
        zdyallfunction.createanswers()
        c1.showuserM()
    
    def qdpart():
        smallest_index=c1.smallest_index
#        global varnum
        dangwei=c2.dangwei
        d=c2.d
        choice=c2.choice
        choiceelement=c2.choiceelement
        yli=c2.yli
        ylj=c2.ylj
        xli=c2.xli
        xlj=c2.xlj
        positions=c2.positions
#        yli,ylj,xli,xlj
        #清空显示距离的label
#        varnum.set('')
        class C_():
            pass
        alp=zdyallfunction.elements[choiceelement-1]['alp']
        if alp==180 or alp==-180:
            Mi=yli-positions[2][1]
            Mj=ylj-positions[0][1]
            Mmid=yli-positions[1][1]
            print(1)
        elif -90<alp<90:
            #确定过某一控制点与轴线平行的直线方程式，计算距离,
            #i端，中点，j端都一样，不过控制点坐标不同
            k=(ylj-yli)/(xlj-xli)
            b=yli-k*xli
            Mi=positions[0][1]-k*positions[0][0]-b
            Mj=positions[2][1]-k*positions[2][0]-b
            Mmid=positions[1][1]-k*positions[1][0]-b
            Mi=Mi/np.sqrt(1+k*k)
            Mj=Mj/np.sqrt(1+k*k)
            Mmid=Mmid/np.sqrt(1+k*k)
            print(2)
        elif alp==90:
            Mi=positions[0][0]-xli
            Mj=positions[2][0]-xlj
            print(3)
            Mmid=positions[1][0]-xli
        elif alp==-90:
            Mi=xli-positions[0][0]
            Mj=xlj-positions[2][0]
            Mmid=xli-positions[1][0]
            print(4)
        else:
            k=(ylj-yli)/(xlj-xli)
            b=yli-k*xli
            Mi=positions[2][1]-k*positions[2][0]-b
            Mj=positions[0][1]-k*positions[0][0]-b
            Mmid=positions[1][1]-k*positions[1][0]-b
            Mi=Mi/np.sqrt(1+k*k)*-1
            Mj=Mj/np.sqrt(1+k*k)*-1
            Mmid=Mmid/np.sqrt(1+k*k)*-1
            print(5)
        #不同档位，数值不同
        if dangwei==1:
            Mi=np.round(Mi/d)
            Mj=np.round(Mj/d)
        if dangwei==0.5:
            Mi=np.round(Mi/(0.5*d))/2
            Mj=np.round(Mj/(0.5*d))/2
        if dangwei==0.25:
            Mi=np.round(Mi/(0.25*d))/4
            Mj=np.round(Mj/(0.25*d))/4
        print('Mi=%f'%Mi,'Mj=%f'%Mj)
        Mmid=np.round(Mmid/d)
        c_=C_()
        
        if choice=='s':
    #        c_['num']=choiceelement
    #        c_['type']=choice
    #        c_['Mi']=0
    #        c_['Mj']=0
    #        c_['Mmid']=0
            pass
        else:
            #c_为用户作答的记录
            c_.num=choiceelement
            c_.type=choice
            c_.Mi=Mi
            c_.Mj=Mj
            c_.Mmid=Mmid
            c_.ns=zdyallfunction.ps
            c_.ne=zdyallfunction.pe
        zdyallfunction.changec(c_)

        c1.smallest_index=-1
        zdyallfunction.drawuserM(c1.smallest_index)
        c2.delete(tkinter.ALL)
        c2.b1.place(x=-100,y=0)
        c2.b2.place(x=-100,y=0)
        c2.b3.place(x=-100,y=0)
        c1.paintline(zdyallfunction.c,c1.relposition)
        c2.delete(tkinter.ALL)
        c2.b1.place(x=-100,y=0)
        c2.b2.place(x=-100,y=0)
        c2.b3.place(x=-100,y=0)
        
        
    def zdytishi():
        if zdyallfunction.jys!=[] or len(zdyallfunction.xys)!=len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='请先去除添加的约束')
            return 0
#        ttt=zdyallfunction.jiyutishi()
#        if ttt==0:
#            tkinter.messagebox.showinfo(title='提示', message='请点击分析与提示，修改作答')
        else:
            weizuoda=1
            for i in range(len(zdyallfunction.a)):
                if len(zdyallfunction.c[i])==len(zdyallfunction.a[i]):
                    weizuoda=0
            if weizuoda==1:
                tkinter.messagebox.showinfo(title='提示', message=zdyallfunction.zhengtitishi)
                return 0
#            if wanchengzuoda==0:
#                tkinter.messagebox.showinfo(title='', message='请先完成作答再比对')
#            else:
            zdycuowunum=zdyallfunction.offerzdytishi()
            if zdycuowunum!=-1:
                tkinter.messagebox.showinfo(title='提示', message=zdyallfunction.zdytishi.iloc[zdycuowunum,4])
            else:
                tkinter.messagebox.showinfo(title='提示', message="特征点作答正确")
    def zdybidui():
        global Qnum
        if zdyallfunction.jys!=[] or len(zdyallfunction.xys)!=len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='请先去除添加的约束')
            return 0
#        ttt=zdyallfunction.jiyutishi()
#        if ttt==0:
##            recordcuoti()
#            tkinter.messagebox.showinfo(title='提示', message='请点击分析与提示，修改作答')
        else:
            wanchengzuoda=1
            for i in range(len(zdyallfunction.a)):
                if len(zdyallfunction.c[i])!=len(zdyallfunction.a[i]):
                    wanchengzuoda=0
            if wanchengzuoda==0:
                tkinter.messagebox.showinfo(title='', message='请先完成作答再比对')
                return 0
            else:
                rp1=zdyallfunction.biduileixing()
                if rp1==0:
                    showcuowu()
                    c1.delete('wrong')
                    pix=c1.relposition[zdyallfunction.cuowunum]['pix']
                    piy=c1.relposition[zdyallfunction.cuowunum]['piy']
                    pjx=c1.relposition[zdyallfunction.cuowunum]['pjx']
                    pjy=c1.relposition[zdyallfunction.cuowunum]['pjy']
                    c1.create_line(pix, piy,
                      pjx, pjy,
                      fill='red',  # 红色
                      width=5,
                      tag=('wrong')
                      )
    #                zdyallfunction.showleixing()
                    #                    recordcuoti()
    #                c1.showuserM()
                else:
                    rp2=zdyallfunction.biduizf()
                    if rp2==0:
                        showcuowu()
                        c1.delete('wrong')
                        pix=c1.relposition[zdyallfunction.cuowunum]['pix']
                        piy=c1.relposition[zdyallfunction.cuowunum]['piy']
                        pjx=c1.relposition[zdyallfunction.cuowunum]['pjx']
                        pjy=c1.relposition[zdyallfunction.cuowunum]['pjy']
                        c1.create_line(pix, piy,
                          pjx, pjy,
                          fill='red',  # 红色
                          width=5,
                          tag=('wrong')
                          )
    #                    zdyallfunction.showzf()
                        #                        recordcuoti()
    #                    c1.showuserM()
                    else:
                        rp3=zdyallfunction.biduixddx()
                        if rp3==0:
                            showcuowu()
                            c1.delete('wrong')
                            pix=c1.relposition[zdyallfunction.cuowunum]['pix']
                            piy=c1.relposition[zdyallfunction.cuowunum]['piy']
                            pjx=c1.relposition[zdyallfunction.cuowunum]['pjx']
                            pjy=c1.relposition[zdyallfunction.cuowunum]['pjy']
                            c1.create_line(pix, piy,
                              pjx, pjy,
                              fill='red',  # 红色
                              width=5,
                              tag=('wrong')
                              )
    #                        zdyallfunction.showxddx()
    #                        #                            recordcuoti()
    #                        c1.showuserM()
                        else:
                            rp4=zdyallfunction.biduijdfp()
                            if rp4==0:
                                showcuowu()
                                c1.delete('wrong')
                                for i in range(len(zdyallfunction.elements)):
                                    if zdyallfunction.elements[i]['pi']['num']==zdyallfunction.cuowunum:
                                        xc=c1.relposition[zdyallfunction.cuowunum]['pix']
                                        yc=c1.relposition[zdyallfunction.cuowunum]['piy']
                                        break
                                    if zdyallfunction.elements[i]['pj']['num']==zdyallfunction.cuowunum:
                                        xc=c1.relposition[zdyallfunction.cuowunum]['pjx']
                                        yc=c1.relposition[zdyallfunction.cuowunum]['pjy']
                                        break
                                print(xc,yc)
                                circle_dimension=int(20/1800*height)
                                c1.create_oval(xc-circle_dimension,yc-circle_dimension,
                                 xc+circle_dimension,yc+circle_dimension,tag='wrong',width=5, outline='red')
    #                            zdyallfunction.showjdfp()
                                #                                recordcuoti()
    #                            c1.showuserM()            
                            else:
                                print('55555555555')
                                text2.delete('0.0','end')
                                tkinter.messagebox.showinfo(title='作答结果', message='恭喜！回答正确')
            
            
            
            
            
            
            
            
            
            
    
                                
                                
    def qualifymanageshangchuan():
        zdyallfunction.qualifymanageshangchuan()    
        tkinter.messagebox.showinfo(title='结果', message='上传成功') 
    global c1,c2                   
    c1=Xuanzecanvas(master=tp2,height=0.5*height,width=0.5*width,bg='white')
    c1.place(x=0,y=0.5*height,anchor='nw')
    c2=Zuodacanvas(master=tp2,height=0.4*height,width=0.4*height,bg='white')
    c2.qualifypartner(c1)
    c2.place(x=0,y=0,anchor='nw')
    c1.qualifypartner(c2)
    hp=int(0.5*height)
    wp=int(0.5*width)
    frame1=tkinter.Frame(tp2,width=0.3*width,height=0.1*height)
    frame1.place(x=0.52*width,y=0.55*height,anchor='nw')
    buttonzdy31=tkinter.Button(frame1,text='开始测试',fg='white',bg='black',font=('微软雅黑',13),width=10,height=1,command=startceshi)
#    buttonzdy32=tkinter.Button(frame1,text='结束测试',fg='white',bg='black',font=('微软雅黑',13),width=10,height=1)
    if zdymode==1:
        buttonzdy33=tkinter.Button(frame1,text='保存上传',fg='white',bg='black',font=('微软雅黑',13),width=10,height=1,command=shangchuan)
    if managemode==1:
        buttonzdy33=tkinter.Button(frame1,text='保存上传',fg='white',bg='black',font=('微软雅黑',13),width=10,height=1,command=qualifymanageshangchuan)
    buttonzdy31.grid(row=0,column=0)
#    buttonzdy32.grid(row=0,column=2)
    buttonzdy33.grid(row=0,column=4)
    
    uploadnotice=tkinter.Label(frame1,text='若您上传的题目被点赞可持续不断获得荣誉积分',font=('微软雅黑',10,'bold'),fg='red')
    uploadnotice.grid(row=0,column=5)
    
    button34=tkinter.Button(tp2,text='确定',font=('微软雅黑',13),width=5,height=1,command=qdpart)
    button34.place(x=0.4*height,y=0.4*height,anchor='sw')
    frame2=tkinter.Frame(tp2,width=0.2*width,height=0.2*height)
    frame2.place(x=0.4*height,y=0.1*height)
    lable31=tkinter.Label(frame2,text='档位选择',font=('微软雅黑',10),width=8,height=1,fg='white',bg='black')
    cmb1 = ttk.Combobox(frame2,width=6)
    cmb1['value'] = ('整数档','0.5档','0.25档')
    def dw(event):
        if (cmb1.get()=="整数档"):
            c2.dangwei=1
        if (cmb1.get()=="0.5档"):
            c2.dangwei=0.5
        if (cmb1.get()=="0.25档"):
            c2.dangwei=0.25
    cmb1.bind("<<ComboboxSelected>>",dw)
    cmb1.current(0)
    lable31.grid(row=0,column=0)
    cmb1.grid(row=1,column=0)
    text2=tkinter.Text(tp2,font=('微软雅黑',10),height=5,width=40)
    text2.place(x=0.8*height,y=height,anchor='sw')
    def showcuowu():
        text2.delete('0.0','end')
        text2.insert('end',zdyallfunction.cuowu)
    
    def moveformer():
        tp2.withdraw()
        tp1.deiconify()
    button35=tkinter.Button(tp2,text='分析提示',font=('微软雅黑',13),width=10,height=1,fg='white',bg='black',command=zdytishi)
    button36=tkinter.Button(tp2,text='提交比对',font=('微软雅黑',13),width=10,height=1,fg='white',bg='black',command=zdybidui)
    button35.place(x=0.9*height,y=0.65*height,anchor='nw')
    button36.place(x=0.9*height,y=0.75*height,anchor='nw')
    c3=tkinter.Canvas(tp2,height=0.5*height,width=0.5*width,bg='white')
    im=Image.open(f'{os.getcwd()}/drawing/question.png')
    photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
    c3.create_image(0,0,anchor='nw',image = photo)
    c3.place(x=0.5*width,y=0,anchor='nw')
    im2=Image.open(f'{os.getcwd()}/infor/zdytishimoveleft.png') 
    imgBtn2 =ImageTk.PhotoImage(im2.resize((int(0.05*width),int(0.05*height)))) 
    buttonmoveleft2=tkinter.Button(tp2,image=imgBtn2,command=moveformer)
    buttonmoveleft2.place(x=0,y=height*1.05,anchor='sw')
    tp2.resizable(0,0)
    def movenext():
        q=tkinter.messagebox.askokcancel(title='提示', message='确认要返回吗？')
        if q==True:
            global zdyceshimodeexist,zdytishimodeexist,zdytimumodeexist
            zdytishimodeexist=0
            zdyceshimodeexist=0
            zdytimumodeexist=0
            try:
                tp.destroy()
            except:
                pass
            try:
                tp1.destroy()
            except:
                pass
            try:
                tp2.destroy()
            except:
                pass
            global managemode
            if managemode!=1:
                modechoice()
            else:
                managemode=0
    im3=Image.open(f'{os.getcwd()}/infor/rightan.png') 
    imgBtn3 =ImageTk.PhotoImage(im3.resize((int(0.05*width),int(0.05*height)))) 
    buttonmoveleft3=tkinter.Button(tp2,image=imgBtn3,command=movenext)
    buttonmoveleft3.place(x=width,y=height*1.05,anchor='se')
    
    
    

    tp2.protocol("WM_DELETE_WINDOW",exittp)
    global achievement1
    achievement1=ACHIEVEMENTSFRAME(tp2,height=height,width=0.1*width,highlightbackground='black',highlightthickness=4)
    achievement1.place(x=width,y=0,anchor='nw')
    achievement1.bind()
    win.mainloop()



def showquestionselection():
    global questionselection
    questionselection=QUESTIONSELECTION()
    questionselection.protocol("WM_DELETE_WINDOW",exittp)
    zuodamode()
#    global tp2
#    tp2.withdraw()

def zuodamode():
    gangdu=[]
    global newquestion,rightanswerquestion
    newquestion=0
    global tp2
    tp2 = tkinter.Toplevel()
    tp2.title('作答模式       版权所有,侵权必究 All Rights Reserved @Tongji University')
    tp2.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
    tp2.geometry('%dx%d+%d+%d'%(1.1*width,height*1.05,dx,dy))
    tp2.resizable(0,0)

    def qdpart():
        smallest_index=c1.smallest_index
        # global varnum
        dangwei=c2.dangwei
        d=c2.d
        choice=c2.choice
        choiceelement=c2.choiceelement
        yli=c2.yli
        ylj=c2.ylj
        xli=c2.xli
        xlj=c2.xlj
        positions=c2.positions
        #        yli,ylj,xli,xlj
        #清空显示距离的label
        #        varnum.set('')
        class C_():
            pass
        alp=zdyallfunction.elements[choiceelement-1]['alp']
        if alp==180 or alp==-180:
            Mi=yli-positions[2][1]
            Mj=ylj-positions[0][1]
            Mmid=yli-positions[1][1]
            print(1)
        elif -90<alp<90:
            #确定过某一控制点与轴线平行的直线方程式，计算距离,
            #i端，中点，j端都一样，不过控制点坐标不同
            k=(ylj-yli)/(xlj-xli)
            b=yli-k*xli
            Mi=positions[0][1]-k*positions[0][0]-b
            Mj=positions[2][1]-k*positions[2][0]-b
            Mmid=positions[1][1]-k*positions[1][0]-b
            Mi=Mi/np.sqrt(1+k*k)
            Mj=Mj/np.sqrt(1+k*k)
            Mmid=Mmid/np.sqrt(1+k*k)
            print(2)
        elif alp==90:
            Mi=positions[0][0]-xli
            Mj=positions[2][0]-xlj
            print(3)
            Mmid=positions[1][0]-xli
        elif alp==-90:
            Mi=xli-positions[0][0]
            Mj=xlj-positions[2][0]
            Mmid=xli-positions[1][0]
            print(4)
        else:
            k=(ylj-yli)/(xlj-xli)
            b=yli-k*xli
            Mi=positions[2][1]-k*positions[2][0]-b
            Mj=positions[0][1]-k*positions[0][0]-b
            Mmid=positions[1][1]-k*positions[1][0]-b
            Mi=Mi/np.sqrt(1+k*k)*-1
            Mj=Mj/np.sqrt(1+k*k)*-1
            Mmid=Mmid/np.sqrt(1+k*k)*-1
            print(5)
        #不同档位，数值不同
        if dangwei==1:
            Mi=np.round(Mi/d)
            Mj=np.round(Mj/d)
        if dangwei==0.5:
            Mi=np.round(Mi/(0.5*d))/2
            Mj=np.round(Mj/(0.5*d))/2
        if dangwei==0.25:
            Mi=np.round(Mi/(0.25*d))/4
            Mj=np.round(Mj/(0.25*d))/4
        print('Mi=%f'%Mi,'Mj=%f'%Mj)
        Mmid=np.round(Mmid/d)
        c_=C_()
        
        if choice=='s':
    #        c_['num']=choiceelement
    #        c_['type']=choice
    #        c_['Mi']=0
    #        c_['Mj']=0
    #        c_['Mmid']=0
            pass
        else:
            #c_为用户作答的记录
            c_.num=choiceelement
            c_.type=choice
            c_.Mi=Mi
            c_.Mj=Mj
            c_.Mmid=Mmid
            c_.ns=zdyallfunction.ps
            c_.ne=zdyallfunction.pe
        zdyallfunction.changec(c_)

        c1.smallest_index=-1
        #        zdyallfunction.drawuserM(c1.smallest_index)
        c1.paintline(zdyallfunction.c,c1.relposition)
        c2.delete(tkinter.ALL)
        c2.b1.place(x=-100,y=0)
        c2.b2.place(x=-100,y=0)
        c2.b3.place(x=-100,y=0)
        zdyallfunction.recordansweringprocess(-1)
        #        c1.showuserM()
    
    #程序自带的提示方式
    def showtishi():
        if zdyallfunction.jys!=[] or len(zdyallfunction.xys)!=len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='请先去除添加的约束')
            return 0
        zdyallfunction.bianbietixing()
        zdyallfunction.jiyutishi()
        if zdyallfunction.tishi!='':
            tkinter.messagebox.showinfo(title='提示', message='%s'%zdyallfunction.tishi)
        if zdyallfunction.tishi=='':
            tkinter.messagebox.showinfo(title='提示', message='特征点作答正确或此题无提示与分析')
    
    #tishichoice先判断给予提示的方式，是自定义还是程序自带的提示方式
    def tishichoice():
        if zdyallfunction.timutishifangshi=="自定义提示":
            zdytishi()
            zdyallfunction.recordansweringprocess(0)
        else:
            showtishi()
            zdyallfunction.recordansweringprocess(1)
    
    #zdytishi是使用自定义的提示
    def zdytishi():
        if zdyallfunction.jys!=[] or len(zdyallfunction.xys)!=len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='请先去除添加的约束')
            return 0
        #        ttt=zdyallfunction.jiyutishi()
        #        if ttt==0:
        #            tkinter.messagebox.showinfo(title='提示', message='请点击分析与提示，修改作答')
        else:
            weizuoda=1
            for i in range(len(zdyallfunction.a)):
                if len(zdyallfunction.a[i])==len(zdyallfunction.c[i]):
                        weizuoda=0 
            if weizuoda==1:
                if len(zdyallfunction.zhengtitishi)>1:
                    tkinter.messagebox.showinfo(title='提示', message=zdyallfunction.zhengtitishi)
                    return 0
                tkinter.messagebox.showinfo(title='提示', message="请先尝试作答")
                return 0
            #            wanchengzuoda=1
            #            for i in range(len(zdyallfunction.a)):
            #                if len(zdyallfunction.c[i])!=len(zdyallfunction.a[i]):
            #                    wanchengzuoda=0
            #            if wanchengzuoda==0:
            #                tkinter.messagebox.showinfo(title='', message='请先完成作答再比对')
            #            else:
            zdycuowunum=zdyallfunction.offerzdytishi()
            zdyallfunction.zdycuowunum=zdycuowunum
            if zdycuowunum!=-1:
                tkinter.messagebox.showinfo(title='提示', message=zdyallfunction.zdytishi.iloc[zdycuowunum,4])
            else:
                tkinter.messagebox.showinfo(title='提示', message="特征点作答正确")
    def zdybidui():
        global Qnum
        global newquestion,rightanswerquestion
        def addlevelcredits():
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="select levelcredits from achievements where userID='%s'"%(zdyallfunction.userID)
            cursor.execute(sql)
            result=cursor.fetchone()
            result=int(result[0])
            conn.commit()
            cursor.close()
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update achievements set levelcredits='%d' where userID='%s'"%(result+round(float(zdyallfunction.timunandu),1)*10,zdyallfunction.userID)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            
        if zdyallfunction.jys!=[] or len(zdyallfunction.xys)!=len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='请先去除添加的约束')
            return 0
        if zdyallfunction.timutishifangshi!='自定义提示':
            zdyallfunction.bianbietixing()
            tishiright=zdyallfunction.jiyutishi()
            print(tishiright)
            zdyallfunction.tishiright=tishiright
            zdyallfunction.recordansweringprocess(2)
            if tishiright==0:
                #            recordcuoti()
                tkinter.messagebox.showinfo(title='提示', message='请点击分析与提示，修改作答')
                if newquestion==1:
                    zdyallfunction.momentanswer_record()
                return 0
        if newquestion==1:
            zdyallfunction.momentanswer_record()
        newquestion=0
        wanchengzuoda=1
        for i in range(len(zdyallfunction.a)):
            if len(zdyallfunction.c[i])!=len(zdyallfunction.a[i]):
                wanchengzuoda=0
        if wanchengzuoda==0:
            tkinter.messagebox.showinfo(title='', message='请先完成作答再比对')
            return 0
        else:
            rp1=zdyallfunction.biduileixing()
            if rp1==0:
                showcuowu()
                c1.delete('wrong')
                pix=c1.relposition[zdyallfunction.cuowunum]['pix']
                piy=c1.relposition[zdyallfunction.cuowunum]['piy']
                pjx=c1.relposition[zdyallfunction.cuowunum]['pjx']
                pjy=c1.relposition[zdyallfunction.cuowunum]['pjy']
                c1.create_line(pix, piy,
                  pjx, pjy,
                  fill='red',  # 红色
                  width=5,
                  tag=('wrong')
                  )
#                zdyallfunction.showleixing()
                #                    recordcuoti()
#                c1.showuserM()
            else:
                rp2=zdyallfunction.biduizf()
                if rp2==0:
                    showcuowu()
                    c1.delete('wrong')
                    pix=c1.relposition[zdyallfunction.cuowunum]['pix']
                    piy=c1.relposition[zdyallfunction.cuowunum]['piy']
                    pjx=c1.relposition[zdyallfunction.cuowunum]['pjx']
                    pjy=c1.relposition[zdyallfunction.cuowunum]['pjy']
                    c1.create_line(pix, piy,
                      pjx, pjy,
                      fill='red',  # 红色
                      width=5,
                      tag=('wrong')
                      )
#                    zdyallfunction.showzf()
                    #                        recordcuoti()
#                    c1.showuserM()
                else:
                    rp3=zdyallfunction.biduixddx()
                    if rp3==0:
                        showcuowu()
                        c1.delete('wrong')
                        pix=c1.relposition[zdyallfunction.cuowunum]['pix']
                        piy=c1.relposition[zdyallfunction.cuowunum]['piy']
                        pjx=c1.relposition[zdyallfunction.cuowunum]['pjx']
                        pjy=c1.relposition[zdyallfunction.cuowunum]['pjy']
                        c1.create_line(pix, piy,
                          pjx, pjy,
                          fill='red',  # 红色
                          width=5,
                          tag=('wrong')
                          )
#                        zdyallfunction.showxddx()
#                        #                            recordcuoti()
#                        c1.showuserM()
                    else:
                        rp4=zdyallfunction.biduijdfp()
                        if rp4==0:
                            showcuowu()
                            c1.delete('wrong')
                            for i in range(len(zdyallfunction.elements)):
                                if zdyallfunction.elements[i]['pi']['num']==zdyallfunction.cuowunum:
                                    xc=c1.relposition[zdyallfunction.cuowunum]['pix']
                                    yc=c1.relposition[zdyallfunction.cuowunum]['piy']
                                    break
                                if zdyallfunction.elements[i]['pj']['num']==zdyallfunction.cuowunum:
                                    xc=c1.relposition[zdyallfunction.cuowunum]['pjx']
                                    yc=c1.relposition[zdyallfunction.cuowunum]['pjy']
                                    break
                            print(xc,yc)
                            circle_dimension=int(20/1800*height)
                            c1.create_oval(xc-circle_dimension,yc-circle_dimension,
                             xc+circle_dimension,yc+circle_dimension,tag='wrong',width=5, outline='red')
#                            zdyallfunction.showjdfp()
                            #                                recordcuoti()
#                            c1.showuserM()
                        else:
                            text2.delete('0.0','end')
                            c1.delete('wrong')
                            c1.delete('choice')
                            if rightanswerquestion==0:
                                addlevelcredits()
                            rightanswerquestion=1
                            global achievement
                            achievement.destroy()
                            achievement=ACHIEVEMENTSFRAME(tp2,height=height,width=0.1*width,highlightbackground='black',highlightthickness=4)
                            achievement.place(x=width,y=0,anchor='nw')
                            tkinter.messagebox.showinfo(title='作答结果', message='恭喜！回答正确')
                            achievement.bind()
                            #                            tkinter.messagebox.showinfo(title='作答结果', message='恭喜！回答正确')
                            #                                recordcorrectnum()
    def showquestion():
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        c3.create_image(0,0,anchor='nw',image = photo)
        win.mainloop()
            
            



        

    #        
    #        def qualifyquestionsymbol(event):
    #                item =tree.selection()[0]
    #                global questionsymbol
    #                questionsymbol=tree.item(item, "values")[0]
    #                zdyallfunction.questionsymbol=tree.item(item, "values")[0]
    #                chuti()
                

    #        global evaluation
    #        evaluation=EVALUATION(tp2,height=0.1*height,width=0.35*width)
    #        evaluation.place(x=0.62*width,y=0.5*height)
    #        evaluation.bind()

    
    
    
    
    
    def chuti():
        global gangdu,newquestion,questionsymbol,rightanswerquestion
        newquestion=1
        rightanswerquestion=0
        ts = time.time()
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        zdyallfunction.starttime=dt
    #        questionsymbol='Tongji_11'
        text2.delete('0.0','end')
        zdyallfunction.jys=[]
        zdyallfunction.xys=[]
        zdyallfunction.scxys=[]
        c1.ufocus=0
        zdyallfunction.switchbjg=0
        lb1.delete(0,'end')
        
        gangdu=[]
        zdyallfunction.daduan=0
        zdyallfunction.duandian=[]
        
        zdyallfunction.getquestion(questionsymbol)
    #        print(zdyallfunction.informatrixs[0])
        zdyallfunction.fileinelements()
        zdyallfunction.file()
        zdyallfunction.calculation()
        zdyallfunction.drawquestion()
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((wp,hp),Image.ANTIALIAS))
        c3.create_image(0,0,anchor='nw',image = photo)
        smallest_index=-1
        showinfor()
        for i in range(len(zdyallfunction.elements)):
            zdyallfunction.duandian.append([0,1])
        #初始化，角约束jys，线约束xys，删除线约束scxys，半结构switchbjg
        #改变刚度的列表gangdu，断点列表duandian
        zdyallfunction.drawuserM(smallest_index)
        c1.relativeposition()
        zdyallfunction.createanswers()
        if zdyallfunction.timutishifangshi!="自定义提示":
            zdyallfunction.bianbiedcx()
            zdyallfunction.bianbietixing()
        c1.showuserM()
        win.mainloop()
    

    global c1,c2,c3,wp,hp,text2,lb1
    c1=Xuanzecanvas(master=tp2,height=0.5*height,width=0.5*width,bg='white')
    c1.place(x=0,y=0.5*height,anchor='nw')
    c2=Zuodacanvas(master=tp2,height=0.4*height,width=0.4*height,bg='white')
    c2.qualifypartner(c1)
    c2.place(x=0,y=0,anchor='nw')
    c1.qualifypartner(c2)
    hp=int(0.5*height)
    wp=int(0.5*width)
    frame1=tkinter.Frame(tp2,width=0.3*width,height=0.1*height)
    frame1.place(x=0.52*width,y=0.52*height,anchor='nw')
    #    def showrecommendation():
    #        global tp2
    #        tp2.withdraw()
    #        global recommendation
    #        recommendation=RECOMMENDATION()
    #        tkinter.messagebox.showinfo(title='提示', message='请您耐心等待界面刷新！')
    #        recommendation.qualifyrecommendationquestions()
    #        win.mainloop()


    buttonzdy31=tkinter.Button(frame1,text='为您推荐',fg='white',bg='black',font=('微软雅黑',13),width=10,height=1,command=showrecommendation)
    #    buttonzdy32=tkinter.Button(frame1,text='结束测试',fg='white',bg='black',font=('微软雅黑',13),width=10,height=1)
    #    buttonzdy33=tkinter.Button(frame1,text='保存上传',fg='white',bg='black',font=('微软雅黑',13),width=10,height=1)
    buttonzdy31.grid(row=0,column=0)
    #    buttonzdy32.grid(row=0,column=2)
    #    buttonzdy33.grid(row=0,column=4)
    button34=tkinter.Button(tp2,text='确定',font=('微软雅黑',13),width=5,height=1,command=qdpart)
    button34.place(x=0.4*height,y=0.4*height,anchor='sw')
    frame2=tkinter.Frame(tp2,width=0.2*width,height=0.2*height)
    frame2.place(x=0.4*height,y=0.1*height)
    lable31=tkinter.Label(frame2,text='档位选择',font=('微软雅黑',10),width=8,height=1,fg='white',bg='black')
    cmb1 = ttk.Combobox(frame2,width=6)
    cmb1['value'] = ('整数档','0.5档','0.25档')
    def dw(event):
        if (cmb1.get()=="整数档"):
            c2.dangwei=1
        if (cmb1.get()=="0.5档"):
            c2.dangwei=0.5
        if (cmb1.get()=="0.25档"):
            c2.dangwei=0.25
    cmb1.bind("<<ComboboxSelected>>",dw)
    cmb1.current(0)
    lable31.grid(row=0,column=0)
    cmb1.grid(row=1,column=0)
    text2=tkinter.Text(tp2,font=('微软雅黑',10),height=5,width=40)
    text2.place(x=0.8*height,y=height,anchor='sw')
    lb1=tkinter.Listbox(tp2,font=('微软雅黑',15),height=10,width=25)
    lb1.place(x=width,y=height,anchor='se')
    def createinfor():
        global gjxx
        gjxx=[]
        for i in range(len(zdyallfunction.calelements)):
            num=zdyallfunction.calelements[i]['num']
            EA=zdyallfunction.calelements[i]['EA']
            l=zdyallfunction.calelements[i]['l']
            if zdyallfunction.calelements[i]['EA']>=1e8:
                EA=-1
            else:
                EA=zdyallfunction.calelements[i]['EA']
            if zdyallfunction.calelements[i]['EI']>=1e6:
                EI=-1
            else:
               EI=zdyallfunction.calelements[i]['EI'] 
            gjxx_='  杆件（%d）L=%d  EA=%d EI=%d'%(num,l,EA,EI)
            gjxx.append(gjxx_)
            
    #显示杆件信息，gjxx
    def showinfor():
        createinfor()
        lb1.delete(0,'end')
        for information in gjxx:
            lb1.insert('end',information)
    def gaibiangangdu():
        #确定改变刚度
        def gangduqd():
              gangdu_=[]
              gangdu_.append(int(entry3.get())) 
              gangdu_.append(int(entry4.get()))
              gangdu_.append(int(entry5.get()))
              gangdu.append(gangdu_.copy())
              entry3.delete(0,'end')
              zdyallfunction.changeEAI(gangdu)
              showinfor()
              zdyallfunction.switchEAI=1
              zdyallfunction.drawquestion()
              showquestion()
        #完成输入后计算
        def gangdujs():
            zdyallfunction.file()
            zdyallfunction.changeEAI(gangdu)
            zdyallfunction.calculation()
            showinfor()
            tp6.destroy()
            #swicthEAI负责是否要用颜色在左上角显示刚度
            zdyallfunction.switchEAI=1
            zdyallfunction.drawquestion()
            showquestion()
            
        def original():
             gangdujs()
    
    
    
        tp6=tkinter.Toplevel()
        tp6.title('改变刚度')
        tp6.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp6.geometry('%dx%d+%d+%d'%(0.3*height,0.3*height,dx,dy))
        frame6=tkinter.Frame(tp6,width=0.64*height,height=0.5*height,)
        frame6.place(x=0,y=0,anchor='nw')
        label3=tkinter.Label(frame6,text='杆件号',font=('微软雅黑',15),width=10,height=1)
        entry3=tkinter.Entry(frame6,font=('微软雅黑',15),width=10)
        label4=tkinter.Label(frame6,text='EA=',font=('微软雅黑',15),width=10,height=1)
        entry4=tkinter.Entry(frame6,font=('微软雅黑',15),width=10)
        label5=tkinter.Label(frame6,text='EI=',font=('微软雅黑',15),width=10,height=1)
        entry5=tkinter.Entry(frame6,font=('微软雅黑',15),width=10)
        button23=tkinter.Button(frame6,text='确定并预览',font=('微软雅黑',15),width=10,height=1,fg='red',command=gangduqd)
        button24=tkinter.Button(frame6,text='关闭',font=('微软雅黑',15),width=10,height=1,fg='red',command=gangdujs)
        label3.grid(row=0,column=0)
        entry3.grid(row=0,column=1)
        label4.grid(row=1,column=0)
        entry4.grid(row=1,column=1)
        label5.grid(row=2,column=0)
        entry5.grid(row=2,column=1)
        button23.grid(row=3,column=0,columnspan=4)
        button24.grid(row=4,column=0,columnspan=4)
        tp6.protocol("WM_DELETE_WINDOW",original)
    def showcuowu():
        text2.delete('0.0','end')
        text2.insert('end',zdyallfunction.cuowu)
        
    noticelable=tkinter.Label(tp2,text='请绘制弯矩图的大致形状，作答的任意过程可点击分析提示并在完成后提交比对',fg='red',font=('微软雅黑',9,'bold'))
    noticelable.place(x=0,y=0.5*height,anchor='sw')
    button35=tkinter.Button(tp2,text='分析提示',font=('微软雅黑',13),width=10,height=1,fg='white',bg='black',command=tishichoice)
    button36=tkinter.Button(tp2,text='提交比对',font=('微软雅黑',13),width=10,height=1,fg='white',bg='black',command=zdybidui)
    button35.place(x=0.9*height,y=0.65*height,anchor='nw')
    button36.place(x=0.9*height,y=0.75*height,anchor='nw')
    c3=tkinter.Canvas(tp2,height=0.5*height,width=0.5*width,bg='white')
    
    c3.place(x=0.5*width,y=0,anchor='nw')
    
    frame0=tkinter.Frame(win,height=0.5*height,width=0.1*height)
    frame0.place(x=0.8*height,y=0,anchor='ne')
    
    
    def showEAI():
        if zdyallfunction.switchEAI==0:
            zdyallfunction.switchEAI=1
        else: 
            zdyallfunction.switchEAI=0
        zdyallfunction.drawrestraintquestion()
        showquestion()
    def jysjm():
        #增角约束
        def zjys():
             if int(entry4.get())>len(zdyallfunction.joints_) or int(entry4.get())>len(zdyallfunction.joints_)<0:
                 tkinter.messagebox.showinfo(title='提示', message='节点号有误，请重新输入')
                 return
             zdyallfunction.jys.append(int(entry4.get()))
             zdyallfunction.drawrestraintquestion()
             showquestion()
    
        #删除角约束
        def sjys():
            if int(entry4.get()) in zdyallfunction.jys:
                zdyallfunction.jys.remove(int(entry4.get()))
            zdyallfunction.drawrestraintquestion()
            showquestion()
        
        #确定
        def queding():
            zdyallfunction.file()
            zdyallfunction.changecalrestraint()
            zdyallfunction.changeEAI(gangdu)
            zdyallfunction.calculation()
            zdyallfunction.drawuserM(c1.smallest_index)
            tp7.destroy()
            c1.showuserM()
            
            
        def originaljys():
            queding()
        
        tp7=tkinter.Toplevel()
        tp7.title('增加角约束')
        tp7.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp7.geometry('%dx%d+%d+%d'%(0.3*height,0.3*height,dx,dy))
        frame7=tkinter.Frame(tp7,width=0.64*height,height=0.5*height,)
        frame7.place(x=0,y=0,anchor='nw')
        label4=tkinter.Label(frame7,text='节点号',font=('微软雅黑',15),width=10,height=1)
        entry4=tkinter.Entry(frame7,font=('微软雅黑',15),width=10)
        button15=tkinter.Button(frame7,text='增加',font=('微软雅黑',15),width=10,height=1,fg='red',command=zjys)
        button16=tkinter.Button(frame7,text='删去',font=('微软雅黑',15),width=10,height=1,fg='red',command=sjys)
        button17=tkinter.Button(frame7,text='确认',font=('微软雅黑',15),width=10,height=1,fg='red',command=queding)
        
        label4.grid(row=0,column=0)
        entry4.grid(row=0,column=1)
        button15.grid(row=1,column=0,columnspan=2)
        button16.grid(row=2,column=0,columnspan=2)
        button17.grid(row=3,column=0,columnspan=2)
        tp7.protocol("WM_DELETE_WINDOW",originaljys)

    #同理如上
    def xysjm():
        class Yueshup():
            pass
        
        
        def zxys():
            if int(entry4.get())>len(zdyallfunction.joints_) or int(entry4.get())>len(zdyallfunction.joints_)<0:
                 tkinter.messagebox.showinfo(title='提示', message='节点号有误，请重新输入')
                 return
            Yueshup_=Yueshup()
            Yueshup_.num=int(entry4.get())
            Yueshup_.alp=int(entry5.get())
            zdyallfunction.xys.append(copy.copy(Yueshup_))
            zdyallfunction.changerestraint()
            zdyallfunction.changecalrestraint()
            zdyallfunction.drawrestraintquestion()
            showquestion()
        
        def sxys():
            for i in range(len(zdyallfunction.xys)):
                print(zdyallfunction.xys[i].num)
                if zdyallfunction.xys[i].num==int(entry4.get()):
                    zdyallfunction.scxys.append(int(entry4.get()))
                    print(zdyallfunction.scxys)
            zdyallfunction.changerestraint()
            zdyallfunction.changecalrestraint()
            zdyallfunction.drawrestraintquestion()
            showquestion()
            
            
        def queding():
            zdyallfunction.file()
            zdyallfunction.changecalrestraint()
            zdyallfunction.changeEAI(gangdu)
            zdyallfunction.calculation()
            zdyallfunction.drawuserM(c1.smallest_index)
            tp7.destroy()
            c1.showuserM()
            
            
            
        def originalxys():
            queding()
    
        tp7=tkinter.Toplevel()
        tp7.title('增加线约束')
        tp7.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp7.geometry('%dx%d+%d+%d'%(0.3*height,0.3*height,dx,dy))
        frame7=tkinter.Frame(tp7,width=0.64*height,height=0.5*height,)
        frame7.place(x=0,y=0,anchor='nw')
        label4=tkinter.Label(frame7,text='节点号',font=('微软雅黑',15),width=10,height=1)
        entry4=tkinter.Entry(frame7,font=('微软雅黑',15),width=10)
        label5=tkinter.Label(frame7,text='角度',font=('微软雅黑',15),width=10,height=1)
        entry5=tkinter.Entry(frame7,font=('微软雅黑',15),width=10)
        button15=tkinter.Button(frame7,text='增加',font=('微软雅黑',15),width=10,height=1,fg='red',command=zxys)
        button16=tkinter.Button(frame7,text='删去',font=('微软雅黑',15),width=10,height=1,fg='red',command=sxys)
        button17=tkinter.Button(frame7,text='确认',font=('微软雅黑',15),width=10,height=1,fg='red',command=queding)
        label4.grid(row=0,column=0)
        entry4.grid(row=0,column=1)
        label5.grid(row=1,column=0)
        entry5.grid(row=1,column=1)
        button15.grid(row=2,column=0,columnspan=2)
        button16.grid(row=3,column=0,columnspan=2)
        button17.grid(row=4,column=0,columnspan=2)
        tp7.protocol("WM_DELETE_WINDOW",originalxys)
    frame0=tkinter.Frame(tp2,height=0.5*height,width=0.1*height)
    frame0.place(x=0.8*height,y=0,anchor='ne')
    button37=tkinter.Button(frame0,text='显示刚度',font=('微软雅黑',12),width=10,height=1,bg='yellow',command=showEAI)
    button38=tkinter.Button(frame0,text='增减角约束',font=('微软雅黑',12),width=10,height=1,command=jysjm,bg='yellow')
    button39=tkinter.Button(frame0,text='增减线约束',font=('微软雅黑',12),width=10,height=1,command=xysjm,bg='yellow')
    button310=tkinter.Button(frame0,text='改变刚度',font=('微软雅黑',12),width=10,height=1,bg='yellow',command=gaibiangangdu)
    def showropemethod():
        rope=Rope(win)
        rope.bind()
    buttonropemethod=tkinter.Button(frame0,text='ropemethod',font=('微软雅黑',12),width=10,height=1,bg='yellow',command=showropemethod)
    button37.grid(row=0,column=0)
    button38.grid(row=1,column=0)
    button39.grid(row=2,column=0)
    button310.grid(row=3,column=0)
    buttonropemethod.grid(row=4,column=0)
    def wjt():
        global newquestion
        if (newquestion==1 and zdyallfunction.jys==[]) and len(zdyallfunction.xys)==len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='您可在增加约束或提交比对后查看')
            return 0
        def fangdaM():
            zdyallfunction.amplifyM(2)
            zdyallfunction.drawM()
            im=Image.open(f'{os.getcwd()}/drawing/M.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp1, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
        def suoxiaoM():
            zdyallfunction.amplifyM(1/2)
            zdyallfunction.drawM()
            im=Image.open(f'{os.getcwd()}/drawing/M.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp1, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
        
    
    
        zdyallfunction.drawM()
        tp1 = tkinter.Toplevel()
        tp1.title('弯矩图')
        tp1.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp1.geometry('%dx%d+%d+%d'%(0.72*height,0.5*height,dx,dy))
        tp1.resizable(0,0)
        im=Image.open(f'{os.getcwd()}/drawing/M.png')
        hp3=int(0.45*height)
        wp3=int(0.72*height)
        photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
        labelphoto3 = tkinter.Label(tp1, image=photo,width=wp3,height=hp3)
        labelphoto3.place(x=0, y=0,anchor='nw')
        
        
        
        frame5=tkinter.Frame(tp1,width=0.72*height,height=0.055*height,bg='deepskyblue')
        frame5.place(x=0,y=0.445*height,anchor='nw')
    
    
        im=Image.open(f'{os.getcwd()}/infor/zheng.png')
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button21=tkinter.Button(tp1,image=imgBtn,command=fangdaM)
        button21.place(x=0.36*height,y=0.5*height,anchor='se')
        
        im=Image.open(f'{os.getcwd()}/infor/fu.png')
        imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button22=tkinter.Button(tp1,image=imgBtn2,command=suoxiaoM)
        button22.place(x=0.36*height,y=0.5*height,anchor='sw')
        
        win.mainloop()
        
    def jlt():
        if (newquestion==1 and zdyallfunction.jys==[]) and len(zdyallfunction.xys)==len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='您可在增加约束或提交比对后查看')
            return 0
        def fangdaF():
            zdyallfunction.amplifyF(2)
            zdyallfunction.drawshearforce()
            im=Image.open(f'{os.getcwd()}/drawing/shearforce.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp2, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
        def suoxiaoF():
            zdyallfunction.amplifyF(1/2)
            zdyallfunction.drawshearforce()
            im=Image.open(f'{os.getcwd()}/drawing/shearforce.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp2, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
    
        zdyallfunction.drawshearforce()
        tp2 = tkinter.Toplevel()
        tp2.title('剪力图')
        tp2.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp2.geometry('%dx%d+%d+%d'%(0.72*height,0.5*height,dx,dy))
        tp2.resizable(0,0)
        im=Image.open(f'{os.getcwd()}/drawing/shearforce.png')
        hp3=int(0.45*height)
        wp3=int(0.72*height)
        photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
        labelphoto4 = tkinter.Label(tp2, image=photo,width=wp3,height=hp3)
        labelphoto4.place(x=0, y=0,anchor='nw')
        
        
        
        frame5=tkinter.Frame(tp2,width=0.72*height,height=0.055*height,bg='deepskyblue')
        frame5.place(x=0,y=0.445*height,anchor='nw')
        
        im=Image.open(f'{os.getcwd()}/infor/zheng.png')
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button21=tkinter.Button(tp2,image=imgBtn,command=fangdaF)
        button21.place(x=0.36*height,y=0.5*height,anchor='se')
        
        im=Image.open(f'{os.getcwd()}/infor/fu.png')
        imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button22=tkinter.Button(tp2,image=imgBtn2,command=suoxiaoF)
        button22.place(x=0.36*height,y=0.5*height,anchor='sw')
        win.mainloop()
    
    #如上同理
    def zlt():
        if (newquestion==1 and zdyallfunction.jys==[]) and len(zdyallfunction.xys)==len(zdyallfunction.scxys):
            tkinter.messagebox.showinfo(title='提示', message='您可在增加约束或提交比对后查看')
            return 0
        def fangdaN():
            zdyallfunction.amplifyN(2)
            zdyallfunction.drawN()
            im=Image.open(f'{os.getcwd()}/drawing/N.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp3, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
        def suoxiaoN():
            zdyallfunction.amplifyN(1/2)
            zdyallfunction.drawN()
            im=Image.open(f'{os.getcwd()}/drawing/N.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp3, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
    
        zdyallfunction.drawN()
        tp3 = tkinter.Toplevel()
        tp3.title('轴力图')
        tp3.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp3.geometry('%dx%d+%d+%d'%(0.72*height,0.5*height,dx,dy))
        tp3.resizable(0,0)
        im=Image.open(f'{os.getcwd()}/drawing/N.png')
        hp3=int(0.45*height)
        wp3=int(0.72*height)
        photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
        labelphoto4 = tkinter.Label(tp3, image=photo,width=wp3,height=hp3)
        labelphoto4.place(x=0, y=0,anchor='nw')
        
        
        
        frame5=tkinter.Frame(tp3,width=0.72*height,height=0.055*height,bg='deepskyblue')
        frame5.place(x=0,y=0.445*height,anchor='nw')
        
        im=Image.open(f'{os.getcwd()}/infor/zheng.png')
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button21=tkinter.Button(tp3,image=imgBtn,command=fangdaN)
        button21.place(x=0.36*height,y=0.5*height,anchor='se')
        
        im=Image.open(f'{os.getcwd()}/infor/fu.png')
        imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button22=tkinter.Button(tp3,image=imgBtn2,command=suoxiaoN)
        button22.place(x=0.36*height,y=0.5*height,anchor='sw')
        win.mainloop()
     
    #如上同理
    def bxt():

        def fangdaD():
            zdyallfunction.amplifydeformation(3)
            zdyallfunction.drawdeformation()
            im=Image.open(f'{os.getcwd()}/drawing/deformation.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp4, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
        def suoxiaoD():
            zdyallfunction.amplifydeformation(1/3)
            zdyallfunction.drawdeformation()
            im=Image.open(f'{os.getcwd()}/drawing/deformation.png')
            hp3=int(0.45*height)
            wp3=int(0.72*height)
            photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
            labelphoto3 = tkinter.Label(tp4, image=photo,width=wp3,height=hp3)
            labelphoto3.place(x=0, y=0,anchor='nw')
            win.mainloop()
    
    
        zdyallfunction.drawdeformation()
        
        tp4 = tkinter.Toplevel()
        tp4.title('变形图')
        tp4.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        tp4.geometry('%dx%d+%d+%d'%(0.72*height,0.5*height,dx,dy))
        tp4.resizable(0,0)
        im=Image.open(f'{os.getcwd()}/drawing/deformation.png')
        hp3=int(0.45*height)
        wp3=int(0.72*height)
        photo = ImageTk.PhotoImage(im.resize((wp3,hp3),Image.ANTIALIAS))
        labelphoto4 = tkinter.Label(tp4, image=photo,width=wp3,height=hp3)
        labelphoto4.place(x=0, y=0,anchor='nw')
        
        
        
        frame5=tkinter.Frame(tp4,width=0.72*height,height=0.055*height,bg='deepskyblue')
        frame5.place(x=0,y=0.445*height,anchor='nw')
        
        im=Image.open(f'{os.getcwd()}/infor/zheng.png')
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button21=tkinter.Button(tp4,image=imgBtn,command=fangdaD)
        button21.place(x=0.36*height,y=0.5*height,anchor='se')
        
        im=Image.open(f'{os.getcwd()}/infor/fu.png')
        imgBtn2 =ImageTk.PhotoImage(im.resize((int(0.05*height),int(0.05*height)))) 
        button22=tkinter.Button(tp4,image=imgBtn2,command=suoxiaoD)
        button22.place(x=0.36*height,y=0.5*height,anchor='sw')
        win.mainloop()    

    frame3=tkinter.Frame(tp2,height=0.5*height,width=0.2*height,)
    frame3.place(x=width-0.5*width,y=0.5*height,anchor='se')
    
    button11=tkinter.Button(frame3,text='弯矩图',font=('微软雅黑',12),width=10,height=1,bg='springgreen',command=wjt)
    button12=tkinter.Button(frame3,text='剪力图',font=('微软雅黑',12),width=10,height=1,bg='springgreen',command=jlt)
    button13=tkinter.Button(frame3,text='轴力图',font=('微软雅黑',12),width=10,height=1,bg='springgreen',command=zlt)
    button14=tkinter.Button(frame3,text='变形图',font=('微软雅黑',12),width=10,height=1,bg='springgreen',command=bxt)
    button11.grid(row=0)
    button12.grid(row=1)
    button13.grid(row=2)
    button14.grid(row=3)
    def moveformer():
    #        q=tkinter.messagebox.askokcancel(title='提示', message='确认要返回模式选择吗？')
    #        if q==True:
        tp2.withdraw()
        global questionselection
        questionselection.deiconify()
    im3=Image.open(f'{os.getcwd()}/infor/leftan.png') 
    imgBtn3 =ImageTk.PhotoImage(im3.resize((int(0.05*width),int(0.05*height)))) 
    buttonmoveleft3=tkinter.Button(tp2,image=imgBtn3,command=moveformer)
    buttonmoveleft3.place(x=0,y=height*1.05,anchor='sw')

    tp2.protocol("WM_DELETE_WINDOW",exittp)
    
    #    def showevaluation():
    #        global evaluation
    #        evaluation=EVALUATION(tp2,height=0.1*height,width=0.3*width)
    #        evaluation.place(x=0.65*width,y=0.5*height)
    #        evaluation.bind()
    #    showevaluation()
    
    tp2.withdraw()
    global achievement
    achievement=ACHIEVEMENTSFRAME(tp2,height=height,width=0.1*width,highlightbackground='black',highlightthickness=4)
    achievement.place(x=width,y=0,anchor='nw')
    achievement.bind()
    

    win.mainloop()
    

#class MYQUESTIONBANK(tkinter.Toplevel):
#    def __init__(self,master=None,**kw):
#        tkinter.Toplevel.__init__(self,master,**kw)
#        self.title('我的题库')
#        self.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
#        self.geometry('%dx%d+%d+%d'%(width,height,dx,dy))
#        self.nb1=ttk.Notebook(self)
#        self.engine1=create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
#        self.engine2=create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/answering_process')
#        sh=win.winfo_screenheight()
#        cellwidth=int(120/1800*sh)
#        s = ttk.Style()
#        s.configure('Treeview', rowheight=int(50/1800*sh),font=('微软雅黑',9))
#        self.frame1=tkinter.Frame(self.nb1,width=width,height=height)
#        self.frame11=tkinter.Frame(self.frame1,width=width,height=0.3*height)
#        self.frame11.place(x=0,y=0,anchor='nw')
#        self.ybar1=tkinter.Scrollbar(self.frame11,orient='vertical')
#        self.tree1=ttk.Treeview(self.frame11,height=8,columns=('col1','col2','col3','col4','col5','col6','col7','col8','col9'),show='headings',selectmode='browse',yscrollcommand=self.ybar1.set)
#        self.ybar1['command']=self.tree1.yview
#        self.canvas11=tkinter.Canvas(self.frame1,height=0.5*height,width=0.5*width,bg='white')
#        self.canvas11.place(x=0,y=0.4*height,anchor='nw')
#        self.button11=tkinter.Button(self.frame1,text='修改题目基本信息',font=('微软雅黑',12),width=15,height=1,fg='white',bg='black',command=self.changemyquestion)
#        self.button12=tkinter.Button(self.frame1,text='修改自定义提示',font=('微软雅黑',12),width=15,height=1,fg='white',bg='black',command=zdytishimode)
#        self.button11.place(x=0.6*width,y=0.5*height,anchor='nw')
#        self.button12.place(x=0.6*width,y=0.6*height,anchor='nw')
#
#        self.tree1.column('#1', width=cellwidth*2, anchor='center')
#        self.tree1.column('#2', width=cellwidth*3, anchor='center')
#        self.tree1.column('#3', width=cellwidth*2, anchor='center')
#        self.tree1.column('#4', width=cellwidth, anchor='center') 
#        self.tree1.column('#5', width=cellwidth, anchor='center')
#        self.tree1.column('#6', width=int(1.5*cellwidth), anchor='center')
#        self.tree1.column('#7', width=cellwidth, anchor='center')
#        self.tree1.column('#8', width=cellwidth*2, anchor='center') 
#        self.tree1.column('#9', width=cellwidth*2, anchor='center')
#        self.tree1.heading('col1', text='题目编号')
#        self.tree1.heading('col2', text='简要描述')
#        self.tree1.heading('col3', text='题目状态')
#        self.tree1.heading('col4', text='绘制内容')
#        self.tree1.heading('col5', text='应用模式')
#        self.tree1.heading('col6', text='提示方式')
#        self.tree1.heading('col7', text='难度系数')
#        self.tree1.heading('col8', text='点赞数')
#        self.tree1.heading('col9', text='被作答次数')
#        
#        self.frame2=tkinter.Frame(self.nb1,width=width,height=height)
#        self.frame21=tkinter.Frame(self.frame2,width=width,height=0.3*height)
#        self.frame21.place(x=0,y=0,anchor='nw')
#        self.ybar2=tkinter.Scrollbar(self.frame21,orient='vertical')
#        self.tree2=ttk.Treeview(self.frame21,height=8,columns=('col1','col2','col3','col4'),show='headings',selectmode='browse',yscrollcommand=self.ybar2.set)
#        
#        self.ybar2['command']=self.tree2.yview
#        self.tree2.column('#1', width=cellwidth*2, anchor='center')
#        self.tree2.column('#2', width=cellwidth*2, anchor='center')
#        self.tree2.column('#3', width=cellwidth*3, anchor='center')
#        self.tree2.column('#4', width=cellwidth, anchor='center') 
#        self.tree2.heading('col1', text='题目编号')
#        self.tree2.heading('col2', text='作答时间')
#        self.tree2.heading('col3', text='简要描述')
#        self.tree2.heading('col4', text='难度系数')   
#        self.canvas21=tkinter.Canvas(self.frame2,height=0.4*height,width=0.4*width,bg='white')
#        self.canvas21.place(x=0,y=0.4*height,anchor='nw')
#        self.canvas22=tkinter.Canvas(self.frame2,height=0.4*height,width=0.4*width,bg='white')
#        self.canvas22.place(x=0.5*width,y=0.4*height,anchor='nw') 
#        self.varnum21=tkinter.StringVar()
#        self.varnum21.set('')
#        self.lable21=tkinter.Label(self.frame2,textvariable=self.varnum21,font=('微软雅黑',12),width=40,height=5)
#        self.lable21.place(x=0.55*width,y=0.8*height,anchor='nw')
#        
#        
#        self.frame3=tkinter.Frame(self.nb1,width=0.5*width,height=height)
#        self.frame31=tkinter.Frame(self.frame3,width=width,height=0.3*height)
#        self.frame31.place(x=0,y=0,anchor='nw')
#        self.ybar3=tkinter.Scrollbar(self.frame31,orient='vertical')
#        self.tree3=ttk.Treeview(self.frame31,height=4,columns=('col1','col2','col3','col4'),show='headings',selectmode='browse',yscrollcommand=self.ybar3.set)
#        
#        self.ybar3['command']=self.tree3.yview
#        self.tree3.column('#1', width=int(cellwidth*1.5), anchor='center')
#        self.tree3.column('#2', width=int(cellwidth*1.5), anchor='center')
#        self.tree3.column('#3', width=int(cellwidth*1.5), anchor='center')
#        self.tree3.column('#4', width=cellwidth*2, anchor='center') 
#        self.tree3.heading('col1', text='群号')
#        self.tree3.heading('col2', text='群名')
#        self.tree3.heading('col3', text='群主')
#        self.tree3.heading('col4', text='群公告')
#        
#        self.frame32=tkinter.Frame(self.frame3,width=0.5*width,height=0.3*height)
##        self.frame32.place(x=0.4*width,y=0,anchor='nw')
#        self.ybar32=tkinter.Scrollbar(self.frame32,orient='vertical')
#        self.tree32=ttk.Treeview(self.frame32,height=5,columns=('col1'),show='headings',selectmode='browse',yscrollcommand=self.ybar32.set)
#        
#        self.ybar32['command']=self.tree32.yview
#        self.tree32.column('#1', width=int(cellwidth*1.5), anchor='center')
##        self.tree32.column('#2', width=int(cellwidth*1.5), anchor='center')
##        self.tree32.column('#3', width=int(cellwidth*1.5), anchor='center')
##        self.tree32.column('#4', width=cellwidth*2, anchor='center') 
#        self.tree32.heading('col1', text='群内成员')
#        
#        self.frame33=tkinter.Frame(self.frame3,width=0.5*width,height=0.2*height)
##        self.frame33.place(x=0,y=0.2*height,anchor='nw')
#        self.lable321=tkinter.Label(self.frame33,text="群号",fg='black')
#        self.text321=tkinter.Text(self.frame33,width=8,height=1,bg='#F5F5F5')
#        self.text321.insert('end','12345678')
#        self.text321.config(state='disabled')
#        
#        self.lable322=tkinter.Label(self.frame33,text="群名",fg='black')
#        self.text322=tkinter.Text(self.frame33,width=20,height=1,bg='#F5F5F5')
#        self.text322.insert('end','12345678')
##        self.text322.config(state='disabled')
#        
#        self.lable323=tkinter.Label(self.frame33,text="群主",fg='black')
#        self.text323=tkinter.Text(self.frame33,width=15,height=1,bg='#F5F5F5')
#        self.text323.insert('end','12345678')
#        
#        self.lable324=tkinter.Label(self.frame33,text="群公告",fg='black')
#        self.text324=tkinter.Text(self.frame33,width=50,height=1,bg='#F5F5F5',fg='red')
#        self.text324.insert('end','12345678嗡嗡嗡嗡嗡嗡')
#        
#        self.lable327=tkinter.Label(self.frame33,text="我的昵称",fg='black')
#        self.text327=tkinter.Text(self.frame33,width=15,height=1,bg='#F5F5F5',fg='red')
#        self.text327.insert('end','12345678嗡嗡嗡嗡嗡嗡')
#        
#        self.Button325=tkinter.Button(self.frame3,text='查看他作答的题目',fg='red')
##        self.Button325.place(x=0.4*width,y=0.25*height)
#        self.Button326=tkinter.Button(self.frame33,text='生成本群教学报告',fg='red')
#        
#        self.lable321.grid(row=0,column=0)
#        self.text321.grid(row=0,column=1)
#        self.lable323.grid(row=0,column=2)
#        self.text323.grid(row=0,column=3)
#        self.lable322.grid(row=1,column=0)
#        self.text322.grid(row=1,column=1)
#        self.lable324.grid(row=2,column=0)
#        self.text324.grid(row=2,column=1,columnspan=4)
#        self.Button326.grid(row=3,column=1)
#        self.lable327.grid(row=1,column=2)
#        self.text327.grid(row=1,column=3)
#        
#
#        
#        
#            
#        self.frame34=tkinter.Frame(self.frame3,width=0.2*width,height=0.1*height)
#        self.frame34.place(x=0,y=0.4*height,anchor='nw')
#        self.lable328=tkinter.Label(self.frame34,text="请输入群号:",fg='black')
#        self.text328=tkinter.Text(self.frame34,width=15,height=1,bg='white',fg='red')
#        self.Button328=tkinter.Button(self.frame34,text='加入群',fg='red')
#        l=tkinter.Label(self.frame34,text='    ')
#        self.Button329=tkinter.Button(self.frame34,text='新建群',fg='red' ,command=self.newqunzu)
#        self.lable328.grid(row=0,column=0)
#        self.text328.grid(row=0,column=1)
#        self.Button328.grid(row=0,column=2)
#        l.grid(row=0,column=3)
#        self.Button329.grid(row=0,column=4)
#        
#        
#        self.canvas31=tkinter.Canvas(self.frame3,height=0.4*height,width=0.4*width)
#        self.canvas31.place(x=0,y=0.5*height,anchor='nw')
#        self.canvas32=tkinter.Canvas(self.frame3,height=0.4*height,width=0.4*width)
#        self.canvas32.place(x=0.5*width,y=0.5*height,anchor='nw') 
#        self.varnum31=tkinter.StringVar()
#        self.varnum31.set('')
#        self.lable31=tkinter.Label(self.frame3,textvariable=self.varnum21,font=('微软雅黑',10),width=40,height=5)
#                                                                                                           
#        self.lable31.place(x=0.57*width,y=0.9*height,anchor='nw')
#        
#        self.frame35=tkinter.Frame(self.frame3,width=width,height=0.3*height)
##        self.frame35.place(x=0.5*width,y=0,anchor='nw')
#        self.ybar33=tkinter.Scrollbar(self.frame35,orient='vertical')
#        self.tree33=ttk.Treeview(self.frame35,height=8,columns=('col1','col2','col3','col4'),show='headings',selectmode='browse',yscrollcommand=self.ybar33.set)
#        
#        self.ybar33['command']=self.tree2.yview
#        self.tree33.column('#1', width=cellwidth*2, anchor='center')
#        self.tree33.column('#2', width=cellwidth*2, anchor='center')
#        self.tree33.column('#3', width=cellwidth*3, anchor='center')
#        self.tree33.column('#4', width=cellwidth, anchor='center') 
#        self.tree33.heading('col1', text='题目编号')
#        self.tree33.heading('col2', text='作答时间')
#        self.tree33.heading('col3', text='简要描述')
#        self.tree33.heading('col4', text='难度系数')   
#        
#        self.nb1.add(self.frame1,text='我贡献的题目')
#        self.nb1.add(self.frame2,text='我做过的题目')
#        self.nb1.add(self.frame3,text='我的群组')
#        
##        self.frame1.place(x=0,y=0)
#        self.tree1.grid(row=0)
#        self.ybar1.grid(row=0,column=1,sticky='ns')
#        self.tree2.grid(row=0)
#        self.ybar2.grid(row=0,column=1,sticky='ns')
#        self.tree3.grid(row=0)
#        self.ybar3.grid(row=0,column=1,sticky='ns')
#        self.tree32.grid(row=0)
#        self.ybar32.grid(row=0,column=1,sticky='ns')
#        self.tree33.grid(row=0)
#        self.ybar33.grid(row=0,column=1,sticky='ns')
#        
#        self.nb1.pack()
#        sql="select * from basic_questioninfor where questionsymbol like('"+"%%%%%s%%%%"%zdyallfunction.userID+"')"
#        print(sql)
#        self.questions=pd.read_sql_query(sql, self.engine1)
#        for i in range(len(self.questions)):
#            tt=[]
#            tt.append(self.questions.iloc[i,0])
#            tt.append(self.questions.iloc[i,2])
#            tt.append(self.questions.iloc[i,4])
#            tt.append(self.questions.iloc[i,5])
#            tt.append(self.questions.iloc[i,6])
#            tt.append(self.questions.iloc[i,7])
#            tt.append(self.questions.iloc[i,8])
#            tt.append(self.questions.iloc[i,9])
#            tt.append(self.questions.iloc[i,10])
#            tt=tuple(tt)
#            self.tree1.insert('',i,values=tt)
#        sql="select momentanswer_record.questionsymbol,momentanswer_record.starttime,basic_questioninfor.generaldescription,"
#        sql=sql+"basic_questioninfor.difficulty,basic_questioninfor.thumbs"
#        sql=sql+" from momentanswer_record , basic_questioninfor "
#        sql=sql+"where momentanswer_record.questionsymbol=basic_questioninfor.questionsymbol "
#        sql=sql+"and momentanswer_record.userID='%s"%zdyallfunction.userID+"'"
#        df=pd.read_sql_query(sql, self.engine1)
#        for i in range(len(df)):
#            tt=[]
#            for j in range(5):
#                tt.append(df.iloc[i,j])
#            tt=tuple(tt)
#            self.tree2.insert('',i,values=tt)
#            
#
#    def deltree1self(self):
#        x=self.tree1.get_children()
#        for item in x:
#            self.tree1.delete(item)
#
#    def showmmycontribution(self):
#        self.deltree1self()
#        sql="select * from basic_questioninfor where questionsymbol like('"+"%%%%%s%%%%"%zdyallfunction.userID+"')"
#        print(sql)
#        self.questions=pd.read_sql_query(sql, self.engine1)
#        for i in range(len(self.questions)):
#            tt=[]
#            tt.append(self.questions.iloc[i,0])
#            tt.append(self.questions.iloc[i,2])
#            tt.append(self.questions.iloc[i,4])
#            tt.append(self.questions.iloc[i,5])
#            tt.append(self.questions.iloc[i,6])
#            tt.append(self.questions.iloc[i,7])
#            tt.append(self.questions.iloc[i,8])
#            tt.append(self.questions.iloc[i,9])
#            tt.append(self.questions.iloc[i,10])
#            tt=tuple(tt)
#            self.tree1.insert('',i,values=tt)
#        
#        
#    def bind(self):
#        self.tree1.bind('<Double-Button-1>',self.qualifyquestionsymbol1)
#        self.tree2.bind('<Double-Button-1>',self.qualifyquestionsymbol2)
#        im=Image.open(f'{os.getcwd()}/infor/rightan.png') 
#        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*width),int(0.05*height)))) 
#        self.button21=tkinter.Button(self.frame2,image=imgBtn,command=self.nextprocess)
#        self.button21.place(x=0.9*width,y=0.8*height,anchor='ne')
#        im2=Image.open(f'{os.getcwd()}/infor/leftan.png') 
#        imgBtn2 =ImageTk.PhotoImage(im2.resize((int(0.05*width),int(0.05*height)))) 
#        self.button22=tkinter.Button(self.frame2,image=imgBtn2,command=self.formerprocess)
#        self.button22.place(x=0.5*width,y=0.8*height,anchor='nw')
#        
##        im=Image.open('infor/rightan.png') 
##        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*width),int(0.05*height)))) 
#        self.button31=tkinter.Button(self.frame3,image=imgBtn,command=self.nextprocess)
#        self.button31.place(x=0.9*width,y=0.9*height,anchor='ne')
##        im2=Image.open('infor/leftan.png') 
##        imgBtn2 =ImageTk.PhotoImage(im2.resize((int(0.05*width),int(0.05*height)))) 
#        self.button32=tkinter.Button(self.frame3,image=imgBtn2,command=self.formerprocess)
#        self.button32.place(x=0.5*width,y=0.9*height,anchor='nw')
#        win.mainloop()
#        
#    def nextprocess(self):
#        if ((self.processnum+1)<len(self.process)):
#            self.processnum=self.processnum+1
#            self.filec()
#            self.showquestion2()
#        else:
#            tkinter.messagebox.showinfo(title='提示', message='这是您有作答记录的最后一步')
#    def formerprocess(self):
#        if (self.processnum)<=0:
#            tkinter.messagebox.showinfo(title='提示', message='这是您有作答记录的第一步')
#        else:
#            zdyallfunction.fileinelements()
#            self.processnum=self.processnum-1
#            self.filec()
#            self.showquestion2()
#            
#    def drawquestion(self):
#        zdyallfunction.getquestion(zdyallfunction.questionsymbol)
#        zdyallfunction.fileinelements()
#        zdyallfunction.file()
#        zdyallfunction.drawquestion()
#    def showquestion1(self):
#        im=Image.open(f'{os.getcwd()}/drawing/question.png')
#        photo = ImageTk.PhotoImage(im.resize((int(0.5*width),int(0.5*height)),Image.ANTIALIAS))
#        self.canvas11.create_image(0,0,anchor='nw',image = photo)
#        win.mainloop()
#        
#    def showquestion2(self):
#        im=Image.open(f'{os.getcwd()}/drawing/question.png')
#        photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
#        self.canvas21.create_image(0,0,anchor='nw',image = photo)
#        self.showprocess()
#        win.mainloop()
#        
#    def qualifyquestionsymbol1(self,event):
#            item = self.tree1.selection()[0]
#            print(item)
#            print(self.tree1.item(item, "values")) 
#            zdyallfunction.questionsymbol=self.tree1.item(item, "values")[0]
#            self.drawquestion()
#            self.showquestion1()
#    def getprocess(self):
#        sql="select * from moment"+zdyallfunction.questionsymbol+" where userID='%s'"%zdyallfunction.userID
#        print(sql)
#        sql=sql+" and starttime='%s'"%self.tree2.item(self.item, "values")[1]
#        self.process=pd.read_sql_query(sql, self.engine2)
#        self.processnum=0
#    
#    def filec(self):
#        columnnum=self.process.shape[1]
#        self.varnum21.set('')
#        for i in range(4,columnnum-1):
#            temp=self.process.iloc[self.processnum,i]
#            temp=temp.split(',')
#            print(self.varnum21.get()=='')
#            print(len(temp)>1)
##            if self.varnum21.get()=='' and len(temp)>1:
##                try:
##                    float(temp[-1])
##                except:
##                    t=temp[-1].strip('\n')
##                    self.varnum21.set(t)
#            if len(temp)!=1:
#                class C_():
#                    pass
#                c_=C_()
#                c_.num=int(temp[0])
#                c_.type=temp[1]
#                c_.Mi=float(temp[2])
#                c_.Mj=float(temp[3])
#                c_.Mmid=float(temp[4])
#                c_.ns=float(temp[5])
#                c_.ne=float(temp[6])
#                zdyallfunction.changec(c_)
#        temp=self.process.iloc[self.processnum,columnnum-1]
#        print(temp[0])
#        if len(temp)>1:
#            t=temp
#            if len(t)>20:
#                t=list(t)
#                t.insert(18,'\n',)
#                t=''.join(t)
#            if len(t)>40:
#                t=list(t)
#                t.insert(36,'\n',)
#                t=''.join(t)
#    #            t=temp.replace('\n',"")
##            print(t)
#            self.varnum21.set(t)
#        zdyallfunction.drawuserM(-1)
#    def showprocess(self):
#        im=Image.open(f'{os.getcwd()}/drawing/userM.png')
#        photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
#        self.canvas22.create_image(0,0,anchor='nw',image = photo)
#        self.mainloop()
#        
#    def qualifyquestionsymbol2(self,event):
#            self.item = self.tree2.selection()[0]
#            print(self.tree2.item(self.item, "values")) 
#            zdyallfunction.questionsymbol=self.tree2.item(self.item, "values")[0]
#            self.drawquestion()
#            self.getprocess()
#            self.filec()
#            self.showquestion2()
#
#    def changemyquestion(self):
#        self.tp11=tkinter.Toplevel()
#        self.tp11.title('我的题库')
#        self.tp11.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
#        self.tp11.geometry('%dx%d+%d+%d'%(0.2*width,0.4*height,dx,dy))
#        self.lable111=tkinter.Label(self.tp11,text="题目状态",fg='red')
#        self.cmb111 = ttk.Combobox(self.tp11)
#        self.cmb111['value'] = ("公开","私密")
#        self.cmb111.current(0)
#        self.lable112=tkinter.Label(self.tp11,text="简要描述",fg='red')
#        self.text112=tkinter.Text(self.tp11,width=30,height=6,highlightthickness=2,highlightcolor='red',
#           highlightbackground='red')
#        self.text112.insert("end","")
#        self.button111=tkinter.Button(self.tp11,text='确认修改题目状态',font=('微软雅黑',10),width=15,height=1,fg='white',bg='black',command=self.changestate)
#        self.button112=tkinter.Button(self.tp11,text='确认修改简要描述',font=('微软雅黑',10),width=15,height=1,fg='white',bg='black',command=self.changegeneraldescription)
#        l1=tkinter.Label(self.tp11,text="    ")
#        l2=tkinter.Label(self.tp11,text="    ")
#        self.lable111.grid(row=0,column=0)
#        self.cmb111.grid(row=1,column=0)
#        l1.grid(row=2,column=0)
#        self.button111.grid(row=3,column=0)
#        self.lable112.grid(row=4,column=0)
#        self.text112.grid(row=5,column=0)
#        l2.grid(row=6,column=0)
#        self.button112.grid(row=7,column=0)
#    def changestate(self):
#        try:
#            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
#            cursor = conn.cursor()
#            sql="update basic_questioninfor set state=%s where questionsymbol=%s"
#            cursor.execute(sql,[self.cmb111.get(),zdyallfunction.questionsymbol])
#            conn.commit()
#            cursor.close()
#            conn.close()
#            self.showmmycontribution()
#            tkinter.messagebox.showinfo(title='提示', message='修改成功！')
#        except:
#            tkinter.messagebox.showinfo(title='提示', message='修改失败！')
#    def changegeneraldescription(self):
#        if len(self.text112.get('0.0','end'))<1:
#            tkinter.messagebox.showinfo(title='提示', message='描述内容不能为空！')
#            return
#        try:
#            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
#            cursor = conn.cursor()
#            sql="update basic_questioninfor set generaldescription=%s where questionsymbol=%s"
#            cursor.execute(sql,[str(self.text112.get('0.0','end')),zdyallfunction.questionsymbol])
#            conn.commit()
#            cursor.close()
#            conn.close()
#            tkinter.messagebox.showinfo(title='提示', message='修改成功！')
#            self.showmmycontribution()
#        except:
#            tkinter.messagebox.showinfo(title='提示', message='修改失败！')
#        win.mainloop()
#    
#    def showqunzu(self):
#        self.frame32.place(x=0.4*width,y=0,anchor='nw')
#        self.frame33.place(x=0,y=0.2*height,anchor='nw')
#        self.frame35.place(x=0.5*width,y=0,anchor='nw')
#        self.Button325.place(x=0.4*width,y=0.25*height)
#        
#    def newqunzu(self):
#        self.tp31=tkinter.Toplevel()
#        self.tp31.title('新建群组')
#        self.tp31.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
#        self.tp31.geometry('%dx%d+%d+%d'%(0.2*width,0.2*height,dx,dy))
#        self.lable_tp31_1=tkinter.Label(self.tp31,text="群名",fg='black')
#        self.entry_tp31_1=tkinter.Entry(self.tp31,width=20)
#        l1=tkinter.Label(self.tp31,text="   ")
#        self.lable_tp31_2=tkinter.Label(self.tp31,text="群公告",fg='black')
#        self.entry_tp31_2=tkinter.Entry(self.tp31,width=20)
#        l2=tkinter.Label(self.tp31,text="   ")
#        self.button_tp31_1=tkinter.Button(self.tp31,text='确认新建',font=('微软雅黑',10))
#        self.lable_tp31_1.grid(row=0,column=0)
#        self.entry_tp31_1.grid(row=0,column=1)
#        l1.grid(row=1,column=0)
#        self.lable_tp31_2.grid(row=2,column=0)
#        self.entry_tp31_2.grid(row=2,column=1)
#        l2.grid(row=3,column=0)
#        self.button_tp31_1.grid(row=4,column=1)
        
        
        



































class REPORT(tkinter.Toplevel):
    def __init__(self,master=None,**kw):
        tkinter.Toplevel.__init__(self,master,**kw)
        self.title('教学报告')
        self.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.geometry('%dx%d+%d+%d'%(0.8*width,0.9*height,dx,dy))
        self.engine1 = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')

        sql="select basic_questioninfor.generaldescription ,count(*) from basic_questioninfor,(select momentanswer_record.questionsymbol  from momentanswer_record,(select * from groupnamelist where groupnum ='%s') as table1 where momentanswer_record.userID=table1.userID) as table2 where basic_questioninfor.questionsymbol =table2.questionsymbol group by basic_questioninfor.generaldescription "%groupnum
        self.reportinfor2= pd.read_sql_query(sql, self.engine1)
        labels = list(self.reportinfor2[['generaldescription']].values.astype(str).flatten())
        sizes=list(self.reportinfor2[['count(*)']].values.astype(int).flatten())
        plt.figure(figsize=(32,20))
        plt.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150,textprops={'fontsize':20,'color':'black'})
        plt.title("用户作答题目类型统计",fontdict={'weight':'normal','size': 40})
        plt.axis('equal')
        plt.legend(loc="best",fontsize=30,ncol=1)
        plt.savefig('drawing/report2.png',bbox_inches='tight',pad_inches=0, )
        plt.close()
        
        
        self.totalnum=0
        for i in list(self.reportinfor2[['count(*)']].values.astype(int).flatten()):
            self.totalnum=self.totalnum+int(i)
        self.l1=tkinter.Label(self,text='所有成员共作答：%d 题'%self.totalnum,fg='black',font=('微软雅黑',12))
        self.canvas=tkinter.Canvas(self,height=0.8*height,width=0.8*width)
        self.canvas.place(x=0,y=0.1*height,anchor='nw')
        im=Image.open(f'{os.getcwd()}/drawing/report2.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.8*width),int(0.8*height)),Image.ANTIALIAS))
        self.canvas.create_image(0,0,anchor='nw',image = photo)
 
        self.l1.pack()
        self.frame1=tkinter.Frame(self,height=0.1*height,width=0.8*width)
#        self.frame1.place(x=0,y=0.9*height,anchor='nw')
        self.frame1.pack()
        self.l2=tkinter.Label(self.frame1,text='关键字: ',fg='black',font=('微软雅黑',12))
        self.searche=tkinter.Entry(self.frame1,width=20)
        lspace2=tkinter.Label(self.frame1,text='    ')
        self.b1=tkinter.Button(self.frame1,text='查看此类题目错误统计',font=('微软雅黑',10),command=self.searchway1)
        self.l2.grid(row=0,column=0)
        self.searche.grid(row=0,column=1)
        lspace2.grid(row=0,column=2)
        self.b1.grid(row=0,column=3)
        self.searchway=-1
        win.mainloop()

        
    def searchway1(self):
        self.searchway=1
        state=self.drawdetailreport()
        if state==1:
            self.showdetailreport()
    def searchway2(self):
        self.searchway=2
        state=self.drawdetailreport()
        if state==1:
            self.showdetailreport()
        
    
    def drawdetailreport(self):
        if self.searchway==1:
            sql = "select tishi.提示或错误 ,count(*) from tishi,basic_questioninfor ,(select * from groupnamelist where groupnum ='%s') as table1 where basic_questioninfor.generaldescription like '%%%%%s%%%%' and tishi.questionsymbol= basic_questioninfor.questionsymbol"%(groupnum,self.searche.get())
            sql=sql+" and table1.userID=tishi.userID  and tishi.提示或错误 !='0' and tishi.提示或错误 !='请点击分析与提示，修改作答' group by tishi.提示或错误"
            self.reportinfor1= pd.read_sql_query(sql, self.engine1)
        if len(self.reportinfor1)==0:
            tkinter.messagebox.showinfo(title='提示', message='未查询到此类题目的细节记录')
            return 0
        labels = list(self.reportinfor1[['提示或错误']].values.astype(str).flatten())
        sizes=list(self.reportinfor1[['count(*)']].values.astype(int).flatten())
        plt.figure(figsize=(32,20))
        plt.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150,textprops={'fontsize':20,'color':'black'})
        if self.searchway==1:
            plt.title("%s类作答错误统计"%self.searche.get(),fontdict={'weight':'normal','size': 50})
        plt.axis('equal')
#        plt.legend(loc="best",fontsize=20,ncol=1)
        plt.savefig('drawing/detailreport.png',bbox_inches='tight',pad_inches=0, )
        plt.close()
        return 1
    def showdetailreport(self):
        self.tp2=tkinter.Toplevel()
        self.tp2.title('我的题库')
        self.tp2.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.tp2.geometry('%dx%d+%d+%d'%(width,height,dx,dy))
        self.canvas2=tkinter.Canvas(self.tp2,height=height,width=width)
        self.canvas2.place(x=0,y=0,anchor='nw')
        im=Image.open(f'{os.getcwd()}/drawing/detailreport.png')
        photo = ImageTk.PhotoImage(im.resize((int(width),int(height)),Image.ANTIALIAS))
        self.canvas2.create_image(0,0,anchor='nw',image = photo)
        win.mainloop()







class MYQUESTIONBANK(tkinter.Toplevel):
    def __init__(self,master=None,**kw):
        tkinter.Toplevel.__init__(self,master,**kw)
        self.title('我的题库')
        self.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.geometry('%dx%d+%d+%d'%(width,height,dx,dy))
        self.nb1=ttk.Notebook(self)
        self.engine1=create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
        self.engine2=create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/answering_process')
        sh=win.winfo_screenheight()
        cellwidth=int(120/1800*sh)
        s = ttk.Style()
        s.configure('Treeview', rowheight=int(50/1800*sh),font=('微软雅黑',9))
        self.frame1=tkinter.Frame(self.nb1,width=width,height=height)
        self.frame11=tkinter.Frame(self.frame1,width=width,height=0.3*height)
        self.frame11.place(x=0,y=0,anchor='nw')
        self.ybar1=tkinter.Scrollbar(self.frame11,orient='vertical')
        self.tree1=ttk.Treeview(self.frame11,height=8,columns=('col1','col2','col3','col4','col5','col6','col7','col8','col9'),show='headings',selectmode='browse',yscrollcommand=self.ybar1.set)
        self.ybar1['command']=self.tree1.yview
        self.canvas11=tkinter.Canvas(self.frame1,height=0.5*height,width=0.5*width,bg='white')
        self.canvas11.place(x=0,y=0.4*height,anchor='nw')
        self.mycontributionhelplabel=tkinter.Label(self.frame1,text="请先双击选中题目",font=('微软雅黑',18,'bold'))
        self.mycontributionhelpbutton=tkinter.Button(self.frame1,text='我贡献的题目帮助',font=('微软雅黑',12),width=15,height=1,fg='white',bg='black',command=self.showmycontributionhelp)
        self.button11=tkinter.Button(self.frame1,text='修改题目基本信息',font=('微软雅黑',12),width=15,height=1,fg='white',bg='black',command=self.changemyquestion)
        self.button12=tkinter.Button(self.frame1,text='修改自定义提示',font=('微软雅黑',12),width=15,height=1,fg='white',bg='black',command=zdytishimode)
        
        self.mycontributionhelplabel.place(x=0.6*width,y=0.4*height)
        self.mycontributionhelpbutton.place(x=0.6*width,y=0.5*height,anchor='nw')
        self.button11.place(x=0.6*width,y=0.6*height,anchor='nw')
        self.button12.place(x=0.6*width,y=0.7*height,anchor='nw')


        self.tree1.column('#1', width=cellwidth*2, anchor='center')
        self.tree1.column('#2', width=cellwidth*3, anchor='center')
        self.tree1.column('#3', width=cellwidth*2, anchor='center')
        self.tree1.column('#4', width=cellwidth, anchor='center') 
        self.tree1.column('#5', width=cellwidth, anchor='center')
        self.tree1.column('#6', width=int(1.5*cellwidth), anchor='center')
        self.tree1.column('#7', width=cellwidth, anchor='center')
        self.tree1.column('#8', width=cellwidth*2, anchor='center') 
        self.tree1.column('#9', width=cellwidth*2, anchor='center')
        self.tree1.heading('col1', text='题目编号')
        self.tree1.heading('col2', text='题型描述')
        self.tree1.heading('col3', text='题目状态')
        self.tree1.heading('col4', text='绘制内容')
        self.tree1.heading('col5', text='应用模式')
        self.tree1.heading('col6', text='提示方式')
        self.tree1.heading('col7', text='难度系数')
        self.tree1.heading('col8', text='点赞数')
        self.tree1.heading('col9', text='被作答次数')
        
        self.frame2=tkinter.Frame(self.nb1,width=width,height=height)
        
        self.mydonequestionhelplabel=tkinter.Label(self.frame2,text="这是您的所有作答记录\n请先双击选中题目\n通过左右箭头逐步查看做题过程",font=('微软雅黑',18,'bold'))
        self.mydonequestionhelpbutton=tkinter.Button(self.frame2,text='我做过的题目帮助',font=('微软雅黑',12),width=15,height=1,fg='white',bg='black',command=self.showmydonequestionhelp)
        
        self.mydonequestionhelplabel.place(x=0.6*width,y=0.05*height)
#        self.mydonequestionhelpbutton.place(x=0.6*width,y=0.3,anchor='nw')
        self.frame21=tkinter.Frame(self.frame2,width=width,height=0.3*height)
        self.frame21.place(x=0,y=0,anchor='nw')
        self.ybar2=tkinter.Scrollbar(self.frame21,orient='vertical')
        self.tree2=ttk.Treeview(self.frame21,height=8,columns=('col1','col2','col3','col4'),show='headings',selectmode='browse',yscrollcommand=self.ybar2.set)
        
        self.ybar2['command']=self.tree2.yview
        self.tree2.column('#1', width=cellwidth*2, anchor='center')
        self.tree2.column('#2', width=cellwidth*2, anchor='center')
        self.tree2.column('#3', width=cellwidth*3, anchor='center')
        self.tree2.column('#4', width=cellwidth, anchor='center') 
        self.tree2.heading('col1', text='题目编号')
        self.tree2.heading('col2', text='作答时间')
        self.tree2.heading('col3', text='题型描述')
        self.tree2.heading('col4', text='难度系数')   
        self.canvas21=tkinter.Canvas(self.frame2,height=0.4*height,width=0.4*width,bg='white')
        self.canvas21.place(x=0,y=0.4*height,anchor='nw')
        #self.canvas22=tkinter.Canvas(self.frame2,height=0.4*height,width=0.4*width,bg='white')
        self.canvas22=Xuanzecanvas(master=self.frame2,height=0.4*height,width=0.4*width,bg='white')
        self.canvas22.place(x=0.5*width,y=0.4*height,anchor='nw') 
        self.varnum21=tkinter.StringVar()
        self.varnum21.set('')
        self.varnum22=tkinter.StringVar()
        self.varnum22.set('')
        self.lable21=tkinter.Label(self.frame2,textvariable=self.varnum21,font=('微软雅黑',10,'bold'),width=40,height=5)
        self.lable21.place(x=0.55*width,y=0.8*height,anchor='nw')
        
        
        self.frame3=tkinter.Frame(self.nb1,width=0.5*width,height=height)
        self.frame31=tkinter.Frame(self.frame3,width=width,height=0.3*height)
        self.frame31.place(x=0,y=0,anchor='nw')
        self.ybar3=tkinter.Scrollbar(self.frame31,orient='vertical')
        self.tree3=ttk.Treeview(self.frame31,height=4,columns=('col1','col2','col3','col4'),show='headings',selectmode='browse',yscrollcommand=self.ybar3.set)
        
        self.ybar3['command']=self.tree3.yview
        self.tree3.column('#1', width=int(cellwidth*1.5), anchor='center')
        self.tree3.column('#2', width=int(cellwidth*1.5), anchor='center')
        self.tree3.column('#3', width=int(cellwidth*1.5), anchor='center')
        self.tree3.column('#4', width=cellwidth*2, anchor='center') 
        self.tree3.heading('col1', text='群号')
        self.tree3.heading('col2', text='群名')
        self.tree3.heading('col3', text='群主')
        self.tree3.heading('col4', text='群公告')
        
        self.frame32=tkinter.Frame(self.frame3,width=0.5*width,height=0.3*height)
#        self.frame32.place(x=0.4*width,y=0,anchor='nw')
        self.ybar32=tkinter.Scrollbar(self.frame32,orient='vertical')
        self.tree32=ttk.Treeview(self.frame32,height=5,columns=('col1'),show='headings',selectmode='browse',yscrollcommand=self.ybar32.set)
        
        self.ybar32['command']=self.tree32.yview
        self.tree32.column('#1', width=int(cellwidth*1.5), anchor='center')
#        self.tree32.column('#2', width=int(cellwidth*1.5), anchor='center')
#        self.tree32.column('#3', width=int(cellwidth*1.5), anchor='center')
#        self.tree32.column('#4', width=cellwidth*2, anchor='center') 
        self.tree32.heading('col1', text='群内成员')
        
        self.frame33=tkinter.Frame(self.frame3,width=0.5*width,height=0.2*height)
#        self.frame33.place(x=0,y=0.2*height,anchor='nw')
        self.lable321=tkinter.Label(self.frame33,text="群号",fg='black')
        self.text321=tkinter.Text(self.frame33,width=8,height=1,bg='#F5F5F5')
        self.text321.insert('end','12345678')
        self.text321.config(state='disabled')
        
        self.lable322=tkinter.Label(self.frame33,text="群名",fg='black')
        self.text322=tkinter.Text(self.frame33,width=20,height=1,bg='#F5F5F5')
        self.text322.insert('end','12345678')
#        self.text322.config(state='disabled')
        
        self.lable323=tkinter.Label(self.frame33,text="群主",fg='black')
        self.text323=tkinter.Text(self.frame33,width=15,height=1,bg='#F5F5F5')

        
        self.lable324=tkinter.Label(self.frame33,text="群公告",fg='black')
        self.text324=tkinter.Text(self.frame33,width=50,height=1,bg='#F5F5F5')
 
        
        self.lable327=tkinter.Label(self.frame33,text="我的昵称",fg='black')
        self.text327=tkinter.Text(self.frame33,width=15,height=1,bg='#F5F5F5')
        
        
        
        self.Button325=tkinter.Button(self.frame3,text='查看他作答的题目',fg='red')
#        self.Button325.place(x=0.4*width,y=0.25*height)

        self.Button326=tkinter.Button(self.frame33,text='生成本群教学报告',fg='black',font=('微软雅黑',12),command=self.createreport,bg='white')
        
        self.lable321.grid(row=0,column=0)
        self.text321.grid(row=0,column=1)
        self.lable323.grid(row=0,column=2)
        self.text323.grid(row=0,column=3)
        self.lable322.grid(row=1,column=0)
        self.text322.grid(row=1,column=1)
        self.lable324.grid(row=2,column=0)
        self.text324.grid(row=2,column=1,columnspan=4)
        self.Button326.grid(row=3,column=1)
        self.lable327.grid(row=1,column=2)
        self.text327.grid(row=1,column=3)
        

        
        
            
        self.frame34=tkinter.Frame(self.frame3,width=0.2*width,height=0.1*height)
        self.frame34.place(x=0,y=0.4*height,anchor='nw')
        self.lable328=tkinter.Label(self.frame34,text="请输入群号:",fg='black',font=('微软雅黑',15))
        self.entry328=tkinter.Entry(self.frame34,width=15,bg='white')
        self.Button328=tkinter.Button(self.frame34,text='加入群',fg='red',command=self.addnewgroup,font=('微软雅黑',15))
        l=tkinter.Label(self.frame34,text='    ')
        self.Button329=tkinter.Button(self.frame34,text='新建群',fg='red' ,command=self.newgroup,font=('微软雅黑',15))
        self.mygrouphelpbutton=tkinter.Button(self.frame34,text='我的群组帮助',font=('微软雅黑',10,'bold'),width=15,height=1,fg='white',bg='black',command=self.showmygrouphelp)
        
        self.lable328.grid(row=0,column=0)
        self.entry328.grid(row=0,column=1)
        self.Button328.grid(row=0,column=2)
        l.grid(row=0,column=3)
        self.Button329.grid(row=0,column=4)
        
        self.mygrouphelpbutton.grid(row=0,column=5)
        
        self.grouptishi=tkinter.Label(self.frame3,text='您可以逐次双击选择表格中的行，从而查看某位群内成员的详细作答过程',font=('微软雅黑',12,'bold'))
        self.grouptishi.place(x=0.5*width,y=0.4*height,anchor='nw')
        
        
        self.canvas31=tkinter.Canvas(self.frame3,height=0.4*height,width=0.4*width)
        self.canvas31.place(x=0,y=0.5*height,anchor='nw')
        self.canvas32=Xuanzecanvas(master=self.frame3,height=0.4*height,width=0.4*width,bg='white')
        self.canvas32.place(x=0.5*width,y=0.5*height,anchor='nw') 
        self.varnum31=tkinter.StringVar()
        self.varnum31.set('')
        self.lable31=tkinter.Label(self.frame3,textvariable=self.varnum22,font=('微软雅黑',10,'bold'),width=30,height=4)
        self.lable31.place(x=0.57*width,y=0.9*height,anchor='nw')
        
        self.frame35=tkinter.Frame(self.frame3,width=width,height=0.3*height)
#        self.frame35.place(x=0.5*width,y=0,anchor='nw')
        self.ybar33=tkinter.Scrollbar(self.frame35,orient='vertical')
        self.tree33=ttk.Treeview(self.frame35,height=8,columns=('col1','col2','col3','col4'),show='headings',selectmode='browse',yscrollcommand=self.ybar33.set)
        
        self.ybar33['command']=self.tree2.yview
        self.tree33.column('#1', width=cellwidth*2, anchor='center')
        self.tree33.column('#2', width=cellwidth*2, anchor='center')
        self.tree33.column('#3', width=cellwidth*3, anchor='center')
        self.tree33.column('#4', width=cellwidth, anchor='center') 
        self.tree33.heading('col1', text='题目编号')
        self.tree33.heading('col2', text='作答时间')
        self.tree33.heading('col3', text='题型描述')
        self.tree33.heading('col4', text='难度系数')   
        
        self.nb1.add(self.frame1,text='我贡献的题目')
        self.nb1.add(self.frame2,text='我做过的题目')
        self.nb1.add(self.frame3,text='我的群组')
        
#        self.frame1.place(x=0,y=0)
        self.tree1.grid(row=0)
        self.ybar1.grid(row=0,column=1,sticky='ns')
        self.tree2.grid(row=0)
        self.ybar2.grid(row=0,column=1,sticky='ns')
        self.tree3.grid(row=0)
        self.ybar3.grid(row=0,column=1,sticky='ns')
        self.tree32.grid(row=0)
        self.ybar32.grid(row=0,column=1,sticky='ns')
        self.tree33.grid(row=0)
        self.ybar33.grid(row=0,column=1,sticky='ns')
        
        self.nb1.pack()
        sql="select * from basic_questioninfor where questionsymbol like('"+"%%%%%s_%%%%"%zdyallfunction.userID+"')"
        print(sql)
        self.questions=pd.read_sql_query(sql, self.engine1)
        for i in range(len(self.questions)):
            tt=[]
            tt.append(self.questions.iloc[i,0])
            tt.append(self.questions.iloc[i,2])
            tt.append(self.questions.iloc[i,4])
            tt.append(self.questions.iloc[i,5])
            tt.append(self.questions.iloc[i,6])
            tt.append(self.questions.iloc[i,7])
            tt.append(self.questions.iloc[i,8])
            tt.append(self.questions.iloc[i,9])
            tt.append(self.questions.iloc[i,10])
            tt=tuple(tt)
            self.tree1.insert('',i,values=tt)
        sql="select momentanswer_record.questionsymbol,momentanswer_record.starttime,basic_questioninfor.generaldescription,"
        sql=sql+"basic_questioninfor.difficulty,basic_questioninfor.thumbs"
        sql=sql+" from momentanswer_record , basic_questioninfor "
        sql=sql+"where momentanswer_record.questionsymbol=basic_questioninfor.questionsymbol "
        sql=sql+"and momentanswer_record.userID='%s"%zdyallfunction.userID+"'"
        df=pd.read_sql_query(sql, self.engine1)
        for i in range(len(df)):
            tt=[]
            for j in range(4):
                tt.append(df.iloc[i,j])
            tt=tuple(tt)
            self.tree2.insert('',i,values=tt)
            
        sql="select * from grouptable,groupnamelist where groupnamelist.userID='%s' and grouptable.groupnum=groupnamelist.groupnum"%zdyallfunction.userID 
        self.mygroup=pd.read_sql_query(sql, self.engine1)
        for i in range(len(self.mygroup)):
            tt=[]
            tt.append(self.mygroup.iloc[0,0])
            tt.append(self.mygroup.iloc[0,1])
            tt.append(self.mygroup.iloc[0,2])
            tt.append(self.mygroup.iloc[0,3])
            tt=tuple(tt)
            self.tree3.insert('',i,values=tt)
        self.resizable(0,0)
     
    def showmycontributionhelp(self):
        mycontributionhelp=HELPTOPLEVEL(name="我贡献的题目帮助",ratio=1.78,picturename='managehelp1.jpg')
        mycontributionhelp.bind()
        
    def showmydonequestionhelp(self):
        mydonequestionhelp=HELPTOPLEVEL(name="我做过题目帮助",ratio=1.78,picturename='managehelp2.jpg')
        mydonequestionhelp.bind()
        
    def showmygrouphelp(self):
        mygrouphelp=HELPTOPLEVEL(name="我的群组帮助",ratio=1.82,picturename='managehelp3.jpg')
        mygrouphelp.bind()
        
    def deltree1self(self):
        x=self.tree1.get_children()
        for item in x:
            self.tree1.delete(item)
            
    def showpartnerquestions(self,event):
        x=self.tree33.get_children()
        for item in x:
            self.tree33.delete(item)
        item = self.tree3.selection()
        sql="select * from groupnamelist,grouptable where groupnamelist.groupnum=grouptable.groupnum and groupnamelist.groupnum='%s' and groupleader='%s'"%(self.tree3.item(item, "values")[0],zdyallfunction.userID)
        
        df=pd.read_sql_query(sql, self.engine1)
        if len(df)==0:
            tkinter.messagebox.showinfo(title='提示', message='您不是群主，无法查看其他人的作答记录')
            return 0
        sql="select * from groupnamelist where groupnum='%s'"%self.tree3.item(item, "values")[0]
        df=pd.read_sql_query(sql, self.engine1)
        item=self.tree32.selection()
        for i in range(len(df)):
            if df.loc[i,'nickname']==self.tree32.item(item, "values")[0]:
                self.partneruserID=df.loc[i,'userID']
        sql="select momentanswer_record.questionsymbol,momentanswer_record.starttime,basic_questioninfor.generaldescription,"
        sql=sql+"basic_questioninfor.difficulty,basic_questioninfor.thumbs"
        sql=sql+" from momentanswer_record , basic_questioninfor "
        sql=sql+"where momentanswer_record.questionsymbol=basic_questioninfor.questionsymbol "
        sql=sql+"and momentanswer_record.userID='%s"%self.partneruserID+"'"
        df=pd.read_sql_query(sql, self.engine1)
        for i in range(len(df)):
            tt=[]
            for j in range(4):
                tt.append(df.iloc[i,j])
            tt=tuple(tt)
            self.tree33.insert('',i,values=tt)

        
        
        
        
        sql="select momentanswer_record.questionsymbol,momentanswer_record.starttime,basic_questioninfor.generaldescription,"
        sql=sql+"basic_questioninfor.difficulty,basic_questioninfor.thumbs"
        sql=sql+" from momentanswer_record , basic_questioninfor "
        sql=sql+"where momentanswer_record.questionsymbol=basic_questioninfor.questionsymbol "
        sql=sql+"and momentanswer_record.userID='%s"%zdyallfunction.userID+"'"
        df=pd.read_sql_query(sql, self.engine1)
        for i in range(len(df)):
            tt=[]
            for j in range(4):
                tt.append(df.iloc[i,j])
            tt=tuple(tt)
            self.tree2.insert('',i,values=tt)
        
    
    def showmmycontribution(self):
        self.deltree1self()
        sql="select * from basic_questioninfor where questionsymbol like('"+"%%%%%s_%%%%"%zdyallfunction.userID+"')"
        print(sql)
        self.questions=pd.read_sql_query(sql, self.engine1)
        for i in range(len(self.questions)):
            tt=[]
            tt.append(self.questions.iloc[i,0])
            tt.append(self.questions.iloc[i,2])
            tt.append(self.questions.iloc[i,4])
            tt.append(self.questions.iloc[i,5])
            tt.append(self.questions.iloc[i,6])
            tt.append(self.questions.iloc[i,7])
            tt.append(self.questions.iloc[i,8])
            tt.append(self.questions.iloc[i,9])
            tt.append(self.questions.iloc[i,10])
            tt=tuple(tt)
            self.tree1.insert('',i,values=tt)
        
    def changemygroupnickname(self,event):
        self.text327['state']='normal'
        
    def changegroupname(self,event):
        item = self.tree3.selection()
        sql="select * from groupnamelist,grouptable where groupnamelist.groupnum=grouptable.groupnum and groupnamelist.groupnum='%s' and groupleader='%s'"%(self.tree3.item(item, "values")[0],zdyallfunction.userID)
        df=pd.read_sql_query(sql, self.engine1)
        if len(df)==0:
            tkinter.messagebox.showinfo(title='提示', message='您不是群主，无法修改公告')
            return 0
        self.text322['state']='normal'
    
    def changegroupnotice(self,event):
        item = self.tree3.selection()
        sql="select * from groupnamelist,grouptable where groupnamelist.groupnum=grouptable.groupnum and groupnamelist.groupnum='%s' and groupleader='%s'"%(self.tree3.item(item, "values")[0],zdyallfunction.userID)
        df=pd.read_sql_query(sql, self.engine1)
        if len(df)==0:
            tkinter.messagebox.showinfo(title='提示', message='您不是群主，无法修改公告')
            return 0
        self.text324['state']='normal'
    
    def qualifychangemygroupnickname(self,event):
        
        if self.text327['state']=='normal':
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update groupnamelist set nickname='%s' where groupnum='%s' and userID='%s' "%(self.text327.get('0.0','end').split('\n')[0],groupnum,zdyallfunction.userID)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            item=self.tree3.selection()
            sql="select * from groupnamelist where groupnum='%s'"%self.tree3.item(item, "values")[0]
            df=pd.read_sql_query(sql, self.engine1)
            print(df)
            x=self.tree32.get_children()
            for item in x:
                self.tree32.delete(item)
            for i in range(len(df)):
                tt=[]
                tt.append(df.loc[i,'nickname'])
                self.tree32.insert('',i,values=tt)
        self.text327['state']='disabled'
    
    def qualifychangegroupname(self,event):
        if self.text322['state']=='normal':
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update grouptable set groupname='%s' where groupnum='%s'"%(self.text322.get('0.0','end').split('\n')[0],groupnum)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
        self.deltree3self()
        self.showmygroup()
        self.text322['state']='disabled'
    
    def qualifychangegroupnotice(self,event):
        if self.text324['state']=='normal':
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update grouptable set groupnotice='%s' where groupnum='%s'"%(self.text324.get('0.0','end').split('\n')[0],groupnum)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
        self.deltree3self()
        self.showmygroup()
        self.text324['state']='disabled'
        
        
        

    
    def bind(self):
        self.tree1.bind('<Double-Button-1>',self.qualifyquestionsymbol1)
        self.tree2.bind('<Double-Button-1>',self.qualifyquestionsymbol2)
        self.tree3.bind('<Double-Button-1>',self.showgroupindetail)
        self.tree32.bind('<Double-Button-1>',self.showpartnerquestions)
        self.tree33.bind('<Double-Button-1>',self.qualifyquestionsymbol3)
        
        self.text322.bind('<Button-1>',self.changegroupname)
        self.text322.bind('<Double-Button-1>',self.changegroupname)
        self.text322.bind('<Return>',self.qualifychangegroupname)
        
        self.text324.bind('<Button-1>',self.changegroupnotice)
        self.text324.bind('<Double-Button-1>',self.changegroupnotice)
        self.text324.bind('<Return>',self.qualifychangegroupnotice)
        
        self.text327.bind('<Double-Button-1>',self.changemygroupnickname)
        self.text327.bind('<Button-1>',self.changemygroupnickname)
        self.text327.bind('<Return>',self.qualifychangemygroupnickname)
        
        
        im=Image.open(f'{os.getcwd()}/infor/rightan.png') 
        imgBtn =ImageTk.PhotoImage(im.resize((int(0.05*width),int(0.05*height)))) 
        self.button21=tkinter.Button(self.frame2,image=imgBtn,command=self.nextprocess)
        self.button21.place(x=0.9*width,y=0.8*height,anchor='ne')
        im2=Image.open(f'{os.getcwd()}/infor/leftan.png') 
        imgBtn2 =ImageTk.PhotoImage(im2.resize((int(0.05*width),int(0.05*height)))) 
        self.button22=tkinter.Button(self.frame2,image=imgBtn2,command=self.formerprocess)
        self.button22.place(x=0.5*width,y=0.8*height,anchor='nw')
        
        self.button31=tkinter.Button(self.frame3,image=imgBtn,command=self.partnernextprocess)
        self.button31.place(x=0.9*width,y=0.9*height,anchor='ne')
        self.button32=tkinter.Button(self.frame3,image=imgBtn2,command=self.partnerformerprocess)
        self.button32.place(x=0.5*width,y=0.9*height,anchor='nw')
        

       
        win.mainloop()
        
    def nextprocess(self):
        if ((self.processnum+1)<len(self.process)):
            self.processnum=self.processnum+1
            self.filec()
            self.showquestion2()
        else:
            tkinter.messagebox.showinfo(title='提示', message='这是您有作答记录的最后一步')
    def formerprocess(self):
        if (self.processnum)<=0:
            tkinter.messagebox.showinfo(title='提示', message='这是您有作答记录的第一步')
        else:
            zdyallfunction.fileinelements()
            self.processnum=self.processnum-1
            self.filec()
            self.showquestion2()
            
            
    def partnernextprocess(self):
        if ((self.processnum+1)<len(self.process)):
            self.processnum=self.processnum+1
            self.partnerfilec()
            self.showquestion3()
        else:
            tkinter.messagebox.showinfo(title='提示', message='这是您有作答记录的最后一步')
    def partnerformerprocess(self):
        if (self.processnum)<=0:
            tkinter.messagebox.showinfo(title='提示', message='这是您有作答记录的第一步')
        else:
            zdyallfunction.fileinelements()
            self.processnum=self.processnum-1
            self.partnerfilec()
            self.showquestion3()
            
    def drawquestion(self):
        zdyallfunction.getquestion(zdyallfunction.questionsymbol)
        zdyallfunction.fileinelements()
        zdyallfunction.file()
        zdyallfunction.drawquestion()
        
    def showquestion1(self):
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.5*width),int(0.5*height)),Image.ANTIALIAS))
        self.canvas11.create_image(0,0,anchor='nw',image = photo)
        win.mainloop()
        
    def showquestion2(self):
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas21.create_image(0,0,anchor='nw',image = photo)
        im2=Image.open(f'{os.getcwd()}/drawing/userM.png')
        photo2 = ImageTk.PhotoImage(im2.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas22.create_image(0,0,anchor='nw',image = photo2)
        self.showprocess()
        win.mainloop()
        
    def showquestion3(self):
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas31.create_image(0,0,anchor='nw',image = photo)
        im=Image.open(f'{os.getcwd()}/drawing/question.png')
        photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas31.create_image(0,0,anchor='nw',image = photo)
        im2=Image.open(f'{os.getcwd()}/drawing/userM.png')
        photo2 = ImageTk.PhotoImage(im2.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
        self.canvas32.create_image(0,0,anchor='nw',image = photo2)

        self.showpartnerprocess()
        win.mainloop()
        
    def qualifyquestionsymbol1(self,event):
            item = self.tree1.selection()[0]
            print(item)
            print(self.tree1.item(item, "values")) 
            zdyallfunction.questionsymbol=self.tree1.item(item, "values")[0]
            self.drawquestion()
            self.showquestion1()
            
    def getprocess(self):
        sql="select * from moment"+zdyallfunction.questionsymbol+" where userID='%s'"%zdyallfunction.userID
        sql=sql+" and starttime='%s'"%self.tree2.item(self.item, "values")[1]
        self.process=pd.read_sql_query(sql, self.engine2)
        self.processnum=0
    
    def getpartnerprocess(self):
        sql="select * from moment"+zdyallfunction.questionsymbol+" where userID='%s'"%self.partneruserID
        sql=sql+" and starttime='%s'"%self.tree33.item(self.item, "values")[1]
        self.process=pd.read_sql_query(sql, self.engine2)
        self.processnum=0
    
    def filec(self):
        columnnum=self.process.shape[1]
        self.varnum21.set('')
        zdyallfunction.c=[]
        for i in range(len(zdyallfunction.elements)):
            c_=[]
            zdyallfunction.c.append(c_)
        for i in range(4,columnnum-1):
            temp=self.process.iloc[self.processnum,i]
            temp=temp.split(',')
            print(self.varnum21.get()=='')
            print(len(temp)>1)
#            if self.varnum21.get()=='' and len(temp)>1:
#                try:
#                    float(temp[-1])
#                except:
#                    t=temp[-1].strip('\n')
#                    self.varnum21.set(t)
            if len(temp)!=1:
                class C_():
                    pass
                c_=C_()
                c_.num=int(temp[0])
                c_.type=temp[1]
                c_.Mi=float(temp[2])
                c_.Mj=float(temp[3])
                c_.Mmid=float(temp[4])
                c_.ns=float(temp[5])
                c_.ne=float(temp[6])
                zdyallfunction.changec(c_)
        temp=self.process.iloc[self.processnum,columnnum-1]
        print(temp[0])
        if len(temp)>1:
            t=temp
#            t=temp.replace('\n',"")
#            print(t)
            
            t=temp
            if len(t)>20:
                t=list(t)
                t.insert(20,'\n',)
                t=''.join(t)
            if len(t)>40:
                t=list(t)
                t.insert(40,'\n',)
                t=''.join(t)
            self.varnum21.set(t)
            
            self.varnum21.set(t)
        zdyallfunction.drawuserM(-1)
    
    
        
    def partnerfilec(self):
        columnnum=self.process.shape[1]
        self.varnum22.set('')
        for i in range(len(zdyallfunction.elements)):
            c_=[]
            zdyallfunction.c.append(c_)
        for i in range(4,columnnum-1):
            temp=self.process.iloc[self.processnum,i]
            temp=temp.split(',')
            print(self.varnum21.get()=='')
            print(len(temp)>1)
#            if self.varnum21.get()=='' and len(temp)>1:
#                try:
#                    float(temp[-1])
#                except:
#                    t=temp[-1].strip('\n')
#                    self.varnum21.set(t)
            if len(temp)!=1:
                class C_():
                    pass
                c_=C_()
                c_.num=int(temp[0])
                c_.type=temp[1]
                c_.Mi=float(temp[2])
                c_.Mj=float(temp[3])
                c_.Mmid=float(temp[4])
                c_.ns=float(temp[5])
                c_.ne=float(temp[6])
                zdyallfunction.changec(c_)
        temp=self.process.iloc[self.processnum,columnnum-1]
        print(temp[0])
        if len(temp)>1:
            t=temp
#            t=temp.replace('\n',"")
#            print(t)
            
            if len(t)>20:
                t=list(t)
                t.insert(19,'\n',)
                t=''.join(t)
            if len(t)>40:
                t=list(t)
                t.insert(38,'\n',)
                t=''.join(t)
            self.varnum22.set(t)
        zdyallfunction.drawuserM(-1)
        
    def showprocess(self):
        self.canvas22.relativeposition_for_manage()
        self.canvas22.paintline(zdyallfunction.c,self.canvas22.relposition)
#        im=Image.open(f'{os.getcwd()}/drawing/userM.png')
#        photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
#        self.canvas22.create_image(0,0,anchor='nw',image = photo)
#        self.mainloop()
    
    def showpartnerprocess(self):
        self.canvas32.relativeposition_for_manage()
        self.canvas32.paintline(zdyallfunction.c,self.canvas32.relposition)
#        im=Image.open(f'{os.getcwd()}/drawing/userM.png')
#        photo = ImageTk.PhotoImage(im.resize((int(0.4*width),int(0.4*height)),Image.ANTIALIAS))
#        self.canvas32.create_image(0,0,anchor='nw',image = photo)
#        self.mainloop()
    
    
    def qualifyquestionsymbol2(self,event):
            self.item = self.tree2.selection()[0]
            print(self.tree2.item(self.item, "values")) 
            zdyallfunction.questionsymbol=self.tree2.item(self.item, "values")[0]
            self.drawquestion()
            self.getprocess()
            self.filec()
            self.showquestion2()

    def changemyquestion(self):
        self.tp11=tkinter.Toplevel()
        self.tp11.title('我的题库')
        self.tp11.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.tp11.geometry('%dx%d+%d+%d'%(0.2*width,0.4*height,dx,dy))
        self.lable111=tkinter.Label(self.tp11,text="题目状态",fg='red')
        self.cmb111 = ttk.Combobox(self.tp11)
        self.cmb111['value'] = ("公开","私密")
        self.cmb111.current(0)
        self.lable112=tkinter.Label(self.tp11,text="题型描述",fg='red')
        self.text112=tkinter.Text(self.tp11,width=30,height=6,highlightthickness=2,highlightcolor='red',
           highlightbackground='red')
        self.text112.insert("end","")
        self.button111=tkinter.Button(self.tp11,text='确认修改题目状态',font=('微软雅黑',10),width=15,height=1,fg='white',bg='black',command=self.changestate)
        self.button112=tkinter.Button(self.tp11,text='确认修改题型描述',font=('微软雅黑',10),width=15,height=1,fg='white',bg='black',command=self.changegeneraldescription)
        l1=tkinter.Label(self.tp11,text="    ")
        l2=tkinter.Label(self.tp11,text="    ")
        self.lable111.grid(row=0,column=0)
        self.cmb111.grid(row=1,column=0)
        l1.grid(row=2,column=0)
        self.button111.grid(row=3,column=0)
        self.lable112.grid(row=4,column=0)
        self.text112.grid(row=5,column=0)
        l2.grid(row=6,column=0)
        self.button112.grid(row=7,column=0)
    def changestate(self):
        try:
            if zdyallfunction.questionsymbol.split('_')[0]!=zdyallfunction.userID:
                tkinter.messagebox.showinfo(title='提示', message='修改失败,请先双击选择题目！')
                return 0
        except:
            pass
        try:
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update basic_questioninfor set state=%s where questionsymbol=%s"
            cursor.execute(sql,[self.cmb111.get(),zdyallfunction.questionsymbol])
            conn.commit()
            cursor.close()
            conn.close()
            self.showmmycontribution()
            tkinter.messagebox.showinfo(title='提示', message='修改成功！')
        except:
            tkinter.messagebox.showinfo(title='提示', message='修改失败！')
    def changegeneraldescription(self):
        try:
            if zdyallfunction.questionsymbol.split('_')[0]!=zdyallfunction.userID:
                tkinter.messagebox.showinfo(title='提示', message='修改失败,请先双击选择题目！')
                return 0
        except:
            pass
        if len(self.text112.get('0.0','end'))<1:
            tkinter.messagebox.showinfo(title='提示', message='描述内容不能为空！')
            return
        try:
            conn = pymysql.connect(host='rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com',user='richzhou',password='Hua!0928',database='allinfor',charset='utf8')
            cursor = conn.cursor()
            sql="update basic_questioninfor set generaldescription=%s where questionsymbol=%s"
            cursor.execute(sql,[str(self.text112.get('0.0','end')),zdyallfunction.questionsymbol])
            conn.commit()
            cursor.close()
            conn.close()
            tkinter.messagebox.showinfo(title='提示', message='修改成功！')
            self.showmmycontribution()
        except:
            tkinter.messagebox.showinfo(title='提示', message='修改失败！')
        win.mainloop()
    
    def showgroupindetail(self,event):
        item = self.tree3.selection()
#        print(self.tree3.item(item, "values")) 
        self.text321.config(state='normal')
        self.text321.delete('0.0','end')
        self.text321.insert ('end',self.tree3.item(item, "values")[0])
        global groupnum
        groupnum=str(self.tree3.item(item, "values")[0])
        self.text321.config(state='disabled')
        
        self.text322.config(state='normal')
        self.text322.delete('0.0','end')
        self.text322.insert ('end',self.tree3.item(item, "values")[1])
        self.text322.config(state='disabled')
        
        self.text323.config(state='normal')
        self.text323.delete('0.0','end')
        self.text323.insert ('end',self.tree3.item(item, "values")[2])
        self.text323.config(state='disabled')
        
        self.text324.config(state='normal')
        self.text324.delete('0.0','end')
        self.text324.insert ('end',self.tree3.item(item, "values")[3])
        self.text324.config(state='disabled')

        print(self.mygroup.iloc[0,0])
        for i in range(len(self.mygroup)):
            if self.mygroup.iloc[i,0]==self.tree3.item(item, "values")[0]:
                self.text327.config(state='normal')
                self.text327.delete('0.0','end')
                self.text327.insert ('end',self.mygroup.iloc[i,6])
                self.text327.config(state='disabled')
        
        self.frame32.place(x=0.4*width,y=0,anchor='nw')
        self.frame33.place(x=0,y=0.2*height,anchor='nw')
        self.frame35.place(x=0.5*width,y=0,anchor='nw')
        #        self.Button325.place(x=0.4*width,y=0.25*height)
        
        sql="select * from groupnamelist where groupnum='%s'"%self.tree3.item(item, "values")[0]
        df=pd.read_sql_query(sql, self.engine1)
        print(df)
        x=self.tree32.get_children()
        for item in x:
            self.tree32.delete(item)
        for i in range(len(df)):
            tt=[]
            tt.append(df.loc[i,'nickname'])
            self.tree32.insert('',i,values=tt)

        
    def newgroup(self):
        self.tp31=tkinter.Toplevel()
        self.tp31.title('新建群组')
        self.tp31.iconbitmap(f'{os.getcwd()}/infor/tubiao.ico')
        self.tp31.geometry('%dx%d+%d+%d'%(0.2*width,0.2*height,dx,dy))
        self.lable_tp31_1=tkinter.Label(self.tp31,text="群名",fg='black')
        self.entry_tp31_1=tkinter.Entry(self.tp31,width=20)
        l1=tkinter.Label(self.tp31,text="   ")
        self.lable_tp31_2=tkinter.Label(self.tp31,text="群公告",fg='black')
        self.entry_tp31_2=tkinter.Entry(self.tp31,width=20)
        l2=tkinter.Label(self.tp31,text="   ")
        self.button_tp31_1=tkinter.Button(self.tp31,text='确认新建',font=('微软雅黑',10),command=self.qualifynewgroup)
        self.lable_tp31_1.grid(row=0,column=0)
        self.entry_tp31_1.grid(row=0,column=1)
        l1.grid(row=1,column=0)
        self.lable_tp31_2.grid(row=2,column=0)
        self.entry_tp31_2.grid(row=2,column=1)
        l2.grid(row=3,column=0)
        self.button_tp31_1.grid(row=4,column=1)
    
    def deltree3self(self):
        x=self.tree3.get_children()
        for item in x:
            self.tree3.delete(item)

    def showmygroup(self):
        self.deltree3self()
        sql="select * from grouptable,groupnamelist where groupnamelist.userID='%s' and grouptable.groupnum=groupnamelist.groupnum"%zdyallfunction.userID 
        self.mygroup=pd.read_sql_query(sql, self.engine1)
        for i in range(len(self.mygroup)):
            tt=[]
            tt.append(self.mygroup.iloc[i,0])
            tt.append(self.mygroup.iloc[i,1])
            tt.append(self.mygroup.iloc[i,2])
            tt.append(self.mygroup.iloc[i,3])
            tt=tuple(tt)
            self.tree3.insert('',i,values=tt)
    
    def addnewgroup(self):
        df=pd.DataFrame(np.zeros((1,3)))
        df.columns=['groupnum','userID','nickname']
        sql="select * from grouptable where groupnum='%s'"%self.entry328.get()
        print(sql)
        num=pd.read_sql_query(sql, self.engine1)
        print(len(num))
        if len(num)==0:
            tkinter.messagebox.showinfo(title='提示', message='不存在此群组')
            return 0
        else:
            df.loc[0,'groupnum']=self.entry328.get()
            df.loc[0,'userID']=zdyallfunction.userID
            df.loc[0,'nickname']=zdyallfunction.nickname
            try:
                df.to_sql('groupnamelist', self.engine1, index= False,if_exists='append')
                self.showmygroup()
                tkinter.messagebox.showinfo(title='提示', message='加入成功')
            except:
                tkinter.messagebox.showinfo(title='提示', message='您已加入或请检测网络')
            
    
    def qualifynewgroup(self):
        try:
            df=pd.DataFrame(np.zeros((1,4)))
            df.columns=['groupnum','groupname','groupleader','groupnotice']
            df2=pd.DataFrame(np.zeros((1,3)))
            df2.columns=['groupnum','userID','nickname']
            df.loc[0,'groupnum']=str(random.randint(0,99999999)).zfill(8)
            df2.loc[0,'groupnum']=df.loc[0,'groupnum']
            df.loc[0,'groupname']=self.entry_tp31_1.get()
            df.loc[0,'groupleader']=zdyallfunction.userID
            df2.loc[0,'userID']=zdyallfunction.userID
            df2.loc[0,'nickname']=zdyallfunction.nickname
            df.loc[0,'groupnotice']=self.entry_tp31_2.get()
            engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
            df.to_sql('grouptable', engine, index= False,if_exists='append')
            engine = create_engine('mysql+pymysql://richzhou:Hua!0928@rm-uf632v8943g1svv2pho.mysql.rds.aliyuncs.com:3306/allinfor')
            df2.to_sql('groupnamelist', engine, index= False,if_exists='append')
            tkinter.messagebox.showinfo(title='提示', message='新建成功')
        except:
            tkinter.messagebox.showinfo(title='提示', message='新建失败请重试')
            
    def qualifyquestionsymbol3(self,event):
            self.item = self.tree33.selection()[0]
            zdyallfunction.questionsymbol=self.tree33.item(self.item, "values")[0]
            self.drawquestion()
            self.getpartnerprocess()
            self.partnerfilec()
            self.showquestion3()



    def createreport(self):
        report=REPORT()
        win.mainloop()










        
win.mainloop()

