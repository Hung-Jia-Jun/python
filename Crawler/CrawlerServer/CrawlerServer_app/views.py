from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import CrawlerServer_app.Crawler as Crawler
from CrawlerServer_app.models import TourData,GrupDescriptionPreset
import pdb
import uuid

def WriteTourData(PageData):
    #輪詢該頁面的所有團體資訊
    for Tours in PageData["All"]:
        #產品名稱
        GrupSnm = str(Tours["GrupSnm"])
        
        #旅遊天數
        GrupLn = str(Tours["GrupLn"])
        
        #出發日期
        LeavDt = str(Tours["LeavDt"])
        
        #價錢
        AgtAm = str(Tours["AgtAm"])
        
        #可售位
        SaleYqt = str(Tours["SaleYqt"])
        
        #總團位
        EstmYqt = str(Tours["EstmYqt"])
        
        #從資料庫撈一個預設內容資料集去關聯
        ReadDB_GrupDescriptionPreset = GrupDescriptionPreset.objects.filter(GrupTitle = "預設行程標題2")
        GrupDescriptionPreset_ = ReadDB_GrupDescriptionPreset.first()
        
        #用ORM儲存爬下來的資料
        tourData = TourData(   GrupSnm = GrupSnm,
                    GrupLn = GrupLn,
                    LeavDt = LeavDt,
                    AgtAm = AgtAm,
                    SaleYqt = SaleYqt,
                    EstmYqt = EstmYqt,
                    GrupDescription = GrupDescriptionPreset_)
        tourData.save()      

#創建預設內容集
@csrf_exempt
def CreateGrupDescription(request):
    GrupTitle = request.GET.get("GrupTitle")
    grupDescription = GrupDescriptionPreset(
                        GrupCd = str(uuid.uuid4()),
                        GrupTitle = GrupTitle)
    grupDescription.save()
    return HttpResponse("OK")


#開始爬蟲
@csrf_exempt
def StartCrawler(request):
    #爬取多個頁面
    for i in range(1,10):
        #總共有兩間旅行社要爬資料 澄果旅遊
        Orangetour_PageData = Crawler.StartCrawlerTourCorporation("orangetour",PageIndex = i)
        

        #總共有兩間旅行社要爬資料 新魅力旅遊
        Newamazing_PageData = Crawler.StartCrawlerTourCorporation("newamazing",PageIndex = i)


        #讀取/寫入資料庫

        #澄果旅遊
        WriteTourData(Orangetour_PageData)

        #新魅力旅遊
        WriteTourData(Newamazing_PageData)

    return HttpResponse("OK")
# Create your views here.
