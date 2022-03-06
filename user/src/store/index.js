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
    barStyle: {},
    cal:[{ str: "", isShow: false }],
    gro:{},
    que:{},
    cut:{},
    xt:{},
    yt:{},
    desc:{},
    style:{},
    
    imgURL: '#'
    
  },
  mutations
})
export default store
