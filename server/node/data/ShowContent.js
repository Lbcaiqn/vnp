const url = 'http://47.107.225.248:8000/ShowImg/'
// const url = 'http://localhost:8000/ShowImg/'

const purl = url+'population/'
const turl = url+'temperature/'

const content = {
  population:{
    dataDesc:{
      title: '数据说明',
      content:[
        {
          title: '',
          text: '这份数据是1949年-2019年的中国人口数据。',
          img:[purl+'data.png']
        }
      ]
    },
    scratter:{
      title: '散点图',
      content:[
        {title:'1949年-2019年总人口变化趋势',text:'以散点图为例，展示最基本的使用，选择要画的图及X轴和Y轴数据。',img:[purl+'scatter/00.png']},
        {title:'',text: '不需要其他设置，就能画出散点图',img:[purl+'scatter/01.png']}
      ]
    },
    plot:{
      title: '折线图',
      content:[
        {
          title:'1949年-2019年的出生率，死亡率和自然增长率的变化趋势',
          text:'折线图最多可支持同时绘制5条折线，这里我们需要画3条折线。',
          img:[purl+'plot/10.png']
        },
        {
          title:'',
          text:`可在【样式选择】中，设置样式，选择黑色模式，使用图例，并输入Y轴描述，选择每条折线的颜色，其他默认`,
          img:[purl+'plot/11.png',purl+'plot/12.png']
        }
      ]
    },
    bar:{
      title: '柱状图',
      content: [
        {
          title:'1999年-2019年总人口变化柱状图',
          text: '柱状图支持绘制绘制3种Y轴数据，这里我们只需要1种Y轴数据',
          img: [purl+'bar/20.png']
        },
        {
          title:'',
          text: '在【高级设置】中，使用数据筛选，筛选出年份大于等于1999年的数据.',
          img: [purl+'bar/21.png',purl+'bar/22.png']
        },
        {
          title:'',
          text: '由于默认的Y轴上下限差距大，且数据分布在120000-140000内,所以造成柱子高度差异不大，可以在【高级选项】中，设置Y轴的上下限。',
          img: [purl+'bar/23.png',purl+'bar/24.png']
        },
        {
          title:'',
          text: '也可以画成水平的柱状图',
          img: [purl+'bar/25.png',purl+'bar/26.png']
        },
        {
          title:'1999年-2019年城镇人口与农村人口在总人口的占比变化',
          text: '由于源数据中没有城镇人口占比和农村人口占比这两个数据。所以需要通过自定义列，用有的数据计算出新的数据。c4代表第四列，c5代表第五烈，c1代表第一列，c4/c1*100则是城镇人口除总人口再乘100转成百分制。',
          img: [purl+'bar/27.png',purl+'bar/28.png',purl+'bar/29.png']
        },
        {
          title:'',
          text: '也可以画叠加柱状图，这里我们尝试使用图例。',
          img: [purl+'bar/210.png',purl+'bar/211.png',purl+'bar/212.png']
        },
        {
          title:'',
          text: '可以看到，图例挡住了柱子，可以设置Y轴上下限解决。',
          img: [purl+'bar/213.png',purl+'bar/214.png']
        },
      ]
    },
    pie:{
      title: '饼图',
      content: [
        {
          title:'总人口',
          text: '绘制饼图需要类别型数据，总人口是数值型数据，可在【高级选项】中转成类别型数据。',
          img: [purl+'pie/30.png']
        },
        {
          title:'',
          text: '划分4个左闭右开的区间：[0,80000)，[80000,110000)，[80000,130000)，[130000,150000)，总人口的值在那个区间，就转化为对应的类别型数据。',
          img: [purl+'pie/31.png',purl+'pie/32.png']
        },
      ]
    }
  },
  temperature:{
    dataDesc: {
      title: '数据说明',
      content: [
        {
          text: '这份数据是1995年-2019年世界各国重要城市的每年每月每日的日均气温数据，共278万行数据',
          img: [turl+'data.png']
        }
      ]
    },
    plot: {
      title: '折线图',
      content: [
        {
          title: '2000年-2019年广州市每年8月的月均气温(摄氏度)变化折线图',
          text: '源数据中，气温数据是华氏度，需要用【自定义列】转化成摄氏度，如如气温数据是第七列，用c7表示',
          img: [turl+'plot/10.png']
        },
        {
          text: '选择数据,摄氏度=(华氏度-32)/1.8',
          img:[turl+'plot/11.png']
        },
        {
          text: '按照条件筛选出数据',
          img:[turl+'plot/12.png']
        },
        {
          text: '筛选后的数据，有每年8月每天的气温，需要按年分组，对气温求均值。',
          img:[turl+'plot/13.png',turl+'plot/14.png',turl+'plot/15.png']
        }
      ]
    },
    bar:{
      title: '柱状图',
      content: [
        {
          title: '2000年-2019年广州市日均气温超过30℃的天数',
          img:[turl+'bar/20.png']
        },
        {
          text: '#1#表示第一个自定义列，即转换出的摄氏度列',
          img:[turl+'bar/21.png']
        },
        {
          text: '按年分组，并对天数计数',
          img:[turl+'bar/22.png']
        },
        {
          text: '设置样式，显示标注即每个柱子上的文本标注',
          img:[turl+'bar/23.png',turl+'bar/24.png']
        },
        {
          title: '2000年-2019年广州市每年的高温(>=30℃)，常温(15℃-30℃)，低温(<15℃)天数占一年天数的百分比',
          img: [turl+'bar/25.png']
        },
        {
          text: '数据处理',
          img: [turl+'bar/26.png']
        },
        {
          text: '设置样式',
          img: [turl+'bar/27.png',turl+'bar/28.png']
        },
        {
          title: '2015年-2019年丹麦(Denmark)，芬兰(Finland)，挪威(Norway)每年低于0℃的天数',
          img:[turl+'bar/29.png']
        },
        {
          text: '数据处理',
          img:[turl+'bar/210.png',turl+'bar/211.png']
        },
        {
          text: '设置样式',
          img: [turl+'bar/212.png',turl+'bar/213.png']
        }
      ]
    },
    pie:{
      title: '饼图',
      content:[
        {
          title: '全球各地每天气温(华氏度)情况，酷冷(<32)，冷(32-59)，温(59-70)，热(70-86)，酷热(>86)',
          img:[turl+'pie/30.png']
        },
        {
          text: '数值型的华氏度转换为类别型，样式默认，查看效果',
          img:[turl+'pie/31.png',turl+'pie/32.png']
        },
        {
          text: '设置样式，再查看效果',
          img:[turl+'pie/33.png',turl+'pie/34.png']
        }
      ]
    }
    
  }
}


module.exports = {
  content
}