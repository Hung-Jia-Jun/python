# 目錄
  * [如何使用本程式](#如何使用本程式)
  * [開始執行輸出辨識圖片](#開始執行輸出辨識圖片)
  * [芒果成熟度辨識](#芒果成熟度辨識)
  * [機器看到的圖像](#處理後機器看到的圖像)




# 芒果成熟度辨識
### 在環境中，要使用機械手臂來摘採芒果
### 一般都是透過人工摘採
### 或是透過機械手臂摘採
![](http://www.merit-times.com.tw/news_pic/20170506/825448_592833.jpg)

[回到目錄](#目錄)

### 這個成熟度引擎可以檢測出下列資料
* 成熟度
* 還有幾天過期
* 機械手臂目標座標

## 未處理前，原始圖像
![](https://github.com/Hung-Jia-Jun/python/blob/master/DeepLearningPrediction/%E8%8A%92%E6%9E%9C%E8%BE%A8%E8%AD%98/YOLO_%E8%8A%92%E6%9E%9C%E6%88%90%E7%86%9F%E5%BA%A6%E8%BE%A8%E8%AD%98/yad2k/images/MangoTree_797.jpg)

[回到目錄](#目錄)

## 處理後機器看到的圖像  
* Maturity
  * 距離到期日還有幾天 
* 49.74% 
  * 機器預測目前成熟度0-100%等百分量級
* Position
  * 發送給機械手臂的座標
![](https://github.com/Hung-Jia-Jun/python/blob/master/DeepLearningPrediction/%E8%8A%92%E6%9E%9C%E8%BE%A8%E8%AD%98/YOLO_%E8%8A%92%E6%9E%9C%E6%88%90%E7%86%9F%E5%BA%A6%E8%BE%A8%E8%AD%98/yad2k/images/out/MangoTree_797.jpg)

[回到目錄](#目錄)

### 程式也能處理受到葉子遮擋的芒果，並取得正確的位置與成熟度預測

![](https://github.com/Hung-Jia-Jun/python/blob/master/DeepLearningPrediction/%E8%8A%92%E6%9E%9C%E8%BE%A8%E8%AD%98/YOLO_%E8%8A%92%E6%9E%9C%E6%88%90%E7%86%9F%E5%BA%A6%E8%BE%A8%E8%AD%98/yad2k/images/out/MangoTree_806.jpg)

[回到目錄](#目錄)

### 晴天、雨天影像都會自動補全 辨識成熟度的效果也不會受到影響
![](https://github.com/Hung-Jia-Jun/python/blob/master/DeepLearningPrediction/%E8%8A%92%E6%9E%9C%E8%BE%A8%E8%AD%98/YOLO_%E8%8A%92%E6%9E%9C%E6%88%90%E7%86%9F%E5%BA%A6%E8%BE%A8%E8%AD%98/yad2k/images/out/MangoTree_816.jpg)

[回到目錄](#目錄)

### 摘採後對採果車內的芒果做辨識也通用，也能檢測出該採果車的平均成熟日期
![](https://github.com/Hung-Jia-Jun/python/blob/master/DeepLearningPrediction/%E8%8A%92%E6%9E%9C%E8%BE%A8%E8%AD%98/YOLO_%E8%8A%92%E6%9E%9C%E6%88%90%E7%86%9F%E5%BA%A6%E8%BE%A8%E8%AD%98/yad2k/images/out/MangoTree_804.jpg)

[回到目錄](#目錄)

### 搭配攝影機縮放，將可對遠距離的芒果樹做預測，不用親自將機器移動過去
![](https://github.com/Hung-Jia-Jun/python/blob/master/DeepLearningPrediction/%E8%8A%92%E6%9E%9C%E8%BE%A8%E8%AD%98/YOLO_%E8%8A%92%E6%9E%9C%E6%88%90%E7%86%9F%E5%BA%A6%E8%BE%A8%E8%AD%98/yad2k/images/out/MangoTree_802.jpg)

[回到目錄](#目錄)

# 如何使用本程式
## Requirements

- [Keras](https://github.com/fchollet/keras)
- [Tensorflow](https://www.tensorflow.org/)
- [Numpy](http://www.numpy.org/)
- [h5py](http://www.h5py.org/) (For Keras model serialization.)
- [Pillow](https://pillow.readthedocs.io/) (For rendering test results.)
- [Python 3](https://www.python.org/)
- [pydot-ng](https://github.com/pydot/pydot-ng) (Optional for plotting model.)
- [OpenCV](#【準備工作】)

[回到目錄](#目錄)



## 【準備工作】
1. 首先安裝python，pip，numpy
2. 安裝教程參考以前的文章：
3. 安裝python：http://blog.csdn.net/lyj_viviani/article/details/51763101 
4. 安裝pip： http://blog.csdn.net/lyj_viviani/article/details/70568434 
5. 安裝numpy：使用命令行輸入pip install numpy即可自動安裝

## 【正式步驟】
1. 進入https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
2. 根據之前python的版本決定下載whl格式文件，下載後進入文件所在位置，命令行輸入pip install * .whl

## 【安裝Anaconda】
1. [Anaconda官方網站](https://anaconda.org/)
2. 依照當前windows版本進行安裝
3. 使用Anaconda的 Terminal 安裝Tensorflow
4. 在Terminal 輸入 pip install tensorflow

[回到目錄](#目錄)


# 開始執行輸出辨識圖片
下載整個我寫的 python 庫
https://github.com/Hung-Jia-Jun/python/archive/master.zip

1. 進入指定的下載內容資料夾路徑
   * python-master\python-master\DeepLearningPrediction\芒果辨識\YOLO_芒果成熟度辨識\yad2k

2. 點擊 Start.bat
3. 程式會讀取 圖片來源資料夾內所有的圖片
   * 來源資料夾python-master\python-master\DeepLearningPrediction\芒果辨識\YOLO_芒果成熟度辨識\yad2k\images
   
   
4. 輸出內容會在 
   * 結果資料夾 : python-master\python-master\DeepLearningPrediction\芒果辨識\YOLO_芒果成熟度辨識\yad2k\images\out
   * 並跟原始資料夾的檔名一樣
   
[回到目錄](#目錄)   



