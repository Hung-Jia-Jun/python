# -*- coding: utf-8 -*-
from socket import *
import SocketServer
from msvcrt import getch
import multiprocessing,os,sys,pdb,time,os
BUFSIZ=1024
User_Sound=""
SceneMode="" #場景模式
os.system("chcp 950")  #設定字碼頁


def WriteSoundTxt(FileLocation,writeTxtInput):
        f = open(FileLocation, 'w') #要同步的playsound.txt
        f.write(writeTxtInput)
        f.close() #關閉文件流
def ReadSoundTxt(FileLocation):
    global User_Sound
    for i in open(FileLocation,'r'):
        User_Sound=i
    if User_Sound=="":
        pass
    return User_Sound



HOST = ''
PORT = 47990

ADDR = (HOST,PORT)

def Python_Client(Send_Msg,Re_Msg):
    Re_Msg=tcpCliSock.recv(BUFSIZ)

def Runthread():
    PlaySound_console=WriteSoundTxt('C:\\A.txt',"") #伺服器端的A.txt辨識指令檔
    Server_Sound_Data=WriteSoundTxt('C:\\PlaySound.txt',"") #伺服器端的Play_Sound.txt
    WriteSoundTxt('C:\\RecogContant.txt',"")#寫入新資料

    HOST = ''
    PORT = 47990

    ADDR = (HOST,PORT)
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(50)
    User_Sound=""
    Temp_Server_Data=""
    Temp_Sound_Console=""
    Temp_RecogContant=""
    Recv_Client_Message=""
    Tempdata=""
    SoundList=[]
    SoundList.append("我是誰")
    SoundList.append("你好阿")
    SoundList.append("我是誰")
    SoundList.append("你好阿")
    SoundList.append("我是誰")
    SoundList.append("你好阿")





    LanguageMode="Chinese"
    PythonConsole="2" #控制客戶端的python
    PlaySound_text="is Message" #發聲字串

    i=0
    ScenesMode=0
    while True:
        print 'waiting for Client connection...'
        tcpCliSock,addr = tcpSerSock.accept()
        #os.system("cls")
        print 'connected Client from: ',addr,".................."
        while True:

            try:
                tcpCliSock.send(" ")#測試connet狀態
                Recv_Client_Message=tcpCliSock.recv(BUFSIZ) #接收指令
            except :
                break #進入等待client的迴圈等待連線

            #Return_Client_py="Send_To_PythonClient:"+PythonConsole+","+LanguageMode+","+PlaySound_text #建構出返回數據  格式為"PythonConsole辨識/發聲,LanguageMode 語言,PlaySound_text  發聲語句,"
            #tcpCliSock.send(Return_Client_py)

            #if Recv_Client_Message[0:13]=="TxtRecognize=":  #
            #    Recv_Client_Message=Recv_Client_Message.replace("TxtRecognize=","") #把Playsound_console=替換成""
            #    PythonConsole=Recv_Client_Message
            #    print "Get TxtRecognize: ",PythonConsole



            if Recv_Client_Message[0:9]=="PlaySound": #處理發聲音檔
                Recv_Client_Message=Recv_Client_Message.replace("PlaySound","") #把PlaySound這個特徵碼拿掉
                PlaySound_text=Recv_Client_Message #把字串存進發聲的變數
                print "Client PlaySound: ",PlaySound_text





            if Recv_Client_Message[0:12]=="TxtRecognize":  #clinet端向Server查詢辨識後的字串
                print "Send TxtRecognize: "
                tcpCliSock.send(Return_message) #回傳server端接收到的使用者辨識字串



            if Recv_Client_Message[0:18]=="Playsound_console=":
                Recv_Client_Message=Recv_Client_Message.replace("Playsound_console=","") #把Playsound_console=替換成""
                PythonConsole=Recv_Client_Message
                print PythonConsole
            if Recv_Client_Message[0:9]=="Sound_Str":  #處理劇本
                SendMsg=""
                ArrayLen=len(SoundList)-3
                if ArrayLen==0:
                    ArrayLen=0
                for i in range(0,ArrayLen):
                    List_Str=SoundList[i]
                    SendMsg+=List_Str+","
                tcpCliSock.send(SendMsg)
                print "Server Send: ",SendMsg
                tcpCliSock.close()






            if Recv_Client_Message[0:6]=="P5_Msg":  #處理劇本
                Recv_Client_Message=Recv_Client_Message.replace("P5_Msg","") #替換掉P5_Msg變成空值
                P5_Msg=Recv_Client_Message.split(",")
                SoundList+=P5_Msg #將劇本檔存入陣列中
                for SoundContant in SoundList: #印出劇本陣列
                    Recv_Client_Message=SoundContant #把當前劇本的語句存入Msg裡面去比對有沒有場景控制字元出現
                    if Recv_Client_Message[0:12]=="Scenes Mode=": #如果場景控制字元出現
                        Recv_Client_Message=Recv_Client_Message.replace("Scenes Mode=","") #替換掉"Scenes Mode="變成空值
                        ScenesMode=Recv_Client_Message
                        print "ScenesMode is : ",ScenesMode
                    elif Recv_Client_Message[0:9]=="Language=": #如果場景控制字元出現
                        Recv_Client_Message=Recv_Client_Message.replace("Language=","") #替換掉"Scenes Mode="變成空值
                        LanguageMode=Recv_Client_Message
                        print "Language is : ",LanguageMode
                        #tcpCliSock.close() #關閉server連線
                    else:
                        print SoundContant #印出劇本陣列





            if Recv_Client_Message[0:5]=="Clear":  #清空劇本內容
                print "Clear SoundStr Array"
                del SoundList[:]
                print SoundList
                #tcpCliSock.close() #關閉server連線







            if Recv_Client_Message[0:12]=="RecogContant":
                message=Recv_Client_Message.split("RecogContant")[1]
                if (Tempdata!=message): #如果server給的資料與現在的暫存器內容不一樣
                    print u"Get RecogContant~ "
                    Tempdata=message #將現在的資料存進Tempdata暫存器
                    WriteSoundTxt('C:\\RecogContant.txt',message)#寫入新資料










        tcpCliSock.close()





Runthread()
