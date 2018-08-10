# coding: utf-8
import csv
FilePath='X_test_submission.csv'
# 開啟 CSV 檔案
with open(FilePath, newline='') as csvfile:
	# 讀取 CSV 檔案內容
	rows = csv.reader(csvfile)
	length=0
	Sussful=0
	# 以迴圈輸出每一列
	for row in rows:
		if row[0].split("_")[0] == row[1].replace(" ",""):
			Sussful+=1
		length+=1
	print("正確率: "+str((Sussful/length)*100))