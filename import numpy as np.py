import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
acid = pd.read_csv("acid_value.csv")
print(acid)
'''
#1、读入acid_value.csv到变量acid里面，完成如下一维插值和二维插值的任务，给出代码和作图结果：
#生成时间自变量x是0到30的整数时间点, 取出acid的5列数据分别作为因变量y1,y2,y3,y4,y5,  
##并且给整个图配一个legend图例以表明图里面每条折线代表哪个温度下的(比如用‘Tem_160’就代表160度下的)。


# 创建时间自变量x
x = np.arange(0, 31)  # 0到30的整数时间点
# 列名温度值
temperatures = [160, 175, 190, 205, 220]
# 提取对应数据
y1 = acid.iloc[:, 0].values
y2 = acid.iloc[:, 1].values
y3 = acid.iloc[:, 2].values
y4 = acid.iloc[:, 3].values
y5 = acid.iloc[:, 4].values

# 设置不同的颜色和标记
colors = ['r', 'g', 'b', 'c', 'm']
markers = ['o', 's', '^', 'D', 'x']

# 创建折线图
plt.figure(figsize=(10, 6))

# 绘制五条折线
plt.plot(x, y1, color=colors[0], marker=markers[0], label=f'Tem_{temperatures[0]}')
plt.plot(x, y2, color=colors[1], marker=markers[1], label=f'Tem_{temperatures[1]}')
plt.plot(x, y3, color=colors[2], marker=markers[2], label=f'Tem_{temperatures[2]}')
plt.plot(x, y4, color=colors[3], marker=markers[3], label=f'Tem_{temperatures[3]}')
plt.plot(x, y5, color=colors[4], marker=markers[4], label=f'Tem_{temperatures[4]}')

# 添加图例、标题和轴标签
plt.legend()
plt.title('acid')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.grid(True)

# 显示图形
plt.show()

#(2)生成时间自变量x是0到30的整数时间点, 取其中温度在220度下的数据列作为因变量y，根据取出来的已知插值点，
#求出时间每隔0.3小时的插值因变量ynew.画出原始数据散点图和插值曲线图，二者画到一起，并做legend，
#再给X轴起名‘Time’和Y轴起名‘Temperature’,图的主标题叫‘acid’
#一维插值
t = np.arange(0, 31)  # 0到30的整数时间点
y = acid['Tem_220']
f =interpolate.interp1d(t,y,kind = 'nearest')
tnew = np.arange(0,30.3,0.3)
ynew = f(tnew)
plt.figure()
plt.scatter(t,y,label='orignal',marker='*')
plt.plot(tnew,ynew,label = 'interpolated',color= 'red')
plt.legend()
plt.show()

#二维插值
#(3)生成时间自变量x是0到30的整数时间点，生成温度自变量y是[160,175,190,205,220]，
#然后把acid当因变量z，做二维插值函数f.  接着生成0到30的、每隔0.2小时间隔的新的时间自变量xnew,
#和每隔1℃的温度的新的自变量ynew, 然后用前面得到的插值函数f计算出新的因变量znew. 最后，把xnew, ynew和znew配合起来做出插值曲面图，
#并把x,y,z的原始数据散点图也做在前面的插值曲面图里，给出legend让你的图具有自明性.
#给X轴起名‘Time’和Y轴起名‘Temperature’,Z轴起名‘acid’，整个图的主标题叫‘surface of acid’.

t = np.arange(0,31)
T = np.array([160,175,190,205,220])
t,T = np.meshgrid(t,T)
acid = acid.T
ax = plt.figure().add_subplot(projection='3d')
ax.plot_surface(t,T,acid,cmap=plt.get_cmap('rainbow'))

f = interpolate.interp2d(t,T,acid,kind= 'cubic')
tnew = np.arange(0,30.2,0.2)
Tnew = np.arange(160,221,1)
znew = f(tnew,Tnew)
#下面是课后要跟着补充操作的
tnew,Tnew = np.meshgrid(tnew,Tnew)#把新的两个自变量打成网格
#接下来作图，把原始数据散点和插值完的新数据曲面做到一起
ax = plt.figure().add_subplot(projection='3d')
#上面这句话是开画图窗口，并且把窗口打扮成要做3d图的样子
ax.scatter(t,T,acid,marker='D',label='original')#做原始数据散点图
ax.plot_surface(tnew,Tnew,znew,cmap=plt.get_cmap('rainbow'),label='interpolated')
#上面这句是做新数据曲面图
ax.set_title('surface of acid') #设置主标题的名字
ax.set_xlabel('Time') #设置X轴的名字
ax.set_ylabel('Temperature') #设置Y轴的名字
ax.set_zlabel('acid') #设置Z轴的名字
plt.show()

# 创建示例数据（时间和温度）
t = np.arange(0, 31)  # 时间点 (0-30小时)
T = np.array([160, 175, 190, 205, 220])  # 温度点

# 创建网格坐标
t_grid, T_grid = np.meshgrid(t, T)  # 注意：这里使用t_grid和T_grid以避免变量名冲突

# 假设酸值数据已经准备好（需要根据实际情况替换）
# 这里只是示例数据，需要替换为实际的acid数据
acid = np.random.rand(len(T), len(t))  # 替换为实际的酸值数据

# 创建插值函数 (使用RegularGridInterpolator替代interp2d)
# 注意：RegularGridInterpolator要求输入网格点是递增的
# 对于二维情况，函数形式为f(x, y)，对应我们的f(t, T)
f = RegularGridInterpolator((t, T), acid.T, method='cubic')

# 创建更密集的网格用于插值结果
tnew = np.arange(0, 30.2, 0.2)
Tnew = np.arange(160, 221, 1)
tnew_grid, Tnew_grid = np.meshgrid(tnew, Tnew)

# 准备查询点
query_points = np.column_stack((tnew_grid.flatten(), Tnew_grid.flatten()))

# 执行插值计算
znew_flat = f(query_points)

# 重塑结果为网格形状
znew = znew_flat.reshape(tnew_grid.shape)

# 可视化结果
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制原始数据散点图
ax.scatter(t_grid, T_grid, acid, marker='D', s=50, color='black', label='原始数据')

# 绘制插值后的曲面图
surf = ax.plot_surface(tnew_grid, Tnew_grid, znew, cmap='rainbow', alpha=0.8, label='插值曲面')

# 添加颜色条
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='酸值')

# 设置图表属性
ax.set_title('surface of acid')
ax.set_xlabel('Time')
ax.set_ylabel('Temperature')
ax.set_zlabel('acid')
ax.legend()

# 调整视角
ax.view_init(elev=30, azim=45)
plt.show()


#2、请对下面数据做二次多项式拟合，画出原始数据散点图和拟合后的曲线图，画到一起，做legend. 给出代码和作图结果。
#xi	0.1	0.2	0.3	0.4	0.5	0.6	0.7	0.8	0.9	1.0	1.1
#yi	-0.447	1.978	3.28	6.16	7.08	7.34	7.66	9.56	9.48	9.30	11.2

#多项式拟合
x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1]
y = [-0.447,1.978,3.28,6.16,7.08,7.34,7.66,9.56,9.48,9.30,11.2]
a = np.polyfit(x,y,2) #2代表多项式的次数
p1 = np.poly1d(a)
y1 = np.polyval(a, x)
plt.figure()
plt.title('多项式拟合')
plt.scatter(x,y,marker='<',color='red',label='orignal')
plt.plot(x,y1,color='blue',label='fitted')
plt.legend()
plt.show()

# 3、读入海水图片haishui.jpg到变量Hai里，读入Horse.jpg到变量Hor里面，
# 然后完成下面任务：
# (1)取出Hor的红色分量图像给Hor_R，取出Hai的红色分量图像给Hai_R;
#
# (2)观察变量Hor_R和Hai_R的行数和列数，将Hai_R取出部分行和部分列到Hai_R1里，
# 使得Hai_R1和Hor_R的行数和列数一样，这里需要自己计算着取；
# (3)将Hai_R1和Hor_R相加，得到H, 并显示H图像，注意用参数cmap='gray';
# (4)取出H的行列数分别给m和n，并定义H1是和H一样大小的零矩阵，
# 然后进行双重for循环通过判断H矩阵的值来填补H1矩阵的值，
# 规则是：如果H某个i, j位置的值大于180的、H1对应位置的值填成255，
# 如果H某个i, j位置的值介于100到180之间、H1对应位置的值填成100，
# 对于H里小于100的值、H1里面对应位置一律填成0。
# 给出本大题所有代码和H、H1图像的显示图片。
import cv2
# (1) 读取图片并提取红色分量（OpenCV默认BGR格式，红色分量为索引2）
Hai = cv2.imread('haishui.jpg')
Hor = cv2.imread('horse.jpg')
Hai_R = Hai[:, :, 2]
Hor_R = Hor[:, :, 2]
# (2) 调整Hai_R尺寸与Hor_R一致
h_horse, w_horse = Hor_R.shape
h_sea, w_sea = Hai_R.shape

# 计算切片起始位置（确保居中裁剪）
start_h = (h_sea - h_horse) // 2 if h_sea > h_horse else 0
start_w = (w_sea - w_horse) // 2 if w_sea > w_horse else 0
end_h = start_h + h_horse
end_w = start_w + w_horse

Hai_R1 = Hai_R[start_h:end_h, start_w:end_w]

# (3) 矩阵相加并显示灰度图像
H = Hor_R + Hai_R1  # 直接相加可能溢出，如需截断可使用cv2.add
plt.imshow(H, cmap='gray')
plt.title('H Image')
plt.axis('off')
plt.show()

# (4) 双重循环生成H1矩阵
m, n = H.shape
H1 = np.zeros((m, n), dtype=np.uint8)  # 初始化零矩阵

for i in range(m):
    for j in range(n):
        val = H[i, j]
        if val > 180:
            H1[i, j] = 255
        elif 100 <= val <= 180:
            H1[i, j] = 100
        else:
            H1[i, j] = 0

# 可选：显示H1结果
plt.imshow(H1, cmap='gray')
plt.title('H1 Image')
plt.axis('off')
plt.show()
'''