from django.db import models

#預設行程描述集
class GrupDescriptionPreset(models.Model):

    # primary key = unique + not null
    # 主鍵 : 是為了保證這張表的預設行程描述集只有一個唯一
    # 唯一鍵 : 是想達成行程標題不重複，但也能讓標題為空的彈性而設計的

    #行程號
    GrupCd = models.TextField(max_length=50,primary_key=True)

    #預設行程內容標題
    GrupTitle = models.TextField(default='預設行程標題',max_length=50,unique=True)

    #行程內容
    GrupContent = models.TextField(default='預設行程內容',max_length=50)
class TourData(models.Model):
    GrupSnm = models.TextField(max_length=50) #產品名稱
    GrupLn = models.TextField(max_length=50) #旅遊天數
    LeavDt = models.TextField(max_length=50) #出發日期
    AgtAm = models.TextField(max_length=50) #價錢
    SaleYqt = models.TextField(max_length=50) #可售位
    EstmYqt = models.TextField(max_length=50) #總團位
    GrupDescription = models.ForeignKey(GrupDescriptionPreset, on_delete=models.CASCADE) #預設行程描述集
    
