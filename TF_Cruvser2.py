#-*- coding: utf-8 -*-　
#引用函數庫

import tensorflow as tf
import numpy as np
import pandas as pd
import pdb
import matplotlib.pyplot as plt

#定義layer
def add_layer(inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases   

    #自由選擇激活函數
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

# 給tensorflow 一個placeholder 隨時置換數據 None 表示會自己計算出放了多少組數據
# 像這裡 None 就會自動放入300組 因為我們等等會放入300組數據訓練 
xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32, [None, 1])

#組裝神經網路
# add hidden layer
l1 = add_layer(xs, 1,30, activation_function=tf.nn.relu)
# add output layer
prediction = add_layer(l1, 30, 1, activation_function=None)

#接下來製造一些數據和雜訊吧 
#製造出範圍為-1~1之間的 row:300 col:1 矩陣
#x_data = np.random.rand(300)
#x_data = x_data.reshape(len(x_data), 1)
f=open('201707_F3_1_8_2454.csv')  
df=pd.read_csv(f)    
listData=[]
for ele in df['Price']:
    listData.append(ele)
#listData=[2102.38,2117.91,2127.94,2117.28,2128.58,2141.6,2166.17,2158.15,2160.58,2157.31,2155.51,2161.94,2163.66,2140.96,2170.61,2183.41,2226.85,2227.34,2230.29,2203.29,2211.03,2228.11,2240.25,2242.98,2228.87,2214.59,2212.35,2200.02,2176.3,2165.78]
#x_data = np.asarray( [3.3, 4.4, 5.5, 6.71, 6.93, 4.168, 9.779, 6.182, 7.59, 2.167, 7.042, 10.791, 5.313, 7.997, 5.654, 9.27, 3.1])[:, np.newaxis]
listDataX=[]
for i in range(len(listData)):
    listDataX.append(i)
x_data = np.asarray( listDataX)[:, np.newaxis]


noise = np.random.normal(0, 1, x_data.shape)

#製造出要讓網路學習的Y 並加上雜訊
y_data= np.asarray( listData)[:, np.newaxis]- 1 + noise

#x_data = np.linspace(-1,1,300)[:, np.newaxis]

#製造出要讓網路學習的Y 並加上雜訊
#y_data = np.square(x_data) - 0.5 + noise
#y_data = np.asarray( [1.7, 2.76, 2.09, 3.19, 1.694, 1.573, 3.366, 2.596, 2.53, 1.221, 2.827, 3.465, 1.65, 2.904, 2.42, 2.94, 1.3])[:, np.newaxis]

# 定義loss function 並且選擇減低loss 的函數 這裡選擇GradientDescentOptimizer
# 其他方法再這裡可以找到 https://www.tensorflow.org/versions/r0.10/api_docs/python/train.html
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),reduction_indices=[1]))
#train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

#loss = tf.reduce_mean(tf.square(ys))
optimizer =tf.train.AdamOptimizer()
train_step=optimizer.minimize(loss)

#全部設定好了之後 記得初始化喔
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
 
# 為了可以可視化我們訓練的結果
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x_data, y_data)
plt.ion()
plt.show()

#宣告儲存模型
saver=tf.train.Saver(tf.global_variables())

#載入模型
#saver.restore(sess, 'modle.ckpt') 

# 之後就可以用for迴圈訓練了
for i in range(50000):
   
     # 整個訓練最核心的code , feed_dict 表示餵入 輸入與輸出
     # x_data:[300,1]   y_data:[300,1]
    _,loss_value=sess.run([train_step,loss], feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        # 畫出下一條線之前 必須把前一條線刪除掉 不然會看不出學習成果
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass
        plt.ylim(200,400)
        # 要取出預測的數值 必須再run 一次才能取出
        prediction_value = sess.run(prediction, feed_dict={xs: x_data})
        # 每隔0.1 秒畫出來
        lines = ax.plot(x_data, prediction_value, 'r-', lw=5,label='data')
        #ax.plot(x_data, prediction_value, 'r-', lw=5,label='data')
        plt.title('use '+str(i)+' Epoch '+"Loss:"+str(loss_value))
        plt.pause(0.01)

    if i % 500== 0:
        print("model_save",saver.save(sess,'modle'))





#saver.restore(sess, 'modle.ckpt') 

plt.pause(999)










