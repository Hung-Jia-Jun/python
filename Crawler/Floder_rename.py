# -*- coding: utf-8 -*-
import io,os,sys,pdb

def Read_txt(location):
	read_recent_contant=[]
	io_open_Txt=os.getcwd()
	io_open_Txt=location
	io_obj=io.open(io_open_Txt, 'r',encoding = 'utf-8') #文字檔位置
	spaceNum=0 #space count
	while True:
		read_cont = io_obj.readline() #逐行讀取文字檔
		read_cont=read_cont.replace("\n","")
		read_recent_contant.append(read_cont)
		if read_cont=="":
			break
	return read_recent_contant


class Write_txt: #append the raw line in text file
	def __init__(self,FileName):
		self.f = open(FileName, 'a')
		self.FileName=FileName
	def Write_Action(self,Msg):
		self.f.write(Msg)
	def CloseFile(self):
		self.f.truncate()
