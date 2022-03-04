#注意，该py文件内使用的路径，以sss.js为准
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
#解析中文/标点符号
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 


# 解析参数-------------------------------------------------------------
<<<<<<< HEAD
with open('../py/1.json','r',encoding='utf8')as fp:
    jsonData = json.load(fp)
=======
f = codecs.open(r'../py/1.txt', 'r+', encoding='utf-8')
argv=f.read().split(' ')
f.close()
>>>>>>> 50b2b81d77f7aa0f3a3844ed9e1e9d8c255517eb

mode = jsonData['mode']
x=jsonData['x']
y=jsonData['y']
cal=jsonData['cal']
que=jsonData['que']
cut=jsonData['cut']
gro=jsonData['gro']
xt=jsonData['xt']
yt=jsonData['yt']

# #-----------------------------------------------------------------------

# #使用参数---------------------------------------------------------------
# #读取文件
data=pd.read_csv(jsonData['filePath'],encoding='utf-8')

#cal
for index,value in enumerate(y):
  if value == 'calculate':
    newColName = 'calculateNewColumn' + cal[index]
    yCal = cal[index].split(' ')
    temp = []
    for c in yCal :
      if c != '+' and c != '-' and c != '*' and c != '/' :
        if c[0] != 'c':
          temp.append(int(c))
        elif c[0] == 'c':
          temp.append(np.array(data[data.columns[int(c[1:])]]))
      else :
        temp2 = temp.pop()
        temp1 = temp.pop()
        if c == '+':
          temp.append(temp1+temp2)
        elif c == '-':
          temp.append(temp1 - temp2)
        elif c == '*':
          temp.append(temp1 * temp2)
        elif c == '/':
          temp.append(temp1 / temp2)
    data[newColName] = temp.pop()
    y[index] = data.columns.size-1

#xval yval
#当参数为索引时
xVal=[]
xSum=len(x)
for i in range(0,xSum):
  xVal.append(data.columns[ int(x[i]) ])

if mode != 'pie':
  yVal=[]
  ySum=len(y)
  for i in range(0,ySum):
    yVal.append(data.columns[ int(y[i]) ])




# #query
if que['useQue']:
   data=data.query(que['que'])

# #cut
# cutName=''
# # if que_cut_gro[1] == 'true':
#   # cutName=que_cut_gro[2]+que_cut_gro[3]
#   # bins=que_cut_gro[2].split(',')
#   # bins=list(map(int,bins))
#   # labels=que_cut_gro[3].split(',')
#   # data[cutName] = pd.cut(data['AvgTemperature'],bins,labels=labels)

#group,x,y
if mode != 'pie':
  xd=[]
  yd=[]
  if gro['useGro']:
    tempData = data.groupby([xVal[0]])
    xd.append(np.array(tempData.mean().index))
    for i in range(len(yVal)):
      yd.append(np.array(tempData.agg({yVal[i]:[gro['gro'][i]]})[yVal[i]]))

  else :
    for i in xVal:
      xd.append(np.array(data[i]))
    for i in yVal:
      yd.append(np.array(data[i]))
# #-------------------------------------------------------------------

#画板样式---------------------------------------------------
plt.figure(figsize=(10,6))
plt.style.use('dark_background')
# plt.title(title)
# if mode != 'pie':
  # plt.xlabel(xName[0]) 
  # plt.ylabel(yName[0]) 
#----------------------------------------------------------------

#xy轴刻度间隔与上下限----------------------------------------------------------
if mode != 'pie':
  if xt[0] == 'none0':
    plt.xticks([])
  elif xt[0] == 'setting0':
    if str(type(x[0])) == "<class 'numpy.str_'>" :
      plt.xticks(np.arange(0,x.size-1,int(xt[3])))
    else :
      plt.xlim(int(xt[1])-0.5,int(xt[2])+0.5)
      plt.xticks(np.arange(int(xt[3]),int(xt[4]),int(xt[5])))
    
  if yt[0] == 'none1':
    plt.yticks([])
  elif yt[0] == 'setting1':
    print(yt)
    if str(type(y[0])) == "<class 'numpy.str_'>" :
      plt.yticks(np.arange(0,y.size-1,int(yt[3])))
    else :
      plt.ylim(int(yt[1]),int(yt[2]))
      plt.yticks(np.arange(int(yt[3]),int(yt[4]),int(yt[5])))
    
    


#--------------------------------------------------------------------

#画图--------------------------------------------#


#散点图

if mode == 'scatter':
  plt.scatter(xd[0], yd[0], label=' ')
#折线图
elif mode == 'plot':
  for i in range(0,len(yd)):
    plt.plot(xd[0],yd[i], label=' ')
#柱状图
elif mode == 'bar':
  if len(yd) == 1 :
    plt.bar(xd[0], yd[0],color="blue", label=' ')

  elif len(yd) == 2 :
    wid=4/xd[0].size
    plt.bar(xd[0]-wid/2, yd[0],color='blue',width=wid, label=' ')
    plt.bar(xd[0]+wid/2, yd[1],color='red',width=wid, label=' ')
  elif len(yd) == 3 :
    wid=2/xd[0].size
    plt.bar(xd[0]-wid, yd[0],width=wid,color='blue', label=' ')
    plt.bar(xd[0], yd[1],width=wid,color='red', label=' ')
    plt.bar(xd[0]+wid, yd[2],width=wid,color='orange', label=' ')
# elif mode == 'pie':
  # pieData = data[cutName].value_counts()
  # plt.pie(x=pieData,labels=pieData.index)

plt.legend() 
savePath='./public/'+mode+'.jpg'
plt.savefig(savePath)
#------------------------------------------------------------------






