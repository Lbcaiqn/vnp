#注意，该py文件内使用的路径，以sss.js为准
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
#解析中文/标点符号
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 


# 解析参数-------------------------------------------------------------

with open('../py/1.json','r',encoding='utf8')as fp:
    jsonData = json.load(fp)

mode = jsonData['mode']
x=jsonData['x']
y=jsonData['y']
cal=jsonData['cal']

que=jsonData['que']
cut=jsonData['cut']
gro=jsonData['gro']
xt=jsonData['xt']
yt=jsonData['yt']

desc=jsonData['desc']

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
plt.title(desc['title']['val'][0])
if mode != 'pie':
  plt.xlabel(desc['xLabel']['val'][0]) 
  plt.ylabel(desc['yLabel']['val'][0]) 
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
  plt.scatter(xd[0], yd[0], label=desc['legend']['val'][0],
             color=jsonData['style']['scatter'][0][0],
             marker=jsonData['style']['scatter'][0][1])
#折线图

elif mode == 'plot':
  for i in range(0,len(yd)):
    if jsonData['style']['plot'][i][2] == 'default':
      jsonData['style']['plot'][i][2] = ''
    if jsonData['style']['plot'][i][3] == '' or jsonData['style']['plot'][i][3] == '0':
      jsonData['style']['plot'][i][3] = '1' 
    for s in jsonData['style']['plot'][i][3]:
      if s < '0' or s > '9':
        jsonData['style']['plot'][i][3] = '1'
        break
    
    
    plt.plot(xd[0],yd[i], label=desc['legend']['val'][i],
            color=jsonData['style']['plot'][i][0],
            linestyle=jsonData['style']['plot'][i][1],
            marker=jsonData['style']['plot'][i][2],
            linewidth=int(jsonData['style']['plot'][i][3])
            
            )
#柱状图
elif mode == 'bar':
  if len(yd) == 1 :
    plt.bar(xd[0], yd[0], label=desc['legend']['val'][0],
           color=jsonData['style']['bar'][0][0] )
    

  elif len(yd) == 2 :
    wid=4/xd[0].size
    plt.bar(xd[0]-wid/2, yd[0],width=wid, label=desc['legend']['val'][0],
           color=jsonData['style']['bar'][0][0])
    plt.bar(xd[0]+wid/2, yd[1],width=wid, label=desc['legend']['val'][1],
            color=jsonData['style']['bar'][1][0])
  elif len(yd) == 3 :
    wid=2/xd[0].size
    plt.bar(xd[0]-wid, yd[0],width=wid, label=desc['legend']['val'][0],
            color=jsonData['style']['bar'][0][0])
    plt.bar(xd[0], yd[1],width=wid, label=desc['legend']['val'][1],
            color=jsonData['style']['bar'][1][0])
    plt.bar(xd[0]+wid, yd[2],width=wid, label=desc['legend']['val'][2],
            color=jsonData['style']['bar'][2][0])
# elif mode == 'pie':
  # pieData = data[cutName].value_counts()
  # plt.pie(x=pieData,labels=pieData.index)


if jsonData['desc']['legend']['useLegend']:
  plt.legend() 
savePath='./public/'+mode+'.jpg'
plt.savefig(savePath)
#------------------------------------------------------------------






