import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations/index.js'
Vue.use(Vuex)

const store = new Vuex.Store({
  state:{
    fd:{
      filePath:'',
      isUpload:false
    },
    mode: '',
    x:[''],
    y:[''],
    cal:[{ str: "", isShow: false }],
    gro:{
      useGro: false,
      gro:['mean'],
    },
    que:{
      useQue:false,
      que:'',
    },
    cut:{
      useCut:false,
      cutBins:'',
      cutLabels:'',
    },
    xt:{
      xtSl:'',
      xtStr:[
        {iid:'0',text:''},
        {iid:'1',text:''},
        {iid:'2',text:''},
        {iid:'3',text:''},
        {iid:'4',text:''},
      ],
    },
    yt:{
      ytSl:'',
      ytStr:[
        {iid:'0',text:''},
        {iid:'1',text:''},
        {iid:'2',text:''},
        {iid:'3',text:''},
        {iid:'4',text:''},
      ],
    },
    desc:{
      title: {iid:'标题：',val:['']},
      xLabel: {iid:'X轴：',val:['']},
      yLabel: {iid:'Y轴：',val:['']},
      legend: {iid:'图例：',val:[''],useLegend: false},
    },
    
    imgURL: '#'
    
  },
  mutations
})
export default store
