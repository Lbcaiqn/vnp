#注意，该py文件内使用的路径，以sss.js为准
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
import sys
import json
#解析中文/标点符号
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 
# plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))

# 解析参数-------------------------------------------------------------

with open('../py/'+sys.argv[1]+'.json','r',encoding='utf8')as fp:
    jsonData = json.load(fp)


mode = jsonData['mode']
x=jsonData['x']
y=jsonData['y']
barStyle=jsonData['barStyle']
cal=jsonData['cal']

que=jsonData['que']
cut=jsonData['cut']
gro=jsonData['gro']
rate=jsonData['rate']
xt=jsonData['xt']
yt=jsonData['yt']
desc=jsonData['desc']
style=jsonData['style']

# #-----------------------------------------------------------------------

# #使用参数---------------------------------------------------------------
# #读取文件
data=pd.read_csv(jsonData['filePath'],encoding='utf-8')

#cal
newColList=[]
for index,value in enumerate(y):
  if value == 'calculate':
    newColName = 'calculateNewColumn' + cal[index].replace(' ','')
    newColList.append(newColName)
    yCal = cal[index].split(' ')
    temp = []
    for c in yCal :
      if c != '+' and c != '-' and c != '*' and c != '/' :
        if c[0] != 'c':
          temp.append(float(c))
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


#query
if que['useQue'] and que['que'] != '':
  query=que['que']
  for i in range(len(newColList)):
    query=query.replace('#1#',newColList[i])
  data=data.query(query)

#cut
cutName=''
if cut['useCut'] :
  cutName=cut['cutBins']+cut['cutLabels']
  bins=cut['cutBins'].split(',')
  bins=list(map(int,bins))
  labels=cut['cutLabels'].split(',')
  if mode == 'pie':
    data[cutName] = pd.cut(data[xVal[0]],bins,labels=labels)
  else:
    data[cutName] = pd.cut(data[yVal[0]],bins,labels=labels)

#group,x,y
if mode != 'pie':
  xd=[]
  yd=[]
  if gro['useGro']:
    tempData = data.groupby([xVal[0]])
    xd.append(np.array(tempData.mean().index))
    if gro['useType'] == 'default':
      for i in range(len(yVal)):
        yd.append(np.array(tempData.agg({yVal[i]:[gro['gro'][i]]})[yVal[i]][gro['gro'][i]]))
    elif gro['useType'] == 'double':
      tempData = data.groupby([xVal[0],data.columns[ int(gro['doubleCol']) ]])
      tempData = tempData.agg({yVal[0]:['mean','max','min','count']})[yVal[0]].unstack()
      length = len(tempData['mean'].columns)
      if length > len(yVal) :  
        lengeh = len(yVal)
      for i in range(length):
        td = tempData[gro['gro'][i]]
        yd.append(np.array(td[td.columns[i]]))
    elif gro['useType'] == 'cut':
      tempData = data.groupby([xVal[0],cutName])
      tempData = tempData.agg({yVal[0]:['mean','max','min','count']})[yVal[0]].unstack()
      print(tempData['count'])
      length = len(tempData['mean'].columns)
      if length > len(yVal) :  
        length = len(yVal)
      for i in range(length):
        td = tempData[gro['gro'][i]]
        yd.append(np.array(td[labels[i]]))

  else :
    for i in xVal:
      xd.append(np.array(data[i]))
    for i in yVal:
      yd.append(np.array(data[i]))


#-------------------------------------------------------------------

#画板样式---------------------------------------------------
figHeight=10
figWidth=6
plt.figure(figsize=(figHeight,figWidth))
if jsonData['theme'] != 'default' :
  plt.style.use(jsonData['theme'])
plt.title(desc['title']['val'][0])
if mode != 'pie' :
  if barStyle['orientation'] == 'vertical' :
    plt.xlabel(desc['xLabel']['val'][0]) 
    plt.ylabel(desc['yLabel']['val'][0])
  elif barStyle['orientation'] == 'horizontal' :
    plt.ylabel(desc['xLabel']['val'][0]) 
    plt.xlabel(desc['yLabel']['val'][0])

