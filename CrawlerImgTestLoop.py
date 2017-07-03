# -*- coding: utf-8 -*-
import base64
import urllib.request
import random
import sqlite3
import time
SleepTime=input ("Sleep time?")
LoopUse=input('''Loop Crawler true or false use "1" or "0" ?''')
while LoopUse=="1":
	FileName=str(random.randint(0,99999))
	urllib.request.urlretrieve("https://4.bp.blogspot.com/-FF5u6je-3vs/V7bIcSEtjLI/AAAAAAAACeQ/m4bdfDdUOncBKBi1NE0vFiMNId5_1s8lQCLcB/s1600/Wallpaper%2B%25E6%25A1%258C%25E5%25B8%2583%2B006-08.jpg", FileName+".jpg")
	with open(FileName+".jpg", "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	conn = sqlite3.connect('Pic.db')
	cursor = conn.cursor()
	cursor.execute('''insert into Picture (_Pic) values ("'''+str(encoded_string)+'")''')
	conn.commit()
	time.sleep(int(SleepTime))
