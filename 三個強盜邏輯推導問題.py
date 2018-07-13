import random


#只說真話
def Robber_A():
	#1+1是否等於2
	if 1+1==2:
		#說真話
		return "True"

def Robber_B():
	#1+1是否等於2
	if 1+1==2:
		#說假話
		return "False"
	

def Robber_C():
	#1+1是否等於2
	if 1+1==2:
		#不管是真是假 ，都隨機回答
		AnserRandom=random.randint(0,1)
		if AnserRandom==0:
			return "True"
		if AnserRandom==1:
			return "False"
	
print("問題:1+1=2嗎?")
print("強盜A:",Robber_A())
print("強盜B:",Robber_B())
print("強盜C:",Robber_C())

RightAns="True"
print("正確答案:",RightAns)



#檢驗強盜是誰
def CheckPerson():
    
    #清空問題陣列
    ResultLi=[]
    
    #重複問一百次問題
    for i in range(100):
        ResultLi.append(Robber_A())
    RightAns_num=0
    FailAns_num=0
    for Result in ResultLi:
        #只要回答正確就統計加一個正確紀錄
        if Result=="True":
            RightAns_num+=1
        #只要回答錯誤就統計加一個錯誤紀錄
        if Result=="False":
            FailAns_num+=1
    正確率=(RightAns_num/100)*100
    錯誤率=(FailAns_num/100)*100
    print ("強盜A的正確率",正確率,"強盜A的錯誤率",錯誤率)      
    
    #清空問題陣列
    ResultLi=[]
    
    #重複問一百次問題
    for i in range(100):
        ResultLi.append(Robber_B())
    RightAns_num=0
    FailAns_num=0
    for Result in ResultLi:
        #只要回答正確就統計加一個正確紀錄
        if Result=="True":
            RightAns_num+=1
            
        #只要回答錯誤就統計加一個錯誤紀錄
        if Result=="False":
            FailAns_num+=1
    正確率=(RightAns_num/100)*100
    錯誤率=(FailAns_num/100)*100
    print ("強盜B的正確率",正確率,"強盜B的錯誤率",錯誤率)      
    
    #清空問題陣列
    ResultLi=[]
    
    #重複問一百次問題
    for i in range(100):
        ResultLi.append(Robber_C())
    RightAns_num=0
    FailAns_num=0
    for Result in ResultLi:
        #只要回答正確就統計加一個正確紀錄
        if Result=="True":
            RightAns_num+=1
            
        #只要回答錯誤就統計加一個錯誤紀錄
        if Result=="False":
            FailAns_num+=1
    正確率=(RightAns_num/100)*100
    錯誤率=(FailAns_num/100)*100
    print ("強盜C的正確率",正確率,"強盜C的錯誤率",錯誤率)      

print ("重複問100次問題後，檢核可信度")
CheckPerson()





Ouput:
    問題:1+1=2嗎?
    強盜A: True
    強盜B: False
    強盜C: False
    正確答案: True
    重複問100次問題後，檢核可信度
    強盜A的正確率 100.0 強盜A的錯誤率 0.0
    強盜B的正確率 0.0 強盜B的錯誤率 100.0
    強盜C的正確率 51.0 強盜C的錯誤率 49.0