#----------------------------------------------------------------
#xy轴刻度间隔与上下限----------------------------------------------------------
if mode != 'pie':
  if barStyle['orientation'] == 'vertical' :
    if xt[0] == 'none0':
      plt.xticks([])
    elif xt[0] == 'setting0':
      if str(type(xd[0][0])) == "<class 'numpy.str_'>" : #若x轴数据是字符串
        plt.xticks(np.arange(0,xd[0].size-1,int(xt[5])))
      else :
        plt.xlim(int(xt[1])-1,int(xt[2])+1)
        plt.xticks(np.arange(int(xt[3]),int(xt[4]),int(xt[5])))
    elif xt[0] == 'default0':
      if str(type(xd[0][0])) == "<class 'numpy.str_'>" : #若x轴数据是字符串
        plt.xticks(np.arange(0,xd[0].size-1,int(xt[5])))
      else :
        plt.xlim(xd[0].min()-1.5,xd[0].max()+1.5)
        plt.xticks(np.arange(xd[0].min(),xd[0].max(),int(xd[0].size/10)+1))

    if yt[0] == 'none1':
      plt.yticks([])
    elif yt[0] == 'setting1':
      if str(type(yd[0][0])) == "<class 'numpy.str_'>" :
        plt.yticks(np.arange(0,yd[0].size-1,int(yt[5])))
      else :
        plt.ylim(int(yt[1]),int(yt[2]))
        plt.yticks(np.arange(int(yt[3]),int(yt[4]),int(yt[5])))

  elif barStyle['orientation'] == 'horizontal' :
    if xt[0] == 'none0':
      plt.yticks([])
    elif xt[0] == 'setting0':
      if str(type(xd[0][0])) == "<class 'numpy.str_'>" :
        plt.yticks(np.arange(0,xd[0].size-1,int(xt[5])))
      else :
        plt.ylim(int(xt[1])-1.5,int(xt[2])+1.5)
        plt.yticks(np.arange(int(xt[3]),int(xt[4]),int(xt[5])))
    elif xt[0] == 'default0':
      if str(type(xd[0][0])) == "<class 'numpy.str_'>" : #若x轴数据是字符串
        plt.yticks(np.arange(0,xd[0].size-1,int(xt[5])))
      else :
        plt.ylim(xd[0].min()-1.5,xd[0].max()+1.5)
        plt.yticks(np.arange(xd[0].min(),xd[0].max(),int(xd[0].size/10)+1))

    if yt[0] == 'none1':
      plt.xticks([])
    elif yt[0] == 'setting1':
      if str(type(yd[0][0])) == "<class 'numpy.str_'>" :
        plt.xticks(np.arange(0,yd[0].size-1,int(yt[5])))
      else :
        plt.xlim(int(yt[1]),int(yt[2]))
        plt.xticks(np.arange(int(yt[3]),int(yt[4]),int(yt[5])))
    

#----------------------------------------------------------------------------
#rate
if rate['useRate'] and len(yd) > 1:
  sum=0
  for i in yd:
    sum=sum+i
  for i in range(len(yd)):
    yd[i] = yd[i] / sum
  
  if rate['isSl'] == '0':
    for i in range(len(yd)):
      yd[i]=yd[i]*100

  for i in range(len(yd)):
    for j in range(yd[i].size):
      yd[i][j]=round(yd[i][j],int(rate['tail']))
  
  if int(rate['tail'])==0 and rate['isSl'] == '0':
    for i in range(len(yd)):
      yd[i]=yd[i].astype(int)


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
    if desc['useText']:
        textData = np.core.defchararray.add(yd[i].astype(str),'%') if rate['useRate'] and len(yd)>1 and rate['isSl']=='0' else yd[i]
        for a,b,c in zip(xd[0],yd[i],textData):
          plt.text(a,
                   b*1.002,
                   c,
                   ha='center',
                   fontsize=str(10*(10/xd[0].size))
                   )
#柱状图
elif mode == 'bar':
  widDeviation=np.zeros(len(yd))
  heiDeviation=[np.zeros(yd[0].size) for i in range(len(yd))]
  if barStyle['fold'] == 'transverse' :
    if len(yd) == 1 :
      widDeviation=[0]
    if len(yd) == 2 :
      widDeviation=[
        -float(jsonData['style']['bar'][0][1])/2,
        float(jsonData['style']['bar'][1][1])/2]
    if len(yd) == 3 :
      widDeviation=[
        -(float(jsonData['style']['bar'][0][1]) + float(jsonData['style']['bar'][1][1]))/2,
        0,
        (float(jsonData['style']['bar'][2][1]) + float(jsonData['style']['bar'][1][1]))/2
      ]
  elif barStyle['fold'] == 'vertical' :
    if len(yd) == 1 :
      heiDeviation = [np.zeros(yd[0].size)]
    elif len(yd) == 2 :
      heiDeviation = [np.zeros(yd[0].size),yd[0]]
    elif len(yd) == 3 :
      heiDeviation = [np.zeros(yd[0].size),yd[0],yd[0]+yd[1]]
  for i in range(0,len(yd)):
    if barStyle['orientation'] == 'vertical' :
      plt.bar(xd[0]+widDeviation[i], yd[i], label=desc['legend']['val'][i],
            color=jsonData['style']['bar'][i][0],
            width=float(jsonData['style']['bar'][i][1]),
            bottom=heiDeviation[i]
            )
      #设置标注
      if desc['useText']:
        hv = 1 if barStyle['fold'] == 'transverse' else 2
        textData = np.core.defchararray.add(yd[i].astype(str),'%') if rate['useRate'] and len(yd)>1 and rate['isSl']=='0' else yd[i]
        for a,b,c,bottom in zip(xd[0]+widDeviation[i],yd[i],textData,heiDeviation[i]):
          plt.text(a,
                   (b/hv+bottom)*1.01,
                   c,
                   ha='center',
                   fontsize=str(10*(10/xd[0].size)/(0.8/float(jsonData['style']['bar'][i][1])))
                   )
        
    elif barStyle['orientation'] == 'horizontal' :
      plt.barh(xd[0]+widDeviation[i], yd[i], label=desc['legend']['val'][i],
            color=jsonData['style']['bar'][i][0],
            height=float(jsonData['style']['bar'][i][1]),
            left=heiDeviation[i])
      #设置标注
      if desc['useText']:
        hv = 1 if barStyle['fold'] == 'transverse' else 2
        textData = np.core.defchararray.add(yd[i].astype(str),'%') if rate['useRate'] and len(yd)>1 and rate['isSl']=='0' else yd[i]
        for a,b,c,bottom in zip(yd[i],xd[0]+widDeviation[i],textData,heiDeviation[i]):
          plt.text((a/hv+bottom)*1.01,
                    b,
                    c,
                    va='center',
                    fontsize=str(10*(10/xd[0].size)/(0.8/float(jsonData['style']['bar'][i][1])))
                    )
#饼图
elif mode == 'pie':
  pieData = data[cutName].value_counts()
  pieColor=[]
  pieExplode=[]
  for i in range(len(pieData)):
    pieColor.append(None)
    pieExplode.append(0)
  for i in style['pie'][0][4]:
    if i['index']!='' and int(i['index'])<=len(pieData):
      pieColor[int(i['index'])-1]=i['color']
      pieExplode[int(i['index'])-1]=float(i['explode'])

  plt.pie(
          x=pieData,labels=pieData.index,
          autopct='%3.1f%%',
          radius=float(style['pie'][0][0]['radius']['val']),
          pctdistance=float(style['pie'][0][1]['pctdistance']['val']),
          labeldistance=float(style['pie'][0][1]['labeldistance']['val']),
          startangle=float(style['pie'][0][2]['startangle']['val']),
          counterclock=style['pie'][0][2]['counterclock']['val'],
          wedgeprops=dict(
            linewidth=float(style['pie'][0][3]['linewidth']['val']),
            width=float(style['pie'][0][0]['occupyRadius']['val']),
            edgecolor=style['pie'][0][3]['color']['val']
            ),
          colors=pieColor,
          explode=pieExplode
          ) 

if jsonData['desc']['legend']['useLegend']:
  plt.legend() 
savePath='./public/DrawImg/'+sys.argv[1]+'.png'
plt.savefig(savePath)
#------------------------------------------------------------------


# 双坐标系，数据透视表，临时输出formdata
# 刻度空值处理，数据类型为字符串时刻度处理
# 饼图自定义列
# 饼图不用转换类别的情况


